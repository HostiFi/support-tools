#!/bin/bash
mongo --port 27217 omada --eval "db.user.find().forEach(printjson);"