import crypt
from datetime import datetime
import os
import string
from random import SystemRandom
import argparse
import pymongo
import random
import logging
import base64
import hashlib

import omada

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='Omada username to create', required=True)
parser.add_argument('-p', '--password', help='Omada password to create')
args = parser.parse_args()

randchoice = SystemRandom().choice
password = 'H137!'.join(random.choice(string.ascii_letters) for i in range(8))

def sha256_crypt(password):
    iterations = 500000
    contents = password.encode("utf-8")
    for i in range(iterations):
        contents = hashlib.sha256(contents).digest()
    return "$shiro1$SHA-256$500000$$" + base64.b64encode(contents).decode('ascii')


def create_super_admin(password):
    logging.info("Creating Omada Super Admin")
    logging.info("Connecting to MongoDB...")
    mdb = omada.db()
    site_ids = []
    logging.info("Gathering omadac_id...")
    omadac_id = mdb.omadac.find_one()["_id"]
    logging.info("Gathering side ids...")
    for site in mdb.site.find():
        site_ids.append(str(site["_id"]))
    logging.info("Inserting User...")
    if omada.version() < (5, 8, 0):
        new_user_id = mdb.user.insert_one({
            "name" : args.username,
            "password" : sha256_crypt(password),
            "omadac_id" : omadac_id,
            "role_type" : 0,
            "verified" : True,
            "permissions" : [ "license", "site", "read", "adopt", "admin", "write", "manage" ],
            "site_ids" : site_ids,
            "alert" : True,
            "all_site" : True,
            "time_created" : int(datetime.utcnow().timestamp()),
            "devices_upgrade_notification" : False,
        }).inserted_id
    else:
        new_tenant_id = mdb.tenant.insert_one({
            "name" : args.username,
            "password" : sha256_crypt(password),
            "omadacs" : [omadac_id],
            "type": 0,
            "created_time" : datetime.fromtimestamp(datetime.utcnow().timestamp(), None),
        }).inserted_id

        new_user_id = mdb.user.insert_one({
            "tenant_id": str(new_tenant_id),
            "name" : args.username,
            "omadac_id" : omadac_id,
            "user_type": 0,
            "role_id" : "master_admin_id",
            "verified" : True,
            "site_ids" : site_ids,
            "favorites": [],
            "alert" : True,
            "all_site" : True,
            "devices_upgrade_notification" : False,
        }).inserted_id

    print("Omada Super Admin created")
    print("Username: " + args.username)
    print("Password: " + password)

if __name__ == "__main__":
    create_super_admin(args.password or password)
