#!/bin/sh

ip link set wlan0 up

killall wpa_supplicant 2>/dev/null
rm -rf /var/run/wpa_supplicant

wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant.conf

sleep 5

udhcpc -i wlan0 &