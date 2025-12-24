# Ollama Migration - Complete Technical Documentation

## NeuroSan v0.6.21 - OpenAI to Ollama Migration

**Migration Date**: December 21-22, 2025  
**Status**: ✅ Complete and Tested

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Solution Architecture](#solution-architecture)
4. [Files Created](#files-created)
5. [Files Modified](#files-modified)
6. [Configuration Details](#configuration-details)
7. [Environment Variables](#environment-variables)
8. [Technical Deep Dive](#technical-deep-dive)
9. [Usage Guide](#usage-guide)
10. [Troubleshooting](#troubleshooting)

---

## Executive Summary

This migration converted NeuroSan from hardcoded OpenAI GPT models to a centralized Ollama-based LLM configuration system. 

### Key Achievements

| Metric | Before | After |
|--------|--------|-------|
| LLM Provider | OpenAI only | Ollama (local + cloud) |
| Config Files to Edit | 55+ files | 1 file |
| API Cost | Pay-per-request | Free (local) |
| Offline Capable | ❌ No | ✅ Yes |
| Model Switching Time | Hours | Seconds |

---

## Problem Statement

### Original Issue

The NeuroSan codebase had **55+ HOCON configuration files** with hardcoded OpenAI model references:

```hocon
# BEFORE: Hardcoded in EVERY agent network file
"llm_config": {
    "model_name": "gpt-4o"
}
```

### Problems Encountered

1. **OpenAI API Key Required** - Every agent network required a valid OpenAI API key
2. **API Costs** - Each request incurred OpenAI usage costs
3. **No Centralized Control** - Changing models required editing 55+ files manually
4. **Authentication Errors** - Missing or invalid API keys caused errors:

```
openai.AuthenticationError: Error code: 401 - Incorrect API key provided: sk-your_***************here
```

### Root Cause Analysis

The error occurred because:

1. HOCON files specified `"model_name": "gpt-4o"` **without** a `"class"` property
2. NeuroSan's LLM factory defaulted to OpenAI when no class was specified
3. The `.env` file had placeholder OpenAI API keys
4. No centralized way to switch all agents to a different provider

### Critical Fix Required

The configuration needed TWO things:

```hocon
# WRONG - Missing class property
"llm_config": {
    "model_name": "mistral:7b"  # ← Still tries OpenAI!
}

# CORRECT - Class property tells NeuroSan which provider to use
"llm_config": {
    "class": "ollama",           # ← REQUIRED for Ollama
    "model_name": "mistral:7b"
}
```

---

## Solution Architecture

### Centralized Configuration Pattern

We created a **single source of truth** for LLM configuration:

```
┌─────────────────────────────────────────────────────────────────┐
│                    registries/llm_config.hocon                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  shared_llm_config         = { class: ollama, ... }     │   │
│  │  shared_llm_config_advanced = { class: ollama, ... }    │   │
│  │  shared_llm_config_local   = { class: ollama, ... }     │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼ include + substitution
┌──────────────────────────┴──────────────────────────────────────┐
│                    All 55+ Agent Networks                       │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ music_nerd   │ │ agent_network│ │ coffee_finder│   ...      │
│  │   .hocon     │ │ _designer    │ │   .hocon     │            │
│  │              │ │   .hocon     │ │              │            │
│  │ llm_config:  │ │ llm_config:  │ │ llm_config:  │            │
│  │ ${shared_    │ │ ${shared_    │ │ ${shared_    │            │
│  │ llm_config}  │ │ llm_config_  │ │ llm_config}  │            │
│  │              │ │ advanced}    │ │              │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

### Three Configuration Tiers

| Tier | Variable | Default Model | Use Case |
|------|----------|---------------|----------|
| **Standard** | `${shared_llm_config}` | `mistral:7b-instruct-v0.3-q4_K_M` | Most agents (4.4GB local) |
| **Advanced** | `${shared_llm_config_advanced}` | `deepseek-v3.1:671b-cloud` | Complex agents (671B cloud) |
| **Local** | `${shared_llm_config_local}` | `mistral:7b-instruct-v0.3-q4_K_M` | Offline fallback |

---

## Files Created

### 1. `registries/llm_config.hocon` (NEW)

**Purpose**: Centralized LLM configuration for all agent networks

**Full Content**:

```hocon
# Copyright © 2025 Cognizant Technology Solutions Corp, www.cognizant.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# ...
#
# END COPYRIGHT

# ============================================================================
# Shared LLM Configuration for Neuro-SAN Agent Networks
# ============================================================================
#
# This file provides centralized LLM configuration that can be included by
# all agent network HOCON files. Change the model here to switch all agents.
#
# USAGE: In your agent network HOCON file, add:
#   include "registries/llm_config.hocon"
#   ...
#   "llm_config": ${shared_llm_config},
#
# For complex agents requiring more capable models:
#   "llm_config": ${shared_llm_config_advanced},
#
# ============================================================================

{
    # -------------------------------------------------------------------------
    # Standard LLM Config - For most agent networks
    # -------------------------------------------------------------------------
    # Uses Ollama local model for fast, free inference
    # Default: mistral:7b-instruct-v0.3-q4_K_M (4.4GB, fast)
    #
    # Override via environment variable: MODEL_NAME
    # Example: set MODEL_NAME=llama3.2:3b-instruct-q4_K_M
    #
    "shared_llm_config": {
        "class": "ollama",
        "model_name": "mistral:7b-instruct-v0.3-q4_K_M",
        "model_name": ${?MODEL_NAME}
    },

    # -------------------------------------------------------------------------
    # Advanced LLM Config - For complex agent networks
    # -------------------------------------------------------------------------
    # Uses Ollama cloud models for tasks requiring higher capability
    # Default: deepseek-v3.1:671b-cloud (latest, most capable)
    #
    # Available Ollama Cloud Models (require OLLAMA_CLOUD_API_KEY):
    #   - deepseek-v3.1:671b-cloud (latest, most capable)
    #   - mistral-large-3:675b-cloud (multilingual, reasoning)
    #   - qwen3-coder:480b-cloud (strong for coding)
    #   - kimi-k2:1t-cloud (massive model)
    #
    # Override via environment variable: MODEL_NAME_ADVANCED
    #
    "shared_llm_config_advanced": {
        "class": "ollama",
        "model_name": "deepseek-v3.1:671b-cloud",
        "model_name": ${?MODEL_NAME_ADVANCED}
    },

    # -------------------------------------------------------------------------
    # Local-Only LLM Config - For offline use
    # -------------------------------------------------------------------------
    # Guaranteed to work without internet/API keys
    # Uses smaller, faster local models
    #
    "shared_llm_config_local": {
        "class": "ollama",
        "model_name": "mistral:7b-instruct-v0.3-q4_K_M",
        "model_name": ${?MODEL_NAME_LOCAL}
    }
}
```

**Key Technical Points**:

1. **`"class": "ollama"`** - This is CRITICAL. It tells NeuroSan's LLM factory to use the Ollama provider instead of defaulting to OpenAI.

2. **`${?MODEL_NAME}`** - The `?` makes the environment variable optional. If set, it overrides the default. HOCON uses "last value wins" semantics.

3. **Three tiers** - Allows different capability levels for different agent types without changing individual files.

---

## Files Modified

### Overview

| Category | Count | Config Applied |
|----------|-------|----------------|
| Root configs | 12 | Mixed (standard/advanced) |
| basic/* | 9 | `${shared_llm_config}` |
| industry/* | 18 | `${shared_llm_config}` |
| tools/* | 20+ | `${shared_llm_config}` |
| tests/* | 1 | `${shared_llm_config}` |
| .env | 1 | Environment variables |
| **TOTAL** | **61+** | - |

### Modification Pattern Applied

**BEFORE** (hardcoded in each file):

```hocon
{
    "llm_config": {
        "model_name": "gpt-4o"
    },
    
    "tools": [
        {
            "name": "AgentName",
            ...
        }
    ]
}
```

**AFTER** (includes shared config):

```hocon
{
    include "registries/llm_config.hocon"
    
    "llm_config": ${shared_llm_config},
    
    "tools": [
        {
            "name": "AgentName",
            ...
        }
    ]
}
```

### Complete File List

#### Root Configuration Files (12 files)

| File | Config Used | Reason |
|------|-------------|--------|
| `agent_network_designer.hocon` | `${shared_llm_config_advanced}` | Complex multi-agent design |
| `agent_network_editor.hocon` | `${shared_llm_config}` | Standard editing tasks |
| `agent_network_instructions_editor.hocon` | `${shared_llm_config}` | Instruction editing |
| `agent_network_query_generator.hocon` | `${shared_llm_config}` | Query generation |
| `agent_network_architect.hocon` | `${shared_llm_config_advanced}` | Complex architecture |
| `conscious_agent.hocon` | `${shared_llm_config_advanced}` | Advanced reasoning |
| `cruse_agent.hocon` | `${shared_llm_config}` | Standard agent |
| `cpg_agents.hocon` | `${shared_llm_config}` | CPG operations |
| `six_thinking_hats.hocon` | `${shared_llm_config}` | Thinking framework |
| `kwik_agents.hocon` | `${shared_llm_config_advanced}` | Memory capabilities |
| `keybank.hocon` | `${shared_llm_config}` | Banking operations |
| `log_analysis_agents.hocon` | `${shared_llm_config}` | Log analysis |

#### Basic Agent Networks (9 files)

| File | Original Model | New Config |
|------|---------------|------------|
| `basic/hello_world.hocon` | `gpt-4o` | `${shared_llm_config}` |
| `basic/music_nerd.hocon` | `gpt-4o` | `${shared_llm_config}` |
| `basic/music_nerd_pro.hocon` | `gpt-4o` | `${shared_llm_config}` |
| `basic/music_nerd_pro_sly.hocon` | `gpt-4o` | `${shared_llm_config}` |
| `basic/music_nerd_llm_fallbacks.hocon` | `gpt-4o` + Claude fallback | `${shared_llm_config}` + `${shared_llm_config_local}` |
| `basic/smart_home.hocon` | `gpt-4o` | `${shared_llm_config}` |
| `basic/advanced_calculator.hocon` | `gpt-4o` | `${shared_llm_config}` |
| `basic/coffee_finder.hocon` | `gpt-4.1-mini` | `${shared_llm_config}` |
| `basic/coffee_finder_advanced.hocon` | `gpt-4.1` | `${shared_llm_config_advanced}` |

#### Industry Agent Networks (18 files)

All use `${shared_llm_config}`:

- `industry/airline_policy.hocon`
- `industry/airbnb.hocon`
- `industry/banking_ops.hocon`
- `industry/booking.hocon`
- `industry/carmax.hocon`
- `industry/consumer_decision_assistant.hocon`
- `industry/expedia.hocon`
- `industry/insurance_agents.hocon`
- `industry/insurance_underwriting_agents.hocon`
- `industry/intranet_agents.hocon`
- `industry/intranet_agents_with_tools.hocon`
- `industry/LinkedInJobSeekerSupportNetwork.hocon`
- `industry/macys.hocon`
- `industry/news_sentiment_analysis.hocon`
- `industry/real_estate.hocon`
- `industry/retail_ops_and_customer_service.hocon`
- `industry/telco_network_orchestration.hocon`
- `industry/telco_network_support.hocon`
- `industry/therapy_vignette_supervisors.hocon`

#### Tools Agent Networks (20+ files)

All use `${shared_llm_config}`:

- `tools/a2a_research_report.hocon`
- `tools/agent_network_html_creator.hocon`
- `tools/agentforce.hocon`
- `tools/agentspace_adapter.hocon`
- `tools/agentic_rag.hocon`
- `tools/anthropic_code_execution.hocon`
- `tools/anthropic_web_search.hocon`
- `tools/arxiv_rag.hocon`
- `tools/brave_search.hocon`
- `tools/confluence_rag.hocon`
- `tools/ddgs_search.hocon`
- `tools/gemini_image_generation.hocon`
- `tools/gmail.hocon`
- `tools/google_search.hocon`
- `tools/mcp_bmi_streamable_http.hocon`
- `tools/now_agents.hocon`
- `tools/openai_code_interpreter.hocon`
- `tools/openai_image_generation.hocon`
- `tools/openai_video_generation.hocon`
- `tools/openai_web_search.hocon`
- `tools/pdf_rag.hocon`
- `tools/visual_question_answering.hocon`
- `tools/wikipedia_rag.hocon`

#### Test Files (1 file)

- `tests/registries/basic/music_nerd_pro.hocon` → `${shared_llm_config}`

---

## Configuration Details

### .env File Additions

The following were added to `.env`:

```bash
# ============================================================================
# LLM Model Configuration (Ollama)
# ============================================================================
# These environment variables override the models in llm_config.hocon
# Change these to switch all agent networks to different models

# MODEL_NAME - Standard model for most agents (local Ollama)
# Options: mistral:7b-instruct-v0.3-q4_K_M, llama3.2:3b-instruct-q4_K_M, mistral
MODEL_NAME=mistral:7b-instruct-v0.3-q4_K_M

# MODEL_NAME_ADVANCED - For complex agents requiring more capability (Ollama Cloud)
# Options: deepseek-v3.1:671b-cloud, mistral-large-3:675b-cloud, kimi-k2:1t-cloud
MODEL_NAME_ADVANCED=deepseek-v3.1:671b-cloud

# MODEL_NAME_LOCAL - Fallback for offline use (guaranteed local)
MODEL_NAME_LOCAL=mistral:7b-instruct-v0.3-q4_K_M

# ============================================================================
# Ollama Configuration
# ============================================================================

# Ollama Local Server Configuration
OLLAMA_HOST=http://localhost:11434

# Ollama Cloud Configuration (for *-cloud models)
OLLAMA_CLOUD_API_KEY=your_ollama_cloud_api_key_here
```

### Server Port Configuration

```bash
# Avoid port 8080 conflict
NEURO_SAN_SERVER_HTTP_PORT=9080
NEURO_SAN_SERVER_GRPC_PORT=30013
```

---

## Environment Variables

### Model Selection Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_NAME` | `mistral:7b-instruct-v0.3-q4_K_M` | Standard model for most agents |
| `MODEL_NAME_ADVANCED` | `deepseek-v3.1:671b-cloud` | Cloud model for complex agents |
| `MODEL_NAME_LOCAL` | `mistral:7b-instruct-v0.3-q4_K_M` | Offline fallback model |

### Ollama Configuration Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | `http://localhost:11434` | Local Ollama server URL |
| `OLLAMA_CLOUD_API_KEY` | (required for cloud) | API key for Ollama Cloud |

### Available Local Models

Check with `ollama list`:

| Model | Size | Speed |
|-------|------|-------|
| `mistral:7b-instruct-v0.3-q4_K_M` | 4.4 GB | Fast |
| `llama3.2:3b-instruct-q4_K_M` | 2.0 GB | Very fast |
| `llama2:latest` | 3.8 GB | Fast |

### Available Cloud Models

| Model | Parameters | Best For |
|-------|------------|----------|
| `deepseek-v3.1:671b-cloud` | 671B | General, highly capable |
| `mistral-large-3:675b-cloud` | 675B | Multilingual, reasoning |
| `kimi-k2:1t-cloud` | 1T | Maximum capability |
| `qwen3-coder:480b-cloud` | 480B | Code generation |
| `devstral-2:123b-cloud` | 123B | Development tasks |

---

## Technical Deep Dive

### How HOCON Include Works

HOCON supports transitive file includes:

```hocon
# In agent_network_designer.hocon
include "registries/llm_config.hocon"
```

This loads `llm_config.hocon` at parse time, making all its definitions available.

### How HOCON Substitution Works

After including, we reference the shared config:

```hocon
"llm_config": ${shared_llm_config}
```

At parse time, `${shared_llm_config}` is replaced with the actual object:

```hocon
"llm_config": {
    "class": "ollama",
    "model_name": "mistral:7b-instruct-v0.3-q4_K_M"
}
```

### How Environment Override Works

HOCON's `${?VAR}` syntax (with `?`) is optional:

```hocon
"shared_llm_config": {
    "class": "ollama",
    "model_name": "default_value",
    "model_name": ${?MODEL_NAME}  # Overrides if MODEL_NAME is set
}
```

HOCON uses **last-value-wins** semantics. If `MODEL_NAME` env var is set, it overrides. If not, the default is used.

### How NeuroSan LLM Factory Works

The LLM factory (`venv/Lib/site-packages/neuro_san/internals/run_context/langchain/llms/default_llm_factory.py`) processes configs:

1. **Read config** - Gets `llm_config` from HOCON
2. **Check class** - Looks for `"class"` property
3. **Select provider**:
   - `"openai"` → `ChatOpenAI`
   - `"anthropic"` → `ChatAnthropic`
   - `"ollama"` → `ChatOllama`
   - (none) → **Defaults to OpenAI** ← This was the bug!
4. **Create LLM** - Instantiates the appropriate LangChain chat model

### Why `"class": "ollama"` is Required

Without the `"class"` property, the factory falls back to OpenAI:

```python
# In default_llm_factory.py (simplified)
def create_llm(self, config):
    model_name = config.get("model_name")
    llm_class = config.get("class")
    
    if llm_class is None:
        # DEFAULT BEHAVIOR: Assume OpenAI
        llm_class = self.infer_class_from_model_name(model_name)
        # gpt-* → openai
        # claude-* → anthropic
        # mistral:* → "No llm entry for model_name" ERROR!
```

The model name `mistral:7b-instruct-v0.3-q4_K_M` doesn't match any known pattern, causing the error:

```
ValueError: No llm entry for model_name mistral:7b-instruct-v0.3-q4_K_M
```

By explicitly setting `"class": "ollama"`, we bypass the inference and directly use Ollama.

---

## Usage Guide

### Quick Start

1. **Ensure Ollama is running**:
   ```bash
   ollama serve
   ```

2. **Pull a model** (if not already):
   ```bash
   ollama pull mistral:7b-instruct-v0.3-q4_K_M
   ```

3. **Start NeuroSan**:
   ```bash
   .\venv\Scripts\Activate.ps1
   py -m run
   ```

4. **Open nsflow UI**: http://localhost:4173

### Switching All Agents to a Different Model

**Option 1: Edit `.env`** (recommended - no restart needed after file change):

```bash
MODEL_NAME=llama3.2:3b-instruct-q4_K_M
```

Restart the server:
```bash
py -m run
```

**Option 2: Edit `llm_config.hocon`**:

```hocon
"shared_llm_config": {
    "class": "ollama",
    "model_name": "llama3.2:3b-instruct-q4_K_M"
}
```

### Using Cloud Models

1. **Get Ollama Cloud API key** from https://ollama.com/cloud

2. **Set in `.env`**:
   ```bash
   OLLAMA_CLOUD_API_KEY=your_actual_api_key
   MODEL_NAME_ADVANCED=deepseek-v3.1:671b-cloud
   ```

3. **Complex agents** (like `agent_network_designer`) will use cloud automatically

### Override for Specific Agent

For one agent that needs a different model:

```hocon
{
    include "registries/llm_config.hocon"
    
    # Override with custom model for THIS agent only
    "llm_config": {
        "class": "ollama",
        "model_name": "qwen3-coder:480b-cloud"
    },
    
    "tools": [...]
}
```

---

## Troubleshooting

### Error: "No llm entry for model_name X"

**Cause**: Missing `"class": "ollama"` in config

**Fix**: Ensure `llm_config.hocon` has:
```hocon
"shared_llm_config": {
    "class": "ollama",  # ← THIS IS REQUIRED
    "model_name": "..."
}
```

### Error: "Connection refused localhost:11434"

**Cause**: Ollama server not running

**Fix**:
```bash
ollama serve
```

### Error: "Model not found: mistral:7b-instruct-v0.3-q4_K_M"

**Cause**: Model not pulled locally

**Fix**:
```bash
ollama pull mistral:7b-instruct-v0.3-q4_K_M
```

### Cloud models timing out

**Cause**: Large cloud models take time to respond

**Fix**: Increase timeout in `.env`:
```bash
OLLAMA_TIMEOUT=120
```

### No response from agent

**Cause**: Model may be loading (first request is slow)

**Fix**: Wait 30-60 seconds for initial model load, or check terminal for errors

---

## Summary

| Aspect | Before Migration | After Migration |
|--------|-----------------|-----------------|
| **LLM Provider** | OpenAI (hardcoded) | Ollama (centralized) |
| **Config Location** | 55+ individual files | 1 central file |
| **Model Switching** | Edit 55+ files | Edit 1 line in `.env` |
| **API Key Required** | OpenAI API key ($$) | None (local) or Ollama Cloud |
| **Cost** | Pay-per-request | Free (local) |
| **Offline Capable** | ❌ No | ✅ Yes |
| **Model Options** | GPT-4 variants | 20+ local + cloud models |

---

**Document Version**: 1.0  
**Last Updated**: December 22, 2025  
**NeuroSan Version**: v0.6.21
