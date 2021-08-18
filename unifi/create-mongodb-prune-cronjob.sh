crontab -l | { cat; echo "0 * * * * /usr/bin/mongo --port 27117 < /root/support-tools/lib/unifi/mongodb/prune.js"; } | crontab -
echo "This server will now prune all UniFi statistics every minute"