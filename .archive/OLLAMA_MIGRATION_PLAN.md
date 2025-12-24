# Ollama Migration Plan - OpenAI to Ollama

## Overview
Migrate the Neuro-SAN platform from OpenAI-dependent models to support both local Ollama models and Ollama Cloud models.

## Current State
- **Default Model**: GPT-4 (requires OPENAI_API_KEY)
- **Default HOCON Config**: `hocon_constants.py` uses `"class": "openai"`
- **LLM Integrations**: langchain-openai dependency

## Target State
- **Local Ollama**: Use locally running Ollama models (mistral, llama, qwen, etc.)
- **Ollama Cloud**: Use Ollama Cloud models with API key
- **Backward Compatibility**: Keep OpenAI support for users who have API keys
- **Easy Switching**: Configure model choice via `.env` file

## Implementation Steps

### 1. Update Dependencies ✅
- Add `langchain-ollama` package
- Keep `langchain-openai` for backward compatibility
- Update requirements.txt

### 2. Create Ollama Configuration ✅
- Add OLLAMA_* variables to `.env`
- Create environment variable documentation

### 3. Update Default Configuration ✅
- Modify `hocon_constants.py` to use Ollama by default
- Make it configurable via environment variables

### 4. Environment Variables Setup ✅
- `OLLAMA_MODEL`: Which Ollama model to use (default: "mistral:7b-instruct-v0.3-q4_K_M")
- `OLLAMA_BASE_URL`: Local Ollama endpoint (default: "http://localhost:11434")
- `OLLAMA_CLOUD_API_KEY`: For Ollama Cloud models
- `LLM_PROVIDER`: Switch between "ollama" and "openai"

### 5. Testing
- Test with local Ollama models
- Test with Ollama Cloud models
- Run `py -m run` command

## Model Recommendations
**Local Models (No API Key Required)**:
- `mistral:7b-instruct-v0.3-q4_K_M` - Fast, good quality
- `llama2:latest` - Popular, well-tested
- `llama3.2:3b-instruct-q4_K_M` - Lightweight option

**Cloud Models (API Key Required)**:
- `qwen3-next:80b-cloud` - Large, powerful
- `mistral-large-3:675b-cloud` - Powerful reasoning
- `deepseek-v3.1:671b-cloud` - Cutting edge
