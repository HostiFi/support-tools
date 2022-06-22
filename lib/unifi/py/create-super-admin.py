import crypt
from datetime import datetime
import os
import string
from random import SystemRandom
import argparse
import pymongo
import random
import logging

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='UniFi username to create', required=True)
parser.add_argument('-p', '--password', help='UniFi password to create')
parser.add_argument('-e', '--email', help='UniFi email to create', required=True)
args = parser.parse_args()

randchoice = SystemRandom().choice
password = ''.join(random.choice(string.ascii_letters) for i in range(8))

def sha512_crypt(password, salt=None, rounds=None):
    if salt is None:
        salt = ''.join([randchoice(string.ascii_letters + string.digits)
                        for _ in range(8)])

    prefix = '$6$'
    if rounds is not None:
        rounds = max(1000, min(999999999, rounds or 5000))
        prefix += 'rounds={0}$'.format(rounds)
    return crypt.crypt(password, prefix + salt)

def create_super_admin(password):
    logging.info("Creating UniFi Super Admin")
    logging.info("Connecting to MongoDB...")
    client = pymongo.MongoClient("mongodb://127.0.0.1:27117/ace")
    mdb = client.ace
    logging.info("Inserting Admin...")
    new_admin_id = insert_admin = mdb.admin.insert_one({
        "email" : args.email,
        "last_site_name" : "default",
        "name" : args.username,
        "x_shadow" : sha512_crypt(password),
        "time_created" : int(datetime.utcnow().timestamp()),
    }).inserted_id

    logging.info("Promoting Admin to Super Admin...")
    mdb.privilege.insert_many(
        {
            "admin_id": str(new_admin_id),
            "site_id": str(site_id["_id"]),
            "role": "admin",
            "permissions": [],
        } for site_id in mdb.site.find()
    )
    print("UniFi Super Admin created")
    print("Username: " + args.username)
    print("Password: " + password)

if __name__ == "__main__":
    create_super_admin(args.password or password)
