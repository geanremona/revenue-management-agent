"""
skills_memory.py
----------------
Manages the persistent state of the agent's internal thresholds, allowing
the agent to self-adjust via Reinforcement Learning from Human Feedback (RLHF).
"""
import json
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SkillsMemory:
    def __init__(self, filepath: str = "data/skills_memory.json"):
        self.filepath = Path(filepath)
        # Default starting skills
        self.state = {
            "watch_threshold": 80.0,
            "critical_threshold": 150.0
        }
        self._load()

    def _load(self):
        if self.filepath.exists():
            try:
                with open(self.filepath, "r") as f:
                    data = json.load(f)
                    self.state.update(data)
            except Exception as e:
                logger.error(f"Failed to load skills memory: {e}")

    def _save(self):
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, "w") as f:
            json.dump(self.state, f, indent=4)

    def reward_agent(self):
        """
        Called when a human APPROVES a critical anomaly (True Positive).
        The agent learns it should be slightly MORE sensitive (lowers threshold).
        """
        old_val = self.state["critical_threshold"]
        # Decrease threshold by 0.5%, floor at 80%
        new_val = max(80.0, old_val - 0.5)
        self.state["critical_threshold"] = round(new_val, 1)
        self._save()
        logger.info(json.dumps({
            "event": "rlhf_reward", 
            "old_critical_threshold": old_val, 
            "new_critical_threshold": self.state["critical_threshold"]
        }))

    def penalize_agent(self):
        """
        Called when a human DISMISSES a critical anomaly (False Positive).
        The agent learns it should be LESS sensitive (raises threshold).
        """
        old_val = self.state["critical_threshold"]
        # Increase threshold by 1.0%, ceiling at 300%
        new_val = min(300.0, old_val + 1.0)
        self.state["critical_threshold"] = round(new_val, 1)
        self._save()
        logger.info(json.dumps({
            "event": "rlhf_penalty", 
            "old_critical_threshold": old_val, 
            "new_critical_threshold": self.state["critical_threshold"]
        }))

    @property
    def watch_threshold(self) -> float:
        return self.state["watch_threshold"]

    @property
    def critical_threshold(self) -> float:
        return self.state["critical_threshold"]
