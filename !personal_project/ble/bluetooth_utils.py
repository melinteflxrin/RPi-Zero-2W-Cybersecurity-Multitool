"""
Bluetooth utility functions for low-level BLE operations.

This module provides functions to control Bluetooth devices and handle
BLE (Bluetooth Low Energy) advertising on Linux systems.

Requires: PyBluez library
"""

import struct
import fcntl
import array
import socket
from errno import EALREADY
import bluetooth._bluetooth as bluez


# BLE Advertisement Types
ADV_IND = 0x00              # Connectable undirected advertising
ADV_DIRECT_IND = 0x01       # Connectable directed advertising
ADV_SCAN_IND = 0x02         # Scannable undirected advertising
ADV_NONCONN_IND = 0x03      # Non-connectable undirected advertising
ADV_SCAN_RSP = 0x04         # Scan response

# HCI Command Parameters
OGF_LE_CTL = 0x08
OCF_LE_SET_ADVERTISING_PARAMETERS = 0x0006
OCF_LE_SET_ADVERTISE_ENABLE = 0x000A
OCF_LE_SET_ADVERTISING_DATA = 0x0008


def toggle_device(dev_id, enable):
    """
    Power ON or OFF a bluetooth device.

    Args:
        dev_id (int): Device id (e.g., 0 for hci0).
        enable (bool): True to enable, False to disable the device.
    
    Raises:
        IOError: If the device operation fails.
    """
    hci_sock = socket.socket(socket.AF_BLUETOOTH,
                             socket.SOCK_RAW,
                             socket.BTPROTO_HCI)
    
    req_str = struct.pack("H", dev_id)
    request = array.array("b", req_str)
    
    try:
        fcntl.ioctl(hci_sock.fileno(),
                    bluez.HCIDEVUP if enable else bluez.HCIDEVDOWN,
                    request[0])
        print(f"Bluetooth device {dev_id} {'enabled' if enable else 'disabled'}")
    except IOError as e:
        if e.errno == EALREADY:
            # Device is already in the desired state
            pass
        else:
            raise
    finally:
        hci_sock.close()


def start_le_advertising(sock, min_interval=1000, max_interval=1000,
                         adv_type=ADV_NONCONN_IND, data=()):
    """
    Start BLE (Bluetooth Low Energy) advertising.

    Args:
        sock: A bluetooth HCI socket (from bluez.hci_open_dev).
        min_interval (int): Minimum advertising interval in units of 0.625ms.
        max_interval (int): Maximum advertising interval in units of 0.625ms.
        adv_type (int): Advertisement type (default: ADV_NONCONN_IND).
        data (tuple): The advertisement data payload (max 31 bytes).
    
    Raises:
        ValueError: If data exceeds 31 bytes.
    """
    own_bdaddr_type = 0      # Public address
    direct_bdaddr_type = 0
    direct_bdaddr = (0,) * 6
    chan_map = 0x07          # All channels: 37, 38, 39
    filter_policy = 0        # Process scan and connection requests from all devices

    # Set advertising parameters
    struct_params = [min_interval, max_interval, adv_type, own_bdaddr_type,
                     direct_bdaddr_type]
    struct_params.extend(direct_bdaddr)
    struct_params.extend((chan_map, filter_policy))

    cmd_pkt = struct.pack("<HHBBB6BBB", *struct_params)
    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_ADVERTISING_PARAMETERS, cmd_pkt)

    # Enable advertising
    cmd_pkt = struct.pack("<B", 0x01)
    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_ADVERTISE_ENABLE, cmd_pkt)

    # Set advertising data
    data_length = len(data)
    if data_length > 31:
        raise ValueError(f"Advertisement data is too long ({data_length} bytes, max is 31)")
    
    cmd_pkt = struct.pack("<B%dB" % data_length, data_length, *data)
    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_ADVERTISING_DATA, cmd_pkt)


def stop_le_advertising(sock):
    """
    Stop BLE advertising.

    Args:
        sock: A bluetooth HCI socket (from bluez.hci_open_dev).
    """
    cmd_pkt = struct.pack("<B", 0x00)
    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_ADVERTISE_ENABLE, cmd_pkt)
