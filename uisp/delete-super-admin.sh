docker exec -it unms-postgres psql -U unms
delete from nms_user_view where username='sshaikh';
\q
echo "Deleted sshaikhSuper Admin"