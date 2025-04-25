#!/bin/bash
apt-get update -y
apt-get install python3 -y
apt-get install python3-pip -y
apt-get install python3-pymongo -y
apt-get install build-essential libssl-dev libffi-dev python3-dev -y
pip3 install bcrypt
pip3 install pyzabbix
pip3 uninstall pymongo bson
