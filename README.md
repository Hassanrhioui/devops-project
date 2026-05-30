# DevOps Project — Hassan Rhioui

A production-equivalent DevOps pipeline built from scratch, demonstrating containerisation, CI/CD automation, and server deployment using industry-standard tools.

---

## Live Demo

> **Application:** `http://192.168.0.19`
> **Health Check:** `http://192.168.0.19/health`
> **Status:** `http://192.168.0.19/status`

---

## Project Overview

This project implements a complete DevOps workflow for a Python Flask web application. Every component reflects real-world practices used in professional DevOps and cloud engineering roles.

```
Developer pushes code
        ↓
GitHub Actions triggers automatically
        ↓
Tests run (pytest)
        ↓
Docker image built and pushed to Docker Hub + GHCR
        ↓
Self-hosted runner deploys to Linux server
        ↓
Health check verifies deployment
        ↓
Application live with monitoring active
```

---

## Tech Stack

| Category | Technology |
|---|---|
| **Application** | Python 3.11, Flask 3.0 |
| **Testing** | pytest |
| **Containerisation** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Container Registry** | Docker Hub, GitHub Container Registry (GHCR) |
| **Web Server** | Nginx (reverse proxy) |
| **Server OS** | Ubuntu 26.04 LTS |
| **Version Control** | Git, GitHub |
| **Monitoring** | Custom bash monitor, cron scheduling |
| **Security** | SSH key authentication, UFW firewall |

---

## Repository Structure

```
devops-project/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions pipeline
│
├── app/
│   ├── __init__.py            # Flask application factory
│   ├── routes.py              # URL routes and endpoints
│   └── static/
│       └── index.html         # Portfolio frontend
│
├── tests/
│   └── test_routes.py         # Automated pytest test suite
│
├── Dockerfile                 # Container build instructions
├── docker-compose.yml         # Local container orchestration
├── .dockerignore              # Docker build exclusions
├── run.py                     # Application entry point
├── requirements.txt           # Python dependencies (pinned)
└── .gitignore                 # Git exclusions
```

---

## CI/CD Pipeline

The pipeline is defined in `.github/workflows/ci-cd.yml` and consists of three jobs:

### Job 1 — Run Tests
- Triggers on every push to `develop` and `main`
- Sets up Python 3.11 on a fresh Ubuntu runner
- Installs dependencies from `requirements.txt`
- Runs the full pytest suite
- Pipeline stops here if any test fails

### Job 2 — Build and Push Docker Image
- Runs only on pushes to `main`
- Requires Job 1 to pass (`needs: test`)
- Logs in to Docker Hub and GitHub Container Registry
- Builds Docker image using `docker/build-push-action`
- Pushes two tags: `latest` and `sha-xxxxxxx` (immutable per commit)
- Uses registry-based layer caching for fast builds

### Job 3 — Deploy to Server
- Runs only on pushes to `main`
- Requires Job 2 to pass (`needs: build-and-push`)
- Executed by a self-hosted GitHub Actions runner on the Ubuntu VM
- Runs `~/deploy.sh` which pulls the new image and restarts the container
- Verifies deployment by calling `/status` endpoint
- Marks pipeline as failed if app does not respond after deployment

```
Push to develop:   test ✅
Push to main:      test ✅ → build-and-push ✅ → deploy ✅
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Serves the portfolio frontend |
| `/health` | GET | Returns app status, uptime, and system info |
| `/status` | GET | Lightweight status check for monitoring |

### `/health` Response Example

```json
{
  "status": "healthy",
  "service": "devops-project",
  "version": "1.0.0",
  "uptime": {
    "seconds": 3600,
    "minutes": 60,
    "hours": 1
  },
  "system": {
    "python": "3.11.x",
    "platform": "Linux",
    "node": "hassanrh-VirtualBox"
  }
}
```

---

## Docker

### Build Locally

```bash
docker build -t devops-project:latest .
```

### Run Locally

```bash
docker compose up -d
```

### Run Tests Inside Container

```bash
docker run --rm devops-project:latest pytest tests/ -v
```

### Pull from Docker Hub

```bash
docker pull hassan23rh/devops-project:latest
docker run -p 5000:5000 hassan23rh/devops-project:latest
```

---

## Local Development Setup

### Prerequisites

- Python 3.11+
- Docker Desktop
- Git

### Steps

```bash
# Clone the repository
git clone https://github.com/Hassanrhioui/devops-project.git
cd devops-project

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py

# Run tests
pytest tests/ -v
```

Application available at `http://localhost:5000`

---

## Branching Strategy

```
main      → production branch — deploys automatically on push
develop   → integration branch — CI tests run, no deployment
```

**Workflow:**

```bash
# Work on develop
git checkout develop
# make changes
git add .
git commit -m "feat: description"
git push origin develop

# Deploy to production
git checkout main
git merge develop
git push origin main
```

---

## Server Setup (Ubuntu VM)

The deployment target is an Ubuntu 26.04 LTS server (VirtualBox VM with bridged networking).

### Key configurations

- **Static IP:** `192.168.0.19`
- **SSH:** Key-based authentication only, password login disabled
- **Firewall:** UFW — ports 22, 80, 5000 allowed
- **Nginx:** Reverse proxy — port 80 → port 5000
- **Docker:** Container runs with `--restart unless-stopped`
- **Monitoring:** Cron job runs `monitor.sh` every minute

### Monitoring and Auto-Recovery

A bash script (`~/monitor.sh`) runs every minute via cron. It:
1. Calls `/status` endpoint
2. Logs failures with timestamps to `/var/log/devops-monitor.log`
3. Automatically restarts the container if it is not responding
4. Only logs errors and hourly confirmations to keep log files lean

### Log Rotation

Docker log rotation is configured in `/etc/docker/daemon.json`:
- Maximum log file size: 10MB
- Maximum log files kept: 3 (30MB total per container)

---

## GitHub Secrets Required

| Secret | Description |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub account username |
| `DOCKERHUB_TOKEN` | Docker Hub access token (Read & Write) |
| `SERVER_HOST` | IP address of the deployment server |
| `SERVER_USER` | SSH username on the deployment server |
| `SSH_PRIVATE_KEY` | Private SSH key for server authentication |

---

## What I Learned

Building this project gave me hands-on experience with:

- Writing production-grade Dockerfiles with layer caching optimisation
- Designing multi-job GitHub Actions pipelines with job dependencies
- Configuring SSH key authentication and server hardening
- Setting up Nginx as a reverse proxy for a containerised application
- Managing Docker images across multiple registries
- Writing bash scripts for automated deployment and health monitoring
- Scheduling tasks with cron
- Applying the principle of least privilege with a dedicated deploy user
- Using Git branching strategy in a professional workflow

---

## Author

**Hassan Rhioui**
IT Graduate — Finland

- GitHub: [github.com/Hassanrhioui](https://github.com/Hassanrhioui)
- LinkedIn: [linkedin.com/in/hassan-rhioui](https://www.linkedin.com/in/rhioui-hassan-691387120/)

---

## License

This project is open source and available under the [MIT License](LICENSE).