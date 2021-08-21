#!/bin/bash
echo "Username of UISP Super Admin to delete: "
read USERNAME
docker exec unms-postgres psql -U unms -c "delete from nms_user_view where username='$USERNAME';"
echo "Deleted UISP Super Admin for $USERNAME"