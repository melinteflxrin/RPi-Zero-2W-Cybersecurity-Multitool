#!/usr/bin/env python3
"""
NameSpoof Attack - Bluetooth Device Name Spoofing

This script implements a Bluetooth device spoofing technique that rapidly changes
the adapter name to various deceptive identifiers. It creates a "fog" of Bluetooth
device names that rotate through a predefined list, confusing nearby devices and
appearing as if multiple different Bluetooth devices are present in the area.

The attack works by:
1. Enabling BLE advertising on specified adapters
2. Continuously cycling through fake device names every N seconds
3. Making it appear as if many different devices are present

This is primarily a camouflage/reconnaissance technique. Use responsibly and
only on devices/networks you own or have explicit permission to test.

Features:
- Multi-adapter support (multiple Bluetooth radios)
- Customizable name rotation interval
- Pre-configured list of humorous/deceptive names
- Graceful shutdown on interrupt
"""

import os
import sys
import time
import random
import subprocess
import signal
from typing import List, Optional


# Deceptive and humorous device names for spoofing
SPOOFED_DEVICE_NAMES = [
    # Tech company branding confusion
    "Samsung Galaxy Tab",
    "iPhone 15",
    "iPad Pro",
    "MacBook Air",
    "Apple Watch Series 9",
    "Google Pixel Watch",
    "Meta Quest 3",
    "PlayStation 5",
    "Xbox Series X",
    "Nintendo Switch",
    
    # Service impersonation (humorous)
    "McDonald's Order System",
    "Starbucks Register",
    "Uber Driver Vehicle",
    "Lyft Driver Car",
    "Amazon Delivery Drone",
    "DHL Logistics Device",
    
    # Scary/intimidating names
    "FBI Surveillance Unit",
    "Police Department Device",
    "Suspicious Network Monitor",
    "Hacker Detection System",
    
    # Fictional references
    "Skynet Terminator",
    "HAL 9000",
    "Siri Personal Assistant",
    "Alexa Amazon Echo",
    "Google Assistant",
    
    # Misleading names
    "Not Your Device",
    "Free Public WiFi",
    "Airport Secure Network",
    "Coffee Shop WiFi",
    "Guest Network",
    "Admin Panel",
    "Network Router",
    "Printer Service",
    
    # Random nonsense
    "Device_001",
    "Unknown_BT_Device",
    "Mystery_Connection",
    "Ghost_Signal",
    "Phantom_Device",
]


class NameSpoofAttack:
    """Manages Bluetooth adapter name spoofing attack."""
    
    def __init__(self, adapter_indices: List[int], interval: int = 5, custom_names: Optional[List[str]] = None):
        """
        Initialize NameSpoof attack.
        
        Args:
            adapter_indices: List of HCI device indices (e.g., [0, 1] for hci0, hci1)
            interval: Seconds between name changes (default: 5)
            custom_names: Optional custom list of names to use instead of default
        """
        self.adapter_indices = adapter_indices
        self.interval = max(1, interval)  # Ensure minimum 1 second
        self.device_names = custom_names if custom_names else SPOOFED_DEVICE_NAMES
        self.running = False
        self.name_change_count = 0
        
        # Register signal handlers for clean shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals gracefully."""
        print(f"\n\n[!] Attack stopped. Changed names {self.name_change_count} times.")
        self.stop()
        sys.exit(0)
    
    def _enable_le_advertising(self, hci_index: int) -> bool:
        """
        Enable Low Energy advertising on a specific adapter.
        
        Args:
            hci_index: HCI device index (0 for hci0, 1 for hci1, etc.)
        
        Returns:
            True if successful, False otherwise
        """
        commands = "\n".join([
            "le on",
            "connectable on",
            "discov on",
            "advertising on",
            "exit"
        ])
        
        try:
            process = subprocess.Popen(
                ["sudo", "btmgmt", "--index", str(hci_index)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(input=commands, timeout=5)
            
            if process.returncode == 0:
                print(f"[+] LE advertising enabled on hci{hci_index}")
                return True
            else:
                print(f"[-] Failed to enable LE advertising on hci{hci_index}: {stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            process.kill()
            print(f"[-] Timeout enabling LE advertising on hci{hci_index}")
            return False
        except Exception as e:
            print(f"[-] Error enabling LE advertising on hci{hci_index}: {e}")
            return False
    
    def _change_adapter_name(self, hci_index: int, new_name: str) -> bool:
        """
        Change the Bluetooth adapter name.
        
        Args:
            hci_index: HCI device index
            new_name: New name to set
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Use btmgmt to change the adapter name
            result = subprocess.run(
                ["sudo", "btmgmt", "--index", str(hci_index), "name", new_name],
                capture_output=True,
                timeout=3,
                text=True
            )
            
            if result.returncode == 0:
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def _rotation_loop(self):
        """Main rotation loop that cycles through adapter names."""
        print(f"[*] Starting NameSpoof attack with {len(self.adapter_indices)} adapter(s)")
        print(f"[*] Name rotation interval: {self.interval}s")
        print(f"[*] Pool of names: {len(self.device_names)}")
        print(f"[*] Press Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            while self.running:
                for hci_index in self.adapter_indices:
                    # Pick random name from pool
                    new_name = random.choice(self.device_names)
                    
                    # Change adapter name
                    if self._change_adapter_name(hci_index, new_name):
                        print(f"[+] hci{hci_index}: {new_name}")
                        self.name_change_count += 1
                    else:
                        print(f"[-] hci{hci_index}: Failed to change name")
                
                # Wait before next rotation
                time.sleep(self.interval)
                
        except Exception as e:
            print(f"[-] Error in rotation loop: {e}")
            self.running = False
    
    def start(self) -> bool:
        """
        Start the NameSpoof attack.
        
        Returns:
            True if attack started successfully, False otherwise
        """
        # First, enable LE advertising on all adapters
        all_enabled = True
        for hci_index in self.adapter_indices:
            if not self._enable_le_advertising(hci_index):
                all_enabled = False
        
        if not all_enabled:
            print("[!] Warning: Some adapters failed to enable LE advertising")
        
        # Start the rotation loop
        try:
            self._rotation_loop()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
        
        return True
    
    def stop(self):
        """Stop the NameSpoof attack and clean up."""
        self.running = False
        print("[*] Disabling advertising...")
        
        # Disable advertising on all adapters
        for hci_index in self.adapter_indices:
            try:
                subprocess.run(
                    ["sudo", "btmgmt", "--index", str(hci_index), "advertising", "off"],
                    capture_output=True,
                    timeout=3
                )
            except Exception:
                pass


def parse_adapter_input(adapter_str: str) -> List[int]:
    """
    Parse adapter input string into list of indices.
    
    Args:
        adapter_str: String like "0" or "0,1,2" or "hci0,hci1"
    
    Returns:
        List of integer indices
    """
    indices = []
    parts = adapter_str.replace("hci", "").split(",")
    
    for part in parts:
        try:
            idx = int(part.strip())
            if 0 <= idx <= 10:  # Reasonable range for HCI devices
                indices.append(idx)
        except ValueError:
            pass
    
    return indices if indices else [0]  # Default to hci0


def run_interactive():
    """Run NameSpoof in interactive mode."""
    print("\n")
    print("╔════════════════════════════════════════╗")
    print("║       NameSpoof Adapter Attack         ║")
    print("║   (Bluetooth Name Rotation Attack)     ║")
    print("╚════════════════════════════════════════╝")
    print()
    
    # Show available adapters
    print("[*] Scanning Bluetooth adapters...")
    try:
        result = subprocess.run(
            ["hciconfig"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(result.stdout)
    except Exception as e:
        print(f"[-] Failed to list adapters: {e}")
        return
    
    # Get adapter selection
    adapter_input = input("[>] Enter adapter indices (e.g., 0 or 0,1,2): ").strip()
    adapter_indices = parse_adapter_input(adapter_input)
    
    # Get rotation interval
    try:
        interval = int(input("[>] Name rotation interval in seconds (default 5): ").strip() or "5")
        interval = max(1, interval)
    except ValueError:
        interval = 5
    
    # Confirm settings
    print(f"\n[*] Configuration:")
    print(f"    Adapters: {[f'hci{i}' for i in adapter_indices]}")
    print(f"    Rotation interval: {interval}s")
    print(f"    Total names: {len(SPOOFED_DEVICE_NAMES)}")
    
    confirm = input("\n[>] Start attack? (y/n): ").strip().lower()
    if confirm != 'y':
        print("[!] Attack cancelled")
        return
    
    # Run attack
    attack = NameSpoofAttack(adapter_indices, interval=interval)
    attack.start()


if __name__ == "__main__":
    run_interactive()
