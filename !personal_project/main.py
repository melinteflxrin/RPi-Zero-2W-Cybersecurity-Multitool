#!/usr/bin/env python3
"""
Attack Suite - Main Menu Interface

A menu-driven application for BLE, Bluetooth, and WiFi attacks and security research tools.
"""

import os
import sys
import time
from colors import (cprint, iprint, wprint, eprint, sprint, cinput, 
                   RED, GREEN, CYAN, BLUE, YELLOW, MAGENTA, WHITE, 
                   BRIGHT, RESET, LIGHT_CYAN, LIGHT_BLUE, clear, print_banner)


class AttackSuite:
    """Main application class for security research attacks."""
    
    def __init__(self):
        self.running = True
    
    def get_adapter_list(self):
        """
        Get list of Bluetooth adapters from user.
        
        Returns:
            list: List of HCI device identifiers (e.g., ["hci0", "hci1"]).
        """
        try:
            num_adapters = int(cinput("How many Bluetooth adapters?", LIGHT_CYAN) or "1")
            adapters = [f"hci{i}" for i in range(num_adapters)]
            iprint(f"Using adapters: {', '.join(adapters)}")
            return adapters
        except ValueError:
            wprint("Invalid input, defaulting to hci0")
            return ["hci0"]
    
    def action_airpods_spam(self):
        """Execute AirPods spam attack."""
        from ble.airpods_spam import airpods_spam
        
        clear()
        print_banner("🎧 AirPods Spam Attack", MAGENTA)
        
        cprint("This attack broadcasts fake AirPods advertisements to nearby iOS devices.", YELLOW)
        cprint("WARNING: Educational purposes only! Use responsibly.\n", RED)
        
        try:
            # Get configuration from user
            adapters = self.get_adapter_list()
            
            interval = int(cinput("Advertising interval (ms)", LIGHT_CYAN) or "200")
            duration = int(cinput("Duration (seconds)", LIGHT_CYAN) or "60")
            num_models = int(cinput("Number of AirPods models (1-5)", LIGHT_CYAN) or "5")
            
            # Validate inputs
            num_models = max(1, min(5, num_models))
            
            print()
            iprint("Starting AirPods spam attack...")
            iprint(f"Press Ctrl+C to stop early")
            print()
            
            # Execute attack
            airpods_spam(
                device_ids=adapters,
                interval=interval,
                num_models=num_models,
                duration=duration
            )
            
            sprint("Attack completed successfully!")
            
        except KeyboardInterrupt:
            wprint("\nAttack stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure PyBluez is installed: pip install pybluez")
        except Exception as e:
            eprint(f"Error during attack: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")

    def action_ad_spam(self):
        """Execute Apple advertisement spam attack."""
        from ble.ad_spam import ad_spam
        
        clear()
        print_banner("🍎 Apple Ad Spam Attack", MAGENTA)
        
        cprint("This attack broadcasts fake Apple device advertisements to nearby devices.", YELLOW)
        cprint("WARNING: Educational purposes only! Use responsibly.\n", RED)
        cprint("TIPS for better results:", CYAN)
        cprint("  • Interval: 0.1-0.5 seconds (lower = more aggressive, higher = more stealth)", WHITE)
        cprint("  • Duration: 30-120 seconds (longer increases chance of detection)", WHITE)
        cprint("  • Use multiple adapters if available for better coverage\n", WHITE)
        
        try:
            # Get configuration from user
            adapters = self.get_adapter_list()
            
            interval = float(cinput("Advertising interval (seconds, 0.1-1.0)", LIGHT_CYAN) or "0.2")
            duration = int(cinput("Duration (seconds)", LIGHT_CYAN) or "60")
            
            # Validate interval
            interval = max(0.05, min(2.0, interval))
            
            print()
            iprint("Starting Apple ad spam attack...")
            iprint(f"Press Ctrl+C to stop early")
            print()
            
            # Execute attack
            ad_spam(
                device_ids=adapters,
                interval=interval,
                duration=duration
            )
            
            sprint("Attack completed successfully!")
            
        except KeyboardInterrupt:
            wprint("\nAttack stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure PyBluez is installed: pip install pybluez")
        except Exception as e:
            eprint(f"Error during attack: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")

    def action_android_spam(self):
        """Execute Android spam attack."""
        from ble.android_spam import android_spam
        
        clear()
        print_banner("📱 Android Spam Attack", MAGENTA)
        
        cprint("This attack broadcasts fake Android device advertisements to nearby devices.", YELLOW)
        cprint("WARNING: Educational purposes only! Use responsibly.\n", RED)
        
        try:
            # Get configuration from user
            adapters = self.get_adapter_list()
            
            interval = float(cinput("Advertising interval (seconds)", LIGHT_CYAN) or "1")
            duration = int(cinput("Duration (seconds)", LIGHT_CYAN) or "60")
            
            print()
            iprint("Starting Android spam attack...")
            iprint(f"Press Ctrl+C to stop early")
            print()
            
            # Execute attack
            android_spam(
                device_ids=adapters,
                interval=interval,
                duration=duration
            )
            
            sprint("Attack completed successfully!")
            
        except KeyboardInterrupt:
            wprint("\nAttack stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure PyBluez is installed: pip install pybluez")
        except Exception as e:
            eprint(f"Error during attack: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    def action_name_spoof(self):
        """Execute NameSpoof adapter name spoofing attack."""
        from ble.name_spoofer import NameSpoofAttack
        
        clear()
        print_banner("🎭 NameSpoof Adapter Spoofing Attack", MAGENTA)
        
        cprint("This attack continuously changes Bluetooth adapter names to deceptive values.", YELLOW)
        cprint("It creates a 'fog' of fake Bluetooth devices by rapid name rotation.", YELLOW)
        cprint("WARNING: Educational purposes only! Use responsibly.\n", RED)
        cprint("TIPS for better results:", CYAN)
        cprint("  • Interval: 1-5 seconds (1 = rapid changes, 5 = slower rotation)", WHITE)
        cprint("  • Use multiple adapters if available for doubled effect", WHITE)
        cprint("  • Nearby devices will see your adapter appear as many devices\n", WHITE)
        
        try:
            # Get configuration from user
            adapters = self.get_adapter_list()
            adapter_indices = [int(a.replace("hci", "")) for a in adapters]
            
            interval = int(cinput("Name rotation interval (seconds, 1-30)", LIGHT_CYAN) or "5")
            interval = max(1, min(30, interval))
            
            print()
            cprint(f"Configuration:")
            cprint(f"  Adapters: {', '.join(adapters)}")
            cprint(f"  Rotation interval: {interval}s")
            cprint(f"  Name pool size: 50+\n")
            
            iprint("Starting NameSpoof attack...")
            iprint(f"Press Ctrl+C to stop", YELLOW)
            print()
            
            # Execute attack
            attack = NameSpoofAttack(adapter_indices, interval=interval)
            attack.start()
            
            sprint("Attack completed successfully!")
            
        except KeyboardInterrupt:
            wprint("\nAttack stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure NameSpoof module is properly installed")
        except Exception as e:
            eprint(f"Error during attack: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    def display_main_menu(self):
        """Display the main category menu."""
        clear()
        
        cprint("╔════════════════════════════════════════════════════════╗", CYAN)
        cprint("║                    MAIN MENU                           ║", CYAN)
        cprint("╠════════════════════════════════════════════════════════╣", CYAN)
        cprint("║                                                        ║", CYAN)
        cprint("║  1) BLE Attacks  - Bluetooth Low Energy Tools         ║", CYAN)
        cprint("║  2) About        - Project Information                ║", CYAN)
        cprint("║  3) Exit         - Quit Application                   ║", CYAN)
        cprint("║                                                        ║", CYAN)
        cprint("╚════════════════════════════════════════════════════════╝", CYAN)
        print()
        
        choice = cinput("Select option", LIGHT_BLUE)
        return choice
    
    def display_ble_menu(self):
        """Display the BLE attacks submenu."""
        clear()
        
        cprint("╔════════════════════════════════════════════════════════╗", CYAN)
        cprint("║                  BLE ATTACKS MENU                      ║", CYAN)
        cprint("╠════════════════════════════════════════════════════════╣", CYAN)
        cprint("║                                                        ║", CYAN)
        cprint("║  1) airpods  - AirPods Spam Attack                    ║", LIGHT_CYAN)
        cprint("║               (Spam iOS devices with fake AirPods)     ║", WHITE)
        cprint("║  2) adseed   - Apple Ad Spam Attack                   ║", LIGHT_CYAN)
        cprint("║               (Spam Apple devices)                     ║", WHITE)
        cprint("║  3) android  - Android Spam Attack                    ║", LIGHT_CYAN)
        cprint("║               (Spam Android devices)                   ║", WHITE)
        cprint("║  4) namespoof- NameSpoof Adapter Spoofing            ║", LIGHT_CYAN)
        cprint("║               (Rotate adapter names - create fog)      ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  b) back     - Return to Main Menu                    ║", YELLOW)
        cprint("║  e) exit     - Quit Application                       ║", RED)
        cprint("║                                                        ║", CYAN)
        cprint("╚════════════════════════════════════════════════════════╝", CYAN)
        print()
        
        choice = cinput("Select attack", LIGHT_BLUE)
        return choice
    
    def display_about(self):
        """Display about information."""
        clear()
        print_banner("ℹ️  About BLE Attack Suite", BLUE)
        
        print(f"""{CYAN}
    BLE Attack Suite v1.0
    
    A collection of Bluetooth Low Energy attack tools for
    security research and educational purposes.
    
    {YELLOW}Features:{RESET}
    • AirPods Spam - Broadcast fake Apple device advertisements
    • AD Spam Scaffold - Educational non-operational loop template
    
    {YELLOW}Requirements:{RESET}
    • Linux operating system
    • Bluetooth adapter with BLE support
    • PyBluez library (pip install pybluez)
    • Root/sudo privileges
    
    {RED}Disclaimer:{RESET}
    This tool is for EDUCATIONAL PURPOSES ONLY.
    Only use on devices you own or have explicit permission to test.
    Unauthorized use may violate laws and regulations.
    
    {GREEN}Author: Personal Project
    License: Educational Use Only{RESET}
        """)
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    def handle_ble_menu(self):
        """Handle BLE submenu navigation."""
        while self.running:
            choice = self.display_ble_menu()
            choice = choice.lower().strip()
            
            if choice in ["1", "airpods"]:
                self.action_airpods_spam()
            elif choice in ["2", "adseed", "adspam"]:
                self.action_ad_spam()
            elif choice in ["3", "android"]:
                self.action_android_spam()
            elif choice in ["4", "namespoof", "spoof"]:
                self.action_name_spoof()
            elif choice in ["b", "back"]:
                break
            elif choice in ["e", "exit", "q", "quit"]:
                self.running = False
                break
            else:
                wprint(f"Invalid option: {choice}")
                time.sleep(1)
    
    def run(self):
        """Main application loop."""
        try:
            while self.running:
                choice = self.display_main_menu()
                choice = choice.lower().strip()
                
                if choice in ["1", "ble", "bluetooth"]:
                    self.handle_ble_menu()
                elif choice in ["2", "about", "info"]:
                    self.display_about()
                elif choice in ["3", "exit", "e", "q", "quit"]:
                    clear()
                    cprint("Thanks for using BLE Attack Suite!", GREEN)
                    cprint("Stay safe and hack responsibly! 👋\n", CYAN)
                    self.running = False
                else:
                    wprint(f"Invalid option: {choice}")
                    time.sleep(1)
        
        except KeyboardInterrupt:
            clear()
            print(f"\n{YELLOW}Interrupted by user. Goodbye!{RESET}\n")
        except Exception as e:
            eprint(f"Unexpected error: {e}")
            sys.exit(1)


def check_requirements():
    """Check if required dependencies are installed."""
    try:
        import bluetooth._bluetooth as bluez
    except ImportError:
        eprint("PyBluez library not found!")
        eprint("Install it with: pip install pybluez")
        eprint("\nOn Linux, you may also need:")
        eprint("  sudo apt-get install python3-dev libbluetooth-dev")
        return False
    
    # Check if running on Linux
    if os.name != 'posix':
        wprint("This tool is designed for Linux systems.")
        wprint("Some features may not work on other platforms.")
    
    # Check if running as root
    if os.geteuid() != 0:
        wprint("Not running as root!")
        wprint("Some BLE operations require sudo/root privileges.")
        wprint("Run with: sudo python3 main.py")
    
    return True


def main():
    """Entry point for the application."""
    if not check_requirements():
        sys.exit(1)
    
    app = AttackSuite()
    app.run()


if __name__ == '__main__':
    main()