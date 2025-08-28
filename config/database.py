import os
from dotenv import load_dotenv
import gridfs
from pymongo import MongoClient

from pathlib import Path
from dotenv import load_dotenv

# Always load from project root (ReceiptMatch_AI/.env)
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env"
print(f"🔍 Loading .env from: {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path)


class MongoConfig:
    def __init__(self):
        self.MONGO_URI = os.getenv('MONGO_URI')
        self.DATABASE_NAME = os.getenv('MONGO_DATABASE')

        print(f"DEBUG MONGO_URI: {self.MONGO_URI}")
        print(f"DEBUG MONGO_DATABASE: {self.DATABASE_NAME}")

        if not self.MONGO_URI:
            raise ValueError("❌ MONGO_URI not found in environment variables.")


    def get_mongo_uri(self):
        return self.MONGO_URI

    def get_gridfs_connection(self):
        client = MongoClient(self.MONGO_URI)
        db = client[self.DATABASE_NAME]
        return gridfs.GridFS(db)


