#!/bin/bash
echo "Username of UISP Super Admin to create: "
read USERNAME
/usr/bin/python3 /root/support-tools/lib/uisp/py/create-super-admin.py -u $USERNAME