#!/bin/bash
echo $HOSTNAME
IFS='.' read -r SERVER string <<< "$HOSTNAME"
a=".hostifi.com"
SERVER+=$a
/usr/bin/python3 ../lib/zabbix/maintenance-mode.py -s $SERVER