import datetime
import pymongo

if __name__ == "__main__":
    db = pymongo.MongoClient("mongodb://127.0.0.1:27117").ace

    cutoff_datetime = datetime.datetime.utcnow() - datetime.timedelta(hours=4)
    cutoff_timestamp = cutoff_datetime.timestamp()
    admins = db.admin.find(
        filter={
            "email": {"$regex": R"(?<!^dev)@hostifi\.com$"},
            "$or": [
                {"time_created": {"$exists": False}},
                {"time_created": {"$lte": cutoff_timestamp}},
            ],
        },
        projection=[],
    )

    for admin in admins:
        db.privilege.delete_many({"admin_id": str(admin["_id"])})
        db.admin.delete_one(admin)
