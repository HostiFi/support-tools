#!/bin/bash
apt-get update -y
apt-get install python3 -y
apt-get install python3-pip -y
apt-get install build-essential libssl-dev libffi-dev python-dev -y
apt-get install python3-pyasn1 -y
apt-get install python3-setuptools -y
pip3 install pymongo==3.5.1
pip3 install bcrypt
pip3 install pyzabbix

