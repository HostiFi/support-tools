#!/usr/bin/python3

import pymongo
import argparse
import json
from bson import ObjectId

parser = argparse.ArgumentParser()
parser.add_argument('-m','--mac', help='UniFi device MAC address to delete')
args = parser.parse_args()

client = pymongo.MongoClient("mongodb://127.0.0.1:27117/ace")
mdb = client.ace
mac = ""
if len(args.mac) != 12 and len(args.mac) != 17:
    print("Invalid MAC address. Length must be either 12 or 17 characters.")
    exit()
elif ":" in args.mac:
    mac = args.mac
elif "-" in args.mac:
    mac = args.mac.replace("-", ":")
else:
    mac += args.mac[0] + args.mac[1] + ":"
    mac += args.mac[2] + args.mac[3] + ":"
    mac += args.mac[4] + args.mac[5] + ":"
    mac += args.mac[6] + args.mac[7] + ":"
    mac += args.mac[8] + args.mac[9] + ":"
    mac += args.mac[10] + args.mac[11]

device = mdb.device.find_one({"mac": mac}, {"_id": 0, "ip": 1, "mac": 1, "model": 1, "model_in_lts": 1, "model_in_eol": 1, "version": 1, "adopted": 1, "inform_url": 1, "inform_ip": 1, "site_id": 1})
if device is None:
    print("Device not found")
    exit()
site_info = mdb.site.find_one({"_id": ObjectId(device["site_id"])}, {"_id": 0, "desc":1, "name":1})

link = ""
try:
    protocol, rest = device["inform_url"].split("://")
    hostname_port = rest.split(":")
    hostname = hostname_port[0]
    link = "https://" + hostname + ":8443/manage/" + site_info["name"] + "/devices"
except:
    link = "Unknown"
print("MAC: " + device.get("mac"))
print("IP: " + device.get("ip"))
print("Model: " + device.get("model"))
print("LTS: " + str(device.get("model_in_lts")))
print("EOL: " + str(device.get("model_in_eol")))
print("Version: " + str(device.get("version")))
print("Inform URL: " + device.get("inform_url"))
print("Inform IP: " + device.get("inform_ip"))
print("Site Name: " + site_info["desc"])
print("Site Code: " + site_info["name"])
print("Link: " + link)
