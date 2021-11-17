import os
import bcrypt
import uuid
import argparse
import string
import random
import re

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='Username of UISP Super Admin to create')
parser.add_argument('-p', '--password', help='UISP password to create')
parser.add_argument('-s', '--site-group-id', help='Site group ID (optional)')
parser.add_argument('-e', '--email', help='UISP email to create')

args = parser.parse_args()
letters = string.ascii_lowercase
if not args.password:
	password = ''.join(random.choice(letters) for i in range(8))
else:
	password = args.password
if not args.email:
	email = args.username + "@hostifi.com"
else:
	email = args.email
random_uuid = str(uuid.uuid4())
bcrypt_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
site_group_id = os.popen('docker exec -t unms-postgres psql -U unms -d unms -t -c "SELECT group_id FROM access_group_site LIMIT 1;"').read()
astr = "docker exec -t unms-postgres psql -U unms -c \"INSERT INTO unms.user (id,username,email,password,role,site_group_id) VALUES ('" + random_uuid + "','" + args.username + "','" + email + "','" + bcrypt_hash.decode('utf-8') + "','superadmin', '" + str(site_group_id).strip() + "');\""
astr = astr.replace('$', '\\$')
print(astr)
r = os.popen(astr).read()
print("UISP Super Admin created")
print("Username: " + args.username)
print("Password: " + password)