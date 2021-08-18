echo "Username email address, or partial email address (like @domain.com) of UniFi Super Admin to delete: "
read USERNAME
/usr/bin/python3 ../lib/unifi/py/delete-super-admin.py -u $USERNAME