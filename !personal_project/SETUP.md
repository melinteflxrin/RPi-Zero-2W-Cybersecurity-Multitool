# Setup Instructions

## STEP 1: System Packages

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip python3-dev
sudo apt-get install -y git curl wget
sudo apt-get install -y bluez bluez-tools
sudo apt-get install -y python3-bluez python3-dbus libbluetooth-dev
sudo apt-get install -y aircrack-ng mdk4 wifite
sudo apt-get install -y dnsmasq hostapd iptables
sudo apt install -y python3-bleak python3-yaml
sudo apt-get install -y arp-scan hping3
```

## STEP 2: Initialize Bluetooth Adapter

```bash
sudo rfkill list                    
sudo rfkill unblock bluetooth       
sudo rfkill unblock all

sudo hciconfig hci0 reset           
hciconfig hci0                      
sudo btmgmt power on                
sudo btmgmt connectable on          
sudo btmgmt discov on               
sudo btmgmt pairable on             
```

## STEP 3: WiFi Adapter Setup (TP-Link Archer T2U PLUS RTL8821AU)

```bash
sudo apt-get update
sudo apt-get install -y git build-essential dkms bc linux-headers-generic

cd ~
git clone https://github.com/morrownr/8821au-20210708.git
cd 8821au-20210708
sudo ./install-driver.sh

sudo reboot
```

```bash
sudo nmcli device set wlan1 managed no
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

## STEP 4: Cloudflare Tunnel Setup

```bash
wget https://github.com/cloudflare/cloudflared/releases/download/2024.12.0/cloudflared-linux-arm64
chmod +x cloudflared-linux-arm64
sudo mv cloudflared-linux-arm64 /usr/local/bin/cloudflared

cloudflared --version
```
