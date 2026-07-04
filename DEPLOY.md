# Deployment Guide: SUSE Rancher (K3s)

This guide covers migrating the Revenue Pilot deployment from a bare-metal `systemd` + `nginx` setup to a single-node lightweight Kubernetes cluster using SUSE Rancher's K3s.

## 1. Prepare the Vultr Server

First, stop and disable the existing Nginx and systemd services to free up port 80 for the K3s LoadBalancer.

```bash
sudo systemctl stop nginx
sudo systemctl disable nginx
sudo systemctl stop revenue-agent
sudo systemctl disable revenue-agent
```

## 2. Install Docker (If not installed)
Since we are building the container on the server to avoid needing a public registry, ensure Docker is installed.
```bash
sudo apt-get update
sudo apt-get install -y docker.io
```

## 3. Install K3s

Run the official K3s installation script:
```bash
curl -sfL https://get.k3s.io | sh -
```

Configure `kubectl` access for the `deploy` user:
```bash
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config
export KUBECONFIG=~/.kube/config
echo "export KUBECONFIG=~/.kube/config" >> ~/.bashrc
```

## 4. Build and Import the Image

Build the Docker image locally on the VM, save it as a tarball, and import it into K3s's containerd runtime so the cluster can run it without pulling from a public registry.

```bash
cd /home/deploy/revenue_agent
sudo docker build -t revenue-agent:latest .
sudo docker save revenue-agent:latest | sudo k3s ctr images import -
```

## 5. Deploy to Kubernetes

Apply the Kubernetes manifests from the `k8s/` directory.

```bash
kubectl apply -f k8s/
```

Verify the pods and services are running:
```bash
kubectl get pods
kubectl get svc
```

You should see `revenue-agent-service` allocated an external IP (or `<pending>` if accessing via the node's IP directly), but K3s's built-in ServiceLB will forward port 80 to your Flask application pods.

Your application is now running in K3s and accessible at `http://<your-vultr-ip>/`!
