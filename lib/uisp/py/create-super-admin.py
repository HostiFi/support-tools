import subprocess
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

def psql(command, **variables):
    return subprocess.run(
        [
            "docker", "exec", "--interactive", "unms-postgres",
            "psql", "--username=unms", "--dbname=unms", "--no-align", "--tuples-only",
            *("--variable={}={}".format(key, value) for key, value in variables.items()),
        ],
        input=command.encode("utf-8"),
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8").splitlines()

site_group_id = psql("SELECT group_id FROM access_group_site LIMIT 1;")[0]
psql(
    "INSERT INTO unms.user(" +
    "    id, username, email, password, role, site_group_id" +
    ") VALUES (" +
    "    :'random_uuid', :'username', :'email', :'password_hash', 'superadmin', :'site_group_id'" +
    ")",
    random_uuid=random_uuid,
    username=args.username,
    email=email,
    password_hash=bcrypt_hash.decode("utf-8"),
    site_group_id=site_group_id,
)

print("UISP Super Admin created")
print("Username: " + args.username)
print("Password: " + password)
