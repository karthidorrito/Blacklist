import os
import sys
import pandas as pd
import os.path
import xlsxwriter
import datetime
import urllib.request
import socket
import dns
import warnings
from dns import resolver 
from requests import get

bls = ["b.barracudacentral.org", "bl.spamcop.net",
       "blacklist.woody.ch", "cbl.abuseat.org", 
       "combined.abuse.ch", "combined.rbl.msrbl.net", 
       "db.wpbl.info", "dnsbl.cyberlogic.net",
       "dnsbl.sorbs.net", "drone.abuse.ch", "drone.abuse.ch",
       "duinv.aupads.org", "dul.dnsbl.sorbs.net", "dul.ru",
       "dynip.rothen.com",
       "http.dnsbl.sorbs.net", "images.rbl.msrbl.net",
       "ips.backscatterer.org", "ix.dnsbl.manitu.net",
       "korea.services.net", "misc.dnsbl.sorbs.net",
       "noptr.spamrats.com", "ohps.dnsbl.net.au", "omrs.dnsbl.net.au",
       "osps.dnsbl.net.au", "osrs.dnsbl.net.au",
       "owfs.dnsbl.net.au", "pbl.spamhaus.org", "phishing.rbl.msrbl.net",
       "probes.dnsbl.net.au", "proxy.bl.gweep.ca", "rbl.interserver.net",
       "rdts.dnsbl.net.au", "relays.bl.gweep.ca", "relays.nether.net",
       "residential.block.transip.nl", "ricn.dnsbl.net.au",
       "rmst.dnsbl.net.au", "smtp.dnsbl.sorbs.net",
       "socks.dnsbl.sorbs.net", "spam.abuse.ch", "spam.dnsbl.sorbs.net",
       "spam.rbl.msrbl.net", "spam.spamrats.com", "spamrbl.imp.ch",
       "t3direct.dnsbl.net.au", "tor.dnsbl.sectoor.de",
       "torserver.tor.dnsbl.sectoor.de", "ubl.lashback.com",
       "ubl.unsubscore.com", "virus.rbl.jp", "virus.rbl.msrbl.net",
       "web.dnsbl.sorbs.net", "wormrbl.imp.ch", "xbl.spamhaus.org",
       "zen.spamhaus.org", "zombie.dnsbl.sorbs.net"]

URLS = [
    #EmergingThreats
    'http://rules.emergingthreats.net/blockrules/compromised-ips.txt',
    #AlienVault
    'http://reputation.alienvault.com/reputation.data',
    #BlocklistDE
    'http://www.blocklist.de/lists/bruteforcelogin.txt']

attributes = [
		["IP Address", "Time", "Emerging Threats", "Alien Vault", "bruteforcelogin", "b.barracudacentral.org", "bl.spamcop.net",
       "blacklist.woody.ch", "cbl.abuseat.org", 
       "combined.abuse.ch", "combined.rbl.msrbl.net", 
       "db.wpbl.info", "dnsbl.cyberlogic.net",
       "dnsbl.sorbs.net", "drone.abuse.ch", "drone.abuse.ch",
       "duinv.aupads.org", "dul.dnsbl.sorbs.net", "dul.ru",
       "dynip.rothen.com",
       "http.dnsbl.sorbs.net", "images.rbl.msrbl.net",
       "ips.backscatterer.org", "ix.dnsbl.manitu.net",
       "korea.services.net", "misc.dnsbl.sorbs.net",
       "noptr.spamrats.com", "ohps.dnsbl.net.au", "omrs.dnsbl.net.au",
       "osps.dnsbl.net.au", "osrs.dnsbl.net.au",
       "owfs.dnsbl.net.au", "pbl.spamhaus.org", "phishing.rbl.msrbl.net",
       "probes.dnsbl.net.au", "proxy.bl.gweep.ca", "rbl.interserver.net",
       "rdts.dnsbl.net.au", "relays.bl.gweep.ca", "relays.nether.net",
       "residential.block.transip.nl", "ricn.dnsbl.net.au",
       "rmst.dnsbl.net.au", "smtp.dnsbl.sorbs.net",
       "socks.dnsbl.sorbs.net", "spam.abuse.ch", "spam.dnsbl.sorbs.net",
       "spam.rbl.msrbl.net", "spam.spamrats.com", "spamrbl.imp.ch",
       "t3direct.dnsbl.net.au", "tor.dnsbl.sectoor.de",
       "torserver.tor.dnsbl.sectoor.de", "ubl.lashback.com",
       "ubl.unsubscore.com", "virus.rbl.jp", "virus.rbl.msrbl.net",
       "web.dnsbl.sorbs.net", "wormrbl.imp.ch", "xbl.spamhaus.org",
       "zen.spamhaus.org", "zombie.dnsbl.sorbs.net", "Blacklist Level"]
	]

def color(text, color_code):
    if sys.platform == "win32" and os.getenv("TERM") != "xterm":
        return text
    return '\x1b[%dm%s\x1b[0m' % (color_code, text)

def red(text):
    return color(text, 31)


def blink(text):
    return color(text, 5)


def green(text):
    return color(text, 32)


def blue(text):
    return color(text, 34)

def content_test(url, ip):
	try:
		request_url = urllib.request.urlopen(url)
		blist = request_url.read().decode().splitlines()
		if url.endswith('reputation.data'):
			for i in range(len(blist)):
				hashidx = blist[i].index('#')
				blist[i] = blist[i][:hashidx]
		if ip in blist:
			return False
		else:
			return True
	except:
		print(red("Couldn't output results to excel file"))

def genResult(attributes, results, filename):
	try:
		wb = xlsxwriter.Workbook(filename)

		ws = wb.add_worksheet()
		data_format = wb.add_format({'bg_color': '#808080', 'border': 1, 'border_color': 'white', 'bold': True, 'font_color': 'white'})
		listed_format = wb.add_format({'bg_color': 'red', 'font_color': 'white'})
		safe = wb.add_format({'bg_color': 'green', 'font_color': 'white'})
		low = wb.add_format({'bg_color': '#339966', 'font_color': 'white'})
		medium = wb.add_format({'bg_color': '#FF9900', 'font_color': 'white'})
		high = wb.add_format({'bg_color': '#FF6600', 'font_color': 'white'})
		chigh = wb.add_format({'bg_color': 'red', 'font_color': 'white'})
		row = 0
		col = 0
		for line in attributes:
			for item in line:
				ws.set_column(0, 62, 15)
				ws.set_row(row, 20)
				ws.write(row, col, item, data_format)
				col += 1
			row += 1
			col = 0
		for line in results:
			for item in line:
				if item == "Listed":
					ws.write(row, col, item, listed_format)
				elif item == "Possibly safe":
					ws.write(row, col, item, safe)
				elif item == "Low":
					ws.write(row, col, item, low)
				elif item == "Medium":
					ws.write(row, col, item, medium)
				elif item == "High":
					ws.write(row, col, item, high)
				elif item == "Critically High":
					ws.write(row, col, item, chigh)
				else:
					ws.write(row, col, item)
				col += 1
			row += 1
			col = 0
	 
		wb.close()
	except Exception as e:
		print(e)
		print(red("Couldn't generate result file"))

def main():


	banner = """
 _     _            _      _ _     _            
| |__ | | __ _  ___| | __ | (_)___| |_ ___ _ __ 
| '_ \| |/ _` |/ __| |/ / | | / __| __/ _ \ '__|
| |_) | | (_| | (__|   <  | | \__ \ ||  __/ |   
|_.__/|_|\__,_|\___|_|\_\ |_|_|___/\__\___|_| 
"""

	print(green(banner))

	if not os.path.exists('input_ip_list.xlsx'):
		wb = xlsxwriter.Workbook("input_ip_list.xlsx")
		ws = wb.add_worksheet()
		data_format = wb.add_format({'bg_color': '#808080', 'border': 1, 'border_color': 'white', 'bold': True, 'font_color': 'white'})
		ws.set_row(0, 20)
		ws.set_column(0, 0, 15)
		ws.write(0, 0, 'IP Address', data_format)
		wb.close()
		print(red("Type IP Addresses in 'input_ip_list.xlsx' and run the program again!!!"))
		return

	df = pd.read_excel('input_ip_list.xlsx', engine='openpyxl')
	Test_IPs = df['IP Address'].tolist()
	currtime = datetime.datetime.now()
	resultfile = "results" + currtime.strftime("_%Y%m%d_%H%M%S") + ".xlsx"
	
	results = []

	for sno, badip in enumerate(Test_IPs):
		try:
			print("IP", sno+1,"/",len(Test_IPs),"\nIP address:", badip)

			details = []
			details.append(badip)
			details.append(currtime.strftime("%d-%m-%Y %H-%M-%S"))
			GOOD = 0
			BAD = 0

			for url in URLS:
				if content_test(url, badip):
					print(green(badip + ' is not listed in ' + url))
					details.append("Not Listed")
					GOOD = GOOD + 1
				else:
					print(red(badip + ' is listed in ' + url))
					details.append("Listed")
					BAD = BAD + 1

			for bl in bls:
				try:
					my_resolver = dns.resolver.Resolver()
					query = '.'.join(reversed(str(badip).split("."))) + "." + bl
					my_resolver.timeout = 5
					my_resolver.lifetime = 5
					answers = my_resolver.resolve(query, "A")
					answer_txt = my_resolver.resolve(query, "TXT")
					print(red(badip + ' is listed in ' + bl) + ' (%s: %s)' % (answers[0], answer_txt[0]))
					BAD = BAD + 1
					details.append("Listed")

				except dns.resolver.NXDOMAIN:
					print(green(badip + ' is not listed in ' + bl))
					GOOD = GOOD + 1
					details.append("Not Listed")

				except dns.resolver.Timeout:
					print(blink('WARNING: Timeout querying ' + bl))
					details.append("-")

				except dns.resolver.NoNameservers:
					print(blink('WARNING: No nameservers for ' + bl))
					details.append("-")

				except dns.resolver.NoAnswer:
					print(blink('WARNING: No answer for ' + bl))
					details.append("-")
					
			print(red('\n{0} is on {1}/{2} blacklists.\n'.format(badip, BAD, (GOOD+BAD))))
			level = ""
			if BAD == 0:
				level = "Possibly safe"
			elif BAD == 1:
				level = "Low"
			elif BAD == 2:
				level = "Medium"
			elif BAD == 3 or BAD == 4:
				level = "High"
			elif BAD >= 5:
				level = "Critically High"
			details.append(level)
			results.append(details)
			genResult(attributes, results, resultfile)
		except:
			print(red("Process failed."))

if __name__ == '__main__':
	main()