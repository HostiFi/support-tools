#!/bin/bash
mongo omada --eval "db.device.count();" --port 27217 --quiet