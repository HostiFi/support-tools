import pymongo
import json
import datetime

four_hours_ago_utc = datetime.datetime.now() - datetime.timedelta(hours = 
4)
client = pymongo.MongoClient("mongodb://127.0.0.1:27117/ace")
mdb = client.ace
admins = mdb.admin.find()
for admin in admins:
    # Check if admin email includes '@hostifi.com'
    if "@hostifi.com" in admin["email"]:
        # Get time_created on the admin account
        try:
            admin_created_at_utc = 
datetime.datetime.utcfromtimestamp(int(admin["time_created"]))
        except Exception as e:
            # Skip accounts where time_created doesn't exist (due to use 
of Ubiquiti SSO)
            continue
        # Delete if older than four hours 
        if admin_created_at_utc < four_hours_ago_utc:
            print("Deleting " + admin["name"] + "...")
            os.system("python3 
/root/support-tools/lib/unifi/py/delete-super-admin.py -u " + 
admin["name"])
            print("Done!")
