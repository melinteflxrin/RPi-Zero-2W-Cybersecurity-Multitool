#!/usr/bin/env python3
"""
Attack Suite - Main Menu Interface

A menu-driven application for BLE, Bluetooth, and WiFi attacks and security research tools.
"""

import os
import sys
import time
from ui import (cprint, iprint, wprint, eprint, sprint, cinput, 
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
        print_banner("AirPods Spam Attack", MAGENTA)
        
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
        print_banner("Apple Ad Spam Attack", MAGENTA)
        
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
        print_banner("Android Spam Attack", MAGENTA)
        
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
        print_banner("NameSpoof Adapter Spoofing Attack", MAGENTA)
        
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
    
    def action_device_scanner(self):
        """Execute BLE Device Scanner reconnaissance tool."""
        from ble.device_scanner import BLEDeviceScanner
        
        clear()
        print_banner("BLE Device Scanner", MAGENTA)
        
        cprint("This tool scans and displays all nearby Bluetooth Low Energy devices in real-time.", YELLOW)
        cprint("Shows device details: MAC address, signal strength, and device names.\n", YELLOW)
        cprint("WARNING: Educational purposes only! Use responsibly.\n", RED)
        
        try:
            # Create scanner
            scanner = BLEDeviceScanner()
            scanner.run()
            
            sprint("BLE device scanner completed!")
            
        except KeyboardInterrupt:
            wprint("\nScan stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure BLE module is properly installed")
        except Exception as e:
            eprint(f"Error during scanning: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    def action_beacon_broadcast(self):
        """Execute Beacon Broadcast WiFi attack."""
        from wifi.beacon_broadcast import BeaconBroadcaster
        
        clear()
        print_banner("Beacon Broadcast Attack", MAGENTA)
        
        cprint("This attack broadcasts fake WiFi networks with customizable parameters.", YELLOW)
        cprint("WARNING: Educational purposes only! Use responsibly.\n", RED)
        
        try:
            # Get WiFi interface from user
            interface = cinput("Enter WiFi interface name (e.g., wlan1)", LIGHT_CYAN) or "wlan1mon"
            
            iprint(f"Using interface: {interface}")
            
            # Create and run attack
            broadcaster = BeaconBroadcaster(interface)
            broadcaster.run_interactive()
            
            sprint("Attack module completed!")
            
        except KeyboardInterrupt:
            wprint("\nAttack stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure WiFi module is properly installed")
        except Exception as e:
            eprint(f"Error during attack: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    def action_ap_network_flood(self):
        """Execute AP Network Flood WiFi attack."""
        from wifi.ap_network_flood import APNetworkFlooder
        
        clear()
        print_banner("AP Network Flood Attack", MAGENTA)
        
        cprint("This attack broadcasts multiple fake WiFi networks from a network list.", YELLOW)
        cprint("WARNING: Educational purposes only! Use responsibly.\n", RED)
        
        try:
            # Get WiFi interface from user
            interface = cinput("Enter WiFi interface name (e.g., wlan1)", LIGHT_CYAN) or "wlan1mon"
            
            iprint(f"Using interface: {interface}")
            
            # Create and run attack
            flooder = APNetworkFlooder(interface)
            flooder.run_interactive()
            
            sprint("Attack module completed!")
            
        except KeyboardInterrupt:
            wprint("\nAttack stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure WiFi module is properly installed")
        except Exception as e:
            eprint(f"Error during attack: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    def action_network_scanner(self):
        """Execute Network Scanner WiFi reconnaissance tool."""
        from wifi.network_scanner import NetworkScanner
        
        clear()
        print_banner("Live Network Scanner", MAGENTA)
        
        cprint("This tool scans and displays all nearby WiFi networks in real-time.", YELLOW)
        cprint("Shows network details: SSID, signal strength, encryption, connected clients.\n", YELLOW)
        cprint("Requirements: WiFi adapter in monitor mode", CYAN)
        cprint("WARNING: Educational purposes only! Use responsibly.\n", RED)
        
        try:
            # Get WiFi interface from user
            interface = cinput("Enter WiFi interface name (e.g., wlan1)", LIGHT_CYAN) or "wlan1mon"
            
            iprint(f"Using interface: {interface}\n")
            
            # Create and run scanner
            scanner = NetworkScanner(interface)
            scanner.run()
            
            sprint("Network scanner completed!")
            
        except KeyboardInterrupt:
            wprint("\nScan stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure WiFi module is properly installed")
        except Exception as e:
            eprint(f"Error during scanning: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    def action_deauth_attack(self):
        """Execute Deauthentication WiFi attack."""
        from wifi.deauth_attack import DeauthAttack
        
        clear()
        print_banner("Deauthentication Attack", MAGENTA)
        
        cprint("This attack sends deauthentication frames to disconnect WiFi clients.", YELLOW)
        cprint("Can target entire networks, routers, or specific devices.\n", YELLOW)
        cprint("Requirements: WiFi adapter in monitor mode", CYAN)
        cprint("WARNING: Educational purposes only! Use responsibly.\n", RED)
        cprint("TIPS:", CYAN)
        cprint("  • Run network scanner first to find target BSSIDs and devices", WHITE)
        cprint("  • ESSID = network name, BSSID = router MAC, Device = client MAC\n", WHITE)
        
        try:
            # Get WiFi interface from user
            interface = cinput("Enter WiFi interface name (e.g., wlan1)", LIGHT_CYAN) or "wlan1mon"
            
            iprint(f"Using interface: {interface}")
            
            # Create and run attack
            deauth = DeauthAttack(interface)
            deauth.run_interactive()
            
            sprint("Deauthentication module completed!")
            
        except KeyboardInterrupt:
            wprint("\nAttack stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure WiFi module is properly installed")
        except Exception as e:
            eprint(f"Error during attack: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    def action_essid_bruteforce(self):
        """Execute ESSID Bruteforce WiFi attack."""
        from wifi.essid_bruteforce import ESSIDBruteforcer
        
        clear()
        print_banner("ESSID Bruteforce Attack", MAGENTA)
        
        cprint("This attack discovers hidden WiFi networks by probing for common SSID names.", YELLOW)
        cprint("Listens for responses to reveal networks that don't broadcast their name.\n", YELLOW)
        cprint("Requirements: WiFi adapter in monitor mode", CYAN)
        cprint("WARNING: Educational purposes only! Use responsibly.\n", RED)
        cprint("TIPS:", CYAN)
        cprint("  • Run network scanner first to find target router BSSID", WHITE)
        cprint("  • Wordlist mode uses 75+ common network names\n", WHITE)
        
        try:
            # Get WiFi interface from user
            interface = cinput("Enter WiFi interface name (e.g., wlan1)", LIGHT_CYAN) or "wlan1mon"
            
            iprint(f"Using interface: {interface}")
            
            # Create and run bruteforcer
            bruteforcer = ESSIDBruteforcer(interface)
            bruteforcer.run_interactive()
            
            sprint("ESSID bruteforce module completed!")
            
        except KeyboardInterrupt:
            wprint("\nAttack stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure WiFi module is properly installed")
        except Exception as e:
            eprint(f"Error during attack: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    def action_packet_capture(self):
        """Execute Packet Capture WiFi analysis tool."""
        from wifi.packet_capture import PacketCapture
        
        clear()
        print_banner("Packet Capture Tool", MAGENTA)
        
        cprint("This tool captures WiFi network traffic to .cap files for analysis.", YELLOW)
        cprint("Captured files can be analyzed with Wireshark or other tools.\n", YELLOW)
        cprint("Requirements: WiFi adapter in monitor mode", CYAN)
        cprint("WARNING: Educational purposes only! Use responsibly.\n", RED)
        cprint("TIPS:", CYAN)
        cprint("  • Use for network forensics and traffic analysis", WHITE)
        cprint("  • Compatible with Wireshark for detailed packet inspection", WHITE)
        cprint("  • Great for learning WiFi protocols\n", WHITE)
        
        try:
            # Get WiFi interface from user
            interface = cinput("Enter WiFi interface name (e.g., wlan1)", LIGHT_CYAN) or "wlan1mon"
            
            iprint(f"Using interface: {interface}")
            
            # Create and run packet capture
            capture = PacketCapture(interface)
            capture.run_interactive()
            
            sprint("Packet capture module completed!")
            
        except KeyboardInterrupt:
            wprint("\nCapture stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure WiFi module is properly installed")
        except Exception as e:
            eprint(f"Error during capture: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    def action_http_dos_attack(self):
        """Execute HTTP Denial of Service attack."""
        from wifi.http_dos import HTTPDOSAttack
        
        clear()
        print_banner("HTTP Denial of Service Attack", MAGENTA)
        
        cprint("This tool floods a target server with HTTP requests to exhaust resources.", YELLOW)
        cprint("It can render web services unavailable or slow them significantly.\n", YELLOW)
        cprint("WARNING: Educational purposes only! Use responsibly.", RED)
        cprint("WARNING: Only test on systems you own or have permission to test!\n", RED)
        cprint("TIPS:", CYAN)
        cprint("  • Threads: Higher = faster flooding, lower = more stealthy (50-500)", WHITE)
        cprint("  • Requests: Total HTTP requests to send (100-100000)", WHITE)
        cprint("  • Uses random user agents to evade simple filtering", WHITE)
        cprint("  • Great for load testing and stress testing servers\n", WHITE)
        
        try:
            # Create and run attack
            attack = HTTPDOSAttack()
            attack.run_interactive()
            
            sprint("HTTP DOS attack module completed!")
            
        except KeyboardInterrupt:
            wprint("\nAttack stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure WiFi HTTP DOS module is properly installed")
        except Exception as e:
            eprint(f"Error during attack: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    
    def action_localdos(self):
        """Execute Local Network DoS attack."""
        from wifi.localdos import localdos
        
        clear()
        print_banner("Local Network DoS Attack", MAGENTA)
        
        cprint("This tool floods devices on your local WiFi network with packets.", YELLOW)
        cprint("It will disconnect the target from the internet temporarily.\n", YELLOW)
        cprint("Requirements: arp-scan and hping3 installed", CYAN)
        cprint("WARNING: Only test on networks/devices you own!\n", RED)
        cprint("TIPS:", CYAN)
        cprint("  • Run network scanner first to find target devices on WiFi", WHITE)
        cprint("  • Get target IP from WiFi settings or use arp-scan", WHITE)
        cprint("  • Target will lose internet during attack, recover when stopped\n", WHITE)
        
        try:
            # Get WiFi interface from user
            interface = cinput("Enter WiFi interface name (e.g., wlan0)", LIGHT_CYAN) or "wlan0"
            
            iprint(f"Using interface: {interface}")
            print()
            
            # Run the localdos attack
            localdos(interface=interface)
            
            sprint("Local DoS attack session completed!")
            
        except KeyboardInterrupt:
            wprint("\nAttack stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure arp-scan and hping3 are installed:")
            eprint("  sudo apt-get install arp-scan hping3")
        except Exception as e:
            eprint(f"Error during attack: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    def action_facebook_phishing(self):
        """Execute Facebook phishing server."""
        from phishing.facebook_phish import FacebookPhishing
        
        clear()
        print_banner("Facebook Phishing Server", MAGENTA)
        
        cprint("This tool hosts a fake Facebook login page to capture credentials.", YELLOW)
        cprint("It is for educational purposes and authorized security testing only.\n", YELLOW)
        cprint("WARNING: Unauthorized phishing is illegal. Use only with permission!\n", RED)
        cprint("TIPS:", CYAN)
        cprint("  • Credentials are logged to a file with timestamps", WHITE)
        cprint("  • Server runs on localhost - use SSH tunneling to access from remote", WHITE)
        cprint("  • All captured attempts are displayed in real-time", WHITE)
        cprint("  • For safety, this only works on localhost (not accessible externally)\n", WHITE)
        
        try:
            # Get port from user
            port_input = cinput("Enter port [8000]: ")
            port = int(port_input) if port_input else 8000
            
            # Validate port
            if not (1 <= port <= 65535):
                eprint("Invalid port number")
                input(f"\n{CYAN}Press Enter to continue...{RESET}")
                return
            
            # Create and run phishing server
            phishing = FacebookPhishing(port=port)
            phishing.run_interactive()
            
            sprint("Phishing server module completed!")
            
        except KeyboardInterrupt:
            wprint("\nServer stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure phishing module is properly installed")
        except Exception as e:
            eprint(f"Error during phishing: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    def action_google_phishing(self):
        """Execute Google phishing server."""
        from phishing.google_phish import GooglePhishing
        
        clear()
        print_banner("Google Phishing Server", MAGENTA)
        
        cprint("This tool hosts a fake Google login page to capture credentials.", YELLOW)
        cprint("It is for educational purposes and authorized security testing only.\n", YELLOW)
        cprint("WARNING: Unauthorized phishing is illegal. Use only with permission!\n", RED)
        cprint("TIPS:", CYAN)
        cprint("  • Credentials are logged to a file with timestamps", WHITE)
        cprint("  • Server supports both localhost (SSH tunnel) and Cloudflare Tunnel", WHITE)
        cprint("  • All captured attempts are displayed in real-time", WHITE)
        cprint("  • Google login page closely mimics the real authentication flow\n", WHITE)
        
        try:
            # Get port from user
            port_input = cinput("Enter port [8000]: ")
            port = int(port_input) if port_input else 8000
            
            # Validate port
            if not (1 <= port <= 65535):
                eprint("Invalid port number")
                input(f"\n{CYAN}Press Enter to continue...{RESET}")
                return
            
            # Create and run phishing server
            phishing = GooglePhishing(port=port)
            phishing.run_interactive()
            
            sprint("Phishing server module completed!")
            
        except KeyboardInterrupt:
            wprint("\nServer stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure phishing module is properly installed")
        except Exception as e:
            eprint(f"Error during phishing: {e}")
        
        input(f"\n{CYAN}Press Enter to continue...{RESET}")
    
    def display_phishing_menu(self):
        """Display the Phishing submenu."""
        clear()
        
        cprint("╔════════════════════════════════════════════════════════╗", CYAN)
        cprint("║               PHISHING ATTACKS MENU                    ║", CYAN)
        cprint("╠════════════════════════════════════════════════════════╣", CYAN)
        cprint("║                                                        ║", CYAN)
        cprint("║  1) facebook  - Facebook Login Phishing Page           ║", LIGHT_CYAN)
        cprint("║                (Capture login credentials)             ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  2) google    - Google Login Phishing Page             ║", LIGHT_CYAN)
        cprint("║                (Capture email & password)              ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  b) back      - Return to Main Menu                    ║", YELLOW)
        cprint("║  e) exit      - Quit Application                       ║", RED)
        cprint("║                                                        ║", CYAN)
        cprint("╚════════════════════════════════════════════════════════╝", CYAN)
        print()
        
        choice = cinput("Select attack", LIGHT_BLUE)
        return choice
    
    def handle_phishing_menu(self):
        """Handle Phishing submenu navigation."""
        while self.running:
            choice = self.display_phishing_menu()
            choice = choice.lower().strip()
            
            if choice in ["1", "facebook"]:
                self.action_facebook_phishing()
            elif choice in ["2", "google"]:
                self.action_google_phishing()
            elif choice in ["b", "back"]:
                break
            elif choice in ["e", "exit", "q", "quit"]:
                self.running = False
                break
            else:
                wprint(f"Invalid option: {choice}")
                time.sleep(1)
    
    def action_l2cap_dos_attack(self):
        """Execute L2CAP Denial of Service attack."""
        from bt.l2cap_dos_attack import L2CAPDOSAttack
        
        clear()
        print_banner("L2CAP Denial of Service Attack", MAGENTA)
        
        cprint("This attack performs L2CAP ping flooding against target Bluetooth devices.", YELLOW)
        cprint("It can potentially disrupt or deny service to target devices.\n", YELLOW)
        cprint("WARNING: Educational purposes only! Use responsibly.\n", RED)
        cprint("TIPS:", CYAN)
        cprint("  • Requires target device MAC address (find with BLE Device Scanner)", WHITE)
        cprint("  • Uses multiple adapters for increased flooding capability", WHITE)
        cprint("  • Packet size affects attack intensity (larger = more bandwidth)\n", WHITE)
        
        try:
            # Get adapters from user
            adapters = self.get_adapter_list()
            
            # Create and run attack
            attack = L2CAPDOSAttack(adapters)
            attack.run_interactive()
            
        except KeyboardInterrupt:
            wprint("\nAttack stopped by user")
        except ImportError as e:
            eprint(f"Module import error: {e}")
            eprint("Make sure BT L2CAP DOS module is properly installed")
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
        cprint("║  1) BLE Attacks      - Bluetooth Low Energy Tools      ║", CYAN)
        cprint("║  2) Bluetooth Attacks- Bluetooth Classic Tools         ║", CYAN)
        cprint("║  3) WiFi Attacks     - WiFi Network Spoofing Tools     ║", CYAN)
        cprint("║  4) Phishing         - Social Engineering Tools        ║", CYAN)
        cprint("║  5) About            - Project Information             ║", CYAN)
        cprint("║  6) Exit             - Quit Application                ║", CYAN)
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
        cprint("║  1) airpods  - AirPods Spam Attack                     ║", LIGHT_CYAN)
        cprint("║               (Spam iOS devices with fake AirPods)     ║", WHITE)
        cprint("║  2) adseed   - Apple Ad Spam Attack                    ║", LIGHT_CYAN)
        cprint("║               (Spam Apple devices)                     ║", WHITE)
        cprint("║  3) android  - Android Spam Attack                     ║", LIGHT_CYAN)
        cprint("║               (Spam Android devices)                   ║", WHITE)
        cprint("║  4) namespoof- NameSpoof Adapter Spoofing              ║", LIGHT_CYAN)
        cprint("║               (Rotate adapter names)                   ║", WHITE)
        cprint("║  5) scanner  - BLE Device Scanner                      ║", LIGHT_CYAN)
        cprint("║               (Discover nearby BLE devices)            ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  b) back     - Return to Main Menu                     ║", YELLOW)
        cprint("║  e) exit     - Quit Application                        ║", RED)
        cprint("║                                                        ║", CYAN)
        cprint("╚════════════════════════════════════════════════════════╝", CYAN)
        print()
        
        choice = cinput("Select attack", LIGHT_BLUE)
        return choice
    
    def display_about(self):
        """Display about information."""
        clear()
        print_banner("About Attack Suite", BLUE)
        
        print(f"""{CYAN}
    Attack Suite v2.0
    
    A collection of Bluetooth and WiFi attack tools for
    security research and educational purposes.
    
    {YELLOW}Features:{RESET}
    • BLE Attacks - AirPods spam, Android spam, Name spoofing
    • WiFi Attacks - Beacon broadcast, AP network flooding
    
    {YELLOW}Requirements:{RESET}
    • Linux operating system
    • Bluetooth adapter with BLE support
    • WiFi adapter in monitor mode (for WiFi attacks)
    • PyBluez library
    • mdk4 tool (for WiFi attacks)
    • Root/sudo privileges
    
    {RED}Disclaimer:{RESET}
    This tool is for EDUCATIONAL PURPOSES ONLY.
    Only use on devices and networks you own or have explicit permission to test.
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
            elif choice in ["5", "scanner", "scan"]:
                self.action_device_scanner()
            elif choice in ["b", "back"]:
                break
            elif choice in ["e", "exit", "q", "quit"]:
                self.running = False
                break
            else:
                wprint(f"Invalid option: {choice}")
                time.sleep(1)
    
    def display_bluetooth_menu(self):
        """Display the Bluetooth attacks submenu."""
        clear()
        
        cprint("╔════════════════════════════════════════════════════════╗", CYAN)
        cprint("║              BLUETOOTH ATTACKS MENU                    ║", CYAN)
        cprint("╠════════════════════════════════════════════════════════╣", CYAN)
        cprint("║                                                        ║", CYAN)
        cprint("║  1) l2cap_dos- L2CAP Denial of Service Attack          ║", LIGHT_CYAN)
        cprint("║               (Flood target with L2CAP echo requests)  ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  b) back     - Return to Main Menu                     ║", YELLOW)
        cprint("║  e) exit     - Quit Application                        ║", RED)
        cprint("║                                                        ║", CYAN)
        cprint("╚════════════════════════════════════════════════════════╝", CYAN)
        print()
        
        choice = cinput("Select attack", LIGHT_BLUE)
        return choice
    
    def handle_bluetooth_menu(self):
        """Handle Bluetooth submenu navigation."""
        while self.running:
            choice = self.display_bluetooth_menu()
            choice = choice.lower().strip()
            
            if choice in ["1", "l2cap_dos", "l2cap"]:
                self.action_l2cap_dos_attack()
            elif choice in ["b", "back"]:
                break
            elif choice in ["e", "exit", "q", "quit"]:
                self.running = False
                break
            else:
                wprint(f"Invalid option: {choice}")
                time.sleep(1)
    
    def display_wifi_menu(self):
        """Display the WiFi attacks submenu."""
        clear()
        
        cprint("╔════════════════════════════════════════════════════════╗", CYAN)
        cprint("║                 WIFI ATTACKS MENU                      ║", CYAN)
        cprint("╠════════════════════════════════════════════════════════╣", CYAN)
        cprint("║                                                        ║", CYAN)
        cprint("║  1) beacon   - Beacon Broadcast Attack                 ║", LIGHT_CYAN)
        cprint("║               (Broadcast fake WiFi networks)           ║", WHITE)
        cprint("║  2) flood    - AP Network Flood Attack                 ║", LIGHT_CYAN)
        cprint("║               (Mass network broadcasting)              ║", WHITE)
        cprint("║  3) scanner  - Live Network Scanner                    ║", LIGHT_CYAN)
        cprint("║               (Discover and monitor nearby networks)   ║", WHITE)
        cprint("║  4) deauth   - Deauthentication Attack                 ║", LIGHT_CYAN)
        cprint("║               (Disconnect WiFi clients from networks)  ║", WHITE)
        cprint("║  5) bruteforce- ESSID Bruteforce Attack                ║", LIGHT_CYAN)
        cprint("║               (Discover hidden networks)               ║", WHITE)
        cprint("║  6) capture  - Packet Capture Tool                     ║", LIGHT_CYAN)
        cprint("║               (Record WiFi traffic to .cap files)      ║", WHITE)
        cprint("║  7) http_dos - HTTP Denial of Service                  ║", LIGHT_CYAN)
        cprint("║               (Flood target server with requests)      ║", WHITE)
        cprint("║  8) localdos - Local Network DoS Attack                ║", LIGHT_CYAN)
        cprint("║               (Flood target device on your WiFi)       ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  b) back     - Return to Main Menu                     ║", YELLOW)
        cprint("║  e) exit     - Quit Application                        ║", RED)
        cprint("║                                                        ║", CYAN)
        cprint("╚════════════════════════════════════════════════════════╝", CYAN)
        print()
        
        choice = cinput("Select attack", LIGHT_BLUE)
        return choice
    
    def handle_wifi_menu(self):
        """Handle WiFi submenu navigation."""
        while self.running:
            choice = self.display_wifi_menu()
            choice = choice.lower().strip()
            
            if choice in ["1", "beacon"]:
                self.action_beacon_broadcast()
            elif choice in ["2", "flood"]:
                self.action_ap_network_flood()
            elif choice in ["3", "scanner", "scan"]:
                self.action_network_scanner()
            elif choice in ["4", "deauth"]:
                self.action_deauth_attack()
            elif choice in ["5", "bruteforce", "essid"]:
                self.action_essid_bruteforce()
            elif choice in ["6", "capture", "wificap"]:
                self.action_packet_capture()
            elif choice in ["7", "http_dos", "httpdos"]:
                self.action_http_dos_attack()
            elif choice in ["8", "localdos", "local_dos", "dos"]:
                self.action_localdos()
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
                
                if choice in ["1", "ble"]:
                    self.handle_ble_menu()
                elif choice in ["2", "bluetooth", "bt"]:
                    self.handle_bluetooth_menu()
                elif choice in ["3", "wifi"]:
                    self.handle_wifi_menu()
                elif choice in ["4", "phishing"]:
                    self.handle_phishing_menu()
                elif choice in ["5", "about", "info"]:
                    self.display_about()
                elif choice in ["6", "exit", "e", "q", "quit"]:
                    clear()
                    cprint("Closing the app...", GREEN)
                    cprint("Bye!\n", CYAN)
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