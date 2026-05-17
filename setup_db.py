# setup_db.py

from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv

import os

load_dotenv()

DB_URI = os.getenv("DATABASE_URL")

print("CONNECTING TO POSTGRES...")

try:

    with PostgresSaver.from_conn_string(DB_URI) as checkpointer:

        checkpointer.setup()

    print("POSTGRES TABLES CREATED")

except Exception as e:

    print(f"ERROR: {str(e)}")