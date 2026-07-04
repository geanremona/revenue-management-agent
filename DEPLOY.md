# Deploying to Vultr + Publishing for the Hackathon

Two independent things to do: (1) get the app running on a Vultr instance,
and (2) push the repo to public GitHub so it can be submitted.

---

## Part 1 — Put the code on GitHub (public repo)

Do this first — it makes Part 2 a one-line `git clone` on the server.

```bash
cd revenue_agent
git init
git add .
git commit -m "Initial commit: revenue management agent"
```

Create a new **public** repo on GitHub (via github.com/new — do NOT initialize
it with a README, since you already have one), then:

```bash
git branch -M main
git remote add origin https://github.com/<your-username>/revenue-management-agent.git
git push -u origin main
```

Before pushing, edit `LICENSE` to put your name in, and double check `.gitignore`
is excluding `__pycache__/`, `.venv/`, and `.env` (it already does).

**For the hackathon submission**, your repo URL is what you submit. Make sure:
- The README's top line clearly states what the project does (judges skim).
- Add a "Live Demo" link once Part 2 is done (edit `README.md` and re-push).
- Consider adding a short GIF/screenshot of the `/` page — hackathon judges
  reward things they can see working in 10 seconds.

---

## Part 2 — Deploy on a Vultr instance

### 1. Spin up the instance

- Vultr dashboard → **Deploy New Server** → Cloud Compute
- Choose **Ubuntu 24.04 LTS**
- Pick the smallest plan (this app is lightweight — 1 vCPU / 1GB RAM is plenty)
- Add your SSH key under "SSH Keys" so you don't get a mailed password
- Deploy, then copy the instance's IP address

### 2. Connect and do basic setup

```bash
ssh root@<your-vultr-ip>
adduser deploy
usermod -aG sudo deploy
su - deploy
```

Install dependencies:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-venv python3-pip git nginx
```

### 3. Clone your repo and set up the app

```bash
cd ~
git clone https://github.com/<your-username>/revenue-management-agent.git revenue_agent
cd revenue_agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Quick smoke test:

```bash
python3 app.py
# in another terminal / or curl from your laptop:
curl http://<your-vultr-ip>:8080/healthz
```

Ctrl+C to stop it once confirmed — you'll run it as a service instead.

### 4. Run it as a persistent service (systemd)

A ready-made unit file is in `deploy/revenue-agent.service`. Copy it in and
enable it:

```bash
sudo cp ~/revenue_agent/deploy/revenue-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now revenue-agent
sudo systemctl status revenue-agent
```

It will now survive reboots and restart automatically if it crashes.

**Option B — Docker instead of systemd**, if you'd rather containerize:

```bash
sudo apt install -y docker.io docker-compose-plugin
sudo docker compose up -d --build
```

(`docker-compose.yml` maps container port 8080 to host port 80, so skip the
Nginx step below if you go this route.)

### 5. Put Nginx in front (so it's on port 80, not :8080)

Skip this if you used Docker Compose above.

```bash
sudo tee /etc/nginx/sites-available/revenue-agent <<'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF
sudo ln -s /etc/nginx/sites-available/revenue-agent /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx
```

### 6. Open the firewall

In the Vultr dashboard → your instance → **Settings → Firewall**, attach or
create a firewall group allowing:
- TCP 22 (SSH) — restrict to your IP if possible
- TCP 80 (HTTP)
- TCP 443 (HTTPS, if you add a domain + SSL below)

On the instance itself, if `ufw` is active:

```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
```

### 7. (Optional) Add a domain + HTTPS

If you point a domain's A record at your Vultr IP:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 8. Verify

Visit `http://<your-vultr-ip>/` (or your domain) — you should see the
Revenue Strategy Brief rendered as a page, with a "Re-run agent" button.

---

## Updating the live deployment after code changes

```bash
ssh deploy@<your-vultr-ip>
cd revenue_agent
git pull
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart revenue-agent
```

(Or `sudo docker compose up -d --build` if using Docker.)

---

## Checklist before submitting

- [ ] Repo is public on GitHub
- [ ] `README.md` explains the project and links to the live Vultr URL
- [ ] `LICENSE` has your name
- [ ] App is reachable at `http://<vultr-ip-or-domain>/` and returns the brief
- [ ] `/healthz` returns `{"status": "ok"}`
- [ ] No secrets/API keys committed (check `.gitignore` covers `.env`)
