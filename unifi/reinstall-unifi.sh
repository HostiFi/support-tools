#!/bin/bash
echo "Still in development, use the Notion guide for now! -rchase"
#exit
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
if find /usr/lib/unifi/data/backup/ -maxdepth 3 -name '*.unf' -type f -printf "%TY-%Tm-%Td %TT %p\n" | sort -r | head -1 | awk '{print $3}'; then
	path_to_latest_backup=$(find /usr/lib/unifi/data/backup/ -maxdepth 3 -name '*.unf' -type f -printf "%TY-%Tm-%Td %TT %p\n" | sort -r | head -1 | awk '{print $3}')
	echo "Backup to be restored:"
	echo $path_to_latest_backup
	echo "Backup date:"
	date -r $path_to_latest_backup
else
	echo "No backups were found!"
fi
echo "Are you sure you want to reinstall UniFi? [y/n]"
read CHOICE
if [[ $CHOICE == "y" || $CHOICE == "Y" ]]; then
	echo "Reinstalling UniFi and restoring from latest backup"
	echo "Restarting the unifi service"
	service unifi stop
	service unifi start
	echo "Trying to run manual-backup.sh"
	parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
	cd "$parent_path"
	/usr/bin/python3 ../lib/unifi/py/manual-backup.py || echo "Error: Manual backup failed!"
	echo "Copying backups to /tmp/reinstall"
	rm -rf /tmp/reinstall-unifi
	mkdir /tmp/reinstall-unifi
	cp -r /usr/lib/unifi/data/backup /tmp/reinstall-unifi
	echo "Copying system.properties to /tmp/reinstall"
	cp /usr/lib/unifi/data/system.properties /tmp/reinstall-unifi/system.properties
	echo "Placing server into Zabbix maintenance mode"
	# This checks if maintenance mode is already enabled (output shows it became disabled),
	# if disabled it runs maintenance-mode.sh again to enable it
	if /bin/bash /root/support-tools/unifi/maintenance-mode.sh | grep 'disabled' > /dev/null; then
	    /bin/bash /root/support-tools/unifi/maintenance-mode.sh
	fi
	echo "Purging UniFi"
	apt-get purge unifi -y
	echo "Installing UniFi"
	apt-get install unifi -y
	apt autoremove
	echo "Restoring from latest backup"
	/usr/bin/python3 ../lib/unifi/py/restore-backup.py -f $path_to_latest_backup -w y || echo "Error: restoring from backup failed!"
	echo "Copying system.properties to new install"
	cp /tmp/reinstall-unifi/system.properties /usr/lib/unifi/data/system.properties
	echo "Installing SSL"
	ssl_name=$(find /etc/letsencrypt/live -mindepth 1 -type d -printf "%TY-%Tm-%Td %TT %f\n" | sort -r | head -1 | awk '{print $3}')
	cd "$parent_path"
	/bin/bash ../lib/unifi/ssl/install-ssl.sh -d $ssl_name -e "support@hostifi.com" || echo "Error: SSL install failed!"
	echo "SSL installed for: $ssl_name"
	echo "Removing server from Zabbix maintenance mode"
	# This checks if maintenance mode is already disabled (output shows it became enabled),
	# if enabled it runs maintenance-mode.sh again to disable it
	if /bin/bash /root/support-tools/unifi/maintenance-mode.sh | grep 'enabled' > /dev/null; then
	    /bin/bash /root/support-tools/unifi/maintenance-mode.sh
	fi
	echo "Done!"
else
	echo "Aborted"
  exit
fi
