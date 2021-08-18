echo "Username of UISP Super Admin to delete: "
read USERNAME
docker exec -it unms-postgres psql -U unms
delete from nms_user_view where username='$USERNAME';
\q
echo "Deleted UISP Super Admin for $USERNAME"