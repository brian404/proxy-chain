import os
import time
import random
import ipaddress
import netifaces as ni
import json

def get_active_interface():
    interfaces = ni.interfaces()
    for interface in interfaces:
        if interface != "lo" and ni.AF_INET in ni.ifaddresses(interface):
            return interface
    return None

def get_random_proxy(proxies):
    return random.choice(proxies)

def get_current_ip(interface):
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    return ip

def change_ip(interface, proxy):
    auth_string = ""
    os.system(f"export http_proxy={auth_string}{proxy['IP']}:{proxy['PORT']}")
    os.system(f"export https_proxy={auth_string}{proxy['IP']}:{proxy['PORT']}")
    time.sleep(2)

if __name__ == "__main__":
    interface = get_active_interface()
    if interface is None:
        print("No active network interface found.")
    else:
        print(f"Current IP address of {interface}: {get_current_ip(interface)}")

        try:
            input("Press Enter to activate IP rotation...")
            with open("proxy_list.json", 'r') as file:
                proxy_list = json.load(file)

            if not proxy_list:
                print("No proxies found in the JSON file.")
            else:
                interval = 30  # Interval in seconds for IP rotation
                while True:
                    proxy = get_random_proxy(proxy_list)
                    change_ip(interface, proxy)
                    time.sleep(interval)
        except KeyboardInterrupt:
            print("IP rotation stopped.")

