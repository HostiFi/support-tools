#!/bin/bash
apt-get update -y
apt-get install python3 -y
apt-get install python3-pip -y
apt-get install build-essential libssl-dev libffi-dev python-dev -y
pip3 install pyasn1
pip3 install pymongo
pip3 install bcrypt
pip3 install pyzabbix
