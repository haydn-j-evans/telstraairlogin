import requests

# Configuration settings and values

username = "USERNAME@wifi.telstra.com"
password = "PASSWORD"
wifiadapter = "wlan0"
wifiap = "Telstra Air"
testurl = "http://captive.apple.com/hotspot-detect.html"
redirecturl = "http://msftconnecttest.com/redirect"

# Check if connected to the internet

r = requests.get(testurl)

successcheck = r.text

if successcheck.find('success') == -1:
	print("Already Connected to the Internet!")
	exit()

# Pull the URL from the redirect portal using standard portal redirection	
	
s = requests.get(redirecturl)

loginurl = s.url

#Find the string start locations for the additional variables needed for our POST login

nasidindex_start = loginurl.find('nasid') + 6
ipaddrindex_start = loginurl.find('ipaddr') + 6
portindex_start = loginurl.find('port') + 8
macaddrindex_start = loginurl.find('macaddr') + 5
challengeindex_start = loginurl.find('challenge') + 10

#If nasid is ever 5 (-1 + 6), the string was not found in the url and thus we are not connected to the portal 

if nasidindex  == 5:
	print("Cannot connect to portal, exiting!")
	exit()

#Find each string end location based on index_start and expected length of value
	
nasidindex_end = nasidindex + 
ipaddrindex_end = ipaddrindex + 
portindex_end = portindex + 
macaddrindex_end = macaddrindex + 
challengeindex_end = challengeindex + 

#Pull each value from URL based on start and end of strings
	
nasid = loginurl[nasidindex_start:nasidindex_end]
ipaddr = loginurl[ipaddrindex_start:ipaddrindex_end]
port = loginurl[portindex_start:portindex_end]
macaddr = loginurl[macaddrindex_start:macaddrindex_end]
challenge = loginurl[challengeindex_start:challengeindex_end]

posturl = https://telstra.portal.fon.com/jcp/telstra?res=login&nasid=

l = requests.post(

