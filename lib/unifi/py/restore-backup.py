import argparse
import random
import os
import socket
from unifi import UniFi

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', help='Path to backup file to be restored')
args = parser.parse_args()

dir_path = os.path.dirname(os.path.abspath(__file__))

password = ''.join(random.choice(string.ascii_letters) for i in range(8))
user = "temprestorescript" + ''.join(random.choice(string.ascii_letters) for i in range(4))

print("Restoring UniFi from " + str(args.file))
print("Creating super admin...")
os.system("/usr/bin/python3 " + dir_path + "/create-super-admin.py -u " + user + " -p " + password + " -e support@hostifi.com")
r = socket.gethostname()
hostname = r.split('.')[0] + ".hostifi.com"
unifi_server = UniFi(hostname, user, password)
unifi_server.login()
unifi_server.restore_backup(args.file)
unifi_server.logout()
os.system("/usr/bin/python3 " + dir_path + "/delete-super-admin.py -u " + user)