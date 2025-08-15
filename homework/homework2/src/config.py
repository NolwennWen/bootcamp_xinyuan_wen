from dotenv import load_dotenv
import os

def load_env():
    """Load environment variables from .env"""
    load_dotenv()

def get_key(key_name):
    """Get value from environment"""
    return os.getenv(key_name)
