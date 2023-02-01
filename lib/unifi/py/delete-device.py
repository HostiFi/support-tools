import pymongo
import argparse
import json

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

r = mdb.device.delete_one({"mac": mac})

if r.deleted_count == 1:
    print("Device deleted")
elif r.deleted_count == 0:
    print("Device not found")
else:
    print("Unknown error occurred")