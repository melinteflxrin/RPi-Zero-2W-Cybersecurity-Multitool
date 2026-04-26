"""
BLE Device Scanner - Bluetooth Low Energy Device Discovery Tool

This module continuously scans for nearby Bluetooth Low Energy devices
and displays real-time information in a "Wall of Sheep" style table.

Uses the bleak library for proper BLE protocol support.
Features: Device names, RSSI, TX Power, distance estimation, company identification,
first seen/last seen timestamps, and persistent device tracking.
"""

import asyncio
import math
import time
import os
import yaml
from datetime import datetime
from ui import (cprint, iprint, wprint, eprint, sprint, cinput, 
                   RED, GREEN, CYAN, YELLOW, MAGENTA, WHITE, 
                   RESET, LIGHT_CYAN, clear)


class BLEDeviceScanner:
    """
    Comprehensive BLE device scanner with company identification,
    distance estimation, and persistent device tracking.
    """
    
    def __init__(self, scan_duration=None):
        """
        Initialize the BLE device scanner.
        
        Args:
            scan_duration (float): Duration for each scan in seconds (None = until Ctrl+C)
        """
        self.scan_duration = scan_duration
        self.devices = {}  # {mac: {name, rssi, tx_power, company, first_seen, last_seen, count}}
        self.running = True
        self.company_ids = self._load_company_ids()
    
    def _load_company_ids(self):
        """Load company identifiers from YAML file."""
        company_ids = {}
        
        # Try to load from company_identifiers.yaml file
        file_path = os.path.join(os.path.dirname(__file__), "company_identifiers.yaml")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Read file and sanitize problematic characters
                    content = f.read()
                    # Try to load the YAML
                    try:
                        data = yaml.safe_load(content)
                    except yaml.YAMLError as e:
                        # If YAML fails due to encoding, try to load line by line
                        wprint(f"Warning: YAML parsing issue, loading manually...")
                        for line in content.split('\n'):
                            line = line.strip()
                            if line.startswith('- value:'):
                                hex_str = line.replace('- value:', '').strip()
                                try:
                                    company_id = int(hex_str, 16)
                                    company_ids[company_id] = f"ID:{hex_str}"
                                except ValueError:
                                    pass
                            elif line.startswith('name:') and company_ids:
                                name = line.replace("name: '", "").replace("'", "").replace('name: "', '').replace('"', '')
                                if name:
                                    # Update last added ID with the name
                                    last_id = list(company_ids.keys())[-1] if company_ids else None
                                    if last_id:
                                        company_ids[last_id] = name
                        return company_ids if company_ids else self._get_fallback_ids()
                    
                    if data and 'company_identifiers' in data:
                        for entry in data['company_identifiers']:
                            try:
                                hex_id = entry.get('value', '')
                                name = entry.get('name', '')
                                
                                if hex_id and name:
                                    company_id = int(hex_id, 16)
                                    company_ids[company_id] = name
                            except (ValueError, AttributeError, TypeError):
                                continue
                    
                    if company_ids:
                        return company_ids
            except Exception as e:
                wprint(f"Warning: Could not load company_identifiers.yaml: {e}")
        
        return self._get_fallback_ids()
    
    def _get_fallback_ids(self):
        """Return fallback hardcoded company IDs."""
        return {
            0x004C: "Apple",
            0x006B: "Google",
            0x0059: "Nordic",
            0x02E5: "Gatt Company",
            0x0075: "Sennheiser",
            0x0006: "Microsoft",
            0x0001: "Ericsson",
            0x0005: "Broadcom",
            0x0009: "Infineon",
            0x000D: "Texas Instruments",
            0x000F: "Philips",
            0x0010: "LG Electronics",
            0x0014: "Lenovo",
            0x004F: "Caterpillar",
            0x0050: "Sony Ericsson",
            0x005B: "RealTek",
            0x005F: "Qualcomm",
        }
    
    def _get_company_name(self, company_id):
        """Get company name from manufacturer ID."""
        if company_id in self.company_ids:
            return self.company_ids[company_id]
        return f"Mfg:{company_id:04X}"
    
    def _calculate_distance(self, tx_power, rssi, propagation_constant=2):
        """
        Calculate estimated distance from TX power and RSSI.
        
        Args:
            tx_power (int): TX power in dBm (typically -20 to 10)
            rssi (int): RSSI value in dBm (negative)
            propagation_constant (int): Path loss exponent (2-4, default 2 for free space)
            
        Returns:
            float: Estimated distance in meters
        """
        if not tx_power or not rssi or tx_power == 0 or rssi == 0:
            return None
        
        try:
            tx_power = -abs(tx_power)
            rssi = -abs(rssi)
            distance = math.pow(10.0, (tx_power - rssi) / (10 * propagation_constant))
            return distance
        except:
            return None
    
    async def start_continuous_scan(self):
        """Start continuous BLE device scanning using bleak."""
        try:
            from bleak import BleakScanner, AdvertisementData, BLEDevice
        except ImportError:
            eprint("bleak library not found!")
            eprint("Install with: pip install bleak")
            eprint("Or create a virtual environment and install there")
            return
        
        try:
            iprint("Starting continuous BLE scan...")
            iprint("Press Ctrl+C to stop scanning\n")
            
            def display_table():
                """Display the devices table."""
                clear()
                print()
                cprint("╔════════════════════════════════════════════════════════════════════════════════════════╗", CYAN)
                cprint("║                                   BLE DEVICE SCANNER                                   ║", CYAN)
                cprint("╚════════════════════════════════════════════════════════════════════════════════════════╝", CYAN)
                print()
                
                # Header
                cprint(f"{'#':<3} {'MAC Address':<18} {'Name':<20} {'RSSI':<8} {'TX Pwr':<8} {'Dist(m)':<8} {'Company':<25} {'First Seen':<12} {'Last Seen':<12}", CYAN)
                cprint("─" * 140, CYAN)
                
                # Rows
                for idx, (mac, info) in enumerate(sorted(self.devices.items()), 1):
                    name = info['name'][:20] if info['name'] else "(unknown)"
                    rssi_str = f"{info['rssi']} dBm"
                    tx_str = f"{info['tx_power']} dBm" if info['tx_power'] else "N/A"
                    
                    # Calculate distance
                    distance = self._calculate_distance(info['tx_power'], info['rssi'])
                    dist_str = f"{distance:.1f}" if distance else "N/A"
                    
                    # Truncate company name to 23 chars with ellipsis
                    company = info['company'] if info['company'] else "Unknown"
                    if len(company) > 23:
                        company = company[:20] + "..."
                    
                    first_seen = info['first_seen'].strftime("%H:%M:%S") if info['first_seen'] else "N/A"
                    last_seen = info['last_seen'].strftime("%H:%M:%S") if info['last_seen'] else "N/A"
                    
                    # Color based on signal strength
                    if info['rssi'] > -50:
                        color = GREEN  # Strong signal
                    elif info['rssi'] > -70:
                        color = YELLOW  # Medium signal
                    else:
                        color = WHITE  # Weak signal
                    
                    cprint(f"{idx:<3} {mac:<18} {name:<20} {rssi_str:<8} {tx_str:<8} {dist_str:<8} {company:<25} {first_seen:<12} {last_seen:<12}", color)
                
                print()
                cprint(f"Total devices: {len(self.devices)}", CYAN)
            
            def detection_callback(device: BLEDevice, advertisement_data: AdvertisementData):
                """Callback for when a device is discovered."""
                mac = device.address
                name = device.name or advertisement_data.local_name or "(unknown)"
                rssi = advertisement_data.rssi or 0
                tx_power = advertisement_data.tx_power if hasattr(advertisement_data, 'tx_power') else None
                
                # Get company from manufacturer data
                company = None
                if hasattr(advertisement_data, 'manufacturer_data') and advertisement_data.manufacturer_data:
                    for company_id in advertisement_data.manufacturer_data.keys():
                        if company_id and company_id != 0:
                            company = self._get_company_name(company_id)
                            break
                
                now = datetime.now()
                
                # Track or update device (silent update, no spam)
                if mac not in self.devices:
                    self.devices[mac] = {
                        'name': name,
                        'rssi': rssi,
                        'tx_power': tx_power,
                        'company': company,
                        'first_seen': now,
                        'last_seen': now,
                        'count': 1
                    }
                else:
                    # Update existing device
                    self.devices[mac]['rssi'] = rssi
                    self.devices[mac]['last_seen'] = now
                    self.devices[mac]['count'] += 1
                    if name and name != "(unknown)":
                        self.devices[mac]['name'] = name
                    if company:
                        self.devices[mac]['company'] = company
                    if tx_power:
                        self.devices[mac]['tx_power'] = tx_power
            
            # Create scanner and run
            scanner = BleakScanner(detection_callback=detection_callback)
            
            async with scanner:
                last_display = 0
                while self.running:
                    try:
                        await asyncio.sleep(0.5)
                        now = time.time()
                        if now - last_display > 2:
                            display_table()
                            last_display = now
                    except KeyboardInterrupt:
                        break
            
            # Final display
            display_table()
            sprint("\nScan completed!")
            
        except Exception as e:
            eprint(f"Error during BLE scan: {e}")
            eprint("Make sure Bluetooth is enabled and available on your system")
    
    def run(self):
        """Main entry point for the BLE device scanner."""

        try:
            asyncio.run(self.start_continuous_scan())
        except KeyboardInterrupt:
            wprint("\nScan interrupted by user")
            self.running = False

