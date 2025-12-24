# Neuro SAN Studio - Quick Start Guide

**Generated:** December 21, 2025  
**Status:** ✅ System Ready for Use

---

## 🎯 What You Have Now

Your Neuro SAN Studio instance is **fully installed and running** with:

- ✅ **Repository:** Cloned from GitHub (9,801 objects)
- ✅ **Virtual Environment:** Python 3.13 with 150+ packages
- ✅ **Framework:** Neuro SAN 0.6.21 + nsflow 0.6.4
- ✅ **LLM Support:** OpenAI, Anthropic, Azure, Google Gemini, Ollama
- ✅ **Documentation:** Comprehensive codebase overview created
- ✅ **Server:** HTTP (8081), gRPC (30014), nsflow UI (4174)

---

## 🚀 Running the Application

### Start the Server

```powershell
# Navigate to project directory
cd "j:\Company\amasQIS\AI\NeuroSan\Neurosan-v02"

# Activate virtual environment (if not already active)
.\venv\Scripts\Activate.ps1

# Run with default settings (server + nsflow UI)
python run.py

# Or with custom ports
python run.py --nsflow-port 4174 --server-http-port 8081 --server-grpc-port 30014
```

### Access the Web Interface

Once the server is running, open your browser:

- **nsflow Developer UI:** http://localhost:4174
- **HTTP API:** http://localhost:8081
- **gRPC Server:** localhost:30014

---

## 📝 Configuration

### Setting Up API Keys

Edit `j:\Company\amasQIS\AI\NeuroSan\Neurosan-v02\.env`:

```env
# Required: At least one LLM provider
OPENAI_API_KEY=sk-your_key_here

# Optional: Additional providers
ANTHROPIC_API_KEY=sk-ant-your_key_here
GOOGLE_API_KEY=your_google_key_here

# Optional: Service integrations
SLACK_BOT_TOKEN=xoxb-your-token
SERVICENOW_INSTANCE=your_instance.service-now.com
```

---

## 🧪 Try a Basic Example

### 1. Music Nerd Agent (Recommended First Test)

**Description:** Single music expert agent that answers questions about music.

**HOCON Config:** `registries/basic/music_nerd.hocon`

**How to test:**
1. Open http://localhost:4174
2. Select "Music Nerd" agent from the dropdown
3. Ask: "What are the best albums of the 1970s?"
4. Agent uses OpenAI/Claude to generate responses

### 2. Hello World Agent

**Description:** Simplest possible agent - just echoes back input.

**HOCON Config:** `registries/basic/hello_world.hocon`

**How to test:**
1. Select "Hello World" agent
2. Enter any text
3. See immediate response

### 3. Coffee Finder

**Description:** Searches for coffee shops (with coded tools).

**HOCON Config:** `registries/basic/coffee_finder.hocon`

**Features:**
- Location-based search
- Custom Python tools integration
- Multi-agent delegation

### 4. Music Nerd Pro (Advanced)

**HOCON Config:** `registries/basic/music_nerd_pro.hocon`

**Features:**
- Multiple specialized agents (Frontman + Sub-agents)
- Custom tools for music database lookup
- Demonstrates inter-agent communication

---

## 🛠️ Create Your Own Agent Network

### 1. Create HOCON Configuration

Create a new file: `registries/my_agent.hocon`

```hocon
agents {
  my_first_agent {
    description = "My first multi-agent network"
    instructions = """
      You are a helpful assistant that answers questions 
      about topics like sports, movies, or technology.
      Always be concise and accurate.
    """
    
    # Choose LLM provider
    model = "openai/gpt-4"           # or "anthropic/claude-3-opus"
    
    # Optional: Add tools
    tools = [
      "web_search",                   # Search the web
      "calculator"                     # Calculate things
    ]
  }
}
```

### 2. Register in Manifest

Edit: `registries/manifest.hocon`

Add your agent to the registry:

```hocon
include "my_agent.hocon"
```

### 3. Test Your Agent

1. Restart the server
2. Select your agent from the web UI
3. Test with queries

---

## 📚 Useful Files to Know

| File | Purpose |
|------|---------|
| [CODEBASE_OVERVIEW.md](CODEBASE_OVERVIEW.md) | Complete documentation (you are here!) |
| [README.md](README.md) | Project overview |
| [docs/examples.md](docs/examples.md) | 20+ example implementations |
| [docs/api_key.md](docs/api_key.md) | API setup instructions |
| [docs/user_guide.md](docs/user_guide.md) | User manual |
| [docs/dev_guide.md](docs/dev_guide.md) | Developer guide |
| [.env](.env) | Your environment configuration |

---

## 🔑 Key Directories

```
j:\Company\amasQIS\AI\NeuroSan\Neurosan-v02\

├── registries/                 # Agent network definitions (HOCON files)
│   ├── basic/                  # Beginner-friendly examples
│   ├── industry/               # Industry-specific agents
│   └── manifest.hocon          # Registry of all agents
│
├── coded_tools/                # Custom Python tools
│   ├── basic/                  # Basic utility tools
│   └── industry/               # Industry-specific tools
│
├── apps/                       # Complete applications
│   ├── conscious_assistant/    # Advanced AI assistant
│   ├── log_analyzer/           # Log analysis agent
│   └── slack/                  # Slack integration
│
├── docs/                       # Documentation
│   ├── examples.md             # All examples
│   ├── api_key.md              # API setup
│   └── examples/               # Detailed examples
│
├── plugins/                    # Observability plugins
│   ├── phoenix/                # Phoenix tracing
│   └── log_bridge/             # Log aggregation
│
└── run.py                      # Main entry point
```

---

## 🎓 Learning Path

### Day 1: Get Familiar
1. ✅ Read this quick start guide
2. ✅ Review CODEBASE_OVERVIEW.md
3. ✅ Run the server
4. ✅ Test "Music Nerd" agent

### Day 2: Explore Examples
1. Try different examples (Coffee Finder, Hello World, etc.)
2. Look at HOCON configurations
3. Understand agent instructions
4. Review tool integrations

### Day 3: Create Custom Agent
1. Design your agent's purpose
2. Write HOCON configuration
3. Create custom tools if needed
4. Test with real queries
5. Iterate and improve

### Day 4+: Advanced Features
1. Add external integrations (ServiceNow, Slack, etc.)
2. Enable Phoenix observability
3. Implement Sly Data protection
4. Deploy to cloud/containers

---

## 🐛 Troubleshooting

### Port Already in Use

If ports 8081, 4174, or 30014 are in use:

```powershell
# Use different ports
python run.py --nsflow-port 4175 --server-http-port 8082 --server-grpc-port 30015
```

### API Key Not Working

1. Check `.env` file exists
2. Verify API key format
3. Test with a simple curl request:

```powershell
curl -X POST http://localhost:8081/v1/agents/basic/music_nerd/query `
  -H "Content-Type: application/json" `
  -d '{"query": "test"}'
```

### Agent Not Responding

1. Check server logs for errors
2. Verify LLM API keys are set
3. Check HOCON syntax in configuration
4. Restart the server

### Virtual Environment Issues

```powershell
# Recreate venv
Remove-Item -Recurse venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 📞 Support Resources

### Documentation
- **Full Codebase Overview:** [CODEBASE_OVERVIEW.md](CODEBASE_OVERVIEW.md)
- **Examples:** [docs/examples.md](docs/examples.md)
- **User Guide:** [docs/user_guide.md](docs/user_guide.md)
- **API Keys:** [docs/api_key.md](docs/api_key.md)

### Online Resources
- **GitHub:** https://github.com/cognizant-ai-lab/neuro-san-studio
- **Main Library:** https://github.com/cognizant-ai-lab/neuro-san
- **DeepWiki:** Ask AI questions about the codebase

### Testing API Endpoints

```powershell
# Test if server is running
curl http://localhost:8081/health

# List all available agents
curl http://localhost:8081/agents

# Query an agent
curl -X POST http://localhost:8081/v1/agents/basic/hello_world/query `
  -H "Content-Type: application/json" `
  -d '{"query": "Hello, how are you?"}'
```

---

## ✨ What's Next?

1. **Explore:** Check out `registries/industry/` for real-world examples
2. **Customize:** Create your first custom agent
3. **Integrate:** Connect external services (Slack, ServiceNow, etc.)
4. **Monitor:** Enable Phoenix observability for production
5. **Deploy:** Containerize and deploy to cloud

---

## 📊 System Information

| Component | Version | Status |
|-----------|---------|--------|
| Python | 3.13 | ✅ |
| neuro-san | 0.6.21 | ✅ |
| nsflow | 0.6.4 | ✅ |
| langchain | 1.0.8 | ✅ |
| OpenAI Support | Latest | ✅ |
| Anthropic Support | Latest | ✅ |
| FastAPI | 0.126.0 | ✅ |
| Uvicorn | 0.40.0 | ✅ |
| gRPC | 1.76.0 | ✅ |

---

## 🎯 Quick Reference: Common Commands

```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Run server with default ports
python run.py

# Run with custom ports
python run.py --nsflow-port 4175 --server-http-port 8082

# Run server only (no web client)
python run.py --server-only

# Run with Flask web client instead of nsflow
python run.py --use-flask-web-client

# View help
python run.py --help

# Stop server (Ctrl+C in terminal)
```

---

**Ready to build intelligent multi-agent systems? Start with a simple example and build from there! 🚀**

*Generated: December 21, 2025 | Location: j:\Company\amasQIS\AI\NeuroSan\Neurosan-v02*
