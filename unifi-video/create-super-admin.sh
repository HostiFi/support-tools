#!/bin/bash
echo "Username of UniFi Super Admin to create: "
read USERNAME
echo "Email address of UniFi Super Admin to create: "
read EMAIL
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
/usr/bin/python3 ../lib/unifi-video/py/create-super-admin.py -u $USERNAME -e $EMAIL