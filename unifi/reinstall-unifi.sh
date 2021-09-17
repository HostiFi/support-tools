#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
path_to_latest_backup=$(find /usr/lib/unifi/data/backup/ -maxdepth 3 -name '*.unf' -type f -printf "%TY-%Tm-%Td %TT %p\n" 2>/dev/null | sort -r | head -1 | awk '{print $3}')
if test -f "$path_to_latest_backup"; then
	echo "Backup to be restored:"
	echo $path_to_latest_backup
	printf "\nBackup date:\n"
	date -r $path_to_latest_backup
	printf "\nBackup size:\n"
	ls -lah $path_to_latest_backup | awk -F " " {'print $5'}
	printf "\n\nAre you sure you want to reinstall UniFi and restore with this backup? [y/n]\n"
else
	printf "\nWarning: No backups were found!"
	printf "\n\nAre you sure you want to reinstall UniFi without a backup? [y/n]\n"
fi
read CHOICE
printf "\nPossible domain names for SSL:\n"
ls /etc/letsencrypt/live
printf "\nEnter a comma separated list of domain names to install a UniFi SSL for:\n"
read DOMAINS
IFS=', ' read -r -a DOMAINLIST <<< "$DOMAINS"
for DOMAIN in "${DOMAINLIST[@]}"
do
  stringprefix=" -d "
  stringpostfix=" "
  DOMAINSTR+=$stringprefix$DOMAIN$stringpostfix
done
printf "\nDo you want to install the latest official version of UniFi? [y/n]\n"
read LATEST_UNIFI_VERSION
if [[ $LATEST_UNIFI_VERSION == "n" || $LATEST_UNIFI_VERSION == "N" ]]; then
	printf "\nEnter the link to the UniFi .deb to install:\n"
	read UNIFI_DEB_LINK
fi
if [[ $CHOICE == "y" || $CHOICE == "Y" ]]; then
	echo "Reinstalling UniFi and restoring from latest backup"
	echo "Restarting the unifi service"
	service unifi stop
	service unifi start
	echo "Trying to run manual-backup.sh"
	parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
	cd "$parent_path"
	/usr/bin/python3 ../lib/unifi/py/manual-backup.py || echo "Error: Manual backup failed!"
	echo "Copying backups to /root/reinstall-unifi"
	rm -rf /root/reinstall-unifi
	mkdir /root/reinstall-unifi
	cp -r /usr/lib/unifi/data/backup /root/reinstall-unifi
	if test -f "$path_to_latest_backup"; then
	    cp $path_to_latest_backup /root/reinstall-unifi/backup/reinstall.unf
	fi
	echo "Copying system.properties to /root/reinstall-unifi"
	cp /usr/lib/unifi/data/system.properties /root/reinstall-unifi/system.properties
	echo "Placing server into Zabbix maintenance mode"
	# This checks if maintenance mode is already enabled (output shows it became disabled),
	# if disabled it runs maintenance-mode.sh again to enable it
	if /bin/bash /root/support-tools/unifi/maintenance-mode.sh | grep 'disabled' 2> /dev/null; then
	    /bin/bash /root/support-tools/unifi/maintenance-mode.sh
	fi
	echo "Purging UniFi"
	apt-get purge unifi -y
	echo "Installing UniFi"
	if [[ $LATEST_UNIFI_VERSION == "n" || $LATEST_UNIFI_VERSION == "N" ]]; then
		printf "\nEnter the link to the UniFi .deb to install:\n"
		wget $UNIFI_DEB_LINK -O /root/reinstall-unifi/unifi.deb
		dpkg -i /root/reinstall-unifi/unifi.deb
	else
		apt-get install unifi -y
	fi
	apt autoremove
	apt-get update -y
	if test -f "/root/reinstall-unifi/backup/reinstall.unf"; then
		echo "Restoring from latest backup"
		/usr/bin/python3 ../lib/unifi/py/restore-backup.py -f "/root/reinstall-unifi/backup/reinstall.unf" -w y || echo "Error: Restoring from backup failed!"
	else
		echo "Killing the wizard"
		/usr/bin/python3 ../lib/unifi/py/restore-backup.py -w y || echo "Error: Killing the wizard failed!"
	fi
	echo "Copying system.properties to new install"
	sed -i 's/is_default=true/is_default=false/g' /root/reinstall-unifi/system.properties
	cp /root/reinstall-unifi/system.properties /usr/lib/unifi/data/system.properties
	echo "Copying backups to new install"
	cp -R /root/reinstall-unifi/backup/* /usr/lib/unifi/data/backup
	echo "Installing SSL"
	parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
	cd "$parent_path"
	/bin/bash ../lib/unifi/ssl/install-ssl.sh $DOMAINSTR -e support@hostifi.com
	echo "Upgrading MongoDB from 3.2.X to 3.6.X"
	bash /root/support-tools/lib/unifi/mongodb/upgrade.sh
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
