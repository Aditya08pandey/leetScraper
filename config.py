import os
from dotenv import load_dotenv

load_dotenv()

import cohere

COHERE_API_KEY  = os.getenv("COHERE_API_KEY")
COHERE_MODEL    = os.getenv("COHERE_MODEL", "command-r-plus")
client = cohere.Client(COHERE_API_KEY)


LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
USER_AGENT       = os.getenv("USER_AGENT", "Mozilla/5.0")

TOTAL_TO_FETCH   = int(os.getenv("TOTAL_TO_FETCH", 200)) 
BATCH_SIZE       = int(os.getenv("BATCH_SIZE", 50))   
REPHRASE_ENABLED = os.getenv("REPHRASE_ENABLED", "true").lower() == "true"

SLEEP_REQ_MIN, SLEEP_REQ_MAX     = 1.5, 2.5 
SLEEP_BATCH_MIN, SLEEP_BATCH_MAX = 1.0, 2.0 


DB_PATH = os.getenv("DB_PATH", "questions.db")
