#!/bin/bash
echo "Username email address, or partial email address (like @domain.com) of UniFi Super Admin to delete: "
read USERNAME
/usr/bin/python3 /root/support-tools/lib/unifi/py/delete-super-admin.py -u $USERNAME