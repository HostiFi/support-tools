from unifi import UniFi
import os
import datetime
import time
import requests
import json
import subprocess
import re
import random
import socket
import string
import warnings

dir_path = os.path.dirname(os.path.abspath(__file__))

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

r = socket.gethostname()
hostname = r.split('.')[0] + ".hostifi.com"

username_postfix = ''.join(random.choice(string.ascii_letters) for i in range(4))

def human_readable(bytes, units=[' bytes','KB','MB','GB','TB', 'PB', 'EB']):
    return str(bytes) + units[0] if bytes < 1024 else human_readable(bytes>>10, units[1:])

def get_unifi_version(server):
    s = requests.Session()
    r = s.get('https://' + server + ':8443/status', verify=False)
    r2 = json.loads(r.text)
    return r2['meta']['server_version']

user = "tempbackupscript" + username_postfix
r = None
try:
    r = subprocess.check_output(["/usr/bin/python3", os.path.join(dir_path, 'create-super-admin.py'), "-u", user, "-e", "support@hostifi.com"])
except subprocess.CalledProcessError as e:
    r = e.r
try:
    password = re.findall("Password: (.+)\n", r.decode('ascii'))[0]
    unifi_server = UniFi(hostname, user, password)
    unifi_server.login()
    unifi_version = get_unifi_version(hostname)
    r = unifi_server.create_manual_backup()
    backup_dl_link = "https://" + hostname + ":8443" + r
    today = datetime.date.today()
    path_to_backup = "/usr/lib/unifi/data/backup/manual_" + unifi_version + "_" + today.strftime("%Y%m%d") + "_" + str(int(time.time())) + ".unf"
    unifi_server.download_backup(path_to_backup, backup_dl_link)
    unifi_server.logout()
    os.system("/usr/bin/python3 " + dir_path + "/delete-super-admin.py -u " + user)
    backup_size_in_bytes = os.stat(path_to_backup).st_size
    print("Manual backup stored at: " + path_to_backup)
    print("Backup size: " + human_readable(backup_size_in_bytes))
except:
    # Delete the admin account if anything fails
    print("Error: backup failed!")
    os.system("/usr/bin/python3 " + dir_path + "/delete-super-admin.py -u " + user)