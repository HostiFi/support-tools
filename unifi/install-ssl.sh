#!/bin/bash
printf "Possible domain names for SSL:\n"
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
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
/bin/bash ../lib/unifi/ssl/install-ssl.sh $DOMAINSTR -e support@hostifi.com