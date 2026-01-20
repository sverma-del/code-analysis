# backend/core/db.py
import os
from tortoise import Tortoise
from dotenv import load_dotenv
load_dotenv(override=True)

SUPABASE_DB_URL = os.environ.get("SUPABASE_DB_URL")

print("Database URL Length:", len(SUPABASE_DB_URL))
TORTOISE_ORM = {
    "connections": {
        "default": SUPABASE_DB_URL # Update with your credentials
    },
    "apps": {
        "models": {
            # Note the path: backend.models.<file_name>
            "models": [
                "models.users", 
                "models.projects", 
                "models.analysis", 
                "models.progress",
                "aerich.models"
            ],
            "default_connection": "default",
        }
    },
}