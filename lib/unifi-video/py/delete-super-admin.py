import json
import random
import string
import time
from random import SystemRandom
from datetime import datetime
import argparse
import pymongo
from bson.objectid import ObjectId

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='UniFi Video username to delete')
args = parser.parse_args()

client = pymongo.MongoClient("mongodb://127.0.0.1:7441/av")
mdb = client.av

class Server():
    def __init__(self, server_name):
        self.server_name = server_name

    def _delete_user(self, account_id):
        print("Deleting user for")
        print(account_id)
        response = ''
        print(self.server_name)
        response = mdb.user.remove({'accountId': ObjectId(account_id)})
        print("Response:")
        print(response)
        return response

    def _delete_account(self, username):
        print("Deleting account for")
        print(username)
        response = ''
        print(self.server_name)
        response = mdb.account.remove({'username': username})
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

    def delete_super_admin(self, username):
        account_id = self._get_account_id(username)
        self._delete_account(username)
        self._delete_user(account_id)

if args.username is not None:
    unifi_video_server = Server('localhost')
    unifi_video_server.delete_super_admin(args.username)
    print("Deleted the account for username: ")
    print(args.username)

else:
    print "Error: Missing arguments. --username is required."