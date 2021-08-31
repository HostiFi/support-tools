#!/bin/bash
echo "Username of UNMS (before version 1.2) Super Admin to create: "
read USERNAME
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
/usr/bin/python3 ../lib/uisp/py/archived/create-super-admin.py -u $USERNAME