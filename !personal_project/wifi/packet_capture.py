"""
Packet Capture - WiFi Traffic Recording Tool

This module captures WiFi network traffic to libpcap (.cap) files
for analysis with tools like Wireshark.
"""

import subprocess
import os
import time
from datetime import datetime
from ui import (cprint, iprint, wprint, eprint, sprint, cinput, 
                   RED, GREEN, CYAN, YELLOW, MAGENTA, WHITE, 
                   RESET, LIGHT_CYAN, clear)


class PacketCapture:
    """
    Captures WiFi network traffic to .cap files for forensic analysis
    and network monitoring.
    """
    
    def __init__(self, interface):
        """
        Initialize the packet capture tool.
        
        Args:
            interface (str): WiFi interface in monitor mode (e.g., "wlan1mon")
        """
        self.interface = interface
        self.process = None
        self.capture_file = None
    
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
    
    def get_default_capture_path(self):
        """
        Generate a default capture file path with timestamp.
        
        Returns:
            str: Path to capture file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create captures folder in the wifi module directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_dir = os.path.join(script_dir, "captures")
        
        # Create directory if it doesn't exist
        try:
            os.makedirs(default_dir, exist_ok=True)
        except Exception as e:
            wprint(f"Could not create directory: {e}")
            default_dir = "/tmp"
        
        return os.path.join(default_dir, f"capture_{timestamp}")
    
    def validate_output_path(self, user_path):
        """
        Validate and prepare output path for capture file.
        
        Args:
            user_path (str): User-provided path
            
        Returns:
            str: Valid file path or None if invalid
        """
        # Expand home directory
        path = os.path.expanduser(user_path)
        
        # Create parent directory if needed
        parent_dir = os.path.dirname(path)
        if parent_dir and not os.path.exists(parent_dir):
            try:
                os.makedirs(parent_dir, exist_ok=True)
                iprint(f"Created directory: {parent_dir}")
            except Exception as e:
                eprint(f"Cannot create directory: {e}")
                return None
        
        # Check write permissions
        test_dir = parent_dir if parent_dir else "."
        if not os.access(test_dir, os.W_OK):
            eprint(f"No write permission for: {test_dir}")
            return None
        
        return path
    
    def start_capture(self, output_path):
        """
        Start capturing WiFi packets to file.
        
        Args:
            output_path (str): Path to save .cap file
        """
        try:
            if not self.verify_monitor_mode():
                eprint(f"Interface {self.interface} is not in monitor mode!")
                return False
            
            iprint(f"Starting packet capture...")
            iprint(f"Interface: {self.interface}")
            iprint(f"Output file: {output_path}")
            iprint(f"Press Ctrl+C to stop capture\n")
            time.sleep(1)
            
            # Run airodump-ng to capture packets
            cmd = f"airodump-ng {self.interface} -w {output_path}"
            
            self.process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            self.capture_file = output_path
            
            # Monitor capture progress
            while self.process:
                try:
                    output = self.process.stdout.readline()
                    if output:
                        cprint(output.rstrip(), CYAN)
                    
                    if self.process.poll() is not None:
                        break
                except KeyboardInterrupt:
                    self.stop_capture()
                    break
            
            return True
            
        except FileNotFoundError:
            eprint("airodump-ng not found!")
            eprint("Install aircrack-ng: sudo apt-get install aircrack-ng")
            return False
        except Exception as e:
            eprint(f"Error during capture: {e}")
            return False
    
    def stop_capture(self):
        """Stop the ongoing packet capture."""
        if self.process:
            try:
                wprint("\nStopping capture...")
                self.process.terminate()
                self.process.wait(timeout=3)
                
                # List captured files
                if self.capture_file:
                    parent_dir = os.path.dirname(self.capture_file)
                    filename = os.path.basename(self.capture_file)
                    
                    try:
                        files = [f for f in os.listdir(parent_dir) if filename in f and f.endswith('.cap')]
                        if files:
                            sprint(f"\nCapture files saved:")
                            for cap_file in files:
                                full_path = os.path.join(parent_dir, cap_file)
                                file_size = os.path.getsize(full_path)
                                size_mb = file_size / (1024 * 1024)
                                cprint(f"  • {full_path} ({size_mb:.2f} MB)", GREEN)
                    except Exception as e:
                        wprint(f"Could not list capture files: {e}")
                
            except subprocess.TimeoutExpired:
                wprint("Force stopping capture...")
                self.process.kill()
            except Exception as e:
                eprint(f"Error stopping capture: {e}")
    
    def run_interactive(self):
        """Run capture with interactive menu."""
        clear()
        cprint("╔════════════════════════════════════════════════════════╗", CYAN)
        cprint("║           PACKET CAPTURE CONFIGURATION                 ║", CYAN)
        cprint("╚════════════════════════════════════════════════════════╝", CYAN)
        print()
        
        cprint("Available options:", YELLOW)
        cprint("  1) Use default path (wifi/captures/capture_TIMESTAMP)", WHITE)
        cprint("  2) Enter custom path", WHITE)
        print()
        
        choice = cinput("Select option", LIGHT_CYAN)
        
        if choice == "1":
            output_path = self.get_default_capture_path()
            iprint(f"Using path: {output_path}")
        elif choice == "2":
            custom_path = cinput("Enter capture file path", LIGHT_CYAN)
            if not custom_path:
                wprint("No path provided, using default")
                output_path = self.get_default_capture_path()
            else:
                output_path = self.validate_output_path(custom_path)
                if not output_path:
                    eprint("Invalid path, using default")
                    output_path = self.get_default_capture_path()
        else:
            wprint("Invalid option, using default")
            output_path = self.get_default_capture_path()
        
        print()
        self.start_capture(output_path)
