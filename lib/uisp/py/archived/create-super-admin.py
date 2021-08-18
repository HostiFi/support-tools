# For creating Super Admins on UNMS before version 1.2
import os
import bcrypt
import uuid
import argparse
import string
import random
import re
parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='Username of UNMS Super Admin to create')
args = parser.parse_args()
letters = string.ascii_lowercase
password = ''.join(random.choice(letters) for i in range(8))
random_uuid = str(uuid.uuid4())
bcrypt_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
astr = "docker exec -it unms-postgres psql -U unms -c \"INSERT INTO unms.user (id,username,email,password,role) VALUES ('" + random_uuid + "','" + args.username + "','" + args.username + "@hostifi.com','" + bcrypt_hash.decode('utf-8') + "','superadmin');\""
astr = astr.replace('$', '\\$')
print(astr)
os.system(astr)
print("UNMS Super Admin created")
print("Username: " + args.username)
print("Password: " + password)