#!/bin/bash
set -euo pipefail

mkdir -p /etc/systemd/system
cat > /etc/systemd/system/unifi-prune-mongodb.service <<'EOF'
[Unit]
Description=Prune statistics from the UniFi database
Requires=unifi.service
After=unifi.service

[Service]
Type=oneshot
ExecStart=/bin/bash /root/support-tools/unifi/prune-mongodb.sh
EOF

cat > /etc/systemd/system/unifi-prune-mongodb.timer <<'EOF'
[Unit]
Description=Prune UniFi statistics every hour

[Timer]
OnCalendar=hourly

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable --now unifi-prune-mongodb.timer

echo "This server will now prune all UniFi statistics every hour"
