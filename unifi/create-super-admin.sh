echo "Username of UniFi Super Admin to create: "
read USERNAME
echo "Email address of UniFi Super Admin to create: "
read EMAIL
apt-get install python3-pip -y
pip3 install bcrypt
/usr/bin/python3 ../lib/unifi/py/create-super-admin.py -u $USERNAME -e $EMAIL