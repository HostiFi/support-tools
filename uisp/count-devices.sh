#!/bin/bash
docker exec unms-postgres psql -U unms -c "SELECT count(*) AS value FROM device WHERE device.authorized IS TRUE AND device.type <> 'blackBox';" -t -X -A