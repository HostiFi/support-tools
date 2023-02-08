import bson
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', help='db file name with path')
args = parser.parse_args()

collection = ""

with open(args.file, "rb") as file_in, open(args.file + "_new", "wb") as file_out:
    for doc in bson.decode_file_iter(file_in):
        if "__cmd" in doc:
            if doc["__cmd"] != "select":
                raise RuntimeError(f"Unknown command: " + doc["__cmd"])
            collection = doc["collection"]
        elif collection in ("event", "alarm", "rogue", "voucher", "guest"):
            continue
        elif collection == "user" and not any(key in doc for key in ("use_fixedip", "blocked", "noted")):
            continue
        file_out.write(bson.encode(doc))