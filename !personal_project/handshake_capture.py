import subprocess
import time
import os
from ui import cprint, iprint, wprint, eprint, cinput, CYAN, GREEN, RED, YELLOW, WHITE, RESET

class HandshakeCapture:
    def __init__(self, interface="wlan1mon"):
        self.monitor_interface = interface
        self.capture_file = None
        self.hccapx_file = None
        
    def scan_networks(self):
        """Scan for available WiFi networks"""
        iprint("Scanning for WiFi networks...")
        
        try:
            # Scan networks
            iprint("Networks found:")
            result = subprocess.check_output(
                f"sudo airodump-ng {self.monitor_interface} --output-format csv -w /tmp/scan --write-interval 1",
                shell=True,
                stderr=subprocess.DEVNULL,
                timeout=5
            )
        except subprocess.TimeoutExpired:
            # Expected - airodump-ng runs indefinitely
            pass
        except Exception as e:
            eprint(f"Scan error: {e}")
            return None
        
        # Parse scan results
        networks = self._parse_networks("/tmp/scan-01.csv")
        return networks
    
    def _parse_networks(self, csv_file):
        """Parse airodump-ng CSV output"""
        networks = []
        try:
            if not os.path.exists(csv_file):
                return networks
            
            with open(csv_file, 'r') as f:
                lines = f.readlines()
            
            in_ap_section = False
            for line in lines:
                line = line.strip()
                if not line or line.startswith("BSSID"):
                    in_ap_section = True
                    continue
                if in_ap_section and line and not line.startswith("Station"):
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) >= 7:
                        bssid = parts[0]
                        power = parts[1]
                        channel = parts[3]
                        ssid = parts[13] if len(parts) > 13 else "Hidden"
                        if bssid != "BSSID" and bssid:
                            networks.append({
                                "bssid": bssid,
                                "power": power,
                                "channel": channel,
                                "ssid": ssid
                            })
            
            return networks
        except Exception as e:
            eprint(f"Error parsing networks: {e}")
            return []
    
    def display_networks(self, networks):
        """Display available networks"""
        if not networks:
            eprint("No networks found")
            return None
        
        cprint("\n" + "="*80 + "\n", CYAN)
        for i, net in enumerate(networks, 1):
            cprint(f"{i}) SSID: {net['ssid']:<30} | BSSID: {net['bssid']} | CH: {net['channel']} | PWR: {net['power']}", GREEN)
        cprint("="*80 + "\n", CYAN)
        
        choice = int(cinput("Select network number")) - 1
        if 0 <= choice < len(networks):
            return networks[choice]
        eprint("Invalid choice")
        return None
    
    def capture_handshake(self, target_network):
        """Capture handshake from target network"""
        bssid = target_network['bssid']
        channel = target_network['channel']
        ssid = target_network['ssid']
        
        iprint(f"Starting handshake capture on {ssid} ({bssid}) - Channel {channel}")
        cprint("\nWaiting for a client to connect and authenticate...\n", YELLOW)
        cprint("This is a PASSIVE capture - no deauth frames will be sent.\n", YELLOW)
        cprint("The handshake will be captured when a device naturally connects to the network.\n", YELLOW)
        
        output_file = f"/tmp/handshake_{ssid.replace(' ', '_')}"
        
        try:
            # Run airodump-ng to capture handshake
            cmd = f"sudo airodump-ng -c {channel} --bssid {bssid} -w {output_file} {self.monitor_interface}"
            
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            iprint("Capture started. Press Ctrl+C when you see [WPA handshake: BSSID] in the output above...")
            
            try:
                process.wait()
            except KeyboardInterrupt:
                iprint("Stopping capture...")
                process.terminate()
                time.sleep(1)
            
            # Check if handshake was captured
            cap_file = f"{output_file}-01.cap"
            if os.path.exists(cap_file):
                iprint(f"Capture file saved: {cap_file}")
                self.capture_file = cap_file
                return cap_file
            else:
                eprint("Capture file not found")
                return None
                
        except Exception as e:
            eprint(f"Error during capture: {e}")
            return None
    
    def convert_to_hccapx(self, cap_file):
        """Convert .cap file to .hccapx format"""
        iprint("Converting to .hccapx format...")
        
        try:
            hccapx_file = cap_file.replace(".cap", ".hccapx")
            
            # Use hcxpcapng if available, otherwise hcxpcapng-to-pmk
            try:
                subprocess.run(
                    ["sudo", "hcxpcapng", "-o", hccapx_file, cap_file],
                    check=True,
                    capture_output=True
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Fallback
                subprocess.run(
                    ["sudo", "hcxpcapng-to-pmk", cap_file, "-o", hccapx_file],
                    check=True,
                    capture_output=True
                )
            
            if os.path.exists(hccapx_file):
                iprint(f"Conversion complete: {hccapx_file}")
                self.hccapx_file = hccapx_file
                return hccapx_file
            else:
                eprint("Conversion failed")
                return None
                
        except subprocess.CalledProcessError as e:
            eprint(f"Conversion error: {e}")
            eprint("Make sure hcxtools is installed: sudo apt install hcxtools")
            return None
        except Exception as e:
            eprint(f"Error: {e}")
            return None
    
    def run_interactive(self):
        """Run the handshake capture tool interactively"""
        cprint("\n[*] WiFi Handshake Capture\n", CYAN)
        
        try:
            # Scan networks
            networks = self.scan_networks()
            if not networks:
                eprint("No networks found or scan failed")
                return
            
            # Select target
            target = self.display_networks(networks)
            if not target:
                return
            
            # Capture handshake
            cap_file = self.capture_handshake(target)
            if not cap_file:
                eprint("Failed to capture handshake")
                return
            
            # Convert to hccapx
            hccapx_file = self.convert_to_hccapx(cap_file)
            if not hccapx_file:
                eprint("Failed to convert to hccapx")
                return
            
            cprint(f"\n✓ Handshake capture complete!\n", GREEN)
            cprint(f"File: {hccapx_file}\n", GREEN)
            cprint(f"Use this file with option 28 (Crack 4-way Handshake) in Jammy\n", YELLOW)
            
        except KeyboardInterrupt:
            iprint("Cancelled")
        except Exception as e:
            eprint(f"Error: {e}")

if __name__ == "__main__":
    # Allow running directly for testing
    import sys
    monitor_iface = sys.argv[1] if len(sys.argv) > 1 else "wlan1mon"
    capture = HandshakeCapture(monitor_iface)
    capture.run_interactive()
