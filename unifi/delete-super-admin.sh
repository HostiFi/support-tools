echo "Username or email address of UniFi Super Admin to delete: "
read USERNAME
apt-get install python3-pip -y
pip3 install pymongo
/usr/bin/python3 ../lib/unifi/py/delete-super-admin.py -u $USERNAME