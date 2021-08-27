#!/bin/bash
echo "Username of UniFi Video Super Admin to delete: "
read USERNAME
/usr/bin/python3 /root/support-tools/lib/unifi-video/py/delete-super-admin.py -u $USERNAME