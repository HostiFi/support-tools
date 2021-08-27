#!/bin/bash
echo "Enter a comma separated list of domain names to install a UniFi SSL for: "
read DOMAINS
IFS=', ' read -r -a DOMAINLIST <<< "$DOMAINS"
for DOMAIN in "${DOMAINLIST[@]}"
do
  stringprefix=" -d "
  stringpostfix=" "
  DOMAINSTR+=$stringprefix$DOMAIN$stringpostfix
done

/bin/bash /root/support-tools/lib/unifi/ssl/install-ssl.sh $DOMAINSTR -e support@hostifi.com