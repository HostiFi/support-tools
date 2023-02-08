#!/bin/bash
echo "MAC of device to find: "
read MAC
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
/usr/bin/python3 ../lib/omada/py/find-device.py -m $MAC