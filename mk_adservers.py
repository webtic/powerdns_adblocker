import requests

sources = [
	'https://adaway.org/hosts.txt',
	'http://adblock.gjtech.net/?format=unix-hosts',
	##'http://adblock.mahakala.is/',
	'http://hosts-file.net/ad_servers.txt',
	##'http://www.malwaredomainlist.com/hostslist/hosts.txt',
	'http://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts;showintro=0',
	'http://someonewhocares.org/hosts/hosts',
	'http://winhelp2002.mvps.org/hosts.txt'
]


def makezone(name):

   tmpl = """zone "%s" { type master; file "/etc/powerdns/null.zone"; allow-update { none; }; };\n"""
   return tmpl % name


zones = open("adservers.conf", "w")

all_zones = set()

for source in sources:
	print source
	r = requests.get(source)
	for line in r.iter_lines():
		# skip # comment lines and lines with html (<)
		if line.startswith('#') or "<" in line:
			continue
		
		line  = line.replace("0.0.0.0", "")
		line  = line.replace("127.0.0.1", "")
		if "#" in line:
			# get part in front of #
			line = line.split('#',1)[0]
		line = line.strip()
		if line and "." in line: 
			all_zones.add(line)

with open("adservers.conf", "w") as zones:
	for zone in all_zones:
		zones.write( makezone(zone) )

	zones.close()

