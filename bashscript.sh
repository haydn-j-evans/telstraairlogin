#!/bin/bash
while true; do

# Configuration
username="USERNAME@wifi.telstra.com"
password="PASSWORD"
wifiadapter="wlan0"
wifiap="Telstra Air"
looptime="300" # in seconds, eg 300 = 5 minutes

# Check if already connected to internet
echo "Checking connection state..."
check=$(curl -s --max-time 10 "http://captive.apple.com/hotspot-detect.html" | grep -q "Success" && echo "Success" || echo "Fail")
if $(echo "$check" | grep -q "Success"); then
echo "Already connected to the internet"
else

# Check if connected to Telstra Air Access Point
if $(iwconfig "$wifiadapter" | grep -q "$wifiap"); then
signal=$(iwconfig "$wifiadapter" | grep 'Signal level=' | awk -F= '{ print $3 }' | awk '{ print $1 }')
echo "Connected to $wifiap WiFi access point"
echo "Signal strength: $signal , ideally this should be under -70dBm, anything over this may experience reliability issues"
else
echo "Not connected to a $wifiap WiFi access point"
fi

# Display in terminal status
echo
echo "Getting WiFi station info..."

# Get wifi ap station info
ipparm=$(curl -s --max-time 10 "http://8.8.8.8" | grep "<LoginURL>")

# Breakdown variables
nasid=$(echo "$ipparm" | grep -Po -- 'nasid=\K[_\-."[:alnum:]]*')
ipaddr=$(echo "$ipparm" | grep -Po -- 'uamip=\K[_\-."[:alnum:]]*')
port=$(echo "$ipparm" | grep -Po -- 'uamport=\K[_\-."[:alnum:]]*')
macaddr=$(echo "$ipparm" | grep -Po -- 'mac=\K[_\-."[:alnum:]]*')
challenge=$(echo "$ipparm" | grep -Po -- 'challenge=\K[_\-."[:alnum:]]*')

# Display the variables in terminal
echo "nasid: $nasid"
echo "ipaddr: $ipaddr"
echo "port: $port"
echo "macaddr: $macaddr"
echo "challenge: $challenge"
echo

# Check viability
if [ "$port" -gt 2 &> /dev/null ]; then

# Connect
echo "Connecting..."
connect=$(wget -qO- --timeout=10 --keep-session-cookies \
--post-data "UserName=$username&Password=$password&_rememberMe=on" \
"https://telstra.portal.fon.com/jcp/telstra?res=login&nasid=$nasid&uamip=$ipaddr&uamport=$port&mac=$macaddr&challenge=$challenge")
echo "$connect"

if $(echo "$connect" | grep -q "You&#39;re connected!"); then
echo "Connected!"
echo
echo "Logout url is:"
logouturl=$(echo "$connect" | grep "<LogoffURL>" | sed 's/\(<LogoffURL>\|<\/LogoffURL>\)//g')
echo "$logouturl"
else
echo "Unable to connect"
looptime="120"
fi

else
echo "Unable to get connection info from the WiFi AP, likely insufficient signal, resetting the wireless network interface..."
echo
ifdown "$wifiadapter"
sleep 1
ifup "$wifiadapter"
looptime="5"
fi
fi

echo "Sleeping for $looptime seconds"
sleep "$looptime"
done
