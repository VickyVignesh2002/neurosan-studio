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
from typing import Dict, Any


class LLMConfig:
    """
    Utility class to get LLM configuration from environment variables.
    Supports both Ollama and OpenAI models.
    """

    @staticmethod
    def get_llm_config() -> Dict[str, Any]:
        """
        Get the appropriate LLM configuration based on environment variables.
        
        Returns:
            Dictionary with 'class' and 'model_name' (and potentially other config)
        """
        llm_provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        
        if llm_provider == "ollama":
            return LLMConfig.get_ollama_config()
        elif llm_provider == "openai":
            return LLMConfig.get_openai_config()
        else:
            # Default to Ollama
            return LLMConfig.get_ollama_config()
    
    @staticmethod
    def get_ollama_config() -> Dict[str, Any]:
        """
        Get Ollama LLM configuration from environment variables.
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
