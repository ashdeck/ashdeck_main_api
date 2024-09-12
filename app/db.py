from pymongo import MongoClient


def connect_to_db():
    db_url = "mongodb+srv://josh:nmG8uRPYEspcE8IE@cluster0.vfimyzq.mongodb.net/test"
    client = MongoClient(db_url, uuidRepresentation='standard')

    try:
        db = client["website_blocker"]
        print("Connected to Database")
        return db
    except Exception:
        print("Connected to database")


db = connect_to_db()
