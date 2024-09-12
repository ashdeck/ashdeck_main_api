from pymongo import MongoClient
from .config import settings


def connect_to_db():
    db_url = settings.DATABASE_URL
    client = MongoClient(db_url, uuidRepresentation='standard')

    try:
        db = client[settings.MONGODB_DATABASE]
        print("Connected to Database")
        return db
    except Exception:
        print("Connected to database")


db = connect_to_db()
