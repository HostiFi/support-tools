import crypt
import os
import string
from random import SystemRandom
import argparse
import pymongo
import logging

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='UniFi username of Super Admin to delete')
args = parser.parse_args()

if args.username is not None or args.email is not None:
    is_email = None
    if "@" in args.username:
        is_email = True
    else:
        is_email = False
    if is_email == False:
        logging.info("Deleting UniFi Super Admin by username")
        logging.info("Connecting to MongoDB...")
        site_ids = []
        client = pymongo.MongoClient("mongodb://127.0.0.1:27117/ace")
        mdb = client.ace
        logging.info("Finding Admin ID...")
        db_dump = mdb.site.find()
        admin_list = mdb.admin.find()
        for admin in admin_list:
            try:
                if admin["name"] == args.username:
                    admin_id = str(admin["_id"])
            except:
                continue
        logging.info("Deleting Admin...")
        mdb.admin.remove({'name': args.username})
        for site in db_dump:
            site_id = str(site["_id"])
            site_ids.append(site_id)
        logging.info("Removing privileges from all sites...")
        for site_id in site_ids:
            mdb.privilege.remove({"admin_id" : admin_id, "site_id" : site_id})
        logging.info("Deleted the account for: ")
        logging.info(args.username)

    else:
        print("Error: Missing argument. --username is required.")

    if is_email == True:
        logging.info("Deleting UniFi Super Admin by email")
        logging.info("Connecting to MongoDB...")
        site_ids = []
        client = pymongo.MongoClient("mongodb://127.0.0.1:27117/ace")
        mdb = client.ace
        logging.info("Finding Admin ID...")
        db_dump = mdb.site.find()
        admin_list = mdb.admin.find()
        for admin in admin_list:
            try:
                if args.username in admin["email"]:
                    admin_id = str(admin["_id"])
                    admin_name = admin["name"]
            except:
                continue
        logging.info("Deleting Admin...")
        mdb.admin.remove({'name': admin_name})
        for site in db_dump:
            site_id = str(site["_id"])
            site_ids.append(site_id)
        logging.info("Removing privileges from all sites...")
        for site_id in site_ids:
            mdb.privilege.remove({"admin_id" : admin_id, "site_id" : site_id})
        logging.info("Deleted the account for username: ")
        logging.info(admin_name)

else:
    print("Error: Missing argument. --email is required.")