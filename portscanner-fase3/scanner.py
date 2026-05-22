import socket
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from datetime import datetime
import csv

# DICIONÁRIO DE SERVIÇOS (COMPLETO ATÉ 5609)
SERVICOS = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP",
    53: "DNS", 67: "DHCP", 68: "DHCP", 69: "TFTP", 80: "HTTP",
    88: "Kerberos", 110: "POP3", 111: "RPC", 119: "NNTP", 123: "NTP",
    135: "RPC", 137: "NETBIOS-NS", 138: "NETBIOS-DGM", 139: "NETBIOS-SSN",
    143: "IMAP", 161: "SNMP", 162: "SNMP-TRAP", 179: "BGP", 194: "IRC",
    389: "LDAP", 443: "HTTPS", 445: "SMB", 465: "SMTPS", 514: "SYSLOG",
    515: "LPD", 520: "RIP", 546: "DHCPv6", 547: "DHCPv6", 554: "RTSP",
    587: "SMTP", 631: "IPP", 636: "LDAPS", 873: "RSYNC", 990: "FTPS",
    993: "IMAPS", 995: "POP3S", 1025: "NFS", 1080: "SOCKS", 1194: "OpenVPN",
    1214: "Kazaa", 1241: "Nessus", 1311: "Dell OpenManage", 1337: "WASTE",
    1433: "MSSQL", 1434: "MSSQL", 1494: "Citrix", 1512: "WINS", 1521: "ORACLE-DB",
    1524: "BACKDOOR!", 1723: "PPTP", 1755: "MMS", 1812: "RADIUS", 1813: "RADIUS",
    1863: "MSNP", 1985: "HSRP", 1998: "X.25", 2000: "Cisco SCCP", 2049: "NFS",
    2082: "cPanel", 2083: "cPanel SSL", 2086: "WHM", 2087: "WHM SSL",
    2095: "cPanel Webmail", 2096: "cPanel Webmail SSL", 2100: "Amiga",
    2181: "ZooKeeper", 2200: "Tux", 2210: "NOAA", 2222: "DirectAdmin",
    2301: "Compaq", 2381: "Compaq", 2480: "OrientDB", 2483: "Oracle",
    2484: "Oracle", 2522: "WinDev", 2525: "SMTP", 2598: "Citrix", 2601: "Zebra",
    2604: "Zebra", 2710: "XBT Tracker", 2800: "HTTP", 2809: "CORBA", 3000: "Ruby",
    3001: "CouchDB", 3006: "GitLab", 3030: "NetPanzer", 3050: "Interbase",
    3074: "Xbox LIVE", 3128: "HTTP Proxy", 3260: "iSCSI", 3268: "LDAP",
    3269: "LDAP SSL", 3283: "Apple Remote", 3305: "MySQL", 3306: "MYSQL",
    3310: "MySQL", 3333: "Eggdrop", 3389: "RDP", 3396: "Novell", 3412: "xmlBlaster",
    3421: "Xware", 3422: "Xware", 3443: "Proxmox", 3456: "VAT", 3483: "Slim",
    3493: "UPS", 3500: "ClickTracks", 3522: "smartclub", 3527: "msg", 3535: "SMTP",
    3544: "Teredo", 3579: "Mesh", 3580: "Mesh", 3659: "Apple SASL", 3667: "SAK",
    3671: "EzPipe", 3689: "DAAP", 3690: "SVN", 3702: "WS-Discovery",
    3724: "World of Warcraft", 3725: "Netia", 3737: "Netia", 3741: "Netia",
    3749: "Cisco", 3784: "Ventrilo", 3785: "Ventrilo", 4000: "ICQ", 4662: "eMule",
    4672: "eMule", 4899: "Radmin", 5000: "UPnP", 5001: "UPnP", 5002: "UPnP",
    5003: "UPnP", 5004: "UPnP", 5005: "UPnP", 5006: "UPnP", 5007: "UPnP",
    5008: "UPnP", 5009: "UPnP", 5010: "UPnP", 5011: "UPnP", 5012: "UPnP",
    5013: "UPnP", 5014: "UPnP", 5015: "UPnP", 5016: "UPnP", 5017: "UPnP",
    5018: "UPnP", 5019: "UPnP", 5020: "UPnP", 5021: "UPnP", 5022: "UPnP",
    5023: "UPnP", 5024: "UPnP", 5025: "UPnP", 5026: "UPnP", 5027: "UPnP",
    5028: "UPnP", 5029: "UPnP", 5030: "UPnP", 5031: "UPnP", 5032: "UPnP",
    5033: "UPnP", 5034: "UPnP", 5035: "UPnP", 5036: "UPnP", 5037: "UPnP",
    5038: "UPnP", 5039: "UPnP", 5040: "UPnP", 5041: "UPnP", 5042: "UPnP",
    5043: "UPnP", 5044: "UPnP", 5045: "UPnP", 5046: "UPnP", 5047: "UPnP",
    5048: "UPnP", 5049: "UPnP", 5050: "UPnP", 5051: "UPnP", 5052: "UPnP",
    5053: "UPnP", 5054: "UPnP", 5055: "UPnP", 5056: "UPnP", 5057: "UPnP",
    5058: "UPnP", 5059: "UPnP", 5060: "SIP", 5061: "SIP-TLS", 5222: "XMPP",
    5223: "XMPP", 5353: "MDNS", 5355: "LLMNR", 5432: "POSTGRESQL",
    5500: "VNC", 5501: "VNC", 5502: "VNC", 5503: "VNC", 5504: "VNC",
    5505: "VNC", 5506: "VNC", 5507: "VNC", 5508: "VNC", 5509: "VNC",
    5510: "VNC", 5511: "VNC", 5512: "VNC", 5513: "VNC", 5514: "VNC",
    5515: "VNC", 5516: "VNC", 5517: "VNC", 5518: "VNC", 5519: "VNC",
    5520: "VNC", 5521: "VNC", 5522: "VNC", 5523: "VNC", 5524: "VNC",
    5525: "VNC", 5526: "VNC", 5527: "VNC", 5528: "VNC", 5529: "VNC",
    5530: "VNC", 5531: "VNC", 5532: "VNC", 5533: "VNC", 5534: "VNC",
    5535: "VNC", 5536: "VNC", 5537: "VNC", 5538: "VNC", 5539: "VNC",
    5540: "VNC", 5541: "VNC", 5542: "VNC", 5543: "VNC", 5544: "VNC",
    5545: "VNC", 5546: "VNC", 5547: "VNC", 5548: "VNC", 5549: "VNC",
    5550: "VNC", 5551: "VNC", 5552: "VNC", 5553: "VNC", 5554: "VNC",
    5555: "VNC", 5556: "VNC", 5557: "VNC", 5558: "VNC", 5559: "VNC",
    5560: "VNC", 5561: "VNC", 5562: "VNC", 5563: "VNC", 5564: "VNC",
    5565: "VNC", 5566: "VNC", 5567: "VNC", 5568: "VNC", 5569: "VNC",
    5570: "VNC", 5571: "VNC", 5572: "VNC", 5573: "VNC", 5574: "VNC",
    5575: "VNC", 5576: "VNC", 5577: "VNC", 5578: "VNC", 5579: "VNC",
    5580: "VNC", 5581: "VNC", 5582: "VNC", 5583: "VNC", 5584: "VNC",
    5585: "VNC", 5586: "VNC", 5587: "VNC", 5588: "VNC", 5589: "VNC",
    5590: "VNC", 5591: "VNC", 5592: "VNC", 5593: "VNC", 5594: "VNC",
    5595: "VNC", 5596: "VNC", 5597: "VNC", 5598: "VNC", 5599: "VNC",
    5600: "VNC", 5601: "VNC", 5602: "VNC", 5603: "VNC", 5604: "VNC",
    5605: "VNC", 5606: "VNC", 5607: "VNC", 5608: "VNC", 5609: "VNC"
}

class PortScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner - SENAI (Fase 3)")
        self.root.geometry("950x750")
        self.root.resizable(False, False)
        
        # Configuração de cores - Azul Marinho
        self.bg_color = "#0a1628"
        self.bg_sec_color = "#0f1f33"
        self.fg_color = "#e0e7f0"
        self.accent_color = "#1e5799"
        self.accent_hover = "#2c6eb3"
        self.success_color = "#27ae60"
        self.error_color = "#e74c3c"
        self.warning_color = "#f39c12"
        self.info_color = "#3498db"
        self.backdoor_color = "#e74c3c"
        
        self.root.configure(bg=self.bg_color)
        
        # Configurações do scanner
        self.MAX_THREADS = 200
        self.TIMEOUT = 1.5
        self.is_scanning = False
        self.scan_thread = None
        self.portas_abertas = []
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Title.TLabel",
                       background=self.bg_color,
                       foreground=self.fg_color,
                       font=("Arial", 20, "bold"))
        
        style.configure("Subtitle.TLabel",
                       background=self.bg_color,
                       foreground="#a0abb8",
                       font=("Arial", 10))
        
        style.configure("Info.TLabel",
                       background=self.bg_color,
                       foreground=self.fg_color,
                       font=("Arial", 11))
        
        style.configure("Main.TFrame", background=self.bg_color)
        style.configure("Input.TFrame", background=self.bg_sec_color)
        style.configure("Result.TFrame", background=self.bg_sec_color)
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, text="PORT SCANNER - SENAI", 
                               style="Title.TLabel")
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(main_frame, 
                                  text="Fase 3 - Scanner Avançado com Multithreading e Banner Grabbing",
                                  style="Subtitle.TLabel")
        subtitle_label.pack(pady=(0, 25))
        
        # Frame de entrada
        input_frame = ttk.Frame(main_frame, style="Input.TFrame")
        input_frame.pack(fill=tk.X, pady=10, padx=10)
        
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Host
        host_label = ttk.Label(input_frame, text="Host / IP:", style="Info.TLabel")
        host_label.grid(row=0, column=0, sticky=tk.W, pady=8, padx=10)
        
        self.host_entry = ttk.Entry(input_frame, width=35, font=("Arial", 11))
        self.host_entry.grid(row=0, column=1, pady=8, padx=10, sticky="ew")
        self.host_entry.insert(0, "127.0.0.1")
        
        # Porta inicial
        start_label = ttk.Label(input_frame, text="Porta Inicial:", style="Info.TLabel")
        start_label.grid(row=1, column=0, sticky=tk.W, pady=8, padx=10)
        
        self.start_entry = ttk.Entry(input_frame, width=20, font=("Arial", 11))
        self.start_entry.grid(row=1, column=1, pady=8, padx=10, sticky="w")
        self.start_entry.insert(0, "1")
        
        # Porta final
        end_label = ttk.Label(input_frame, text="Porta Final:", style="Info.TLabel")
        end_label.grid(row=2, column=0, sticky=tk.W, pady=8, padx=10)
        
        self.end_entry = ttk.Entry(input_frame, width=20, font=("Arial", 11))
        self.end_entry.grid(row=2, column=1, pady=8, padx=10, sticky="w")
        self.end_entry.insert(0, "1000")
        
        # Timeout
        timeout_label = ttk.Label(input_frame, text="Timeout (segundos):", style="Info.TLabel")
        timeout_label.grid(row=3, column=0, sticky=tk.W, pady=8, padx=10)
        
        self.timeout_entry = ttk.Entry(input_frame, width=20, font=("Arial", 11))
        self.timeout_entry.grid(row=3, column=1, pady=8, padx=10, sticky="w")
        self.timeout_entry.insert(0, "1.5")
        
        # Threads
        threads_label = ttk.Label(input_frame, text="Máx. Threads:", style="Info.TLabel")
        threads_label.grid(row=4, column=0, sticky=tk.W, pady=8, padx=10)
        
        self.threads_entry = ttk.Entry(input_frame, width=20, font=("Arial", 11))
        self.threads_entry.grid(row=4, column=1, pady=8, padx=10, sticky="w")
        self.threads_entry.insert(0, "200")
        
        # Banner Grabbing
        self.banner_var = tk.BooleanVar(value=True)
        banner_check = tk.Checkbutton(input_frame, text="Capturar Banner (Banner Grabbing)",
                                     variable=self.banner_var,
                                     bg=self.bg_sec_color,
                                     fg=self.fg_color,
                                     selectcolor=self.bg_sec_color,
                                     font=("Arial", 10))
        banner_check.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=8, padx=10)
        
        # Botões
        button_frame = ttk.Frame(main_frame, style="Main.TFrame")
        button_frame.pack(fill=tk.X, pady=15)
        
        self.scan_button = tk.Button(button_frame, text="INICIAR SCAN",
                                    command=self.start_scan,
                                    bg=self.accent_color, fg="white",
                                    font=("Arial", 12, "bold"),
                                    padx=30, pady=8, cursor="hand2",
                                    relief=tk.RAISED, borderwidth=0,
                                    activebackground=self.accent_hover)
        self.scan_button.pack(pady=5)
        
        self.clear_button = tk.Button(button_frame, text="LIMPAR RESULTADOS",
                                     command=self.clear_results,
                                     bg="#2c3e50", fg=self.fg_color,
                                     font=("Arial", 10), padx=20, pady=5,
                                     cursor="hand2", relief=tk.RAISED, borderwidth=0)
        self.clear_button.pack(pady=5)
        
        self.save_button = tk.Button(button_frame, text="SALVAR RESULTADOS",
                                    command=self.save_results,
                                    bg="#2c3e50", fg=self.fg_color,
                                    font=("Arial", 10), padx=20, pady=5,
                                    cursor="hand2", relief=tk.RAISED, borderwidth=0)
        self.save_button.pack(pady=5)
        
        # Progresso
        self.progress_frame = ttk.Frame(main_frame, style="Main.TFrame")
        self.progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_label = tk.Label(self.progress_frame, text="", bg=self.bg_color, fg=self.fg_color, font=("Arial", 9))
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate', length=500)
        
        # Resultados
        result_frame = ttk.Frame(main_frame, style="Result.TFrame")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_text = tk.Text(result_frame, bg="#0c1a2e", fg=self.fg_color,
                                  font=("Consolas", 10), wrap=tk.WORD,
                                  relief=tk.FLAT, padx=15, pady=15)
        
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tags de cor
        self.result_text.tag_config("success", foreground=self.success_color)
        self.result_text.tag_config("error", foreground=self.error_color)
        self.result_text.tag_config("warning", foreground=self.warning_color)
        self.result_text.tag_config("info", foreground=self.info_color)
        self.result_text.tag_config("backdoor", foreground=self.backdoor_color, font=("Consolas", 10, "bold"))
        self.result_text.tag_config("title", foreground=self.accent_color, font=("Consolas", 11, "bold"))
        
        # Status
        self.status_label = tk.Label(self.root, text="Pronto para escanear...",
                                    bg=self.bg_color, fg=self.fg_color,
                                    font=("Arial", 9), anchor=tk.W,
                                    padx=20, pady=5)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
    def get_service_name(self, port):
        return SERVICOS.get(port, "DESCONHECIDO")
    
    def grab_banner(self, host, port, timeout=3):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            sock.send(b"\n")
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            banner = banner.replace('\r', ' ').replace('\n', ' ')[:150]
            return banner
        except:
            return None
    
    def check_port(self, host, port, timeout):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            resultado = sock.connect_ex((host, port))
            sock.close()
            return resultado == 0
        except:
            return False
    
    def log_message(self, message, tag=None):
        self.result_text.insert(tk.END, message + "\n", tag)
        self.result_text.see(tk.END)
        self.root.update()
    
    def clear_results(self):
        self.result_text.delete(1.0, tk.END)
        self.portas_abertas = []
        self.log_message("=" * 70, "title")
        self.log_message("            NOVA VARREDURA INICIADA", "title")
        self.log_message("=" * 70, "title")
    
    def scan_single_port(self, host, port, timeout, capture_banner):
        self.log_message(f"\n[INFO] Verificando porta {port}...", "info")
        
        if self.check_port(host, port, timeout):
            servico = self.get_service_name(port)
            self.log_message(f"[+] PORTA {port} ABERTA - {servico}", "success" if servico != "BACKDOOR!" else "backdoor")
            
            if capture_banner:
                banner = self.grab_banner(host, port, timeout)
                if banner:
                    self.log_message(f"   Banner: {banner}", "info")
            return True
        else:
            self.log_message(f"[-] PORTA {port} FECHADA ou FILTRADA", "error")
            return False
    
    def scan_port_range(self, host, start_port, end_port, timeout, max_threads, capture_banner):
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        portas_abertas = []
        total = end_port - start_port + 1
        completadas = 0
        
        self.log_message(f"\n[INFO] Host alvo: {host}", "info")
        self.log_message(f"[INFO] Range: {start_port} - {end_port}", "info")
        self.log_message(f"[INFO] Total de portas: {total}", "info")
        self.log_message(f"[INFO] Timeout: {timeout} segundos", "info")
        self.log_message(f"[INFO] Threads: {max_threads}", "info")
        self.log_message(f"[INFO] Banner Grabbing: {'Sim' if capture_banner else 'Nao'}", "info")
        self.log_message("-" * 70, "warning")
        
        inicio_tempo = time.time()
        
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = {}
            for porta in range(start_port, end_port + 1):
                if not self.is_scanning:
                    break
                future = executor.submit(self.check_port, host, porta, timeout)
                futures[future] = porta
            
            for future in as_completed(futures):
                if not self.is_scanning:
                    break
                    
                porta = futures[future]
                completadas += 1
                
                percentual = (completadas / total) * 100
                self.progress_bar['value'] = percentual
                self.progress_label.config(text=f"Progresso: {completadas}/{total} ({percentual:.1f}%)")
                self.root.update()
                
                if future.result():
                    servico = self.get_service_name(porta)
                    portas_abertas.append({'porta': porta, 'servico': servico, 'banner': None})
                    
                    if capture_banner:
                        banner = self.grab_banner(host, porta, timeout)
                        if banner:
                            portas_abertas[-1]['banner'] = banner
                            self.log_message(f"[+] PORTA {porta:5d} ABERTA - {servico} → Banner: {banner[:80]}", 
                                           "success" if servico != "BACKDOOR!" else "backdoor")
                        else:
                            self.log_message(f"[+] PORTA {porta:5d} ABERTA - {servico}", 
                                           "success" if servico != "BACKDOOR!" else "backdoor")
                    else:
                        self.log_message(f"[+] PORTA {porta:5d} ABERTA - {servico}", 
                                       "success" if servico != "BACKDOOR!" else "backdoor")
        
        tempo_total = time.time() - inicio_tempo
        return portas_abertas, tempo_total, total
    
    def run_scan(self, host, start_port, end_port, timeout, max_threads, capture_banner):
        try:
            if start_port == end_port:
                self.scan_single_port(host, start_port, timeout, capture_banner)
                self.portas_abertas = [{'porta': start_port, 'servico': self.get_service_name(start_port), 'banner': None}]
                if capture_banner and self.check_port(host, start_port, timeout):
                    banner = self.grab_banner(host, start_port, timeout)
                    if banner:
                        self.portas_abertas[0]['banner'] = banner
                tempo_total = 0
                total = 1
            else:
                self.portas_abertas, tempo_total, total = self.scan_port_range(
                    host, start_port, end_port, timeout, max_threads, capture_banner
                )
            
            if not self.is_scanning:
                self.log_message("\n[!] SCAN INTERROMPIDO PELO USUÁRIO", "warning")
                return
            
            self.log_message("\n" + "=" * 70, "title")
            self.log_message("                 RESUMO DA VARREDURA", "title")
            self.log_message("=" * 70, "title")
            self.log_message(f"Host alvo:        {host}", "info")
            self.log_message(f"Range varrido:    {start_port} - {end_port}", "info")
            self.log_message(f"Total portas:     {total}", "info")
            self.log_message(f"Portas abertas:   {len(self.portas_abertas)}", "success" if self.portas_abertas else "warning")
            self.log_message(f"Tempo total:      {tempo_total:.2f} segundos", "info")
            
            if self.portas_abertas:
                self.log_message("\n--- PORTAS ABERTAS ENCONTRADAS ---", "success")
                for p in self.portas_abertas:
                    critico = "" if p['servico'] == "BACKDOOR!" else "  "
                    self.log_message(f"  {critico} Porta {p['porta']:5d} : {p['servico']}", 
                                   "backdoor" if p['servico'] == "BACKDOOR!" else "success")
                    if p.get('banner'):
                        self.log_message(f"         Banner: {p['banner'][:100]}", "info")
            else:
                self.log_message("\n[!] Nenhuma porta aberta encontrada.", "warning")
            
            self.log_message("=" * 70, "title")
            self.status_label.config(text="Scan finalizado com sucesso!")
            
        except socket.gaierror:
            self.log_message(f"[ERRO] Host '{host}' não encontrado ou inválido", "error")
        except Exception as e:
            self.log_message(f"[ERRO] {str(e)}", "error")
        finally:
            self.scan_complete()
    
    def start_scan(self):
        if self.is_scanning:
            self.stop_scan()
            return
        
        self.clear_results()
        
        host = self.host_entry.get().strip()
        if not host:
            messagebox.showerror("Erro", "Digite um host/IP válido!")
            return
        
        try:
            start_port = int(self.start_entry.get().strip())
            end_port = int(self.end_entry.get().strip())
            timeout = float(self.timeout_entry.get().strip())
            max_threads = int(self.threads_entry.get().strip())
            
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                raise ValueError
            if timeout <= 0:
                raise ValueError
            if max_threads < 1 or max_threads > 500:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos!\nPortas: 1-65535\nTimeout: >0\nThreads: 1-500")
            return
        
        self.is_scanning = True
        self.scan_button.config(text="PARAR SCAN", bg=self.error_color)
        self.clear_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.host_entry.config(state=tk.DISABLED)
        self.start_entry.config(state=tk.DISABLED)
        self.end_entry.config(state=tk.DISABLED)
        self.timeout_entry.config(state=tk.DISABLED)
        self.threads_entry.config(state=tk.DISABLED)
        
        self.progress_bar.pack(pady=5)
        self.progress_bar['value'] = 0
        
        self.status_label.config(text="Escaneando portas...")
        
        self.scan_thread = threading.Thread(
            target=self.run_scan,
            args=(host, start_port, end_port, timeout, max_threads, self.banner_var.get()),
            daemon=True
        )
        self.scan_thread.start()
    
    def stop_scan(self):
        self.is_scanning = False
        self.status_label.config(text="Parando scan...")
        self.log_message("\n[!] Solicitando parada do scan...", "warning")
    
    def scan_complete(self):
        self.is_scanning = False
        self.scan_button.config(text="INICIAR SCAN", bg=self.accent_color)
        self.clear_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        self.host_entry.config(state=tk.NORMAL)
        self.start_entry.config(state=tk.NORMAL)
        self.end_entry.config(state=tk.NORMAL)
        self.timeout_entry.config(state=tk.NORMAL)
        self.threads_entry.config(state=tk.NORMAL)
        self.progress_bar.pack_forget()
        self.progress_label.config(text="")
    
    def save_results(self):
        if not self.portas_abertas:
            messagebox.showwarning("Aviso", "Nenhum resultado para salvar!")
            return
        
        filetype = [("Arquivo CSV", "*.csv"), ("Arquivo TXT", "*.txt"), ("Todos os arquivos", "*.*")]
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=filetype)
        
        if filename:
            try:
                if filename.endswith('.csv'):
                    with open(filename, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Porta', 'Servico', 'Banner'])
                        for p in self.portas_abertas:
                            writer.writerow([p['porta'], p['servico'], p.get('banner', '')])
                else:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write("=" * 70 + "\n")
                        f.write("RELATORIO DE VARREDURA - PORT SCANNER SENAI\n")
                        f.write("=" * 70 + "\n")
                        f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"Host: {self.host_entry.get()}\n\n")
                        for p in self.portas_abertas:
                            f.write(f"Porta {p['porta']}: {p['servico']}\n")
                            if p.get('banner'):
                                f.write(f"  Banner: {p['banner']}\n")
                
                messagebox.showinfo("Sucesso", f"Arquivo salvo:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar:\n{str(e)}")

def main():
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
