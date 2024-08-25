from pathlib import Path


SelfIndexPath = Path(__file__).parent/"resources"/"index.js"
DefaultLLOBConfig = Path(__file__).parent/"resources"/"default_config.json"


__all__ = ["SelfIndexPath", "DefaultLLOBConfig"]
