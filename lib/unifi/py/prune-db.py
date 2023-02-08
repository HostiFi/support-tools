import bson
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', help='db file name with path')
args = parser.parse_args()

docs = []
encoded_docs = []
current_collection = ""

with open(args.file, 'rb') as f:
    for doc in bson.decode_file_iter(f):
        docs.append(doc)

for doc in docs:
    if 'collection' in doc:
        current_collection = doc['collection']
        encoded_doc = bson.encode(doc)
        encoded_docs.append(encoded_doc)
        continue
    if current_collection == "event":
        continue
    if current_collection == "alarm":
        continue
    if current_collection == "rogue":
        continue
    if current_collection == "voucher":
        continue
    if current_collection == "guest":
        continue
    if current_collection == "user":
        if 'use_fixedip' in doc or 'blocked' in doc or 'noted' in doc:
            encoded_doc = bson.encode(doc)
            encoded_docs.append(encoded_doc)
            continue
        else:
            continue
    encoded_doc = bson.encode(doc)
    encoded_docs.append(encoded_doc)

with open(args.file + "_new", 'wb') as f:
    for doc in encoded_docs:
        f.write(doc)
