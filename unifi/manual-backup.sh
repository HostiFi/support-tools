#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
/usr/bin/python3 ../lib/unifi/py/manual-backup.py