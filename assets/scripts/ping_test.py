#!/usr/bin/python
"""

Gray Reyes
ping_test.py
"""

import os 
import subprocess
import sys

# clears terminal 
def clear_display():
	os.system('clear')
# dynamically gets default : ip r 
def get_default_gateway():
	try:
		result = subprocess.run(['ip','r'], capture_output = True, text=True)
		for line in result.stdout.splitlines():
			if line.startswith('default'):
				return line.split()[2]
	except Exception as e:
		print("error:", e)
	return None

# pings host 4 times 
def ping_host(host):
	try:
		subprocess.run(['ping','-c','4',host], check=True)
		print("Ping to " + host + " completed successfully")
	except subprocess.CalledProcessError:
		print(f"ping to {host} failed")
	except Exception as e:
		print("error: ", e)
def main():
	while True:
		clear_display()
		print("network connectivity menu:")
		print("1. display the default gateway")
		print("2. test local connectivity")
		print("3. test remote connectivity")
		print("4. test dns resolution")
		print("5. exit/quit script")
		choice = input("Enter your choice (1-5: ").strip()
		
		if choice == "1":
			gateway = get_default_gateway()
			if gateway:
				print("Default gateway: " + gateway)
			else:
				print("Default gateway: NOT FOUND")
		elif choice =="2":
			gateway = get_default_gateway()
			if gateway:
				print("Testing local connectivity (default gateway: " + gateway)
				ping_host(gateway)
			else: 
				print("local connectivity test skipped: default gateway NOT FOUND")
		elif choice == "3":
			remote_ip = "129.21.3.17"
			print("Testing remote connectivity (RIT DNS): " + remote_ip)
			ping_host(remote_ip)
		elif choice == "4":
			dns_host = "www.google.com"
			print("Testing DNS resoultion (ping hostname): " + dns_host)
			ping_host(dns_host)
		elif choice == "5":
			print("Exiting/quiting script ")
			sys.exit(0)
		else:
			print("Invalid choice. Please select 1-5")
		input("Press enter to return to menu")

if __name__ == "__main__":
	main()


