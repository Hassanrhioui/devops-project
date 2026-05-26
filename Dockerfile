# ── Stage: Base image ──────────────────────────────────────────
# Start from the official Python 3.14.5 slim image.
# This gives us a minimal Linux environment with Python pre-installed.
FROM python:3.14.5-slim

# ── Set environment variables ──────────────────────────────────
# PYTHONDONTWRITEBYTECODE: Stops Python from writing .pyc bytecode files.
# These are unnecessary inside a container.
ENV PYTHONDONTWRITEBYTECODE=1

# PYTHONUNBUFFERED: Forces Python to output logs immediately without buffering.
# Critical for seeing your app's logs in real time via docker logs.
ENV PYTHONUNBUFFERED=1

# ── Set working directory ──────────────────────────────────────
# All subsequent commands run from this path inside the container.
# The directory is created automatically if it does not exist.
WORKDIR /app

# ── Install dependencies ───────────────────────────────────────
# Copy requirements.txt FIRST — before copying the rest of the code.
# Why: Docker caches each layer. If requirements.txt has not changed,
# Docker reuses the cached pip install layer on the next build.
# This saves significant time during development.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ── Copy application code ──────────────────────────────────────
# Copy everything else after installing dependencies.
# If only your code changes (not requirements), Docker skips
# the pip install layer and reuses the cache.
COPY . .

# ── Expose the port ────────────────────────────────────────────
# Documents that the container listens on port 5000.
# This does not publish the port — it is metadata for Docker and humans.
# The actual port binding happens when you run the container.
EXPOSE 5000

# ── Define the start command ───────────────────────────────────
# CMD defines what runs when the container starts.
# Using the list format (exec form) is preferred over the string form
# because it starts the process directly without a shell wrapper,
# ensuring signals like SIGTERM are passed correctly to Python.
CMD ["python", "run.py"]