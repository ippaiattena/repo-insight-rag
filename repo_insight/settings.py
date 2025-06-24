from functools import lru_cache
from chromadb.config import Settings

@lru_cache(maxsize=None)
def get_shared_settings(persist_dir: str) -> Settings:
    return Settings(persist_directory=persist_dir, allow_reset=True)