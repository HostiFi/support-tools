#!/bin/bash
echo "Username of UISP Super Admin to create: "
read USERNAME
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
/usr/bin/python3 ../lib/uisp/py/create-super-admin.py -u $USERNAME