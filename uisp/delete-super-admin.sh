#!/bin/bash
echo "Username of UISP Super Admin to delete: "
read USERNAME
docker exec --interactive unms-postgres \
       psql --username=unms --dbname=unms --variable=username="$USERNAME" \
       <<<"DELETE FROM nms_user_view WHERE username = :'username'"
echo "Deleted UISP Super Admin for $USERNAME"
