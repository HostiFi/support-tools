#!/bin/bash
echo "Username of UniFi Video Super Admin to delete: "
read USERNAME
/usr/bin/python3 ../lib/unifi-video/py/delete-super-admin.py -u $USERNAME