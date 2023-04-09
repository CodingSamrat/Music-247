import os
from typing import Mapping

from filexdb import FileXdb
from pymongo import MongoClient
from dotenv import load_dotenv
from Bot.config import DATABASE, is_in_development_mode

__all__ = ("Collections", "Database")

#: Database engine
ENGINE = DATABASE["engine"]


class Collections:
    GUILD = "guild"
    USER = "user"


def get_filexdb_collection(coll_name: str):
    if ENGINE == "filexdb":

        #: Initiating Database
        if is_in_development_mode:
            db = FileXdb(DATABASE["db"], DATABASE["db_dir"], mode="json")
            collection = db.collection(coll_name)

            return collection

        elif not is_in_development_mode:
            db = FileXdb(DATABASE["db"], DATABASE["db_dir"])
            collection = db.collection(coll_name)

            return collection


def get_mongodb_collection(coll_name: str):
    if ENGINE == "mongodb":

        load_dotenv()
        MONGO_STRING = os.getenv('MONGO_STRING')
        client = MongoClient(MONGO_STRING)

        #: Initiating Database
        db = client[DATABASE["db"]]

        #: Creating Collection
        collection = db[coll_name]

        return collection


class Database:
    @staticmethod
    def find(_collection: str, _id: str):
        if ENGINE == "filexdb":
            coll = get_filexdb_collection(_collection)
            data = coll.find({"_id": _id})

            if len(data) > 0:
                return data[0]
            elif len(data) <= 0:
                return None

        elif ENGINE == "mongodb":
            coll = get_mongodb_collection(_collection)
            data = coll.find_one({"_id": _id})
            return data

    @staticmethod
    def insert(_collection: str, _document: Mapping):
        if ENGINE == "filexdb":
            coll = get_filexdb_collection(_collection)
            coll.insert(_document)

        elif ENGINE == "mongodb":
            coll = get_mongodb_collection(_collection)
            coll.insert_one(_document)

    @staticmethod
    def update(_collection: str, _document: Mapping, _id: str):
        if ENGINE == "filexdb":
            coll = get_filexdb_collection(_collection)
            coll.update(_document, {"_id": _id})

        elif ENGINE == "mongodb":
            coll = get_mongodb_collection(_collection)
            coll.update_one({"_id": _id}, {"$set": _document})




