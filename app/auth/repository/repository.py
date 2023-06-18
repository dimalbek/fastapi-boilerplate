from datetime import datetime
from typing import Optional

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> Optional[dict]:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user

    def update_user(self, user_id: str, data: dict):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "phone": data["phone"],
                    "name": data["name"],
                    "city": data["city"],
                }
            },
        )

    def set_user_like(self, user_id: str, shanyrak_id: str):
        likes = self.get_user_likes(user_id)
        likes.add(shanyrak_id)

        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "likes": list(likes),
                }
            },
        )

    def get_user_likes(self, user_id: str) -> set:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return set(user["likes"]) if "likes" in user else set()

    def delete_user_like(self, user_id: str, shanyrak_id: str):
        likes = self.get_user_likes(user_id)
        print(likes)
        if shanyrak_id in likes:
            likes.remove(shanyrak_id)

        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "likes": list(likes),
                }
            },
        )

    def get_shanyraks_by_id(self, user_id) -> list:
        shanyrak_ids = self.get_user_likes(user_id)
        obj_shanyrak_ids = [ObjectId(shanyrak_id) for shanyrak_id in shanyrak_ids]
        print("ids", obj_shanyrak_ids)
        shanyraks = self.database["shanyraks"].find({"_id": {"$in": obj_shanyrak_ids}})

        return list(shanyraks)
    
    def save_avatar(self, user_id: str, url: str):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "avatar_url": 1,
                }
            },
        )

    def delete_avatar(self, user_id: str):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$unset": {
                    "avatar_url": "",
                }
            },
        )
    
    def get_avatar(self, user_id: str) -> Optional[str]:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user.get("avatar_url") if user else None