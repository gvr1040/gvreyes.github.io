#!/usr/bin/env python3

# Name: Gray Reyes
# Date: March 24, 2026
# Course: NSSA221
# Assignment: System Report Script

import os
import platform
import socket
import subprocess
import ipaddress
from datetime import datetime


def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except:
        return "N/A"


def clear_terminal():
    os.system("clear")


def get_hostname():
    output = run_command("hostname -s")
    if output:
        return output
    return socket.gethostname()


def get_domain():
    output = run_command("hostname -d")
    if output:
        return output
    return "N/A"


def get_ip_and_mask():
    output = run_command("ip -4 -o addr show scope global")
    if not output:
        return "N/A", "N/A"

    lines = output.splitlines()

    for line in lines:
        parts = line.split()
        index = 0

        while index < len(parts):
            if parts[index] == "inet":
                address = parts[index + 1]
                if "/" in address:
                    ip, prefix = address.split("/")
                    try:
                        net = ipaddress.IPv4Network("0.0.0.0/" + prefix)
                        return ip, str(net.netmask)
                    except:
                        return ip, "N/A"
            index += 1

    return "N/A", "N/A"


def get_gateway():
    output = run_command("ip route | awk '/default/ {print $3; exit}'")
    return output if output else "N/A"


def get_dns():
    dns1 = "N/A"
    dns2 = "N/A"

    try:
        with open("/etc/resolv.conf") as file:
            servers = []
            for line in file:
                if line.startswith("nameserver"):
                    parts = line.split()
                    if len(parts) > 1:
                        servers.append(parts[1])

            if len(servers) >= 1:
                dns1 = servers[0]
            if len(servers) >= 2:
                dns2 = servers[1]
    except:
        pass

    return dns1, dns2


def get_os_info():
    name = "N/A"
    version = "N/A"

    try:
        with open("/etc/os-release") as file:
            for line in file:
                if line.startswith("PRETTY_NAME="):
                    name = line.split("=", 1)[1].strip().strip('"')
                if line.startswith("VERSION_ID="):
                    version = line.split("=", 1)[1].strip().strip('"')
    except:
        pass

    return name, version


def get_kernel():
    return platform.release()


def get_disk():
    total = run_command("df -h / --output=size | tail -1")
    used = run_command("df -h / --output=used | tail -1")
    free = run_command("df -h / --output=avail | tail -1")

    return total or "N/A", used or "N/A", free or "N/A"


def get_cpu_model():
    output = run_command("grep -m 1 'model name' /proc/cpuinfo | cut -d ':' -f2")
    return output.strip() if output else "N/A"


def get_cpu_counts():
    logical = run_command("nproc")
    cores = run_command("lscpu | awk '/Core\\(s\\) per socket/ {print $4}'")
    sockets = run_command("lscpu | awk '/Socket\\(s\\)/ {print $2}'")

    if cores and sockets:
        try:
            total_cores = str(int(cores) * int(sockets))
        except:
            total_cores = logical
    else:
        total_cores = logical

    return logical or "N/A", total_cores or "N/A"


def get_memory():
    output = run_command("free -h")
    if not output:
        return "N/A", "N/A"

    lines = output.splitlines()

    for line in lines:
        if line.startswith("Mem:"):
            parts = line.split()
            if len(parts) >= 7:
                return parts[1], parts[6]

    return "N/A", "N/A"


def build_report():
    date = datetime.now().strftime("%B %d, %Y")

    hostname = get_hostname()
    domain = get_domain()
    ip, mask = get_ip_and_mask()
    gateway = get_gateway()
    dns1, dns2 = get_dns()

    os_name, os_version = get_os_info()
    kernel = get_kernel()

    disk_total, disk_used, disk_free = get_disk()

    cpu_model = get_cpu_model()
    cpu_count, cpu_cores = get_cpu_counts()

    ram_total, ram_available = get_memory()

    report = ""
    report += "System Report - " + date + "\n\n"

    report += "Device Information\n"
    report += "Hostname: " + hostname + "\n"
    report += "Domain: " + domain + "\n\n"

    report += "Network Information\n"
    report += "IP Address: " + ip + "\n"
    report += "Gateway: " + gateway + "\n"
    report += "Network Mask: " + mask + "\n"
    report += "DNS1: " + dns1 + "\n"
    report += "DNS2: " + dns2 + "\n\n"

    report += "Operating System Information\n"
    report += "Operating System: " + os_name + "\n"
    report += "OS Version: " + os_version + "\n"
    report += "Kernel Version: " + kernel + "\n\n"

    report += "Storage Information\n"
    report += "System Drive Total: " + disk_total + "\n"
    report += "System Drive Used: " + disk_used + "\n"
    report += "System Drive Free: " + disk_free + "\n\n"

    report += "Processor Information\n"
    report += "CPU Model: " + cpu_model + "\n"
    report += "Number of processors: " + cpu_count + "\n"
    report += "Number of cores: " + cpu_cores + "\n\n"

    report += "Memory Information\n"
    report += "Total RAM: " + ram_total + "\n"
    report += "Available RAM: " + ram_available + "\n"

    return report


def save_log(report, hostname):
    home = os.path.expanduser("~")
    path = os.path.join(home, hostname + "_system_report.log")

    with open(path, "w") as file:
        file.write(report)


def main():
    clear_terminal()

    report = build_report()
    hostname = get_hostname()

    print(report)
    save_log(report, hostname)


if __name__ == "__main__":
    main()


