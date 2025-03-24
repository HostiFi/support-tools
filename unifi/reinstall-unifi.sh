#!/bin/bash
systemctl stop unifi && rm -rf /var/lib/unifi/* && reboot
