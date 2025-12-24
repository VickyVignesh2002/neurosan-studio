# Neuro SAN Studio - Complete Installation & Deployment Guide

**Version:** 2.0  
**Last Updated:** December 24, 2025  
**Supports:** Windows, macOS, Linux, Azure Cloud

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Local Machine Setup](#local-machine-setup)
   - [Windows Installation](#windows-installation)
   - [macOS/Linux Installation](#macoslinux-installation)
4. [Ollama Setup](#ollama-setup)
   - [Installing Ollama](#installing-ollama)
   - [Pulling Models](#pulling-models)
   - [Configuring Ollama](#configuring-ollama)
5. [LLM Provider Configuration](#llm-provider-configuration)
6. [Running NeuroSAN](#running-neurosan)
7. [Azure Cloud Deployment](#azure-cloud-deployment)
   - [Azure VM Setup](#azure-vm-setup)
   - [Ollama on Azure](#ollama-on-azure)
   - [Docker Deployment on Azure](#docker-deployment-on-azure)
   - [Azure Container Instances](#azure-container-instances)
8. [Verification & Testing](#verification--testing)
9. [Troubleshooting](#troubleshooting)
10. [Quick Reference](#quick-reference)

---

## Overview

Neuro SAN Studio is a hands-on playground for the Neuro SAN multi-agent orchestration framework. This guide covers complete setup for both local development and Azure cloud deployment.

### Key Features
- 🗂️ **Data-Driven Configuration**: Agent networks defined via HOCON files
- 🔀 **Adaptive Communication**: AAOSA Protocol for autonomous task delegation
- 🛠️ **Flexible LLM Support**: OpenAI, Anthropic, Azure OpenAI, Google Gemini, Ollama
- 📈 **Multi-Agent Systems**: Build sophisticated AI agent networks
- 🌐 **Cloud-Agnostic**: Deploy anywhere - local, containers, or cloud

### Architecture Overview
```
┌─────────────────────────────────────────────────────────┐
│                    Neuro SAN Studio                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │   nsflow    │  │  HTTP API   │  │    gRPC API     │  │
│  │  Web UI     │  │  Port 8080  │  │   Port 30011    │  │
│  │ Port 4173   │  │             │  │                 │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────┤
│                    Agent Networks                        │
│  ┌─────────────────────────────────────────────────┐    │
│  │  HOCON Configs → Agents → LLM Providers         │    │
│  │  (registries/)   (coded_tools/)  (Ollama/OpenAI)│    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### Required Software

| Software | Minimum Version | Download Link |
|----------|-----------------|---------------|
| Python | 3.11+ (recommended 3.13) | [python.org](https://www.python.org/downloads/) |
| Git | 2.30+ | [git-scm.com](https://git-scm.com/downloads) |
| Ollama | Latest | [ollama.ai](https://ollama.ai/download) |

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 8 GB | 16 GB+ |
| Storage | 10 GB | 50 GB (for models) |
| CPU | 4 cores | 8+ cores |
| GPU (optional) | - | NVIDIA with 8GB+ VRAM |

### Required API Keys (Optional - choose one or more)

| Provider | Get API Key |
|----------|-------------|
| OpenAI | [platform.openai.com](https://platform.openai.com/signup) |
| Anthropic | [console.anthropic.com](https://console.anthropic.com/) |
| Google Gemini | [ai.google.dev](https://ai.google.dev/gemini-api/docs/api-key) |
| Azure OpenAI | [azure.microsoft.com](https://azure.microsoft.com/en-us/products/ai-services/openai-service/) |

> **Note:** Ollama provides FREE local LLM inference - no API key required!

---

## Local Machine Setup

### Windows Installation

#### Step 1: Install Python 3.13

```powershell
# Option 1: Download from python.org
# Visit https://www.python.org/downloads/ and install Python 3.13+

# Option 2: Using winget (Windows Package Manager)
winget install Python.Python.3.13

# Verify installation
python --version
# Expected output: Python 3.13.x
```

#### Step 2: Install Git

```powershell
# Using winget
winget install Git.Git

# Verify installation
git --version
```

#### Step 3: Clone the Repository

```powershell
# Navigate to your preferred directory
cd C:\Projects

# Clone the repository
git clone https://github.com/YOUR_USERNAME/neurosan-studio.git
cd neurosan-studio
```

#### Step 4: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip
```

#### Step 5: Install Dependencies

```powershell
# Install all required packages
pip install -r requirements.txt

# Verify neuro-san installation
pip show neuro-san
# Should show: Version: 0.6.21
```

#### Step 6: Configure Environment

```powershell
# Copy example environment file
Copy-Item .env.example .env

# Edit .env file with your configuration
notepad .env
```

**Required `.env` Configuration:**

```env
# Server Configuration
NEURO_SAN_SERVER_HOST="localhost"
NEURO_SAN_SERVER_GRPC_PORT=30011
NEURO_SAN_SERVER_HTTP_PORT=8080

# Thinking file path (Windows)
THINKING_FILE="C:\\tmp\\agent_thinking.txt"

# LLM Provider Selection (choose one)
LLM_PROVIDER=ollama

# Ollama Configuration (if using Ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct
OLLAMA_TEMPERATURE=0.7
OLLAMA_MAX_TOKENS=2048

# OR OpenAI Configuration (if using OpenAI)
# OPENAI_API_KEY=sk-your-api-key-here
# LLM_PROVIDER=openai
```

---

### macOS/Linux Installation

#### Step 1: Install Python 3.13

**macOS (using Homebrew):**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.13

# Verify installation
python3 --version
```

**Ubuntu/Debian Linux:**
```bash
# Update package list
sudo apt update

# Install Python 3.13
sudo apt install python3.13 python3.13-venv python3-pip

# Verify installation
python3 --version
```

**RHEL/CentOS/Fedora:**
```bash
# Fedora
sudo dnf install python3.13

# RHEL/CentOS (may need additional repos)
sudo yum install python3.13

# Verify
python3 --version
```

#### Step 2: Clone and Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/neurosan-studio.git
cd neurosan-studio

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit configuration
nano .env  # or vim .env
```

**Linux/macOS `.env` Configuration:**

```env
# Server Configuration
NEURO_SAN_SERVER_HOST="localhost"
NEURO_SAN_SERVER_GRPC_PORT=30011
NEURO_SAN_SERVER_HTTP_PORT=8080

# Thinking file path (Linux/macOS)
THINKING_FILE="/tmp/agent_thinking.txt"

# LLM Provider
LLM_PROVIDER=ollama

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct
OLLAMA_TEMPERATURE=0.7
```

---

## Ollama Setup

Ollama allows you to run powerful open-source LLMs locally without any API costs.

### Installing Ollama

#### Windows

```powershell
# Option 1: Download installer from ollama.ai
# Visit https://ollama.ai/download and run the installer

# Option 2: Using winget
winget install Ollama.Ollama

# Verify installation
ollama --version
```

#### macOS

```bash
# Using Homebrew
brew install ollama

# Or download from ollama.ai
curl -fsSL https://ollama.ai/install.sh | sh

# Verify
ollama --version
```

#### Linux

```bash
# Official install script
curl -fsSL https://ollama.ai/install.sh | sh

# Verify installation
ollama --version
```

### Starting Ollama Service

```bash
# Start Ollama server (runs in background)
ollama serve

# On Windows, Ollama typically starts automatically as a service
# Check if running:
curl http://localhost:11434/api/tags
```

### Pulling Models

Pull one or more models based on your needs:

#### Recommended Models

```bash
# Best balance of speed and quality (RECOMMENDED)
ollama pull mistral:7b-instruct

# Excellent for general tasks
ollama pull llama2

# Latest Llama model
ollama pull llama3.2

# For coding tasks
ollama pull deepseek-coder

# For chat applications
ollama pull neural-chat

# Lightweight and fast
ollama pull phi
```

#### Model Selection Guide

| Model | Size | Best For | Speed | Quality |
|-------|------|----------|-------|---------|
| `mistral:7b-instruct` | 4 GB | General use | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| `llama2` | 4-7 GB | Reasoning | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| `llama3.2` | 2-8 GB | Latest features | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| `deepseek-coder` | 7 GB | Code generation | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| `neural-chat` | 4 GB | Conversations | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| `phi` | 1.7 GB | Quick responses | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

#### Verify Models

```bash
# List installed models
ollama list

# Test a model
ollama run mistral "Hello, how are you?"
```

### Configuring Ollama

#### Basic Configuration in `.env`

```env
# Ollama Settings
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct
OLLAMA_TEMPERATURE=0.7
OLLAMA_TOP_P=0.9
OLLAMA_MAX_TOKENS=2048
OLLAMA_TIMEOUT=300
```

#### GPU Acceleration (NVIDIA)

Ollama automatically detects and uses NVIDIA GPUs. Ensure you have:

1. **NVIDIA Drivers** installed
2. **CUDA Toolkit** (optional but recommended)

```bash
# Check GPU detection
nvidia-smi

# Ollama will automatically use GPU if available
ollama run mistral "Test GPU acceleration"
```

---

## LLM Provider Configuration

### Using Ollama (FREE - No API Key Required)

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct
OLLAMA_TEMPERATURE=0.7
OLLAMA_MAX_TOKENS=2048
```

### Using OpenAI

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4o
```

### Using Anthropic Claude

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### Using Azure OpenAI

```env
LLM_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
OPENAI_API_VERSION=2024-12-01-preview
```

### Using Google Gemini

```env
LLM_PROVIDER=google
GOOGLE_API_KEY=your-google-api-key
GOOGLE_MODEL=gemini-pro
```

---

## Running NeuroSAN

### Quick Start

```bash
# Ensure virtual environment is activated
# Windows: .\venv\Scripts\Activate.ps1
# Linux/macOS: source venv/bin/activate

# Start NeuroSAN with default settings
python run.py
```

### Available Ports

| Service | Default Port | Description |
|---------|--------------|-------------|
| nsflow UI | 4173 | Web-based agent designer |
| HTTP API | 8080 | REST API endpoint |
| gRPC API | 30011 | gRPC service endpoint |

### Custom Configuration

```bash
# Run with custom ports
python run.py \
    --nsflow-port 4174 \
    --server-http-port 8081 \
    --server-grpc-port 30012

# Run with specific log level
python run.py --log-level debug
```

### Access the Application

Once running, open your browser:

- **nsflow Web UI:** http://localhost:4173
- **HTTP API:** http://localhost:8080
- **API Health Check:** http://localhost:8080/health

---

## Azure Cloud Deployment

### Azure VM Setup

#### Step 1: Create Azure VM

**Using Azure Portal:**

1. Go to [portal.azure.com](https://portal.azure.com)
2. Click "Create a resource" → "Virtual Machine"
3. Configure:
   - **Image:** Ubuntu Server 22.04 LTS
   - **Size:** Standard_D4s_v3 (4 vCPUs, 16 GB RAM) or larger
   - **For GPU:** Standard_NC6s_v3 or Standard_NC4as_T4_v3
   - **Networking:** Allow ports 22 (SSH), 4173, 8080, 11434
4. Create and wait for deployment

**Using Azure CLI:**

```bash
# Login to Azure
az login

# Create resource group
az group create --name neurosan-rg --location eastus

# Create VM (CPU-only)
az vm create \
    --resource-group neurosan-rg \
    --name neurosan-vm \
    --image Ubuntu2204 \
    --size Standard_D4s_v3 \
    --admin-username azureuser \
    --generate-ssh-keys \
    --public-ip-sku Standard

# Create VM (with GPU - for faster inference)
az vm create \
    --resource-group neurosan-rg \
    --name neurosan-gpu-vm \
    --image Ubuntu2204 \
    --size Standard_NC4as_T4_v3 \
    --admin-username azureuser \
    --generate-ssh-keys \
    --public-ip-sku Standard
```

#### Step 2: Open Required Ports

```bash
# Open ports for NeuroSAN
az vm open-port --resource-group neurosan-rg --name neurosan-vm --port 4173 --priority 1001
az vm open-port --resource-group neurosan-rg --name neurosan-vm --port 8080 --priority 1002
az vm open-port --resource-group neurosan-rg --name neurosan-vm --port 30011 --priority 1003
az vm open-port --resource-group neurosan-rg --name neurosan-vm --port 11434 --priority 1004
```

#### Step 3: Connect to VM

```bash
# Get public IP
az vm list-ip-addresses --resource-group neurosan-rg --name neurosan-vm --output table

# SSH into VM
ssh azureuser@<PUBLIC_IP>
```

### Ollama on Azure

#### Install Ollama on Azure VM

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
sudo systemctl enable ollama
sudo systemctl start ollama

# Verify
ollama --version
```

#### Configure Ollama for Remote Access

```bash
# Edit Ollama service to listen on all interfaces
sudo mkdir -p /etc/systemd/system/ollama.service.d
sudo tee /etc/systemd/system/ollama.service.d/override.conf << EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
EOF

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart ollama

# Verify it's listening on all interfaces
curl http://localhost:11434/api/tags
```

#### Pull Models on Azure

```bash
# Pull recommended models (may take 10-30 minutes depending on size)
ollama pull mistral:7b-instruct
ollama pull llama2

# For GPU VMs, you can run larger models
ollama pull llama2:70b  # 40GB+ download
```

#### GPU Setup for Azure (NVIDIA T4/A100)

```bash
# Install NVIDIA drivers (for NC-series VMs)
sudo apt install -y nvidia-driver-535

# Reboot
sudo reboot

# After reboot, verify GPU
nvidia-smi

# Ollama will automatically use GPU
ollama run mistral "Hello from Azure GPU!"
```

### Install NeuroSAN on Azure VM

```bash
# Install Python 3.13
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev -y

# Clone repository
git clone https://github.com/YOUR_USERNAME/neurosan-studio.git
cd neurosan-studio

# Setup virtual environment
python3.13 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env
```

**Azure `.env` Configuration:**

```env
# Azure VM Configuration
NEURO_SAN_SERVER_HOST="0.0.0.0"
NEURO_SAN_SERVER_GRPC_PORT=30011
NEURO_SAN_SERVER_HTTP_PORT=8080
NSFLOW_HOST="0.0.0.0"

# Thinking file
THINKING_FILE="/tmp/agent_thinking.txt"

# Ollama (local on same VM)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct
OLLAMA_TEMPERATURE=0.7
```

#### Run NeuroSAN as Background Service

```bash
# Option 1: Using nohup
nohup python run.py > neurosan.log 2>&1 &

# Option 2: Using screen
screen -S neurosan
python run.py
# Press Ctrl+A, then D to detach

# Option 3: Using systemd (recommended for production)
sudo tee /etc/systemd/system/neurosan.service << EOF
[Unit]
Description=NeuroSAN Studio
After=network.target ollama.service

[Service]
Type=simple
User=azureuser
WorkingDirectory=/home/azureuser/neurosan-studio
Environment=PATH=/home/azureuser/neurosan-studio/venv/bin
ExecStart=/home/azureuser/neurosan-studio/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable neurosan
sudo systemctl start neurosan
sudo systemctl status neurosan
```

### Docker Deployment on Azure

#### Build Docker Image

```bash
# On your local machine or Azure VM
cd neurosan-studio

# Build the Docker image
docker build -f deploy/Dockerfile -t neurosan-studio:latest .
```

#### Run with Docker

```bash
# Run with Ollama (host network for Ollama access)
docker run -d \
    --name neurosan \
    --network host \
    -e OLLAMA_BASE_URL=http://localhost:11434 \
    -e OLLAMA_MODEL=mistral:7b-instruct \
    -e LLM_PROVIDER=ollama \
    -v $(pwd)/registries:/usr/local/neuro-san/myapp/registries \
    neurosan-studio:latest

# Or with OpenAI
docker run -d \
    --name neurosan \
    -p 8080:8080 \
    -p 30011:30011 \
    -e OPENAI_API_KEY=sk-your-key \
    -e LLM_PROVIDER=openai \
    neurosan-studio:latest
```

#### Docker Compose with Ollama

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

  neurosan:
    build:
      context: .
      dockerfile: deploy/Dockerfile
    container_name: neurosan
    ports:
      - "4173:4173"
      - "8080:8080"
      - "30011:30011"
    environment:
      - LLM_PROVIDER=ollama
      - OLLAMA_BASE_URL=http://ollama:11434
      - OLLAMA_MODEL=mistral:7b-instruct
    depends_on:
      - ollama
    volumes:
      - ./registries:/usr/local/neuro-san/myapp/registries
      - ./coded_tools:/usr/local/neuro-san/myapp/coded_tools

volumes:
  ollama_data:
```

```bash
# Start all services
docker-compose up -d

# Pull model in Ollama container
docker exec -it ollama ollama pull mistral:7b-instruct

# View logs
docker-compose logs -f
```

### Azure Container Instances (ACI)

For serverless container deployment:

```bash
# Create container registry
az acr create --resource-group neurosan-rg --name neurosanregistry --sku Basic

# Login to registry
az acr login --name neurosanregistry

# Tag and push image
docker tag neurosan-studio:latest neurosanregistry.azurecr.io/neurosan-studio:latest
docker push neurosanregistry.azurecr.io/neurosan-studio:latest

# Create container instance
az container create \
    --resource-group neurosan-rg \
    --name neurosan-aci \
    --image neurosanregistry.azurecr.io/neurosan-studio:latest \
    --cpu 4 \
    --memory 16 \
    --ports 8080 30011 \
    --environment-variables \
        LLM_PROVIDER=openai \
        OPENAI_API_KEY=sk-your-key \
    --dns-name-label neurosan-demo
```

---

## Verification & Testing

### Health Checks

```bash
# Check Ollama
curl http://localhost:11434/api/tags

# Check NeuroSAN HTTP API
curl http://localhost:8080/health

# Check nsflow UI
curl http://localhost:4173
```

### Test Agent Networks

1. Open http://localhost:4173 in your browser
2. Select "Music Nerd" from the agent dropdown
3. Type: "What are the best albums of 2024?"
4. Verify you get a response

### Run Tests

```bash
# Run unit tests
pytest tests/ -v

# Run integration tests
pytest tests/integration/ -v --integration
```

---

## Troubleshooting

### Common Issues

#### 1. "Connection refused" to Ollama

```bash
# Check if Ollama is running
systemctl status ollama  # Linux
ollama serve             # Start manually

# Verify connection
curl http://localhost:11434/api/tags
```

#### 2. Port Already in Use

```bash
# Find process using port (Linux/macOS)
lsof -i :8080
kill -9 <PID>

# Windows PowerShell
Get-NetTCPConnection -LocalPort 8080 | Select-Object OwningProcess
Stop-Process -Id <PID> -Force
```

#### 3. Model Not Found

```bash
# List installed models
ollama list

# Pull missing model
ollama pull mistral:7b-instruct

# Update .env with exact model name
```

#### 4. Out of Memory

```bash
# Use smaller model
ollama pull phi  # Only 1.7GB

# Update .env
OLLAMA_MODEL=phi
```

#### 5. Slow Responses

- Use GPU if available
- Switch to smaller/faster model
- Reduce `OLLAMA_MAX_TOKENS`

### Logs

```bash
# NeuroSAN logs
tail -f logs/runner.log.*

# Ollama logs
journalctl -u ollama -f  # Linux
```

---

## Quick Reference

### Essential Commands

```bash
# Start NeuroSAN
python run.py

# Start Ollama
ollama serve

# Pull a model
ollama pull mistral:7b-instruct

# List models
ollama list

# Test model
ollama run mistral "Hello!"

# Check ports (Linux)
ss -tlnp | grep -E '8080|4173|11434|30011'
```

### Environment Variables Summary

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM backend (ollama/openai/anthropic) | ollama |
| `OLLAMA_BASE_URL` | Ollama server URL | http://localhost:11434 |
| `OLLAMA_MODEL` | Model name | mistral:7b-instruct |
| `NEURO_SAN_SERVER_HTTP_PORT` | HTTP API port | 8080 |
| `NEURO_SAN_SERVER_GRPC_PORT` | gRPC API port | 30011 |
| `NSFLOW_PORT` | nsflow UI port | 4173 |

### Useful URLs

- **nsflow UI:** http://localhost:4173
- **HTTP API:** http://localhost:8080
- **Ollama API:** http://localhost:11434
- **API Docs:** http://localhost:8080/docs

---

## Support

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/neurosan-studio/issues)
- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/neurosan-studio/discussions)
- **Documentation:** See [docs/](docs/) folder

---

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.txt](LICENSE.txt) file for details.

---

**Happy Building with Neuro SAN! 🚀**
