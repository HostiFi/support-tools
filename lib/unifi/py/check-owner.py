#!/usr/bin/python3
import pymongo
import json
from bson import ObjectId

client = pymongo.MongoClient("mongodb://127.0.0.1:27117/ace")
mdb = client.ace

super_cloudaccess = mdb.setting.find_one({"key": "super_cloudaccess"})
ubic_uuid = super_cloudaccess["ubic_uuid"]
admin = mdb.admin.find_one({"ubic_uuid": ubic_uuid})
owner_email = admin["email"]
owner_name = admin["name"]
owner_ubic_name = admin["ubic_name"]

print("Owner")
print("Email: " + owner_email)
print("Username: " + owner_name)
print("UI SSO: " + owner_ubic_name)