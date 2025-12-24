"""
Script to update all HOCON files to use centralized LLM config.
Run from the project root: python scripts/update_llm_config.py
"""

import os
import re
from pathlib import Path

# Project root
ROOT = Path(r"J:\Company\amasQIS\AI\NeuroSan\Neurosan-v02")
REGISTRIES = ROOT / "registries"

# Files to skip (already use local models or have special config)
SKIP_FILES = {
    "llm_config.hocon",  # Our new shared config
    "music_nerd_local.hocon",
    "music_nerd_pro_local.hocon",
    "music_nerd_pro_sly_local.hocon",
    "aaosa.hocon",  # Shared instructions, no llm_config
    "aaosa_basic.hocon",  # Shared instructions, no llm_config
}

# Files that need advanced config (complex agents)
ADVANCED_CONFIG_FILES = {
    "agent_network_designer.hocon",
    "agent_network_architect.hocon",
    "conscious_agent.hocon",
}

# Pattern to match llm_config blocks
LLM_CONFIG_PATTERNS = [
    # Standard format: "llm_config": { "model_name": "gpt-4o" },
    re.compile(r'"llm_config":\s*\{\s*"model_name":\s*"[^"]+",?\s*\},?', re.MULTILINE),
    # With trailing comma variations
    re.compile(r'"llm_config":\s*\{\s*\n\s*"model_name":\s*"[^"]+",?\s*\n\s*\},?', re.MULTILINE),
    # With comment
    re.compile(r'"llm_config":\s*\{\s*\n\s*#[^\n]*\n\s*"model_name":\s*"[^"]+",?\s*\n\s*\},?', re.MULTILINE),
]

# Include statement to add
INCLUDE_STATEMENT = 'include "registries/llm_config.hocon"\n\n'

def get_include_path(file_path: Path) -> str:
    """Get the correct include path based on file location."""
    rel_path = file_path.relative_to(REGISTRIES)
    depth = len(rel_path.parts) - 1
    if depth == 0:
        return 'include "registries/llm_config.hocon"'
    else:
        # For files in subdirectories like basic/, tools/, industry/
        return 'include "registries/llm_config.hocon"'

def update_hocon_file(file_path: Path, use_advanced: bool = False) -> bool:
    """Update a single HOCON file to use shared LLM config."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Check if already updated
        if 'include "registries/llm_config.hocon"' in content:
            print(f"  SKIP (already updated): {file_path.name}")
            return False
        
        # Check if has llm_config
        if '"llm_config"' not in content and "'llm_config'" not in content:
            print(f"  SKIP (no llm_config): {file_path.name}")
            return False
        
        # Determine which config to use
        config_ref = "${shared_llm_config_advanced}" if use_advanced else "${shared_llm_config}"
        
        # Add include statement after the opening brace
        # Find the first { after the copyright header
        first_brace = content.find('{')
        if first_brace == -1:
            print(f"  ERROR (no opening brace): {file_path.name}")
            return False
        
        # Insert include after the opening brace
        include_line = f'\n    include "registries/llm_config.hocon"\n'
        content = content[:first_brace+1] + include_line + content[first_brace+1:]
        
        # Replace llm_config block with reference
        # Handle various formats
        
        # Pattern 1: "llm_config": { "model_name": "..." },
        pattern1 = re.compile(
            r'"llm_config":\s*\{\s*\n?\s*(?:#[^\n]*\n\s*)?'
            r'"model_name":\s*"[^"]+",?\s*\n?\s*\},?',
            re.MULTILINE
        )
        
        # Pattern 2: "llm_config": { \n "model_name": "..." \n },
        pattern2 = re.compile(
            r'"llm_config":\s*\{[^}]+\},?',
            re.MULTILINE | re.DOTALL
        )
        
        replacement = f'"llm_config": {config_ref},'
        
        # Try pattern 1 first
        new_content = pattern1.sub(replacement, content)
        if new_content == content:
            # Try pattern 2
            new_content = pattern2.sub(replacement, content)
        
        if new_content == original_content.replace(original_content, original_content):
            print(f"  WARNING (no replacement made): {file_path.name}")
        
        # Write back
        file_path.write_text(new_content, encoding='utf-8')
        config_type = "ADVANCED" if use_advanced else "standard"
        print(f"  UPDATED ({config_type}): {file_path.name}")
        return True
        
    except Exception as e:
        print(f"  ERROR: {file_path.name} - {e}")
        return False

def main():
    print("=" * 60)
    print("Updating HOCON files to use centralized LLM config")
    print("=" * 60)
    
    # Find all .hocon files in registries
    hocon_files = list(REGISTRIES.glob("**/*.hocon"))
    print(f"\nFound {len(hocon_files)} HOCON files\n")
    
    updated = 0
    skipped = 0
    errors = 0
    
    for file_path in sorted(hocon_files):
        filename = file_path.name
        
        # Skip certain files
        if filename in SKIP_FILES:
            print(f"  SKIP (in skip list): {filename}")
            skipped += 1
            continue
        
        # Determine if this needs advanced config
        use_advanced = filename in ADVANCED_CONFIG_FILES
        
        if update_hocon_file(file_path, use_advanced):
            updated += 1
        else:
            skipped += 1
    
    print("\n" + "=" * 60)
    print(f"Summary: {updated} updated, {skipped} skipped")
    print("=" * 60)

if __name__ == "__main__":
    main()
