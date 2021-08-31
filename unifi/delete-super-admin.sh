#!/bin/bash
echo "Username email address, or partial email address (like @domain.com) of UniFi Super Admin to delete: "
read USERNAME
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
/usr/bin/python3 ../lib/unifi/py/delete-super-admin.py -u $USERNAME