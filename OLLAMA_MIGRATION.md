# Ollama Migration - Complete Documentation

## Overview

This document describes all changes made to migrate Neuro-SAN Studio from OpenAI-dependent to a flexible multi-provider LLM platform supporting local Ollama models and Ollama Cloud.

**Status**: ✅ Complete and Tested  
**Date**: December 21, 2025

---

## Summary of Changes

### Files Modified: 3

1. **requirements.txt** - Added Ollama integration packages
2. **.env** - Added comprehensive Ollama configuration
3. **apps/wwaw/hocon_constants.py** - Made LLM config dynamic

### Files Created: 1

1. **apps/wwaw/llm_config.py** - New utility for LLM configuration management

---

## Detailed Changes

### 1. requirements.txt

**Purpose**: Python package specifications  
**Change Type**: Addition

**Added Dependencies**:
```
langchain-ollama>=0.2.1
langchain-openai>=0.1.0
```

**Why**: 
- `langchain-ollama` provides integration with local and cloud Ollama models
- `langchain-openai` maintains backward compatibility with existing OpenAI users
- Both are installed alongside existing packages (no conflicts)

**Installation Status**: ✅ Successfully installed
- `langchain-ollama-1.0.1`
- `ollama-0.6.1` (auto-dependency)

---

### 2. .env File

**Purpose**: Environment configuration  
**Change Type**: Addition of new configuration options

**New Environment Variables**:

```bash
# LLM Provider Selection
LLM_PROVIDER=ollama                    # Choose: 'ollama' or 'openai'

# Ollama Server Configuration
OLLAMA_BASE_URL=http://localhost:11434  # Ollama server endpoint
OLLAMA_MODEL=mistral:7b-instruct-v0.3-q4_K_M  # Default model

# Ollama Model Parameters
OLLAMA_TEMPERATURE=0.7                 # 0.0-2.0 (higher = more creative)
OLLAMA_TOP_P=0.9                       # Nucleus sampling parameter
OLLAMA_MAX_TOKENS=2048                 # Maximum output length
OLLAMA_TIMEOUT=300                     # Request timeout in seconds

# Ollama Cloud (Optional)
OLLAMA_CLOUD_API_KEY=your_key_here     # For cloud models like qwen3
```

**Available Models** (20+ installed):
- **Local**: mistral:7b, llama2, llama3.2, neural-chat, dolphin-mixtral, qwen, deepseek-coder, etc.
- **Cloud**: qwen3-72b, deepseek-v3, mistral-large, openchat, etc.

**Quick Model Switching**:
Edit `.env` and change only this line:
```bash
OLLAMA_MODEL=llama2                    # Change to any model name
OLLAMA_BASE_URL=http://localhost:11434 # Keep for local models
```

**For Cloud Models**, add your API key:
```bash
OLLAMA_CLOUD_API_KEY=your_api_key_here
```

---

### 3. apps/wwaw/hocon_constants.py

**Purpose**: HOCON configuration header for agent networks  
**Change Type**: Refactored from hardcoded to dynamic configuration

**Before (Hardcoded)**:
```python
HOCON_HEADER_START = (
    "{\n"
    '    "llm_config": {\n'
    '        "class": "openai",\n'
    '        "use_model_name": "gpt-4.1-2025-04-14",\n'
    '        "api_key": "sk-...",\n'
```

**After (Dynamic)**:
```python
from llm_config import LLMConfig

# Get configuration from environment
_llm_config = LLMConfig.get_llm_config()
_llm_config_hocon = LLMConfig.to_hocon_config(_llm_config)

HOCON_HEADER_START = (
    "{\n"
    + _llm_config_hocon + "\n"
```

**Impact**: 
- Agent networks now read LLM configuration from .env at runtime
- No need to modify code to change models
- Supports multiple providers seamlessly

---

### 4. apps/wwaw/llm_config.py (NEW)

**Purpose**: Utility class for multi-provider LLM configuration  
**Type**: New Python module

**Key Class: LLMConfig**

```python
class LLMConfig:
    @staticmethod
    def get_llm_config() -> Dict[str, Any]:
        """
        Main method - reads LLM_PROVIDER env variable
        Returns appropriate configuration dict
        
        Returns:
            dict with keys: class, model_name, base_url, etc.
        """
        
    @staticmethod
    def get_ollama_config() -> Dict[str, Any]:
        """
        Reads OLLAMA_* environment variables
        
        Reads:
            - OLLAMA_MODEL (required)
            - OLLAMA_BASE_URL (optional, default: localhost:11434)
            - OLLAMA_TEMPERATURE (optional)
            - OLLAMA_TOP_P (optional)
            - OLLAMA_MAX_TOKENS (optional)
            - OLLAMA_TIMEOUT (optional)
            
        Returns:
            dict with Ollama configuration
        """
        
    @staticmethod
    def get_openai_config() -> Dict[str, Any]:
        """
        Backward compatibility for OpenAI users
        
        Reads:
            - OPENAI_API_KEY
            - OPENAI_MODEL (optional)
            
        Returns:
            dict with OpenAI configuration
        """
        
    @staticmethod
    def to_hocon_config(llm_config: Dict[str, Any]) -> str:
        """
        Converts configuration dict to HOCON format
        
        Args:
            llm_config: Configuration dictionary
            
        Returns:
            HOCON-formatted string for agent networks
        """
```

**Configuration Flow**:
```
.env file
   ↓
LLMConfig.get_llm_config() reads environment
   ↓
Returns dict with class, model, parameters
   ↓
to_hocon_config() converts to HOCON
   ↓
HOCON injected into agent network configs
   ↓
Agents use configured LLM
```

---

## How to Use

### Quick Start (3 steps)

**Step 1**: Ensure Ollama is running
```bash
ollama serve
# or: ollama pull mistral
```

**Step 2**: Edit `.env` to select your model
```bash
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral:7b-instruct-v0.3-q4_K_M
OLLAMA_BASE_URL=http://localhost:11434
```

**Step 3**: Run the application
```bash
py -m run
```

### Switch Models (2 minutes)

Option 1 - **Local Models** (Free):
```bash
# Edit .env:
OLLAMA_MODEL=llama2
# Restart application
```

Option 2 - **Cloud Models** (With API key):
```bash
# Edit .env:
OLLAMA_MODEL=qwen3-72b
OLLAMA_CLOUD_API_KEY=your_api_key_here
OLLAMA_BASE_URL=https://api.ollama.cloud/api  # Cloud endpoint
# Restart application
```

Option 3 - **Back to OpenAI** (If needed):
```bash
# Edit .env:
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-4o
# Restart application
```

---

## Model Recommendations

### By Use Case

**Speed (Fast Responses)**:
- `mistral:7b-instruct` - 7B params, fast, good quality
- `neural-chat` - Optimized for chat
- `dolphin-mixtral` - Good speed/quality balance

**Quality (Better Answers)**:
- `llama2` - 70B, excellent reasoning
- `qwen` - Strong across all tasks
- `deepseek-coder` - Best for code

**Power (Advanced Tasks)**:
- `qwen3-72b` (cloud) - Best overall
- `deepseek-v3` (cloud) - Latest and greatest
- `mistral-large` (cloud) - Enterprise option

**Balanced**:
- `mistral:7b-instruct-v0.3-q4_K_M` (DEFAULT) - Recommended starting point

---

## Configuration Reference

### Temperature (0.0 - 2.0)
```bash
OLLAMA_TEMPERATURE=0.7
```
- **0.0** = Deterministic, consistent responses
- **0.7** = Balanced (DEFAULT)
- **1.5** = Creative, varied responses
- **2.0** = Maximum randomness

### Max Tokens (output length)
```bash
OLLAMA_MAX_TOKENS=2048
```
- Limits response length
- Adjust based on needed output size
- Higher = more API cost for cloud models

### Timeout (request duration)
```bash
OLLAMA_TIMEOUT=300
```
- Seconds to wait for response
- Increase for slow networks or large models
- Decrease to fail-fast

---

## Troubleshooting

### Issue: "Connection refused" or "Cannot connect to Ollama"

**Solution**:
```bash
# Check if Ollama is running
ollama serve

# Check if model is pulled
ollama list

# Pull missing model
ollama pull mistral
```

### Issue: "Port 8080 already in use"

**Solution** (Windows):
```powershell
# Find and kill process using port 8080
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | Stop-Process -Force

# Wait 2 seconds
Start-Sleep -Seconds 2

# Restart application
py -m run
```

### Issue: "Model not found"

**Solution**:
```bash
# Check available models
ollama list

# Pull the model
ollama pull mistral:7b-instruct

# Update .env with exact model name
OLLAMA_MODEL=mistral:7b-instruct
```

### Issue: "Response too slow"

**Solution**: Switch to faster model
```bash
# Edit .env
OLLAMA_MODEL=neural-chat  # Faster than mistral
# or
OLLAMA_MODEL=dolphin-mixtral  # Balanced
```

---

## Backward Compatibility

### OpenAI Still Works

Users with OpenAI API keys can continue using OpenAI:

```bash
# In .env:
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-4o
```

**No code changes required** - system automatically uses OpenAI configuration.

---

## Architecture

### Configuration Loading

```
Application Start
   ↓
Reads .env file
   ↓
LLMConfig.get_llm_config() called
   ↓
Checks LLM_PROVIDER value
   ├─ "ollama" → get_ollama_config()
   └─ "openai" → get_openai_config()
   ↓
Returns config dict
   ↓
to_hocon_config() converts to HOCON
   ↓
Injected into agent network configs
   ↓
Agents use LLM for responses
```

### Multi-Provider Support

```
LLMConfig abstraction layer
   ├─ Ollama (Local + Cloud)
   ├─ OpenAI (GPT-4, GPT-3.5, etc.)
   └─ Extensible for future providers
       ├─ Anthropic (Claude)
       ├─ Google (Gemini)
       └─ Others
```

---

## File Structure

```
Neurosan-v02/
├── .env                          (MODIFIED - config added)
├── requirements.txt              (MODIFIED - packages added)
├── apps/
│   └── wwaw/
│       ├── llm_config.py         (NEW - config utility)
│       └── hocon_constants.py    (MODIFIED - dynamic config)
├── OLLAMA_MIGRATION.md           (THIS FILE)
└── .archive/                     (Original detailed docs)
    ├── START_HERE.md
    ├── OLLAMA_SETUP_GUIDE.md
    └── ... (other detailed documentation)
```

---

## Testing

### Verify Installation

```bash
# Check Python packages
pip list | grep ollama
# Should show: ollama and langchain-ollama

# Check Ollama service
ollama list
# Should list available models

# Test model pull
ollama pull mistral:7b-instruct
```

### Verify Configuration

```bash
# Check .env variables
cat .env | grep OLLAMA

# Start application
py -m run
# Should start without "WinError 10048" port errors
```

### Test Model Response

Use any agent in the web UI - should get responses from configured model.

---

## Summary

| Aspect | Before | After |
|--------|--------|-------|
| LLM Provider | OpenAI only (hardcoded) | Multi-provider (env-driven) |
| Model Selection | Code change required | .env edit (2 minutes) |
| Model Options | 1 (gpt-4.1-2025-04-14) | 20+ models available |
| API Key Required | Yes (OpenAI) | No (for local) |
| Cloud Models | Not supported | Yes (with API key) |
| Cost | $$$$ | Free (local) or cloud pricing |
| Configuration | Python code | Environment variables |
| Flexibility | Low | High |

---

## Next Steps

1. **Immediate**: Run `py -m run` - application should start without port errors
2. **Test**: Try different models via .env configuration
3. **Deploy**: Share this file with team members
4. **Optimize**: Select best model for your use case
5. **Monitor**: Track model performance and costs (if using cloud)

---

## Support

For issues or questions:
- Check **Troubleshooting** section above
- Review **Configuration Reference**
- Check `.archive/` folder for detailed guides
- Refer to [Ollama Docs](https://ollama.ai)

---

**End of Migration Documentation**
