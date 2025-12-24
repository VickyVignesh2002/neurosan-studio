# Copyright © 2025 Cognizant Technology Solutions Corp, www.cognizant.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# END COPYRIGHT

import os
import urllib.request
import urllib.error
import json
from typing import Dict, Any, Optional, List


class LLMConfig:
    """
    Utility class to get LLM configuration from environment variables.
    Supports Ollama (local), Ollama Cloud, OpenAI, and other providers.
    
    Features:
    - Automatic fallback: If local Ollama is unavailable, automatically falls back to Ollama Cloud
    - Set OLLAMA_AUTO_FALLBACK=true to enable (enabled by default)
    - Set OLLAMA_API_KEY for cloud fallback to work
    
    Ollama Cloud Usage:
    - Set LLM_PROVIDER=ollama_cloud (or let it auto-fallback)
    - Set OLLAMA_API_KEY=your_api_key (get from https://ollama.com/settings/keys)
    - Set OLLAMA_MODEL to a cloud model (e.g., gpt-oss:120b-cloud)
    
    See: https://docs.ollama.com/cloud
    """

    # Ollama Cloud API endpoint
    OLLAMA_CLOUD_URL = "https://ollama.com"
    
    # Default cloud model for fallback
    DEFAULT_CLOUD_MODEL = "llama3.2:3b"

    @staticmethod
    def is_ollama_running(base_url: str = "http://localhost:11434", timeout: float = 5.0) -> bool:
        """
        Check if local Ollama server is running and accessible.
        
        Args:
            base_url: Ollama server URL
            timeout: Connection timeout in seconds
            
        Returns:
            True if Ollama is running, False otherwise
        """
        try:
            url = f"{base_url.rstrip('/')}/api/tags"
            request = urllib.request.Request(url, method='GET')
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.status == 200
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
            return False

    @staticmethod
    def get_local_models(base_url: str = "http://localhost:11434", timeout: float = 5.0) -> List[str]:
        """
        Get list of locally available Ollama models.
        
        Args:
            base_url: Ollama server URL
            timeout: Connection timeout in seconds
            
        Returns:
            List of model names, empty list if Ollama is not running
        """
        try:
            url = f"{base_url.rstrip('/')}/api/tags"
            request = urllib.request.Request(url, method='GET')
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = json.loads(response.read().decode('utf-8'))
                models = data.get('models', [])
                return [m.get('name', '') for m in models if m.get('name')]
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, json.JSONDecodeError):
            return []

    @staticmethod
    def is_model_available(model_name: str, base_url: str = "http://localhost:11434") -> bool:
        """
        Check if a specific model is available locally.
        
        Args:
            model_name: Name of the model to check
            base_url: Ollama server URL
            
        Returns:
            True if model is available, False otherwise
        """
        models = LLMConfig.get_local_models(base_url)
        if not models:
            return False
        
        # Check exact match or partial match (e.g., "mistral" matches "mistral:7b-instruct")
        model_base = model_name.split(':')[0].lower()
        for available_model in models:
            available_base = available_model.split(':')[0].lower()
            if model_name.lower() == available_model.lower() or model_base == available_base:
                return True
        return False

    @staticmethod
    def get_llm_config() -> Dict[str, Any]:
        """
        Get the appropriate LLM configuration based on environment variables.
        
        Automatic Fallback Logic:
        1. If LLM_PROVIDER=ollama, check if local Ollama is running
        2. If local Ollama is not running and OLLAMA_API_KEY is set, fallback to cloud
        3. If OLLAMA_AUTO_FALLBACK=false, skip fallback check
        
        Supported LLM_PROVIDER values:
        - "ollama" (default): Local Ollama server (with auto-fallback to cloud)
        - "ollama_cloud": Ollama Cloud API (requires OLLAMA_API_KEY)
        - "openai": OpenAI API
        
        Returns:
            Dictionary with 'class' and 'model_name' (and potentially other config)
        """
        llm_provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        
        if llm_provider == "ollama":
            return LLMConfig.get_ollama_config_with_fallback()
        elif llm_provider == "ollama_cloud":
            return LLMConfig.get_ollama_cloud_config()
        elif llm_provider == "openai":
            return LLMConfig.get_openai_config()
        else:
            # Default to Ollama local with fallback
            return LLMConfig.get_ollama_config_with_fallback()

    @staticmethod
    def get_ollama_config_with_fallback() -> Dict[str, Any]:
        """
        Get Ollama config with automatic fallback to cloud if local is unavailable.
        
        Fallback conditions (all must be true):
        1. OLLAMA_AUTO_FALLBACK is not "false" (enabled by default)
        2. Local Ollama is not running OR requested model is not available
        3. OLLAMA_API_KEY is set
        
        Returns:
            Local Ollama config if available, otherwise Cloud config
        """
        auto_fallback = os.getenv("OLLAMA_AUTO_FALLBACK", "true").lower() != "false"
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        requested_model = os.getenv("OLLAMA_MODEL", "mistral:7b-instruct-v0.3-q4_K_M")
        api_key = os.getenv("OLLAMA_API_KEY")
        
        # Check if local Ollama is available
        ollama_running = LLMConfig.is_ollama_running(base_url)
        model_available = LLMConfig.is_model_available(requested_model, base_url) if ollama_running else False
        
        # Determine if we should fallback
        should_fallback = False
        fallback_reason = ""
        
        if auto_fallback and api_key:
            if not ollama_running:
                should_fallback = True
                fallback_reason = f"Local Ollama not running at {base_url}"
            elif not model_available:
                should_fallback = True
                fallback_reason = f"Model '{requested_model}' not found locally"
        
        if should_fallback:
            print(f"⚠️  {fallback_reason}")
            print(f"🌐 Automatically falling back to Ollama Cloud...")
            return LLMConfig.get_ollama_cloud_config(fallback_model=requested_model)
        
        # Use local Ollama
        if not ollama_running:
            print(f"⚠️  Warning: Local Ollama not running at {base_url}")
            if not api_key:
                print(f"💡 Tip: Set OLLAMA_API_KEY to enable automatic cloud fallback")
        elif not model_available and ollama_running:
            available_models = LLMConfig.get_local_models(base_url)
            print(f"⚠️  Warning: Model '{requested_model}' not found locally")
            if available_models:
                print(f"📋 Available models: {', '.join(available_models[:5])}")
            if not api_key:
                print(f"💡 Tip: Set OLLAMA_API_KEY to enable automatic cloud fallback")
        
        return LLMConfig.get_ollama_config()
    
    @staticmethod
    def get_ollama_config() -> Dict[str, Any]:
        """
        Get LOCAL Ollama LLM configuration from environment variables.
        Uses local Ollama server (default: http://localhost:11434)
        """
        config = {
            "class": "ollama",
            "model_name": os.getenv("OLLAMA_MODEL", "mistral:7b-instruct-v0.3-q4_K_M"),
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        }
        
        # Add optional Ollama parameters
        temperature = os.getenv("OLLAMA_TEMPERATURE")
        if temperature is not None:
            config["temperature"] = float(temperature)
        
        top_p = os.getenv("OLLAMA_TOP_P")
        if top_p is not None:
            config["top_p"] = float(top_p)
        
        # Timeout for requests (useful for large models)
        timeout = os.getenv("OLLAMA_TIMEOUT")
        if timeout is not None:
            config["timeout"] = float(timeout)
        
        return config

    @staticmethod
    def get_ollama_cloud_config(fallback_model: Optional[str] = None) -> Dict[str, Any]:
        """
        Get OLLAMA CLOUD configuration from environment variables.
        
        Args:
            fallback_model: Optional model name to use (for automatic fallback scenarios)
        
        Requires:
        - OLLAMA_API_KEY: Your API key from https://ollama.com/settings/keys
        - OLLAMA_MODEL: Cloud model name (e.g., gpt-oss:120b-cloud, qwen3:32b-cloud)
        
        See available cloud models: https://ollama.com/search?c=cloud
        Docs: https://docs.ollama.com/cloud
        """
        api_key = os.getenv("OLLAMA_API_KEY")
        if not api_key:
            raise ValueError(
                "OLLAMA_API_KEY is required for Ollama Cloud. "
                "Get your API key from: https://ollama.com/settings/keys"
            )
        
        # Use fallback model if provided, otherwise use env var or default cloud model
        if fallback_model:
            # For fallback, use the same model name - Ollama Cloud supports many models
            model = os.getenv("OLLAMA_CLOUD_MODEL", fallback_model)
        else:
            model = os.getenv("OLLAMA_MODEL", LLMConfig.DEFAULT_CLOUD_MODEL)
        
        config = {
            "class": "ollama",
            "model_name": model,
            "base_url": LLMConfig.OLLAMA_CLOUD_URL,
            "api_key": api_key,  # Ollama Cloud requires API key
        }
        
        # Add optional parameters
        temperature = os.getenv("OLLAMA_TEMPERATURE")
        if temperature is not None:
            config["temperature"] = float(temperature)
        
        top_p = os.getenv("OLLAMA_TOP_P")
        if top_p is not None:
            config["top_p"] = float(top_p)
        
        timeout = os.getenv("OLLAMA_TIMEOUT", "300")  # Cloud may need longer timeout
        config["timeout"] = float(timeout)
        
        print(f"☁️  Using Ollama Cloud: {model}")
        
        return config
    
    @staticmethod
    def get_openai_config() -> Dict[str, Any]:
        """
        Get OpenAI LLM configuration from environment variables.
        """
        return {
            "class": "openai",
            "model_name": os.getenv("OPENAI_MODEL", "gpt-4o"),
        }
    
    @staticmethod
    def to_hocon_config(llm_config: Dict[str, Any]) -> str:
        """
        Convert LLM config dict to HOCON format string.
        """
        hocon_lines = ['    "llm_config": {']
        
        for key, value in llm_config.items():
            if key == "class" or key == "model_name":
                hocon_lines.append(f'        "{key}": "{value}",')
            elif isinstance(value, str):
                hocon_lines.append(f'        "{key}": "{value}",')
            elif isinstance(value, (int, float)):
                hocon_lines.append(f'        "{key}": {value},')
            elif isinstance(value, bool):
                hocon_lines.append(f'        "{key}": {str(value).lower()},')
        
        # Remove trailing comma from last line
        if hocon_lines[-1].endswith(","):
            hocon_lines[-1] = hocon_lines[-1][:-1]
        
        hocon_lines.append("    },")
        
        return "\n".join(hocon_lines)
