#!/usr/bin/env python3
import subprocess
import datetime
import os

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except subprocess.CalledProcessError:
        return "N/A"

# Time
now = datetime.datetime.now()
print(f"Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# Battery (Linux, via upower or /sys/class)
battery = run("upower -i $(upower -e | grep BAT) | grep -E 'percentage|state'")
print("Battery:")
print(battery if battery else "No battery info")

# Network (active interface)
net_dev = run("ip route get 1.1.1.1 | awk '{print $5}'")
if net_dev != "N/A":
    ip_addr = run(f"ip addr show {net_dev} | grep 'inet ' | awk '{{print $2}}' | cut -d/ -f1")
    ssid = run(f"iwgetid -r")  # Wi-Fi SSID
    print(f"Network ({net_dev}): {ip_addr}")
    if ssid:
        print(f"SSID: {ssid}")
else:
    print("Network: N/A")

# CPU usage
cpu = run("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'")
print(f"CPU Usage: {cpu}%")

# Memory usage
mem = run("free -h | grep Mem | awk '{print $3 \"/\" $2}'")
print(f"Memory Usage: {mem}")

# Disk usage
disk = run("df -h / | tail -1 | awk '{print $3 \"/\" $2}'")
print(f"Disk Usage: {disk}")

# Hostname / User
print(f"User: {os.getlogin()}  Host: {run('hostname')}")
