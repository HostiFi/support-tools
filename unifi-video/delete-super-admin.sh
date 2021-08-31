#!/bin/bash
echo "Username of UniFi Video Super Admin to delete: "
read USERNAME
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
/usr/bin/python3 ..lib/unifi-video/py/delete-super-admin.py -u $USERNAME