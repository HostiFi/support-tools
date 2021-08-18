import json
import random
import string
import time
from random import SystemRandom
from datetime import datetime
import argparse
import pymongo
from bson.objectid import ObjectId
import bcrypt
import bson

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='UniFi Video username to create')
parser.add_argument('-e','--email', help='UniFi Video username to create')
args = parser.parse_args()

randchoice = SystemRandom().choice
client = pymongo.MongoClient("mongodb://127.0.0.1:7441/av")
mdb = client.av

class Server():
    def __init__(self, server_name):
        self.server_name = server_name

    def _get_random_api_key(self, size=32, chars=string.ascii_uppercase + string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def _get_random_adoption_key(self, size=8, chars=string.ascii_uppercase + string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def _get_random_reset_key(self, size=32, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_random_password(self, size=8, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def _create_user(self, account_id, super_admin_id):
        print("Deleting user for")
        print(account_id)
        response = ''
        print(self.server_name)
        response = mdb.user.insert({'accountId': ObjectId(account_id), 'userGroupId': ObjectId(super_admin_id), "disabled" : False, "apiKey" : self.get_random_api_key(), "enableApiAccess" : True, "enableLocalAccess" : True, "motionAlertSchedules" : { }, "subscribedMotion" : [ ], "subscribedCameraConnection" : [ ], "adoptionKey" : self.get_random_adoption_key(), "enableEmail" : True, "enablePush" : True, "sysDisconnectEmailAlert" : True, "sysDisconnectPushAlert" : True })
        print("Response:")
        print(response)
        return response

    def _create_account(self, username, email, hashed):
        print("Creating account for")
        print(username)
        response = ''
        print(self.server_name)
        response = mdb.account.insert({'email': email, 'username': username, 'password': hashed, 'name': username, 'language': 'English', "resetKey" : self.get_random_reset_key(), "lastIp" : "192.247.121.76", "lastLogInTimestamp" : bson.int64.Int64(100)})
        print("Response:")
        print(response)
        return response

    def _get_account_id(self, username):
        print("Getting account id for")
        print(username)
        response = ''
        print(self.server_name)
        response = mdb.account.find({'username': username})
        print("Account id:")
        print(response[0]["_id"])
        return response[0]["_id"]

    def _get_super_admin_user_group_id(self):
        print("Getting Super Admin id")
        response = ''
        print(self.server_name)
        response = mdb.usergroup.find({'groupType': "SUPER_ADMIN"}, {"_id"})
        print("Super Admin id:")
        print(response[0]["_id"])
        return response[0]["_id"]

    def create_super_admin(self, username, email):
        password = self.get_random_password()
        salt = bcrypt.gensalt(prefix=b"2a")
        hashed = bcrypt.hashpw(password, salt)
        super_admin_id = self._get_super_admin_user_group_id()
        self._create_account(username, email, hashed)
        account_id = self._get_account_id(username)
        self._create_user(account_id, super_admin_id)
        print("UniFi Video Super Admin created")
        print("Username: " + args.username)
        print("Password: " + password)

if args.email is not None and args.password is not None and args.username is not None:
    unifi_video_server = Server('localhost')
    unifi_video_server.create_super_admin(args.username, args.email)
else:
    print "Error: Missing arguments. --username, and --email are required."