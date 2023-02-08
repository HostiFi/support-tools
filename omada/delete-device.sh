#!/bin/bash
read -p "MAC of device to delete: " MAC
cd "$(dirname "${BASH_SOURCE[0]}")"
/usr/bin/python3 ../lib/omada/py/delete-device.py -m "$MAC"
