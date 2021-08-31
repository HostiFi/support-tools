#!/bin/bash
echo "Domain name to redirect 80, 443 to 8443 for: "
read DOMAIN
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
/usr/bin/python3 ../lib/unifi/py/redirect.py -d $DOMAIN