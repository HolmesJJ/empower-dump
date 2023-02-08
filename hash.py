import hashlib
import pymongo

CONFIG = {
    "HOST": "127.0.0.1",
    "PORT": 27017,
    "DATABASE": "empower-auth"
}

client = pymongo.MongoClient(CONFIG["HOST"], CONFIG["PORT"])
database = client[CONFIG["DATABASE"]]


if __name__ == "__main__":
    for document in database.patient.find({}):
        hashed = hashlib.sha256(document["password"].encode("utf-8")).hexdigest()
        database.patient.update_one({"_id": document["_id"]}, {"$set": {"password": hashed}})
