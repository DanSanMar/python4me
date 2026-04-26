import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import os
import re
from datetime import datetime

class Scan4MeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ALL 4 ME - scan4me.py v3.5.2")
        self.root.geometry("1250x900")
        
        # --- Configuración de Colores ---
        self.bg_main = "#f5f5f5"      # Gris muy claro
        self.bg_panel = "#ffffff"     # Blanco
        self.fg_text = "#2d2d2d"      # Gris oscuro/Negro
        self.accent_blue = "#005fb8"  # Azul profesional
        self.accent_green = "#28a745" # Verde éxito
        
        self.root.configure(bg=self.bg_main)

        # Variables de estado
        self.target = tk.StringVar()
        self.sub_path = tk.StringVar()
        self.xml_status = tk.BooleanVar(value=False)
        self.folder = ""
        
        self.setup_ui()

    def setup_ui(self):
        # --- Banner y Logo ---
        header_frame = tk.Frame(self.root, bg=self.accent_blue, pady=10)
        header_frame.pack(fill="x")

        logo_text = """
    █████╗ ██╗      ██╗      ██╗  ██╗███╗   ███╗███████╗
   ██╔══██╗██║      ██║      ██║  ██║████╗ ████║██╔════╝
   ███████║██║      ██║      ███████║██╔████╔██║█████╗  
   ██╔══██║██║      ██║      ╚════██║██║╚██╔╝██║██╔══╝  
   ██║  ██║███████╗███████╗      ██║██║ ╚═╝ ██║███████╗
   ╚═╝  ╚═╝╚══════╝╚══════╝      ╚═╝╚═╝     ╚═╝╚══════╝"""
        
        logo_label = tk.Label(header_frame, text=logo_text, font=("Courier New", 10, "bold"), 
                             fg="white", bg=self.accent_blue, justify="left")
        logo_label.pack()
        
        tk.Label(header_frame, text="░▒▓ ALL 4 ME ▓▒░ - Pentesting & CTF Tool", 
                 fg="white", bg=self.accent_blue, font=("Segoe UI", 10, "italic")).pack()

        # --- Panel de Configuración ---
        config_frame = tk.LabelFrame(self.root, text=" 🎯 Configuración del Objetivo ", 
                                    bg=self.bg_panel, fg=self.fg_text, font=("Segoe UI", 16, "bold"), padx=15, pady=10)
        config_frame.pack(fill="x", padx=20, pady=10)

        # Target e IP
        tk.Label(config_frame, text="Target (IP/Host):", bg=self.bg_panel).grid(row=0, column=0, sticky="w")
        tk.Entry(config_frame, textvariable=self.target, width=25, font=("Consolas", 14)).grid(row=0, column=1, padx=10)

        tk.Label(config_frame, text="Ruta/Subdominio (ej: /phpmyadmin):", bg=self.bg_panel).grid(row=0, column=2, sticky="w")
        tk.Entry(config_frame, textvariable=self.sub_path, width=25, font=("Consolas", 14)).grid(row=0, column=3, padx=10)

        tk.Checkbutton(config_frame, text="Generar Reporte XML", variable=self.xml_status, 
                       bg=self.bg_panel, activebackground=self.bg_panel).grid(row=0, column=4, padx=20)

        # --- Menú de Herramientas ---
        tools_frame = tk.Frame(self.root, bg=self.bg_main)
        tools_frame.pack(fill="x", padx=20)

        # Botones Principales con Descripción
        self.create_tool_btn(tools_frame, "🚀 AUTO SCAN", "Fase 1 + Fase 2 + Vulns", self.start_auto_scan, self.accent_green)
        
        # Submenú Nmap (Dropdown)
        nmap_frame = tk.Frame(tools_frame, bg=self.bg_main)
        nmap_frame.pack(side="left", padx=5)
        tk.Label(nmap_frame, text="Opciones Nmap:", bg=self.bg_main, font=("Segoe UI", 10)).pack()
        self.nmap_opt = ttk.Combobox(nmap_frame, width=30, state="readonly", values=[
            "1. Reconocimiento Rápido (OS/Versión)",
            "2. Escaneo de Puertos Totales (p-)",
            "3. Enumeración de Servicios (sCV)",
            "4. Escaneo de Vulnerabilidades (Vuln)",
            "5. UDP Discovery (Top 20)",
            "6. Web Recon (Scripts HTTP)"
        ])
        self.nmap_opt.set("Selecciona modo Nmap...")
        self.nmap_opt.pack()
        tk.Button(nmap_frame, text="Ejecutar Selección", command=self.run_nmap_submenu, bg="#555", fg="white").pack(fill="x", pady=2)

        # Otras herramientas
        self.create_tool_btn(tools_frame, "🔍 WHATWEB", "Tech Stack", self.run_whatweb, "#5f378a")
        self.create_tool_btn(tools_frame, "📂 FEROXBUSTER", "Fuzzing Web", self.run_ferox, "#c1272d")
        self.create_tool_btn(tools_frame, "WordPress", "WPSCan", self.run_wpscan, "#217346")

        # --- Consola de Salida ---
        console_label = tk.Label(self.root, text=" 🖥️ Consola de Ejecución (Logs de Auditoría)", 
                                 bg=self.bg_main, fg=self.fg_text, font=("Segoe UI", 12, "bold"))
        console_label.pack(anchor="w", padx=20, pady=(10, 0))
        
        self.output = scrolledtext.ScrolledText(self.root, bg="#ffffff", fg="#1e1e1e", 
                                               font=("Consolas", 14), insertbackground="black",
                                               highlightthickness=1, highlightbackground="#cccccc")
        self.output.pack(expand=True, fill="both", padx=20, pady=10)

    def create_tool_btn(self, parent, title, desc, cmd, color):
        frame = tk.Frame(parent, bg=self.bg_main)
        frame.pack(side="left", padx=5)
        tk.Label(frame, text=desc, bg=self.bg_main, font=("Segoe UI", 10, "italic")).pack()
        btn = tk.Button(frame, text=title, command=cmd, bg=color, fg="white", 
                        width=15, font=("Segoe UI", 9, "bold"), relief="flat")
        btn.pack(pady=2)

    # --- LÓGICA DE EJECUCIÓN ---

    def write_log(self, text, tag=None):
        self.output.insert(tk.END, text + "\n", tag)
        self.output.see(tk.END)
        if self.folder:
            with open(f"{self.folder}/reporte_completo.txt", "a", encoding="utf-8") as f:
                f.write(text + "\n")

    def run_command(self, cmd, callback=None):
        def task():
            target = self.target.get()
            if not target:
                messagebox.showwarning("Error", "¡Debes indicar un objetivo!")
                return

            if not self.folder:
                date_str = datetime.now().strftime("%d-%m-%Y")
                self.folder = f"Auditoria_{target}_{date_str}"
                if not os.path.exists(self.folder): os.makedirs(self.folder)

            self.write_log(f"\n[🕒 {datetime.now().strftime('%H:%M:%S')}] EJECUTANDO: {cmd}\n" + "-"*60)
            
            try:
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                         text=True, shell=True, encoding='utf-8', errors='replace')
                
                output_content = []
                for line in process.stdout:
                    self.write_log(line.strip())
                    output_content.append(line.strip())
                
                process.wait()
                if callback:
                    callback("\n".join(output_content))
                
                self.write_log("-"*60 + "\n✅ Tarea completada.")
            except Exception as e:
                self.write_log(f"❌ ERROR: {str(e)}")

        threading.Thread(target=task, daemon=True).start()

    # --- ACCIONES ---

    def start_auto_scan(self):
        """ Lógica de Escaneo Automático """
        target = self.target.get()
        self.write_log(f"🚀 Iniciando Escaneo Automático Fase 1 (Discovery) en {target}...")
        self.run_command(f"nmap -sS -p- --open -T4 -Pn -n {target}", callback=self.fase_2_auto)

    def fase_2_auto(self, output):
        ports = re.findall(r"(\d+)/tcp\s+open", output)
        if not ports:
            self.write_log("⚠️ No se detectaron puertos abiertos.")
            return
        
        port_list = ",".join(ports)
        self.write_log(f"✅ Puertos encontrados: {port_list}. Iniciando Fase 2 (Scripts/Versiones)...")
        
        xml_flag = ""
        if self.xml_status.get():
            xml_flag = f"-oA {self.folder}/nmap_auto_{datetime.now().strftime('%H%M%S')}"

        self.run_command(f"nmap -sSCV -Pn -p {port_list} {xml_flag} {self.target.get()}", 
                         callback=lambda _: self.fase_3_vuln(port_list))

    def fase_3_vuln(self, port_list):
        self.write_log("🚀 Iniciando Fase 3 (Vulnerabilidades)...")
        self.run_command(f"nmap --script vuln -p {port_list} {self.target.get()}")

    def run_nmap_submenu(self):
        choice = self.nmap_opt.get()
        target = self.target.get()
        
        modes = {
            "1.": f"nmap -sS -O -sV -Pn -T4 {target}",
            "2.": f"nmap -sS -p- -Pn {target}",
            "3.": f"nmap -sSCV -Pn {target}",
            "4.": f"nmap --script vuln -Pn {target}",
            "5.": f"nmap -sU -Pn --top-ports 20 -T4 {target}",
            "6.": f"nmap -p 80,443 -Pn -sV --script http-enum,http-title,http-methods {target}"
        }

        for key, cmd in modes.items():
            if choice.startswith(key):
                if self.xml_status.get():
                    cmd += f" -oX {self.folder}/nmap_custom_{datetime.now().strftime('%H%M%S')}.xml"
                self.run_command(cmd)
                return
        messagebox.showinfo("Info", "Por favor, selecciona una opción válida del menú.")

    def run_whatweb(self):
        self.run_command(f"whatweb -a 3 -v {self.target.get()}")

    def run_ferox(self):
        url = self.target.get()
        if not url.startswith("http"): url = f"http://{url}"
        # Wordlist por defecto para Windows/Kali
        wordlist = "/usr/share/seclists/Discovery/Web-Content/common.txt" if os.name != 'nt' else "common.txt"
        self.run_command(f"feroxbuster --url {url} -w {wordlist} -t 50 --no-recursion")

    def run_wpscan(self):
        target = self.target.get()
        sub = self.sub_path.get()
        url = target if target.startswith("http") else f"http://{target}"
        if sub: url = f"{url.rstrip('/')}/{sub.lstrip('/')}"
        
        self.run_command(f"wpscan --url {url} -e u,ap --detection-mode aggressive --force")

if __name__ == "__main__":
    root = tk.Tk()
    app = Scan4MeApp(root)
    root.mainloop()