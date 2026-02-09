import argparse
import re
import sys

import pymongo

parser = argparse.ArgumentParser()
parser.add_argument("--owner", action="store_true", help="no-op")
parser.add_argument(
    '-u','--username', required=True, help='UniFi username of Super Admin to delete'
)

if __name__ == "__main__":
    args = parser.parse_args()
    if "@" in args.username:
        query = {
            "email": {"$regex": re.sub(r"[^A-Za-z0-9]", r"\\\g<0>", args.username)}
        }
    else:
        query = {"name": args.username}

    db = pymongo.MongoClient("mongodb://127.0.0.1:27117").ace
    admin = db.admin.find_one_and_delete(query)
    if admin is None:
        print("Admin not found!")
        sys.exit(1)

    name = admin.get("name") or admin.get("ubic_name") or None
    if name is not None:
        print(f"Deleted admin: {name}")
    else:
        print("Deleted admin with unknown name")

    print("Removing privileges from all sites...")
    db.privilege.delete_many({"admin_id": str(admin["_id"])})
