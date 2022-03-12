import pymongo
import json

client = pymongo.MongoClient("mongodb://127.0.0.1:27117/ace")
mdb = client.ace
sites = mdb.site.find()
site_ids = []
for site in sites:
    site_id = str(site["_id"])
    if mdb.device.count({"site_id":site_id}) > 0:
    	site_ids.append(site_id)

SITES_COUNT = len(site_ids)

# UGW3     ugw  USG-3P
UGW3_COUNT = mdb.device.count({"model":'UGW3'})
# UGW4     ugw  USG-Pro-4
UGW4_COUNT = mdb.device.count({"model":'UGW4'})
# UGWHD4   ugw  USG
UGWHD4_COUNT = mdb.device.count({"model":'UGWHD4'})
# UGWXG    ugw  USG-XG-8
UGWXG_COUNT = mdb.device.count({"model":'UGWXG'})
# UXGPRO   uxg  UniFi NeXt-Gen Gateway PRO
UXGPRO_COUNT = mdb.device.count({"model":'UXGPRO'})

# Sites with gt 0 devices
OUTPUT_OBJ = {'site': SITES_COUNT, 'ugw3': UGW3_COUNT, 'ugw4': UGW4_COUNT, 'ugwhd4': UGWHD4_COUNT, 'ugwxg': UGWXG_COUNT, 'uxgpro': UXGPRO_COUNT}
OUTPUT_JSON = json.dumps(OUTPUT_OBJ)
print(OUTPUT_JSON)