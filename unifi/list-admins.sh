#!/bin/bash
mongo --port 27117 ace --eval "db.admin.find().forEach(printjson);"