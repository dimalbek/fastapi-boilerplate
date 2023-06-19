from typing import Optional, List

from bson.objectid import ObjectId
from pymongo.database import Database
from pymongo.results import DeleteResult, UpdateResult


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, payload: dict):
        payload["user_id"] = ObjectId(user_id)
        shanyrak = self.database["shanyraks"].insert_one(payload)
        return shanyrak.inserted_id

    def get_shanyrak_by_id(self, shanyrak_id: str, user_id: str) -> Optional[dict]:
        user = self.database["shanyraks"].find_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
        return user

    def get_all_shanyraks(self, user_id: str) -> List[dict]:
        shanyraks = self.database["shanyraks"].find({"user_id": ObjectId(user_id)})
        return list(shanyraks)
    
    def update_shanyrak_by_id(self, shanyrak_id: str, user_id: str, data: dict) -> UpdateResult:
        return self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)},
            update={
                "$set": data,
            },
        )

    def delete_shanyrak_by_id(self, shanyrak_id: str, user_id: str) -> DeleteResult:
        return self.database["shanyraks"].delete_one(
            {"_id": ObjectId(shanyrak_id), "user_id": ObjectId(user_id)}
        )
    

    def pagination_shanyraks(self, limit, offset, rooms_count, price_from, price_until, latitude=None, longitude=None, radius=None):
        sort_filter = {}

        if rooms_count is not None:
            sort_filter["rooms_count"] = {"$gt": rooms_count}
        
        if price_until is not None and price_from is not None:    
            sort_filter["price"] = {"$gt": price_from, "$lt": price_until}
        
        elif price_from is None and price_until is not None:
            sort_filter["price"] = {"$lt": price_until}
        
        elif price_until is None and price_from is not None:
            sort_filter["price"] = {"$gt": price_from}
        
        if latitude is not None and longitude is not None and radius is not None:
            sort_filter["location"] = {
                "$geoWithin": {
                    "$centerSphere": [[longitude, latitude], radius / 6371]
                }
            }

        cursor = self.database["shanyraks"].find(sort_filter).limit(limit).skip(offset).sort("created_at")
        shanyraks = []
        for obj in cursor:
            obj["_id"] = str(obj["_id"])  
            obj["user_id"] = str(obj["user_id"])
            shanyraks.append(obj)

        return shanyraks
    

class PostRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_post(self, input: dict):
        payload = {
            "city": input["city"],
            "message": input["message"],
            "user_id": ObjectId(input["user_id"])
        }

        self.database["posts"].insert_one(payload)
