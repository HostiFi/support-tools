#!/bin/bash
echo "Username of UniFi Super Admin to create: "
read USERNAME
echo "Email address of UniFi Super Admin to create: "
read EMAIL
/usr/bin/python3 /root/support-tools/lib/unifi-video/py/create-super-admin.py -u $USERNAME -e $EMAIL