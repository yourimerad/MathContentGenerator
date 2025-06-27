import json
from pathlib import Path
from typing import Any, Dict, Optional
import aiofiles

class APICache:
    """Système de cache pour optimiser les appels API"""
    def __init__(self, cache_dir: Path = Path(".cache")):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        self.memory_cache: Dict[str, Any] = {}
        
    def get_cache_key(self, prompt: str, context: Optional[str] = None) -> str:
        """Génère une clé de cache unique"""
        import hashlib
        content = f"{prompt}:{context or ''}"
        return hashlib.md5(content.encode()).hexdigest()
        
    async def get(self, key: str) -> Optional[Any]:
        """Récupère une valeur du cache"""
        if key in self.memory_cache:
            return self.memory_cache[key]
            
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            async with aiofiles.open(cache_file, 'r') as f:
                data = json.loads(await f.read())
                self.memory_cache[key] = data
                return data
        return None
        
    async def set(self, key: str, value: Any) -> None:
        """Stocke une valeur dans le cache"""
        self.memory_cache[key] = value
        cache_file = self.cache_dir / f"{key}.json"
        async with aiofiles.open(cache_file, 'w') as f:
            await f.write(json.dumps(value, ensure_ascii=False, indent=2)) 