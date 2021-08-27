#!/bin/bash
# Parse domains to an array
while getopts e:d: option; do
  case $option in
    "d") DOMAINS+=("$OPTARG");;
    "e") EMAIL=${OPTARG};;
  esac
done

for DOMAIN in "${DOMAINS[@]}"; do
  stringprefix=" -d "
  stringpostfix=" "
  DOMAINSTR+=$stringprefix$DOMAIN$stringpostfix
done

apt-get autoremove -y
modprobe ip_tables
echo 'ip_tables' >> /etc/modules

echo "Removing Apache2"
apt-get remove apache2 -y

echo "Installing NGINX"
apt-get install nginx-light -y

echo "Installing Let's Encrypt"
apt-get update -y
apt-get install python-certbot-nginx -t stretch-backports -y

echo "Getting cert"
certbot --nginx --email $EMAIL --agree-tos --no-eff-email --expand $DOMAINSTR --no-redirect --quiet --force-renewal

echo "Importing cert to UniFi"
/bin/bash /root/support-tools/lib/unifi/ssl/import-ssl.sh -d ${DOMAINS[0]}

echo "Creating certbot cron"
crontab -l > /root/certbotcron
echo "0 22 * * * /usr/bin/certbot renew" >> /root/certbotcron
crontab /root/certbotcron
rm /root/certbotcron

echo "Creating Let's Encrypt cron"
crontab -l > /root/letsencryptcron
echo "0 23 * * * /bin/bash /root/support-tools/lib/ssl/import-ssl.sh -d ${DOMAINS[0]}" >> /root/letsencryptcron
crontab /root/letsencryptcron
rm /root/letsencryptcron

echo "Removing old SSL script"
rm /root/unifi-ssl.sh

echo "Restarting services"
systemctl restart nginx
systemctl restart unifi

echo "Done!"