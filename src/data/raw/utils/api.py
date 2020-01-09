import os
from dotenv import load_dotenv, find_dotenv


def get_key():
    dotenv_fp = find_dotenv()
    load_dotenv(dotenv_fp)
    return os.environ.get('API_KEY')
