# Neuro SAN Studio - Complete Codebase Overview

**Setup Date:** December 21, 2025  
**Repository:** https://github.com/cognizant-ai-lab/neuro-san-studio.git  
**Status:** ✅ Cloned, Virtual Environment Created, All Dependencies Installed

---

## 📋 Executive Summary

**Neuro SAN Studio** is an open-source, data-driven multi-agent orchestration framework by Cognizant designed to simplify building intelligent, collaborative AI systems. It enables rapid development of sophisticated multi-agent applications using declarative HOCON configuration files, supporting multiple LLM providers (OpenAI, Anthropic, Azure, Ollama, Google Gemini, etc.).

### Core Purpose
- **Build multi-agent networks in minutes** without extensive coding
- **Declarative configuration approach** using HOCON format
- **Adaptive inter-agent communication** using the AAOSA Protocol
- **Enterprise-ready** with robust tracing, logging, and observability
- **Cloud-agnostic** deployment with support for local, container, and cloud environments

---

## 🏗️ Directory Structure & Components

### 1. **Root Level Files**

#### Key Executable & Configuration
- **`run.py`** (563 lines)
  - Main entry point for starting the Neuro SAN server and web client
  - Handles CLI argument parsing
  - Manages process lifecycle (server, web client, plugins)
  - Supports optional parameters: `--nsflow` (developer UI), `--flask` (web UI), `--phoenix` (observability)
  - **Usage:** `python -m run` or `python run.py`

#### Configuration & Documentation
- **`.env.example`** (125 lines)
  - Template for environment variables
  - Contains LLM API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)
  - Server configuration (HOST, PORT, WEB_CLIENT_PORT)
  - THINKING_FILE path configuration
  
- **`pyproject.toml`**
  - Project metadata and build configuration
  - Tool configurations: isort, black, flake8, pylint, pytest, coverage
  - Line length: 119 characters
  - Testing setup with pytest and coverage (target: 10.0+ fail rate)

- **`requirements.txt`**
  - Core dependencies including:
    - `neuro-san==0.6.21` (main framework)
    - `nsflow==0.6.4` (web UI framework)
    - `python-dotenv==1.0.1` (environment variable management)
    - LLM integrations: `langchain-anthropic`, `langchain-openai`
    - Observability: OpenTelemetry, Phoenix
    - Tools: pypdf, aiofiles, rich

- **`requirements-build.txt`**
  - Development and testing dependencies
  - Code quality: black, flake8, pylint, isort
  - Testing: pytest, pytest-asyncio, pytest-cov, pytest-xdist
  - Code analysis: pymarkdownlnt, coverage

- **`logging.json`**
  - Logging configuration for local development
  - JSON-formatted logging setup

- **`Makefile`**
  - Convenience commands for common tasks (build, test, lint, format)

---

### 2. **`/apps`** - Application Implementations

Contains example applications demonstrating Neuro SAN capabilities:

```
apps/
├── conscious_assistant/          # Advanced consciousness-like behavior
├── cruse/                         # CRUSE agent framework example
├── log_analyzer/                  # Real-time log analysis agent
├── slack/                         # Slack bot integration
├── wwaw/                          # Web & Web Apps example
└── __init__.py
```

**Purpose:** Each folder contains complete, runnable applications demonstrating:
- Multi-agent orchestration patterns
- Integration with external services
- Real-world use cases

---

### 3. **`/coded_tools`** - Custom Python Tools & Extensions

Custom Python implementations that agents can use. Organized by use case:

```
coded_tools/
├── agent_network_architect/       # Creates custom agent architectures
├── agent_network_designer/        # Meta-agent for designing networks
├── agent_network_editor/          # Editor for agent configurations
├── agent_network_instructions_editor/  # Editor for agent instructions
├── anthropic_tool.py              # Anthropic-specific tool implementations
├── basic/                         # Basic utility tools
│   ├── advanced_calculator/       # Complex mathematical operations
│   ├── coffee_finder_advanced/    # Location-based search example
│   ├── music_nerd_pro/            # Music database tools
│   ├── music_nerd_pro_local/      # Local music tools
│   ├── music_nerd_pro_sly/        # Sly Data protected tools
│   └── music_nerd_pro_sly_local/  # Local Sly Data tools
├── cruse_agent/                   # CRUSE agent tools
├── get_agent_network_definition.py # Utility to retrieve network definitions
├── industry/                      # Industry-specific tools (finance, healthcare, etc.)
├── kwik_agents/                   # KWIK learning agent tools
├── openai_tool.py                 # OpenAI-specific tool implementations
├── smart_home/                    # Smart home automation tools
├── tools/                         # Shared tool utilities
└── __init__.py
```

**Key Features:**
- Extensible Python tool framework
- Integration with LLM provider-specific capabilities
- Support for custom coded tools that agents invoke

---

### 4. **`/registries`** - HOCON Agent Configuration Files

Central registry of agent network definitions using HOCON (Human-Optimized Config Object Notation):

```
registries/
├── aaosa.hocon                    # AAOSA Protocol implementation
├── aaosa_basic.hocon              # Basic AAOSA example
├── agent_network_architect.hocon  # Architecture designer agent
├── agent_network_designer.hocon   # Network designer agent
├── agent_network_editor.hocon     # Configuration editor agent
├── agent_network_instructions_editor.hocon  # Instructions editor
├── agent_network_query_generator.hocon      # Query generation
├── basic/                         # Basic examples
│   ├── advanced_calculator.hocon  # Math operations
│   ├── coffee_finder.hocon        # Location finder
│   ├── coffee_finder_advanced.hocon
│   ├── hello_world.hocon          # "Hello World" agent
│   ├── music_nerd.hocon           # Music expert agent
│   ├── music_nerd_llm_fallbacks.hocon  # Fallback handling
│   ├── music_nerd_local.hocon     # Local LLM variant
│   ├── music_nerd_pro.hocon       # Professional music agent
│   ├── music_nerd_pro_local.hocon # Local variant
│   ├── music_nerd_pro_sly.hocon   # Sly Data variant
│   ├── music_nerd_pro_sly_local.hocon
│   └── smart_home.hocon           # Smart home control
├── conscious_agent.hocon          # Consciousness experiment
├── cpg_agents.hocon               # CPG (Central Pattern Generator) agents
├── cruse_agent.hocon              # CRUSE agent network
├── industry/                      # Industry-specific networks
│   ├── Airline Policy 360        # Airline operations
│   ├── Banking Operations         # Financial services
│   ├── Consumer Decisions         # E-commerce recommendations
│   ├── Insurance Underwriting     # Insurance processes
│   ├── Real Estate Agent          # Property management
│   ├── Retail Operations          # Retail customer service
│   ├── Telco Network Orchestration
│   └── Therapy Vignette Supervision
├── keybank.hocon                  # Banking example
├── kwik_agents.hocon              # KWIK learning agents
├── log_analysis_agents.hocon      # Log analysis network
├── manifest.hocon                 # Network manifest/registry
├── manifest_deploy.hocon          # Deployment manifest
├── six_thinking_hats.hocon        # De Bono's thinking hats
├── tools/                         # Tool registry and definitions
└── __init__.py
```

**HOCON Format Highlights:**
- Declarative agent network definitions
- Agent roles, capabilities, and tools
- LLM provider configurations
- Inter-agent communication patterns
- Protocol definitions (AAOSA)

---

### 5. **`/plugins`** - Observability & Monitoring Plugins

Framework for adding monitoring and tracing capabilities:

```
plugins/
├── log_bridge/
│   └── process_log_bridge.py      # Log aggregation bridge
├── phoenix/
│   └── phoenix_plugin.py           # Phoenix AI observability integration
└── __init__.py
```

**Capabilities:**
- **Log Bridge:** Centralized logging across agent processes
- **Phoenix Plugin:** Real-time tracing and observability for agent interactions
- Supports OpenTelemetry for distributed tracing
- Session-level metrics and debugging information

---

### 6. **`/servers`** - External Integration Servers

Bridges to external systems and protocols:

```
servers/
├── a2a/                           # Agent-to-Agent (A2A) protocol
├── mcp/                           # Model Context Protocol (MCP)
├── neuro_san/                     # Core Neuro SAN server
└── __init__.py
```

**Integrations:**
- **A2A Protocol:** Communication between Neuro SAN agents and other frameworks (CrewAI, etc.)
- **MCP:** Model Context Protocol for context and tool management
- **Core Server:** Main Neuro SAN gRPC/HTTP server

---

### 7. **`/docs`** - Documentation

Comprehensive documentation and examples:

```
docs/
├── api_key.md                     # API key setup and testing
├── comparative_analysis.md        # Comparison with other frameworks
├── dev_guide.md                   # Developer guide
├── examples/                      # Detailed example implementations
│   ├── basic/
│   ├── tools/
│   ├── industry/
│   └── [20+ use-case examples]
├── examples.md                    # Complete examples index (451 lines)
├── images/                        # Screenshots and diagrams
├── integration_quickstart.md      # Quick setup for integrations
├── search_tools.md                # Documentation for search tools
├── toolbox.md                     # Tool usage guide
├── tutorial.md                    # Step-by-step tutorials
└── user_guide.md                  # User manual
```

---

### 8. **`/mcp`** - Model Context Protocol Implementation

MCP-specific implementations:

```
mcp/
├── [MCP servers and configurations]
```

---

### 9. **`/tests`** - Test Suite

Comprehensive testing with pytest:

```
tests/
├── [Unit and integration tests]
└── [Test fixtures and mocks]
```

**Testing Framework:**
- pytest with asyncio support
- Coverage reporting (target >80%)
- Parameterized tests for multiple scenarios
- Integration tests marked for external services

---

## 🔑 Core Technologies & Dependencies

### LLM Provider Support
- **OpenAI:** GPT-4, GPT-3.5, Embeddings
- **Anthropic:** Claude 3 family
- **Azure OpenAI:** Enterprise deployments
- **Google Gemini:** Multi-modal capabilities
- **Ollama:** Local LLM support
- **Custom:** Extensible provider interface

### Framework Stack
- **langchain** & **langchain-core**: LLM orchestration
- **langgraph**: Agent state graphs
- **pydantic**: Data validation
- **fastapi** & **nsflow**: Web interface
- **grpcio**: Inter-service communication
- **boto3**: AWS integration
- **opentelemetry**: Distributed tracing

### Observability
- **OpenTelemetry SDK & API**: Tracing framework
- **Phoenix**: AI application observability
- **Custom Log Bridge**: Process-level logging aggregation

### Data & Tools
- **pypdf**: PDF processing
- **beautifulsoup4**: HTML/XML parsing
- **langchain-community**: 100+ tool integrations
- **langchain-mcp-adapters**: MCP protocol support

---

## 🚀 How to Run the Application

### Prerequisites
- Python 3.12+ (tested with 3.13)
- Virtual environment activated: `.venv\Scripts\Activate.ps1` (Windows)

### Step 1: Configure Environment Variables

Copy `.env.example` to `.env` and update:

```bash
# .env file setup
NEURO_SAN_SERVER_HOST=localhost
NEURO_SAN_SERVER_PORT=30013
NEURO_SAN_WEB_CLIENT_PORT=5003
OPENAI_API_KEY=your_actual_key_here  # Required for OpenAI models
ANTHROPIC_API_KEY=optional_key       # For Claude models
THINKING_FILE=C:\tmp\agent_thinking.txt  # Windows path
```

### Step 2: Start the Application

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run with default settings (gRPC server + Flask web client)
python -m run

# Run with nsflow UI (Vite-based developer UI on port 4173)
python -m run --nsflow

# Run with Phoenix observability enabled
python -m run --phoenix

# Run with all features
python -m run --nsflow --phoenix
```

### What Starts:
1. **Neuro SAN Server** (gRPC): localhost:30013
2. **Web Client**: localhost:5003 (Flask) or localhost:4173 (nsflow)
3. **Optional Phoenix**: Port 6062 (observability dashboard)

### Expected Output:
```
Root directory: j:\Company\amasQIS\AI\NeuroSan\Neurosan-v02
Starting Neuro SAN server...
Server running on localhost:30013
Web client ready at http://localhost:5003
```

---

## 📚 Key Examples to Explore

### Basic Examples (Start Here!)
1. **Hello World** (`registries/basic/hello_world.hocon`)
   - Single agent, basic setup
   - Great for understanding HOCON format

2. **Music Nerd** (`registries/basic/music_nerd.hocon`)
   - Single music expert agent
   - Tests follow-up questions
   - Deterministic answer testing

3. **Music Nerd Pro** (`registries/basic/music_nerd_pro.hocon`)
   - Frontman agent with specialized sub-agents
   - Demonstrates tool integration
   - Shows multi-agent delegation

4. **Coffee Finder** (`registries/basic/coffee_finder.hocon`)
   - Location-based search
   - Real-world integration example

### Advanced Examples
- **AAOSA Protocol** (Adaptive Autonomous Orchestration of Semi-Autonomous Agents)
- **Agent Network Designer** (Meta-agent that creates other agents)
- **CRUSE** (Cognitive Robot Understanding through Social Exploration)
- **Conscious Assistant** (Consciousness experiment)

### Industry Examples (`registries/industry/`)
- Banking Operations
- Insurance Underwriting
- Retail Customer Service
- Healthcare (Therapy Vignette Supervision)
- Real Estate Agent Network
- Airline Policy Assistant
- Telco Network Orchestration
- Sentiment Analysis

---

## 🛠️ Common Tasks

### Create a New Agent Network

1. **Create HOCON file** in `registries/` or `registries/basic/`:
```hocon
agents {
  my_agent {
    description = "My agent description"
    instructions = "Agent instructions..."
    model = "openai/gpt-4"
    tools = [...]
  }
}
```

2. **Define tools** in `coded_tools/` if needed
3. **Update manifest** in `registries/manifest.hocon`
4. **Run via CLI** or web interface

### Add Custom Python Tool

1. Create file in `coded_tools/your_tool_folder/`
2. Implement tool class inheriting from base
3. Register in HOCON configuration
4. Test with agent network

### Enable Observability

```bash
# With Phoenix tracing
python -m run --phoenix

# Access dashboard at http://localhost:6062
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│           Neuro SAN Studio Application                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Web Client   │  │ nsflow UI    │  │ CLI Interface│  │
│  │ (Flask)      │  │ (Vite)       │  │              │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │           │
│         └─────────────────┼─────────────────┘           │
│                           │                              │
│                    ┌──────▼──────┐                       │
│                    │ Neuro SAN   │                       │
│                    │ gRPC Server │                       │
│                    │ (port 30013)│                       │
│                    └──────┬──────┘                       │
│                           │                              │
│        ┌──────────────────┼──────────────────┐           │
│        │                  │                  │           │
│  ┌─────▼────┐    ┌────────▼────────┐ ┌────▼─────────┐  │
│  │  /apps   │    │ /registries     │ │   /plugins   │  │
│  │          │    │ (HOCON configs) │ │  (Phoenix,   │  │
│  │Applications│   │ Agent networks  │ │ Log Bridge)  │  │
│  └──────────┘    └─────────────────┘ └──────────────┘  │
│        │                  │                  │           │
│  ┌─────▼────────────────────────────────────▼────────┐  │
│  │         /coded_tools                               │  │
│  │   Custom Python Tool Implementations              │  │
│  │   (Calculators, Searchers, Analyzers, etc.)      │  │
│  └──────────────────────────────────────────────────┘  │
│        │                                                 │
│  ┌─────▼────────────────────────────────────────────┐  │
│  │      LLM Integrations & External Services       │  │
│  │  (OpenAI, Anthropic, Azure, Ollama, etc.)      │  │
│  │  (ServiceNow, Slack, Gmail, etc.)              │  │
│  └──────────────────────────────────────────────────┘  │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 Multi-Agent Communication Flow

```
User Query
    │
    ▼
┌─────────────────────┐
│  Frontman Agent     │
│  (Task Router)      │
└────────┬────────────┘
         │
    ┌────┴────────────────────────┐
    │                             │
    ▼                             ▼
┌──────────────┐          ┌──────────────┐
│  Sub-Agent 1 │          │  Sub-Agent 2 │
│  (Specialist)│          │ (Specialist) │
└──────┬───────┘          └──────┬───────┘
       │                         │
       ▼                         ▼
    [Tool 1]                  [Tool 2]
  [LLM Call]                [LLM Call]
       │                         │
       └────────────┬────────────┘
                    ▼
            ┌──────────────────┐
            │  Response Merger │
            │  (Frontman)      │
            └────────┬─────────┘
                     ▼
                User Response
```

---

## 📝 File Statistics Summary

| Component | Count | Purpose |
|-----------|-------|---------|
| HOCON Configs | 30+ | Agent network definitions |
| Python Tools | 10+ | Custom implementations |
| Example Apps | 5+ | Complete applications |
| Doc Files | 10+ | Comprehensive documentation |
| Test Files | TBD | Unit & integration tests |

---

## 🔐 Security & Data Protection

### Sly Data Feature
- Sensitive data protection between agents
- Data remains encrypted during inter-agent communication
- Prevents direct LLM exposure to sensitive information

### API Key Management
- Environment variables via `.env` file
- Support for multiple LLM providers
- Secure credential handling

### Network Security
- gRPC with TLS support
- CORS-enabled web endpoints
- Optional authentication layers

---

## 🌐 Supported LLM Models

### OpenAI
- gpt-4, gpt-4-turbo, gpt-3.5-turbo
- DALL-E for image generation
- Code Interpreter capability

### Anthropic
- Claude 3 Opus, Sonnet, Haiku
- Code execution capability
- Extended context windows

### Azure OpenAI
- Enterprise deployment
- Regional endpoints
- Managed service

### Google Gemini
- Multi-modal capabilities
- Image understanding
- Code execution

### Local Models (Ollama)
- Run models locally
- Privacy-focused
- Cost-effective

---

## ✅ Current Setup Status

| Task | Status | Details |
|------|--------|---------|
| Repository Clone | ✅ Complete | 9,801 objects, 54.38 MiB |
| Virtual Environment | ✅ Complete | Python 3.13 |
| Dependencies Install | ✅ Complete | 150+ packages installed |
| neuro-san Framework | ✅ Complete | v0.6.21 installed |
| nsflow UI | ✅ Complete | v0.6.4 installed |
| LangChain Suite | ✅ Complete | All providers installed |
| Documentation | ✅ Complete | All docs available |
| Tests Ready | ✅ Ready | pytest configured |
| Phoenix Optional | ✅ Ready | Install additional deps if needed |

---

## 🎯 Next Steps to Get Started

1. **Copy `.env.example` to `.env`** and add your API keys
2. **Choose a basic example** (Music Nerd recommended)
3. **Run the application**: `python -m run --nsflow`
4. **Open web UI** at http://localhost:4173
5. **Create test queries** against the example agents
6. **Explore HOCON configs** to understand agent definitions
7. **Build your own agent network** following the examples

---

## 📖 Documentation Files

- **[README.md](README.md)** - Project overview
- **[docs/examples.md](docs/examples.md)** - 20+ complete examples
- **[docs/dev_guide.md](docs/dev_guide.md)** - Developer guide
- **[docs/api_key.md](docs/api_key.md)** - API setup instructions
- **[docs/user_guide.md](docs/user_guide.md)** - User manual
- **[docs/comparative_analysis.md](docs/comparative_analysis.md)** - Comparison with other frameworks

---

## 🤝 Contributing & Support

- **GitHub:** https://github.com/cognizant-ai-lab/neuro-san-studio
- **Issues:** Report bugs and request features
- **Discussions:** Community Q&A and collaboration
- **DeepWiki:** Ask AI questions about the codebase

---

**Generated:** December 21, 2025 | **System:** Windows | **Python:** 3.13 | **Framework:** Neuro SAN 0.6.21
