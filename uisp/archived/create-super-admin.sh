#!/bin/bash
echo "Username of UNMS Super Admin to create: "
read USERNAME
/usr/bin/python3 ../../lib/uisp/py/archived/create-super-admin.py -u $USERNAME