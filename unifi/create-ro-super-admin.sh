#!/bin/bash
read -p "Username of UniFi Read-Only Super Admin to create: " USERNAME
read -p "Email address of UniFi Super Admin to create: " EMAIL
cd "$(dirname "${BASH_SOURCE[0]}")"
/usr/bin/python3 ../lib/unifi/py/create-super-admin.py -u "$USERNAME" -e "$EMAIL" --read-only
