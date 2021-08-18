import os
import bcrypt
import uuid
import argparse
import string
import random
import re
parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='UISP username of Super Admin to create')
args = parser.parse_args()
letters = string.ascii_lowercase
password = ''.join(random.choice(letters) for i in range(8))
random_uuid = str(uuid.uuid4())
bcrypt_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
site_group_id= os.popen('docker exec -it unms-postgres psql -U unms -d unms -t -c "SELECT group_id FROM access_group_site LIMIT 1;"').read()
astr = "docker exec -it unms-postgres psql -U unms -c \"INSERT INTO unms.user (id,username,email,password,role,site_group_id) VALUES ('" + random_uuid + "','" + args.username + "','" + args.username + "@hostifi.com','" + bcrypt_hash.decode('utf-8') + "','superadmin', '" + str(site_group_id).strip() + "');\""
astr = astr.replace('$', '\\$')
print(astr)
os.system(astr)
print("UISP Super Admin created")
print("Username: " + args.username)
print("Password: " + password)