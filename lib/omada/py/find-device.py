import pymongo
import argparse
import json
from bson import ObjectId

parser = argparse.ArgumentParser()
parser.add_argument('-m','--mac', help='UniFi device MAC address to delete')
args = parser.parse_args()

client = pymongo.MongoClient("mongodb://127.0.0.1:27217/omada")
mdb = client.omada
mac = ""
if len(args.mac) != 12 and len(args.mac) != 17:
    print("Invalid MAC address. Length must be either 12 or 17 characters.")
    exit()
elif "-" in args.mac:
    mac = args.mac
elif ":" in args.mac:
    mac = args.mac.replace(":", "-")
else:
    mac += args.mac[0] + args.mac[1] + "-"
    mac += args.mac[2] + args.mac[3] + "-"
    mac += args.mac[4] + args.mac[5] + "-"
    mac += args.mac[6] + args.mac[7] + "-"
    mac += args.mac[8] + args.mac[9] + "-"
    mac += args.mac[10] + args.mac[11]

device = mdb.device.find_one({"mac": mac}, {"_id": 0, "ip": 1, "mac": 1, "model": 1, "version": 1, "site_id": 1})
if device is None:
    print("Device not found")
    exit()

device_site_id = ""
if device["site_id"] == "Default"
    device_site_id = "Default"
else:
    device_site_id = ObjectId(device["site_id"])

site_info = mdb.site.find_one({"_id": device_site_id}, {"_id": 0, "desc":1, "name":1})

print("MAC: " + device["mac"])
print("IP: " + device["ip"])
print("Model: " + device["model"])
print("Version: " + str(device["version"]))
print("Site Name: " + site_info["name"])