import socket
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class PortScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner - SENAI (Fase 2)")
        self.root.geometry("750x650")
        self.root.resizable(False, False)
        
        # Configuração de cores - Azul Marinho
        self.bg_color = "#0a1628"      # Azul marinho mais escuro
        self.bg_sec_color = "#0f1f33"  # Azul marinho secundário
        self.fg_color = "#e0e7f0"      # Cinza claro para texto
        self.accent_color = "#1e5799"   # Azul médio para elementos
        self.accent_hover = "#2c6eb3"   # Azul mais claro para hover
        self.success_color = "#27ae60"  # Verde para sucesso
        self.error_color = "#e74c3c"    # Vermelho para erro
        self.warning_color = "#f39c12"  # Laranja para aviso
        self.info_color = "#3498db"     # Azul claro para info
        
        self.root.configure(bg=self.bg_color)
        
        # Dicionário de serviços
        self.servicos = {
            20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPC", 135: "RPC",
            139: "NETBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS",
            995: "POP3S", 1433: "MSSQL", 1521: "ORACLE-DB", 3306: "MYSQL",
            3389: "RDP", 5432: "POSTGRESQL", 5900: "VNC", 6379: "REDIS",
            27017: "MONGODB", 8080: "HTTP-ALT", 8443: "HTTPS-ALT"
        }
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        """Configurar estilos dos widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilos para labels
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
        
        style.configure("Result.TLabel",
                       background=self.bg_sec_color,
                       foreground=self.fg_color,
                       font=("Consolas", 10))
        
        # Estilo para frames
        style.configure("Main.TFrame", background=self.bg_color)
        style.configure("Input.TFrame", background=self.bg_sec_color)
        style.configure("Result.TFrame", background=self.bg_sec_color)
        
        # Estilo para botões
        style.configure("Custom.TButton",
                       background=self.accent_color,
                       foreground="white",
                       font=("Arial", 11, "bold"),
                       padding=12)
        
        # Estilo para entrada de texto
        style.configure("Custom.TEntry",
                       fieldbackground="white",
                       foreground="black",
                       font=("Arial", 11))
        
    def create_widgets(self):
        """Criar todos os widgets da interface"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, text="PORT SCANNER - SENAI", 
                               style="Title.TLabel")
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(main_frame, 
                                  text="Scanner de Range de Portas com Identificação de Serviços",
                                  style="Subtitle.TLabel")
        subtitle_label.pack(pady=(0, 25))
        
        # Frame de entrada de dados
        input_frame = ttk.Frame(main_frame, style="Input.TFrame")
        input_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Configurar grid do input_frame
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Host/IP
        host_label = ttk.Label(input_frame, text="Host / IP:", 
                              style="Info.TLabel")
        host_label.grid(row=0, column=0, sticky=tk.W, pady=8, padx=10)
        
        self.host_entry = ttk.Entry(input_frame, width=35, 
                                   font=("Arial", 11))
        self.host_entry.grid(row=0, column=1, pady=8, padx=10, sticky="ew")
        self.host_entry.insert(0, "127.0.0.1")
        
        # Porta inicial
        start_label = ttk.Label(input_frame, text="Porta Inicial:", 
                               style="Info.TLabel")
        start_label.grid(row=1, column=0, sticky=tk.W, pady=8, padx=10)
        
        self.start_entry = ttk.Entry(input_frame, width=20, 
                                    font=("Arial", 11))
        self.start_entry.grid(row=1, column=1, pady=8, padx=10, sticky="w")
        self.start_entry.insert(0, "1")
        
        # Porta final
        end_label = ttk.Label(input_frame, text="Porta Final:", 
                             style="Info.TLabel")
        end_label.grid(row=2, column=0, sticky=tk.W, pady=8, padx=10)
        
        self.end_entry = ttk.Entry(input_frame, width=20, 
                                  font=("Arial", 11))
        self.end_entry.grid(row=2, column=1, pady=8, padx=10, sticky="w")
        self.end_entry.insert(0, "100")
        
        # Timeout
        timeout_label = ttk.Label(input_frame, text="Timeout (segundos):", 
                                 style="Info.TLabel")
        timeout_label.grid(row=3, column=0, sticky=tk.W, pady=8, padx=10)
        
        self.timeout_entry = ttk.Entry(input_frame, width=20, 
                                      font=("Arial", 11))
        self.timeout_entry.grid(row=3, column=1, pady=8, padx=10, sticky="w")
        self.timeout_entry.insert(0, "2")
        
        # Frame para botões
        button_frame = ttk.Frame(main_frame, style="Main.TFrame")
        button_frame.pack(fill=tk.X, pady=15)
        
        # Botão de scan
        self.scan_button = tk.Button(button_frame, 
                                    text="INICIAR SCAN",
                                    command=self.start_scan,
                                    bg=self.accent_color,
                                    fg="white",
                                    font=("Arial", 12, "bold"),
                                    padx=30,
                                    pady=8,
                                    cursor="hand2",
                                    relief=tk.RAISED,
                                    borderwidth=0,
                                    activebackground=self.accent_hover,
                                    activeforeground="white")
        self.scan_button.pack(pady=5)
        
        # Botão de limpar
        self.clear_button = tk.Button(button_frame,
                                     text="LIMPAR RESULTADOS",
                                     command=self.clear_results,
                                     bg="#2c3e50",
                                     fg=self.fg_color,
                                     font=("Arial", 10),
                                     padx=20,
                                     pady=5,
                                     cursor="hand2",
                                     relief=tk.RAISED,
                                     borderwidth=0,
                                     activebackground="#34495e")
        self.clear_button.pack(pady=5)
        
        # Barra de progresso
        self.progress_frame = ttk.Frame(main_frame, style="Main.TFrame")
        self.progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_label = tk.Label(self.progress_frame, 
                                      text="",
                                      bg=self.bg_color,
                                      fg=self.fg_color,
                                      font=("Arial", 9))
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, 
                                           mode='determinate',
                                           length=400)
        
        # Frame de resultados
        result_frame = ttk.Frame(main_frame, style="Result.TFrame")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Text widget para resultados
        self.result_text = tk.Text(result_frame, 
                                  bg="#0c1a2e",
                                  fg=self.fg_color,
                                  font=("Consolas", 10),
                                  wrap=tk.WORD,
                                  relief=tk.FLAT,
                                  padx=15,
                                  pady=15,
                                  selectbackground=self.accent_color)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(result_frame, 
                                 orient=tk.VERTICAL,
                                 command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar tags de cor
        self.result_text.tag_config("success", foreground=self.success_color)
        self.result_text.tag_config("error", foreground=self.error_color)
        self.result_text.tag_config("warning", foreground=self.warning_color)
        self.result_text.tag_config("info", foreground=self.info_color)
        self.result_text.tag_config("title", foreground=self.accent_color, font=("Consolas", 11, "bold"))
        
        # Status bar
        self.status_label = tk.Label(self.root, 
                                    text="Pronto para escanear...",
                                    bg=self.bg_color,
                                    fg=self.fg_color,
                                    font=("Arial", 9),
                                    anchor=tk.W,
                                    padx=20,
                                    pady=5)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Thread de scan
        self.scan_thread = None
        self.is_scanning = False
        
    def get_service_name(self, port):
        """Retorna o nome do serviço para a porta"""
        return self.servicos.get(port, "DESCONHECIDO")
    
    def check_port(self, host, port, timeout=2):
        """Verifica se uma porta está aberta"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            resultado = sock.connect_ex((host, port))
            sock.close()
            return resultado == 0
        except:
            return False
    
    def log_message(self, message, tag=None):
        """Adiciona mensagem ao resultado"""
        self.result_text.insert(tk.END, message + "\n", tag)
        self.result_text.see(tk.END)
        self.root.update()
    
    def clear_results(self):
        """Limpa os resultados"""
        self.result_text.delete(1.0, tk.END)
        self.log_message("=" * 65, "title")
        self.log_message("            NOVA VARREDURA INICIADA", "title")
        self.log_message("=" * 65, "title")
    
    def scan_port_range(self, host, start_port, end_port, timeout):
        """Escaneia range de portas"""
        portas_abertas = []
        total_portas = end_port - start_port + 1
        scan_count = 0
        
        self.log_message(f"\n[INFO] Host alvo: {host}", "info")
        self.log_message(f"[INFO] Range: {start_port} - {end_port}", "info")
        self.log_message(f"[INFO] Total de portas: {total_portas}", "info")
        self.log_message(f"[INFO] Timeout: {timeout} segundo(s)", "info")
        self.log_message("-" * 65, "warning")
        
        for porta in range(start_port, end_port + 1):
            if not self.is_scanning:
                self.log_message("\n[!] SCAN INTERROMPIDO PELO USUÁRIO", "warning")
                return portas_abertas, scan_count
            
            scan_count += 1
            
            # Atualizar progresso
            percentual = (scan_count / total_portas) * 100
            self.progress_bar['value'] = percentual
            self.progress_label.config(text=f"Escaneando: {scan_count}/{total_portas} ({percentual:.1f}%)")
            self.root.update()
            
            if self.check_port(host, porta, timeout):
                servico = self.get_service_name(porta)
                portas_abertas.append((porta, servico))
                self.log_message(f"[+] PORTA {porta:5d} ABERTA     → Serviço: {servico}", "success")
        
        return portas_abertas, total_portas
    
    def run_scan(self):
        """Executa o scan em thread separada"""
        try:
            host = self.host_entry.get().strip()
            start_port = int(self.start_entry.get().strip())
            end_port = int(self.end_entry.get().strip())
            timeout = float(self.timeout_entry.get().strip())
            
            # Validações
            if not host:
                self.log_message("[ERRO] Digite um host/IP válido!", "error")
                return
            
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                self.log_message("[ERRO] Range inválido! (1-65535 e inicial < final)", "error")
                return
            
            if timeout <= 0:
                self.log_message("[ERRO] Timeout deve ser maior que 0!", "error")
                return
            
            # Verificar conectividade básica
            self.log_message(f"\n[INFO] Testando conectividade com {host}...", "info")
            if not self.check_port(host, 80, timeout) and not self.check_port(host, 443, timeout):
                self.log_message("[AVISO] Host pode estar inacessível ou sem portas comuns abertas", "warning")
            
            # Marcar tempo de início
            tempo_inicio = time.time()
            
            # Executar scan
            portas_abertas, total_portas = self.scan_port_range(host, start_port, end_port, timeout)
            
            # Calcular tempo total
            tempo_total = time.time() - tempo_inicio
            
            # Resumo final
            self.log_message("\n" + "=" * 65, "title")
            self.log_message("                 RESUMO DA VARREDURA", "title")
            self.log_message("=" * 65, "title")
            self.log_message(f"Host alvo:        {host}", "info")
            self.log_message(f"Range varrido:    {start_port} - {end_port}", "info")
            self.log_message(f"Total portas:     {total_portas}", "info")
            self.log_message(f"Portas abertas:   {len(portas_abertas)}", "success" if portas_abertas else "warning")
            self.log_message(f"Portas fechadas:  {total_portas - len(portas_abertas)}", "info")
            self.log_message(f"Tempo total:      {tempo_total:.2f} segundos", "info")
            
            if portas_abertas:
                self.log_message("\n--- PORTAS ABERTAS ENCONTRADAS ---", "success")
                for porta, servico in portas_abertas:
                    self.log_message(f"  {porta:5d} : {servico}", "success")
            else:
                self.log_message("\n[!] Nenhuma porta aberta encontrada no range especificado.", "warning")
            
            self.log_message("=" * 65, "title")
            self.status_label.config(text="Scan finalizado com sucesso!")
            
        except ValueError as e:
            self.log_message(f"[ERRO] Valor inválido: {e}", "error")
        except socket.gaierror:
            self.log_message(f"[ERRO] Host '{host}' não encontrado ou inválido", "error")
        except socket.error as e:
            self.log_message(f"[ERRO] Problema de socket: {e}", "error")
        except Exception as e:
            self.log_message(f"[ERRO] Erro inesperado: {e}", "error")
        finally:
            self.scan_complete()
    
    def start_scan(self):
        """Inicia o scan"""
        if self.is_scanning:
            self.stop_scan()
            return
        
        # Limpar resultados anteriores
        self.clear_results()
        
        # Validar entradas
        try:
            start_port = int(self.start_entry.get().strip())
            end_port = int(self.end_entry.get().strip())
            timeout = float(self.timeout_entry.get().strip())
            
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                messagebox.showerror("Erro", "Range de portas inválido!\n(1-65535 e inicial < final)")
                return
            
            if timeout <= 0:
                messagebox.showerror("Erro", "Timeout deve ser maior que 0!")
                return
                
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos!")
            return
        
        # Configurar interface para scan
        self.is_scanning = True
        self.scan_button.config(text="PARAR SCAN", bg=self.error_color)
        self.clear_button.config(state=tk.DISABLED)
        self.host_entry.config(state=tk.DISABLED)
        self.start_entry.config(state=tk.DISABLED)
        self.end_entry.config(state=tk.DISABLED)
        self.timeout_entry.config(state=tk.DISABLED)
        
        # Mostrar barra de progresso
        self.progress_bar.pack(pady=5)
        self.progress_bar['value'] = 0
        
        self.status_label.config(text="Escaneando portas...")
        
        # Iniciar thread
        self.scan_thread = threading.Thread(target=self.run_scan, daemon=True)
        self.scan_thread.start()
    
    def stop_scan(self):
        """Para o scan em andamento"""
        self.is_scanning = False
        self.status_label.config(text="Parando scan...")
        self.log_message("\n[!] Solicitando parada do scan...", "warning")
    
    def scan_complete(self):
        """Finaliza o scan"""
        self.is_scanning = False
        self.scan_button.config(text="INICIAR SCAN", bg=self.accent_color)
        self.clear_button.config(state=tk.NORMAL)
        self.host_entry.config(state=tk.NORMAL)
        self.start_entry.config(state=tk.NORMAL)
        self.end_entry.config(state=tk.NORMAL)
        self.timeout_entry.config(state=tk.NORMAL)
        
        # Esconder barra de progresso
        self.progress_bar.pack_forget()
        self.progress_label.config(text="")
        
        if not self.scan_thread or not self.scan_thread.is_alive():
            pass

def main():
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
