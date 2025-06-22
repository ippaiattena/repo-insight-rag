import os
from dotenv import load_dotenv

def load_api_key() -> str:
    """
    .env ファイルから OpenAI API キーを読み込んで返す。
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY が .env に設定されていません。")
    return api_key
