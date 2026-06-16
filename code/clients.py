from pymongo import MongoClient
from minio import Minio
from code.config import *


mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]


def insert(collection, data):
    db[collection].insert_one(data)


def find(collection, query=None):
    if query is None:
        query = {}

    return list(db[collection].find(query))


def upsert(collection, query, data):
    db[collection].update_one(
        query,
        {"$set": data},
        upsert=True
    )


minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)


def init_bucket():
    if not minio_client.bucket_exists(MINIO_BUCKET):
        minio_client.make_bucket(MINIO_BUCKET)


def upload_file(file_path, object_name):
    result = minio_client.fput_object(
        MINIO_BUCKET,
        object_name,
        file_path
    )

    return result


def download_file(object_name, destination):
    minio_client.fget_object(
        MINIO_BUCKET,
        object_name,
        destination
    )