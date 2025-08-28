import sys, os
import streamlit as st
from mongoengine import connect, disconnect
from mongoengine.connection import get_connection

# Optional: only import MongoConfig if not using Streamlit secrets
try:
    from config.database import MongoConfig
except ImportError:
    MongoConfig = None


def connect_to_db():
    try:
        # Check if already connected
        get_connection()
        print("Already connected to MongoDB.")
        return
    except Exception:
        pass

    # Try Streamlit secrets first
    mongo_uri = None
    try:
        mongo_uri = st.secrets["MONGO_URI"]
        print("Using Mongo URI from Streamlit secrets.")
    except Exception:
        # Fallback to MongoConfig
        if MongoConfig:
            mongo_config = MongoConfig()
            mongo_uri = mongo_config.get_mongo_uri()
            print("Using Mongo URI from MongoConfig.")

    if not mongo_uri:
        raise ValueError("MongoDB URI not found in Streamlit secrets or MongoConfig!")

    try:
        connect(host=mongo_uri)
        print("Successfully connected to MongoDB.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")


def disconnect_from_db():
    disconnect()
    print("Disconnected from MongoDB.")


def check_db_connection():
    try:
        connection = get_connection()
        db = connection.get_database()
        db.list_collection_names()
        return True
    except Exception as e:
        print(f"Database connection check failed: {e}")
        return False
