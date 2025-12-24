# Ollama Quick Reference

## 🚀 Common Commands

### Start/Stop Services

```bash
# Start Ollama server (if not running as service)
ollama serve

# Check if Ollama is running
curl http://localhost:11434/api/tags

# List all installed models
ollama list

# Download a new model
ollama pull mistral:7b-instruct-v0.3-q4_K_M
ollama pull llama2:latest
ollama pull llama3.2:3b-instruct-q4_K_M
```

### Run Application

```bash
# Activate virtual environment
cd J:\Company\amasQIS\AI\NeuroSan\Neurosan-v02
.\venv\Scripts\Activate.ps1

# Run with default settings (uses Ollama)
py -m run

# View logs
Get-Content logs/thinking_dir/* -Wait
```

---

## 🎯 Model Quick Selection

### For First Time (Fastest Setup)
```dotenv
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral:7b-instruct-v0.3-q4_K_M
OLLAMA_BASE_URL=http://localhost:11434
```

### For Lightweight/Speed
```dotenv
OLLAMA_MODEL=llama3.2:3b-instruct-q4_K_M
```

### For Quality
```dotenv
OLLAMA_MODEL=llama2:latest
```

### For Cloud Power
```dotenv
OLLAMA_MODEL=qwen3-next:80b-cloud
OLLAMA_CLOUD_API_KEY=your_api_key
```

---

## 📊 Model Comparison

```
┌──────────────────────┬────────┬─────────┬─────────┐
│ Model                │ Size   │ Speed   │ Quality │
├──────────────────────┼────────┼─────────┼─────────┤
│ llama3.2:3b          │ 2.0 GB │ ⚡⚡⚡   │ ⭐⭐   │
│ mistral:7b*          │ 4.4 GB │ ⚡⚡    │ ⭐⭐⭐ │
│ llama2:latest        │ 3.8 GB │ ⚡⚡    │ ⭐⭐⭐ │
│ qwen3-next:80b*      │ Cloud  │ ⚡     │ ⭐⭐⭐⭐│
│ mistral-large:675b*  │ Cloud  │ ⚡     │ ⭐⭐⭐⭐│
│ deepseek-v3.1:671b*  │ Cloud  │ ⚡     │ ⭐⭐⭐⭐│
└──────────────────────┴────────┴─────────┴─────────┘
* = Our current model / Cloud model requires API key
```

---

## 🔄 Switching Models

### Quick Switch Steps

1. **Edit `.env`:**
   ```bash
   # Change this line:
   OLLAMA_MODEL=mistral:7b-instruct-v0.3-q4_K_M
   
   # To this (example):
   OLLAMA_MODEL=llama2:latest
   ```

2. **Restart application:**
   ```bash
   py -m run
   ```

3. **Done!** New model is active

---

## 🧪 Test Your Setup

### Minimal Test
```bash
# Check Ollama connection
curl http://localhost:11434/api/tags

# Should show:
# {
#   "models": [
#     {"name": "mistral:7b-instruct-v0.3-q4_K_M", ...},
#     ...
#   ]
# }
```

### Full Application Test
```bash
py -m run

# Check logs - should see:
# ✓ Environment variables loaded
# ✓ LLM provider configured as: ollama
# ✓ Model: mistral:7b-instruct-v0.3-q4_K_M
# ✓ Server starting...
```

---

## 📁 .env Configuration Quick Map

```
.env File Location:
J:\Company\amasQIS\AI\NeuroSan\Neurosan-v02\.env

Key Sections:
┌─────────────────────────────────────┐
│ LLM Provider Selection              │
│ LLM_PROVIDER=ollama                 │ ← Change here
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│ Ollama Configuration                │
│ OLLAMA_MODEL=mistral:7b...          │ ← Change model here
│ OLLAMA_BASE_URL=http://localhost... │ ← Change server here
│ OLLAMA_TEMPERATURE=0.7              │ ← Tune parameters here
└─────────────────────────────────────┘
```

---

## ⚠️ Common Issues & Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| "Connection refused" | Run `ollama serve` |
| "Model not found" | Run `ollama pull mistral:7b-instruct-v0.3-q4_K_M` |
| "Out of memory" | Use smaller model (3B instead of 7B) |
| "Slow responses" | Use faster model or cloud option |
| "App not using new model" | Restart with `py -m run` |

---

## 📈 Performance Tuning

### Fast Response (Trade quality for speed)
```dotenv
OLLAMA_MODEL=llama3.2:3b-instruct-q4_K_M
OLLAMA_TEMPERATURE=0.5
OLLAMA_MAX_TOKENS=512
OLLAMA_TIMEOUT=60
```

### Best Quality (Accept slower responses)
```dotenv
OLLAMA_MODEL=llama2:latest
OLLAMA_TEMPERATURE=0.7
OLLAMA_MAX_TOKENS=2048
OLLAMA_TIMEOUT=300
```

### Balanced (Recommended)
```dotenv
OLLAMA_MODEL=mistral:7b-instruct-v0.3-q4_K_M
OLLAMA_TEMPERATURE=0.7
OLLAMA_MAX_TOKENS=1024
OLLAMA_TIMEOUT=180
```

---

## 🔗 Useful Links

| Resource | URL |
|----------|-----|
| Ollama Official | https://ollama.ai |
| Ollama Models | https://ollama.ai/library |
| Ollama Docs | https://github.com/ollama/ollama |
| Neuro-SAN Docs | See `docs/` folder |
| LangChain Ollama | https://python.langchain.com/docs/integrations/llms/ollama |

---

## 📝 Configuration Examples

### Example 1: Fast & Free (Default)
```dotenv
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral:7b-instruct-v0.3-q4_K_M
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TEMPERATURE=0.7
```

### Example 2: Ultra Fast (Lightweight)
```dotenv
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2:3b-instruct-q4_K_M
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TEMPERATURE=0.5
OLLAMA_MAX_TOKENS=512
```

### Example 3: High Quality
```dotenv
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama2:latest
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TEMPERATURE=0.8
OLLAMA_MAX_TOKENS=2048
```

### Example 4: Cloud Powered (Powerful)
```dotenv
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen3-next:80b-cloud
OLLAMA_CLOUD_API_KEY=your_key_here
OLLAMA_TIMEOUT=300
```

---

## 🎯 Which Model Should I Use?

### Decision Tree

```
Start here → Need to download model?
             ├─ YES → Use local (Free, no key needed)
             │        └─ Need fast? → llama3.2:3b (2GB)
             │        └─ Need quality? → mistral:7b (4.4GB)
             │        └─ Need best local? → llama2:latest
             │
             └─ NO → Use cloud (API key needed, faster)
                     └─ General → qwen3-next:80b-cloud
                     └─ Coding → qwen3-coder:480b-cloud
                     └─ Latest → deepseek-v3.1:671b-cloud
```

---

## ✅ Verification Checklist

- [ ] Ollama installed and running (`ollama serve`)
- [ ] At least one model downloaded (`ollama list`)
- [ ] `.env` file configured with LLM settings
- [ ] Virtual environment activated
- [ ] Application started with `py -m run`
- [ ] No errors in logs
- [ ] Can see model responses

---

## 🆘 Getting Help

**Check these in order:**

1. **Verify Ollama:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Check installed models:**
   ```bash
   ollama list
   ```

3. **Check app logs:**
   ```bash
   Get-Content logs/thinking_dir/* -Tail 20
   ```

4. **Restart everything:**
   ```bash
   ollama serve  # In separate window
   py -m run      # In another window
   ```

---

## 📚 Additional Resources

- Full setup guide: `OLLAMA_SETUP_GUIDE.md`
- Migration details: `OLLAMA_MIGRATION_PLAN.md`
- Original README: `README.md`
- User guide: `docs/user_guide.md`

---

**Last Updated:** December 21, 2025
