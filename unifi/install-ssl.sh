# WIP
echo "Enter a comma separated list of domain names to install a UniFi SSL for: "
read DOMAINS
/bin/bash ../lib/unifi/ssl/install-ssl.sh -d $DOMAINS