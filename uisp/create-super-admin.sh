echo "Username of Super Admin to create: "
read USERNAME
apt-get install python3-pip -y
pip3 install bcrypt
/usr/bin/python3 ../lib/uisp/py/create-super-admin.py -u $USERNAME