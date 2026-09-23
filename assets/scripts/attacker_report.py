#!/usr/bin/env python3

# Gray Rey
# April 24, 2026
# attacker_report.py

import os
import re
from datetime import datetime
from geoip import geolite2


def main():
    # clear terminal
    os.system("clear")

    # dictionary to store counts
    ip_counts = {}

    # regex pattern for IP addresses
    pattern = r"\b\d{1,3}(?:\.\d{1,3}){3}\b"

    # open log file
    log_file = open("syslog.log", "r")

    # read file line by line
    for line in log_file:
        if "Failed password" in line:
            match = re.search(pattern, line)

            if match:
                ip = match.group()

                if ip in ip_counts:
                    ip_counts[ip] = ip_counts[ip] + 1
                else:
                    ip_counts[ip] = 1

    log_file.close()

    # list for attackers
    attackers = []

    # filter IPs with 10+ attempts
    for ip in ip_counts:
        count = ip_counts[ip]

        if count >= 10:
            result = geolite2.lookup(ip)

            if result is None:
                country = "Unknown"
            else:
                if result.country is None:
                    country = "Unknown"
                else:
                    country = result.country

            attackers.append((count, ip, country))

    # sort ascending by count
    attackers.sort()

    # get current date
    today = datetime.now().strftime("%B %d, %Y")

    # print report
    print("Attacker Report - " + today)
    print()
    print("{:<8} {:<18} {:<10}".format("COUNT", "IP ADDRESS", "COUNTRY"))

    for attacker in attackers:
        print("{:<8} {:<18} {:<10}".format(attacker[0], attacker[1], attacker[2]))


# run program
if __name__ == "__main__":
    main()

