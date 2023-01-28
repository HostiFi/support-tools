import crypt
import os
import string
from random import SystemRandom
import argparse
import pymongo
import logging

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='Omada username of Super Admin to delete')
args = parser.parse_args()

if args.username is not None:
    is_email = None
    if "@" in args.username:
        is_email = True
    else:
        is_email = False

    if is_email == False:
        logging.info("Deleting Omada Super Admin by username")
        logging.info("Connecting to MongoDB...")
        client = pymongo.MongoClient("mongodb://127.0.0.1:27217/omada")
        mdb = client.omada
        logging.info("Finding Admin ID...")
        logging.info("Deleting Admin...")
        mdb.user.delete_many({'name': args.username})
        print("Deleted the account for: ")
        print(args.username)

    if is_email == True:
        logging.info("Deleting Omada Super Admin by email")
        logging.info("Connecting to MongoDB...")
        client = pymongo.MongoClient("mongodb://127.0.0.1:27217/omada")
        mdb = client.omada
        user_list = mdb.user.find()
        user_name = ""
        for user in user_list:
            try:
                if args.username in base64.b64decode(user["email"]).decode('utf-8'):
                    user_name = user["name"]
            except:
                continue
        logging.info("Deleting Admin...")
        mdb.user.delete_many({'name': user_name})
        print("Deleted the account for username: ")
        print(args.username)

else:
    print("Error: Missing argument. --username is required.")