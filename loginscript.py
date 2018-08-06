import requests

# Configuration settings and values

username = "USERNAME@wifi.telstra.com"
password = "PASSWORD"
wifiap = "Telstra Air"
testurl = "http://captive.apple.com/hotspot-detect.html"
redirecturl = "http://msftconnecttest.com/redirect"
portalurl = "https://telstra.portal.fon.com/jcp/telstra?res=login"
logoffending = "/logoff"

# Check if connected to the internet

r = requests.get(testurl)

successcheck = r.text

if successcheck.find("Success") != -1:
	print("\n")
	print("Already Connected to the Internet!")
	exit()

# Pull the URL and session cookies from the redirect portal using standard portal redirection	
	
s = requests.get(redirecturl)

loginurl = s.url
logincookies = s.cookies

#Find the string start locations for the additional variables needed for our POST login

nasidindex_start = loginurl.find("nasid") + 6
uamipindex_start = loginurl.find("uamip") + 6
portindex_start = loginurl.find("uamport") + 8
macaddrindex_start = loginurl.find("mac") + 4
challengeindex_start = loginurl.find("challenge") + 10

#If nasid is ever 5 (-1 + 6), the string was not found in the url and thus we are not connected to the portal 

if nasidindex_start  == 5:
	print("\n")
	print("Cannot connect to portal, exiting!")
	exit()

#Find each string end location based on index_start and expected length of value
	
nasidindex_end = nasidindex_start + 17
uamipindex_end = uamipindex_start + 12
portindex_end = portindex_start + 4
macaddrindex_end = macaddrindex_start + 17
challengeindex_end = challengeindex_start + 32

#Pull each value from URL based on start and end of strings
	
nasid = loginurl[nasidindex_start:nasidindex_end]
uamip = loginurl[uamipindex_start:uamipindex_end]
port = loginurl[portindex_start:portindex_end]
macaddr = loginurl[macaddrindex_start:macaddrindex_end]
challenge = loginurl[challengeindex_start:challengeindex_end]

#Create Login URL based on the information gathered

nasidtext = "Gateway MAC is " + nasid
uamiptest = "Gateway address is " + uamip
porttext = "Admin port is " + port
adaptertext = "Adapter MAC is " + macaddr
challengetext = "Login Challenge ID is " + challenge

print("\n")
print(nasidtext)
print(uamiptest)
print(porttext)
print(adaptertext)
print(challengetext)

posturl = portalurl + "&nasid=" + nasid + "&uamip=" + uamip + "&uamport=" + port + "&mac=" + macaddr + "&challenge=" + challenge

#Create POST variables

h = requests.session()

postdata = {"UserName": username, "Password": password, "_rememberMe": "on"}

l = h.post(posturl, data=postdata, cookies=logincookies)

results = l.url

logouturl = "http://" + uamip + ":" + port + logoffending

#If successful, displays  
if results.find("success") != -1:
	print("\n")
	print("Success! Connected to the internet\n")
	print("Logout address is " + logouturl + "\n")
	exit()

print("\n")	
print("Not sucessful, check your settings and try again\n") 

exit()

