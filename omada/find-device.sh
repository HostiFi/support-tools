#!/bin/bash
read -p "MAC of device to find: " MAC
cd "$(dirname "${BASH_SOURCE[0]}")"
/usr/bin/python3 ../lib/omada/py/find-device.py -m "$MAC"
