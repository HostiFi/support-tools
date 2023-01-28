#!/bin/bash
echo "Username, email address, or partial email address (like @domain.com) of Omada Super Admin to delete: "
read USERNAME
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
/usr/bin/python3 ../lib/omada/py/delete-super-admin.py -u $USERNAME