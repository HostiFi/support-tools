#!/bin/bash
echo "Domain name to redirect 80, 443 to 8443 for: "
read DOMAIN
/usr/bin/python3 /root/support-tools/lib/unifi/py/redirect.py -d $DOMAIN