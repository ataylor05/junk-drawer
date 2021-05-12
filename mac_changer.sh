#!/bin/bash
# add to cron
# @reboot /root/Documents/macchanger.sh
macchanger -r eth0 > /tmp/macs
macchanger -r wlan0 >> /tmp/macs
