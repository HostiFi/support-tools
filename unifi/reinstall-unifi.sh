#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
path_to_latest_backup=$(find /usr/lib/unifi/data/backup/ -maxdepth 3 -name '*.unf' -type f -printf "%TY-%Tm-%Td %TT %p\n" 2>/dev/null | sort -r | head -1 | awk '{print $3}')
if test -f "$path_to_latest_backup"; then
	echo "Backup to be restored:"
	echo $path_to_latest_backup
	printf "\nBackup date:"
	date -r $path_to_latest_backup
	printf "\n\nAre you sure you want to reinstall UniFi and restore with this backup? [y/n]"
else
	printf "\nWarning: No backups were found!"
	printf "\n\nAre you sure you want to reinstall UniFi without a backup? [y/n]"
fi
read CHOICE
echo "\nPossible domain names for SSL:"
ls /etc/letsencrypt/live
echo "\n\nEnter a comma separated list of domain names to install a UniFi SSL for:"
read DOMAINS
IFS=', ' read -r -a DOMAINLIST <<< "$DOMAINS"
for DOMAIN in "${DOMAINLIST[@]}"
do
  stringprefix=" -d "
  stringpostfix=" "
  DOMAINSTR+=$stringprefix$DOMAIN$stringpostfix
done
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
	if /bin/bash /root/support-tools/unifi/maintenance-mode.sh | grep 'disabled' 2> /dev/null; then
	    /bin/bash /root/support-tools/unifi/maintenance-mode.sh
	fi
	echo "Purging UniFi"
	apt-get purge unifi -y
	echo "Installing UniFi"
	apt-get install unifi -y
	apt autoremove
	echo "Restoring from latest backup"
	/usr/bin/python3 ../lib/unifi/py/restore-backup.py -f $path_to_latest_backup -w y || echo "Error: Restoring from backup failed!"
	echo "Copying system.properties to new install"
	cp /tmp/reinstall-unifi/system.properties /usr/lib/unifi/data/system.properties
	echo "Installing SSL"
	parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
	cd "$parent_path"
	/bin/bash ../lib/unifi/ssl/install-ssl.sh $DOMAINSTR -e support@hostifi.com
	echo "Removing server from Zabbix maintenance mode"
	# This checks if maintenance mode is already disabled (output shows it became enabled),
	# if enabled it runs maintenance-mode.sh again to disable it
	if /bin/bash /root/support-tools/unifi/maintenance-mode.sh | grep 'enabled' 2> /dev/null; then
	    /bin/bash /root/support-tools/unifi/maintenance-mode.sh
	fi
	echo "Done!"
else
	echo "Aborted"
  exit
fi
