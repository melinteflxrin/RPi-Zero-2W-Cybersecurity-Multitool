"""
ESSID Bruteforce - Hidden Network Discovery Tool

This module discovers hidden WiFi networks by probing for common SSIDs
and listening for responses from target access points.
"""

import subprocess
import os
import time
from ui import (cprint, iprint, wprint, eprint, sprint, cinput, 
                   RED, GREEN, CYAN, YELLOW, MAGENTA, WHITE, 
                   RESET, LIGHT_CYAN, clear)


class ESSIDBruteforcer:
    """
    Discovers hidden WiFi networks by probing for SSID names
    and detecting responses from access points.
    """
    
    def __init__(self, interface):
        """
        Initialize the ESSID bruteforcer.
        
        Args:
            interface (str): WiFi interface in monitor mode (e.g., "wlan1mon")
        """
        self.interface = interface
        self.process = None
        self.found_ssids = []
    
    def verify_monitor_mode(self):
        """
        Verify that the interface is in monitor mode.
        
        Returns:
            bool: True if interface is in monitor mode, False otherwise
        """
        try:
            result = subprocess.run(
                ["iwconfig", self.interface],
                capture_output=True,
                text=True,
                timeout=5
            )
            return "Monitor" in result.stdout
        except Exception as e:
            eprint(f"Error checking monitor mode: {e}")
            return False
    
    def get_wordlist_path(self):
        """
        Get the path to the common SSIDs wordlist.
        
        Returns:
            str: Path to wordlist file or None if not found
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        wordlist_path = os.path.join(script_dir, "common_ssids.txt")
        
        if os.path.exists(wordlist_path):
            return wordlist_path
        return None
    
    def bruteforce_with_wordlist(self, bssid, wordlist_path):
        """
        Bruteforce hidden SSIDs using a wordlist.
        
        Args:
            bssid (str): Target router MAC address
            wordlist_path (str): Path to wordlist file containing SSIDs
        """
        try:
            if not os.path.exists(wordlist_path):
                eprint(f"Wordlist not found: {wordlist_path}")
                return
            
            # Count SSIDs in wordlist
            with open(wordlist_path, 'r') as f:
                ssid_count = sum(1 for _ in f)
            
            iprint(f"Targeting router: {bssid}")
            iprint(f"Wordlist SSIDs: {ssid_count}")
            iprint("Starting ESSID bruteforce (Ctrl+C to stop)\n")
            time.sleep(1)
            
            # Run mdk4 with wordlist probing
            cmd = f"mdk4 {self.interface} p -t {bssid} -f {wordlist_path} -s 100"
            
            self.process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Monitor output
            while self.process:
                try:
                    output = self.process.stdout.readline()
                    if output and "Job's done" not in output:
                        cprint(output.rstrip(), CYAN)
                    
                    if self.process.poll() is not None:
                        break
                except KeyboardInterrupt:
                    self.stop_bruteforce()
                    break
            
            sprint("Bruteforce completed!")
            
        except FileNotFoundError:
            eprint("mdk4 not found. Install aircrack-ng: sudo apt-get install aircrack-ng")
        except Exception as e:
            eprint(f"Error during bruteforce: {e}")
        finally:
            if self.process:
                try:
                    self.process.terminate()
                    self.process.wait(timeout=2)
                except:
                    self.process.kill()
    
    def bruteforce_with_custom(self, bssid, ssid_list):
        """
        Bruteforce using custom list of SSIDs.
        
        Args:
            bssid (str): Target router MAC address
            ssid_list (list): List of SSIDs to probe
        """
        try:
            iprint(f"Targeting router: {bssid}")
            iprint(f"Testing {len(ssid_list)} SSIDs")
            iprint("Starting ESSID bruteforce (Ctrl+C to stop)\n")
            time.sleep(1)
            
            found = []
            for idx, ssid in enumerate(ssid_list, 1):
                try:
                    # Use mdk4 to probe for each SSID
                    cmd = f"mdk4 {self.interface} p -t {bssid} -e {ssid} -s 50"
                    
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=3
                    )
                    
                    # Check if response received (mdk4 output indicates found)
                    if result.stdout or result.returncode == 0:
                        cprint(f"Found: {ssid}", GREEN)
                        found.append(ssid)
                    else:
                        cprint(f"Probing: {ssid}", CYAN)
                    
                    # Progress indicator
                    if idx % 5 == 0:
                        iprint(f"Progress: {idx}/{len(ssid_list)}")
                
                except KeyboardInterrupt:
                    wprint("\nBruteforce stopped by user")
                    break
                except subprocess.TimeoutExpired:
                    pass
                except Exception as e:
                    pass
            
            # Print results
            print()
            if found:
                sprint(f"Found {len(found)} hidden ESSID(s):")
                for ssid in found:
                    cprint(f"  • {ssid}", GREEN)
            else:
                wprint("No hidden ESSIDs found")
            
        except Exception as e:
            eprint(f"Error during bruteforce: {e}")
    
    def stop_bruteforce(self):
        """Terminate the bruteforce process."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except:
                self.process.kill()
    
    def display_mode_menu(self):
        """Display bruteforce mode selection."""
        print()
        cprint("╔════════════════════════════════════════════════════════╗", CYAN)
        cprint("║            SELECT BRUTEFORCE MODE                      ║", CYAN)
        cprint("╠════════════════════════════════════════════════════════╣", CYAN)
        cprint("║                                                        ║", CYAN)
        cprint("║  1) Wordlist Mode                                      ║", LIGHT_CYAN)
        cprint("║     Use common SSID list (recommended)                 ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  2) Custom SSIDs                                       ║", LIGHT_CYAN)
        cprint("║     Manually enter SSIDs to probe                      ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  0) Cancel                                             ║", YELLOW)
        cprint("║                                                        ║", CYAN)
        cprint("╚════════════════════════════════════════════════════════╝", CYAN)
    
    def run_interactive(self):
        """Interactive ESSID bruteforce menu."""
        while True:
            clear()
            cprint("╔════════════════════════════════════════════════════════╗", MAGENTA)
            cprint("║               ESSID BRUTEFORCE ATTACK                  ║", MAGENTA)
            cprint("╚════════════════════════════════════════════════════════╝", MAGENTA)
            print()
            cprint(f"Interface: {self.interface}", LIGHT_CYAN)
            cprint(f"Monitor Mode: ", LIGHT_CYAN, end='')
            sprint("Verified" if self.verify_monitor_mode() else "Not detected")
            print()
            
            bssid = cinput("Enter target router MAC (BSSID)", LIGHT_CYAN)
            if not bssid:
                break
            
            self.display_mode_menu()
            choice = cinput("Select mode", LIGHT_CYAN)
            
            if choice == "0":
                break
            elif choice == "1":
                wordlist_path = self.get_wordlist_path()
                if wordlist_path:
                    clear()
                    self.bruteforce_with_wordlist(bssid, wordlist_path)
                else:
                    eprint("Wordlist not found: common_ssids.txt")
            elif choice == "2":
                clear()
                cprint("Enter SSIDs to probe (one per line, empty line when done):", YELLOW)
                ssid_list = []
                while True:
                    ssid = cinput("SSID", LIGHT_CYAN)
                    if not ssid:
                        break
                    ssid_list.append(ssid)
                
                if ssid_list:
                    clear()
                    self.bruteforce_with_custom(bssid, ssid_list)
                else:
                    wprint("No SSIDs entered")
            else:
                wprint(f"Invalid option: {choice}")
                time.sleep(1)
            
            if choice in ["1", "2"]:
                input(f"\n{CYAN}Press Enter to continue...{RESET}")
