"""
PORT SCANNER - SENAI
FASE 1 - Scanner de porta única
Autores: Laura Mendes Teixeira e Joy Gabriella Sanchez da Silva
"""

import socket
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class PortScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Scanner - SENAI (Fase 1)")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Configurar cor de fundo azul marinho
        self.bg_color = "#0a1928"  # Azul marinho escuro
        self.fg_color = "#e0e7f0"  # Cinza claro para texto
        self.accent_color = "#1e4d7c"  # Azul médio para elementos
        self.success_color = "#2ecc71"  # Verde para portas abertas
        self.error_color = "#e74c3c"    # Vermelho para erros
        
        self.root.configure(bg=self.bg_color)
        
        # Configurar estilo
        self.setup_styles()
        
        # Criar widgets
        self.create_widgets()
        
    def setup_styles(self):
        """Configurar estilos dos widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para labels
        style.configure("Title.TLabel", 
                       background=self.bg_color,
                       foreground=self.fg_color,
                       font=("Arial", 18, "bold"))
        
        style.configure("Info.TLabel",
                       background=self.bg_color,
                       foreground=self.fg_color,
                       font=("Arial", 11))
        
        # Estilo para entrada de texto
        style.configure("Custom.TEntry",
                       fieldbackground="white",
                       foreground="black",
                       font=("Arial", 11))
        
        # Estilo para frame
        style.configure("Custom.TFrame",
                       background=self.bg_color)
        
        style.configure("Result.TFrame",
                       background="#0f2338",
                       relief="solid",
                       borderwidth=1)
        
    def create_widgets(self):
        """Criar todos os widgets da interface"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, style="Custom.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, text="PORT SCANNER - SENAI", 
                                style="Title.TLabel")
        title_label.pack(pady=(0, 10))
        
        # Subtítulo indicando Fase 1
        subtitle_label = ttk.Label(main_frame, 
                                   text="Fase 1 - Scanner de Porta Única",
                                   style="Info.TLabel")
        subtitle_label.pack(pady=(0, 30))
        
        # Frame para entrada de dados
        input_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        input_frame.pack(fill=tk.X, pady=10)
        
        # Host/IP
        host_label = ttk.Label(input_frame, text="Host / IP:", 
                              style="Info.TLabel")
        host_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.host_entry = ttk.Entry(input_frame, width=35, 
                                   font=("Arial", 11))
        self.host_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        self.host_entry.insert(0, "127.0.0.1")
        
        # Porta
        port_label = ttk.Label(input_frame, text="Porta:", 
                              style="Info.TLabel")
        port_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.port_entry = ttk.Entry(input_frame, width=35, 
                                   font=("Arial", 11))
        self.port_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        self.port_entry.insert(0, "80")
        
        # Timeout
        timeout_label = ttk.Label(input_frame, text="Timeout (segundos):", 
                                 style="Info.TLabel")
        timeout_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.timeout_entry = ttk.Entry(input_frame, width=35, 
                                      font=("Arial", 11))
        self.timeout_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        self.timeout_entry.insert(0, "2")
        
        # Botão de scan
        self.scan_button = tk.Button(input_frame, 
                                    text="INICIAR SCAN",
                                    command=self.start_scan,
                                    bg=self.accent_color,
                                    fg="white",
                                    font=("Arial", 12, "bold"),
                                    padx=30,
                                    pady=8,
                                    cursor="hand2",
                                    relief=tk.RAISED,
                                    borderwidth=2,
                                    activebackground="#2c6eb3",
                                    activeforeground="white")
        self.scan_button.grid(row=3, column=0, columnspan=2, 
                            pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        
        # Frame para resultados
        result_frame = ttk.Frame(main_frame, style="Result.TFrame")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Text widget para mostrar resultados
        self.result_text = tk.Text(result_frame, 
                                  bg="#0f2338",
                                  fg=self.fg_color,
                                  font=("Consolas", 11),
                                  wrap=tk.WORD,
                                  relief=tk.FLAT,
                                  padx=15,
                                  pady=15)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(result_frame, 
                                 orient=tk.VERTICAL,
                                 command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_label = tk.Label(self.root, 
                                    text="✅ Pronto para escanear...",
                                    bg=self.bg_color,
                                    fg=self.fg_color,
                                    font=("Arial", 9),
                                    anchor=tk.W,
                                    padx=20,
                                    pady=5)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configurar grid weights
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Configurar tags de cor
        self.result_text.tag_config("success", foreground=self.success_color)
        self.result_text.tag_config("error", foreground=self.error_color)
        self.result_text.tag_config("info", foreground=self.accent_color)
        
    def log_message(self, message, tag=None):
        """Adicionar mensagem ao resultado"""
        self.result_text.insert(tk.END, message + "\n", tag)
        self.result_text.see(tk.END)
        self.root.update()
        
    def check_port(self, host, port, timeout=2):
        """Verificar se uma porta está aberta"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            resultado = sock.connect_ex((host, port))
            sock.close()
            return resultado == 0
        except:
            return False
            
    def run_scan(self, host, port, timeout):
        """Executar o scan em uma thread separada"""
        try:
            # Limpar resultados anteriores
            self.result_text.delete(1.0, tk.END)
            
            self.log_message("=" * 50, "info")
            self.log_message("       PORT SCANNER - SENAI (FASE 1)", "info")
            self.log_message("=" * 50, "info")
            self.log_message(f"\n[INFO] Host: {host}", "info")
            self.log_message(f"[INFO] Porta: {port}", "info")
            self.log_message(f"[INFO] Timeout: {timeout} segundos", "info")
            self.log_message("-" * 50, "info")
            
            # Verificar a porta
            self.status_label.config(text=f"🔄 Verificando porta {port}...")
            
            if self.check_port(host, port, timeout):
                self.log_message(f"\n[+] PORTA {port} ABERTA em {host}", "success")
            else:
                self.log_message(f"\n[-] PORTA {port} FECHADA ou FILTRADA em {host}", "error")
            
            self.log_message("\n" + "=" * 50, "info")
            self.log_message("         SCAN FINALIZADO!", "success")
            self.log_message("=" * 50, "info")
            
        except socket.gaierror:
            self.log_message(f"\n[ERRO] Host '{host}' não encontrado ou inválido", "error")
        except socket.error as e:
            self.log_message(f"\n[ERRO] Problema de socket: {e}", "error")
        except Exception as e:
            self.log_message(f"\n[ERRO] Erro inesperado: {e}", "error")
        finally:
            # Reativar botão e parar progress bar
            self.scan_button.config(state=tk.NORMAL, text="INICIAR SCAN")
            self.progress.stop()
            self.progress.pack_forget()
            self.status_label.config(text="✅ Scan finalizado!")
            
    def start_scan(self):
        """Iniciar o processo de scan"""
        # Validar entrada
        host = self.host_entry.get().strip()
        if not host:
            messagebox.showerror("Erro", "Digite um host/IP válido!")
            return
        
        # Validar porta
        try:
            port = int(self.port_entry.get().strip())
            if port < 1 or port > 65535:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Porta inválida! Use um número entre 1 e 65535")
            return
            
        # Validar timeout
        try:
            timeout = float(self.timeout_entry.get().strip())
            if timeout <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Timeout inválido! Use um número positivo!")
            return
        
        # Desativar botão e iniciar scan
        self.scan_button.config(state=tk.DISABLED, text="ESCANEANDO...")
        self.progress.pack(fill=tk.X, pady=(0, 10))
        self.progress.start(10)
        self.status_label.config(text="🔄 Escaneando...")
        
        # Iniciar thread para não travar a interface
        scan_thread = threading.Thread(
            target=self.run_scan,
            args=(host, port, timeout),
            daemon=True
        )
        scan_thread.start()

def main():
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()