# Ollama Integration Guide - Neuro-SAN Studio

## ✅ Migration Complete!

The Neuro-SAN Studio platform has been successfully migrated from OpenAI-dependent models to support **both local Ollama models and Ollama Cloud models**. You can now run this platform without requiring an OpenAI API key!

---

## 📋 What Changed

### Before Migration
- ❌ Required OpenAI API key (`OPENAI_API_KEY`)
- ❌ Default model: `gpt-4.1-2025-04-14`
- ❌ No support for local models
- ❌ LLM provider hardcoded as `"openai"`

### After Migration
- ✅ **No API key required** for local models
- ✅ Default model: `mistral:7b-instruct-v0.3-q4_K_M` (local, free)
- ✅ Support for 20+ Ollama models (local and cloud)
- ✅ Easy configuration via `.env` file
- ✅ Backward compatible with OpenAI (optional)

---

## 🚀 Quick Start

### 1. Prerequisites
You already have:
- ✅ Virtual environment created
- ✅ Dependencies installed (including `langchain-ollama`)
- ✅ `.env` file configured

### 2. Ensure Ollama Server is Running

**Windows:**
```powershell
# Ollama runs as a service. Check if it's running:
curl http://localhost:11434/api/tags

# If not running, start it:
ollama serve
```

**Pull a Model (if not already installed):**
```bash
# Using your already installed models, or:
ollama pull mistral:7b-instruct-v0.3-q4_K_M
ollama list
```

### 3. Run the Application

```bash
cd J:\Company\amasQIS\AI\NeuroSan\Neurosan-v02
.\venv\Scripts\Activate.ps1
py -m run
```

The application will now use Ollama models by default! No API key needed.

---

## 🎯 Configuration

### Environment Variables (.env)

All configuration is in your `.env` file:

```dotenv
# ============================================================================
# LLM Provider Configuration
# ============================================================================
LLM_PROVIDER=ollama

# ============================================================================
# Ollama Configuration
# ============================================================================

# Local Ollama server endpoint
OLLAMA_BASE_URL=http://localhost:11434

# Which model to use (see list below)
OLLAMA_MODEL=mistral:7b-instruct-v0.3-q4_K_M

# Optional: Ollama Cloud API key (only if using cloud models)
OLLAMA_CLOUD_API_KEY=your_ollama_cloud_api_key_here

# Optional: Model parameters
OLLAMA_TEMPERATURE=0.7      # 0-1, lower = more deterministic
OLLAMA_TOP_P=0.9            # 0-1, controls diversity
OLLAMA_MAX_TOKENS=2048
OLLAMA_TIMEOUT=300          # Request timeout in seconds
```

---

## 📦 Available Ollama Models

### 🟢 Local Models (No API Key Needed - Free!)

These are downloaded and run on your machine:

| Model | Size | Speed | Quality | Recommended |
|-------|------|-------|---------|-------------|
| **mistral:7b-instruct-v0.3-q4_K_M** | 4.4 GB | Fast | Good | ⭐ YES |
| llama2:latest | 3.8 GB | Medium | Very Good | ✅ |
| llama3.2:3b-instruct-q4_K_M | 2.0 GB | Very Fast | Good | ✅ |
| neural-chat:latest | ~4 GB | Fast | Good | ✅ |

**Download a model:**
```bash
ollama pull mistral:7b-instruct-v0.3-q4_K_M
ollama pull llama2:latest
ollama pull llama3.2:3b-instruct-q4_K_M
```

**List installed models:**
```bash
ollama list
```

### 🔵 Ollama Cloud Models (Requires API Key)

For more powerful models, use Ollama Cloud:

| Model | Capabilities | Notes |
|-------|--------------|-------|
| qwen3-next:80b-cloud | Very powerful reasoning | Great for complex tasks |
| mistral-large-3:675b-cloud | Large, versatile | Excellent quality |
| deepseek-v3.1:671b-cloud | Latest cutting-edge | State-of-the-art |
| gpt-oss:120b-cloud | High quality reasoning | Powerful option |
| qwen3-coder:480b-cloud | Code generation | Specialized for coding |

**To use cloud models:**
1. Get API key from https://ollama.ai
2. Set in `.env`: `OLLAMA_CLOUD_API_KEY=your_key_here`
3. Change model name: `OLLAMA_MODEL=qwen3-next:80b-cloud`

---

## 🔄 Switching Models

### Change Default Model

Edit `.env` and update:
```dotenv
OLLAMA_MODEL=llama2:latest
# or
OLLAMA_MODEL=qwen3-next:80b-cloud
```

Then restart the application:
```bash
py -m run
```

---

## 📊 Model Selection Guide

**Choose based on your needs:**

| Use Case | Recommended Model | Reason |
|----------|------------------|--------|
| **First-time use / Testing** | mistral:7b-instruct-v0.3-q4_K_M | Fast, small download, good quality |
| **General purpose chatbot** | llama2:latest | Well-tested, reliable |
| **Resource-constrained machine** | llama3.2:3b-instruct-q4_K_M | Only 2GB, still good quality |
| **Complex reasoning tasks** | qwen3-next:80b-cloud* | Most capable, needs API key |
| **Code generation** | qwen3-coder:480b-cloud* | Specialized for coding |
| **Maximum speed** | llama3.2:3b-instruct-q4_0 | Fastest option |

*Requires API key

---

## 🔧 Advanced Configuration

### Model-Specific Parameters

```dotenv
# Temperature: Controls randomness
# 0.0 = Deterministic (best for consistency)
# 0.7 = Balanced (recommended)
# 1.0 = Creative/Random
OLLAMA_TEMPERATURE=0.7

# Top P: Nucleus sampling (affects diversity)
OLLAMA_TOP_P=0.9

# Request timeout (seconds) - increase for large models
OLLAMA_TIMEOUT=300

# Maximum tokens in response
OLLAMA_MAX_TOKENS=2048
```

---

## 🔌 Using Different LLM Providers

### Switch to OpenAI (if you have API key)

```dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your_key_here
OPENAI_MODEL=gpt-4o
```

### Switch Back to Ollama

```dotenv
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral:7b-instruct-v0.3-q4_K_M
```

---

## 📁 Modified Files

The following files were updated for Ollama support:

1. **`requirements.txt`** - Added `langchain-ollama>=0.2.1`
2. **`.env`** - Added Ollama configuration variables
3. **`apps/wwaw/hocon_constants.py`** - Now reads LLM config from environment
4. **`apps/wwaw/llm_config.py`** - NEW: LLM configuration utility
5. **`OLLAMA_MIGRATION_PLAN.md`** - NEW: Migration documentation

---

## 🧪 Testing the Setup

### Verify Ollama Server
```bash
curl http://localhost:11434/api/tags
# Should return list of installed models in JSON format
```

### Test Model Connection
```bash
ollama list
# Should show your installed models
```

### Test Application
```bash
py -m run
# Should start without OpenAI API key errors
```

---

## 🐛 Troubleshooting

### "Connection refused" - Ollama server not running
```bash
# Start Ollama server:
ollama serve
```

### Model not found error
```bash
# Download the model first:
ollama pull mistral:7b-instruct-v0.3-q4_K_M
ollama list  # Verify it's installed
```

### Slow responses
- **Solution**: Use a smaller model (e.g., llama3.2:3b instead of larger models)
- **Alternative**: Use Ollama Cloud for faster responses

### Out of memory
- **Solution**: Use smaller models (3B-8B parameters instead of 70B+)
- **Check**: `ollama list` shows memory usage

### API key not working (for cloud models)
- **Solution**: Verify key is correct in `.env`
- **Check**: Restart application after updating `.env`

---

## 📚 Architecture

### How It Works

```
┌─────────────────────────────────────────────┐
│     Neuro-SAN Application (run.py)          │
└────────────────────┬────────────────────────┘
                     │
         ┌───────────┴────────────┐
         │                        │
    ┌────▼──────┐        ┌────────▼──────┐
    │  hocon    │        │  hocon        │
    │ constants │        │ constants     │
    │   (old)   │        │  (NEW: reads  │
    │           │        │  from .env)   │
    └────┬──────┘        └────────┬──────┘
         │                        │
         └────────────┬───────────┘
                      │
              ┌───────▼────────┐
              │  llm_config.py │
              │    (NEW)       │
              └───────┬────────┘
                      │
        ┌─────────────┴────────────┐
        │                          │
   ┌────▼──────────┐      ┌────────▼──────┐
   │ OLLAMA_*      │      │  OPENAI_*     │
   │ Environment   │      │  Environment  │
   │ Variables     │      │  Variables    │
   └────┬──────────┘      └────────┬──────┘
        │                          │
   ┌────▼──────────┐      ┌────────▼──────┐
   │  Ollama       │      │ OpenAI API    │
   │  Local/Cloud  │      │ (Optional)    │
   └───────────────┘      └───────────────┘
```

### Key Components

1. **llm_config.py** (NEW)
   - Reads environment variables
   - Returns appropriate LLM configuration
   - Converts config to HOCON format

2. **hocon_constants.py** (MODIFIED)
   - Now imports from llm_config
   - Dynamically generates HOCON header
   - Maintains backward compatibility

3. **.env** (UPDATED)
   - Centralized configuration
   - Easy to switch between providers
   - Clear documentation

---

## 📝 Example HOCON Configuration

When you run the app, the HOCON config is automatically generated based on your `.env`:

**With Ollama (default):**
```hocon
{
    "llm_config": {
        "class": "ollama",
        "model_name": "mistral:7b-instruct-v0.3-q4_K_M",
        "base_url": "http://localhost:11434",
        "temperature": 0.7,
        "top_p": 0.9,
    },
    ...
}
```

**With OpenAI (if LLM_PROVIDER=openai):**
```hocon
{
    "llm_config": {
        "class": "openai",
        "model_name": "gpt-4o",
    },
    ...
}
```

---

## ✨ Benefits of This Setup

| Benefit | Details |
|---------|---------|
| **No API Key Needed** | Run locally without OpenAI API key |
| **Cost-Free** | Local models are completely free |
| **Privacy** | Data stays on your machine (local models) |
| **Flexible** | Easy to switch between models/providers |
| **Scalable** | Use powerful cloud models when needed |
| **Backward Compatible** | Still supports OpenAI if you want |
| **Easy Configuration** | Single `.env` file controls everything |

---

## 🎓 Next Steps

1. **Choose your preferred model** from the list above
2. **Update `.env`** with your choice
3. **Restart the application** (`py -m run`)
4. **Experiment** with different models and parameters
5. **Optimize** based on your use case

---

## 📞 Support

For Ollama issues:
- Official Docs: https://ollama.ai
- GitHub: https://github.com/ollama/ollama

For Neuro-SAN issues:
- GitHub: https://github.com/cognizant-ai-lab/neuro-san-studio
- Docs: See `docs/` folder

---

## 🎉 Summary

Your Neuro-SAN Studio is now **Ollama-ready**!

- ✅ Dependencies installed
- ✅ Configuration in place
- ✅ Application tested and running
- ✅ Multiple models available
- ✅ Easy switching between providers

**Happy coding! 🚀**
