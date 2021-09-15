import argparse
import random
import os
import socket
from unifi import UniFi
import string
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument('-f','--file', help='Path to backup file to be restored')
parser.add_argument('-w','--wizard', help='Kill the wizard [y/n]')
args = parser.parse_args()

try:
    dir_path = os.path.dirname(os.path.abspath(__file__))
    password = ''.join(random.choice(string.ascii_letters) for i in range(8))
    user = "temprestorescript" + ''.join(random.choice(string.ascii_letters) for i in range(4))
    email = user + "@hostifi.com"
    r = socket.gethostname()
    hostname = r.split('.')[0] + ".hostifi.com"
    if args.wizard == "y":
        unifi_server = UniFi(hostname, user, password)
        unifi_server.complete_unifi_wizard(email)
        unifi_server.login()
    else:
        print("Creating super admin...")
        os.system("/usr/bin/python3 " + dir_path + "/create-super-admin.py -u " + user + " -p " + password + " -e support@hostifi.com")
        unifi_server = UniFi(hostname, user, password)
        unifi_server.login()
    if args.file is not None:
        print("Restoring UniFi from " + str(args.file))
        unifi_server.restore_backup(args.file)
    unifi_server.logout()
    os.system("/usr/bin/python3 " + dir_path + "/delete-super-admin.py -u " + user)
except Exception as e:
    logging.info(e)
    print("Error: restore failed!")
    os.system("/usr/bin/python3 " + dir_path + "/delete-super-admin.py -u " + user)