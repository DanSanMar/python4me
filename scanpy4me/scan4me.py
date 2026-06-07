import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import os
import re
from datetime import datetime
import glob

class Scan4MeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ALL 4 ME - scan4me.py v5.6 (GUI Edition)")
        
        # --- Configuración de Pantalla Completa ---
        try:
            self.root.state('zoomed') # Windows
        except:
            self.root.attributes('-zoomed', True) # Linux
            
        self.root.geometry("1400x900")
        
        # --- Colores y Fuentes Grandes ---
        self.bg_main = "#eef2f5"
        self.bg_panel = "#ffffff"
        self.fg_text = "#1a1a1a"
        self.accent_blue = "#0f4c75"
        self.accent_green = "#28a745"
        self.accent_red = "#c1272d"
        self.accent_purple = "#5f378a"
        
        self.f_title = ("Segoe UI", 16, "bold")
        self.f_label = ("Segoe UI", 14, "bold")
        self.f_entry = ("Consolas", 14)
        self.f_btn = ("Segoe UI", 12, "bold")
        self.f_console = ("Consolas", 13)

        self.root.configure(bg=self.bg_main)

        # --- Variables de Estado ---
        self.target = tk.StringVar()
        self.sub_path = tk.StringVar()
        self.xml_status = tk.BooleanVar(value=True)
        self.txt_status = tk.BooleanVar(value=True)
        self.folder = ""
        self.is_scanning = False

        self.check_root()
        self.setup_ui()

    def check_root(self):
        if os.name != 'nt' and os.geteuid() != 0:
            messagebox.showwarning("Atención", "No estás ejecutando el script como ROOT (sudo).\n\nAlgunas funciones como Nmap SYN (-sS) o arp-scan fallarán. Reinicia con 'sudo python3 scan4me.py'.")

    def setup_ui(self):
        # --- 1. BANNER Y LOGO ---
        header_frame = tk.Frame(self.root, bg=self.accent_blue, pady=15)
        header_frame.pack(fill="x")

        logo_text = """    █████╗ ██╗      ██╗      ██╗  ██╗███╗   ███╗███████╗
   ██╔══██╗██║      ██║      ██║  ██║████╗ ████║██╔════╝
   ███████║██║      ██║      ███████║██╔████╔██║█████╗  
   ██╔══██║██║      ██║      ╚════██║██║╚██╔╝██║██╔══╝  
   ██║  ██║███████╗███████╗      ██║██║ ╚═╝ ██║███████╗
   ╚═╝  ╚═╝╚══════╝╚══════╝      ╚═╝╚═╝     ╚═╝╚══════╝"""
        
        tk.Label(header_frame, text=logo_text, font=("Courier New", 12, "bold"), fg="#00f0ff", bg=self.accent_blue, justify="left").pack()
        tk.Label(header_frame, text="░▒▓ ALL 4 ME ▓▒░ - Interactive GUI Scanner [v5.6]", fg="white", bg=self.accent_blue, font=self.f_title).pack(pady=(10,0))

        # --- 2. PANEL DE CONFIGURACIÓN ---
        config_frame = tk.LabelFrame(self.root, text=" 🎯 1. Configuración del Objetivo ", bg=self.bg_panel, fg=self.fg_text, font=self.f_title, padx=20, pady=15)
        config_frame.pack(fill="x", padx=30, pady=15)

        tk.Label(config_frame, text="Target (IP/Dominio):", bg=self.bg_panel, font=self.f_label).grid(row=0, column=0, sticky="w")
        tk.Entry(config_frame, textvariable=self.target, width=25, font=self.f_entry).grid(row=0, column=1, padx=15)

        tk.Label(config_frame, text="Ruta Web (ej: /wordpress):", bg=self.bg_panel, font=self.f_label).grid(row=0, column=2, sticky="w", padx=(20,0))
        tk.Entry(config_frame, textvariable=self.sub_path, width=20, font=self.f_entry).grid(row=0, column=3, padx=15)

        tk.Checkbutton(config_frame, text="Generar Reportes XML/HTML/MD", variable=self.xml_status, font=self.f_label, bg=self.bg_panel).grid(row=0, column=4, padx=20)
        tk.Checkbutton(config_frame, text="Guardar Log TXT", variable=self.txt_status, font=self.f_label, bg=self.bg_panel).grid(row=0, column=5)

        # --- 3. PANEL DE HERRAMIENTAS ---
        tools_frame = tk.LabelFrame(self.root, text=" 🚀 2. Ejecución de Herramientas ", bg=self.bg_panel, fg=self.fg_text, font=self.f_title, padx=20, pady=15)
        tools_frame.pack(fill="x", padx=30, pady=5)

        top_tools = tk.Frame(tools_frame, bg=self.bg_panel)
        top_tools.pack(fill="x", pady=5)

        self.create_tool_btn(top_tools, "🌐 DISCOVER HOSTS", "Mapeo de Red Local (ARP/Ping)", self.run_network_discovery, "#e67e22")
        self.create_tool_btn(top_tools, "⚡ AUTO SCAN (CTF)", "Fase 1 + Sigilo + Versiones + Vulns", self.start_auto_scan, self.accent_green)
        self.create_tool_btn(top_tools, "🔍 WHATWEB", "Reconocimiento Stack Web", self.run_whatweb, self.accent_purple)
        self.create_tool_btn(top_tools, "📂 FEROXBUSTER", "Fuzzing Directorios Web", self.run_ferox, self.accent_red)
        self.create_tool_btn(top_tools, "Ⓜ️ WPSCAN", "Auditoría WordPress", self.run_wpscan, "#0073aa")

        bottom_tools = tk.Frame(tools_frame, bg=self.bg_panel)
        bottom_tools.pack(fill="x", pady=(15, 0))

        # Nmap Submenu
        nmap_frame = tk.Frame(bottom_tools, bg=self.bg_panel)
        nmap_frame.pack(side="left", padx=10)
        tk.Label(nmap_frame, text="Opciones Específicas de NMAP:", bg=self.bg_panel, font=self.f_label).pack(anchor="w")
        
        self.nmap_opt = ttk.Combobox(nmap_frame, width=50, state="readonly", font=self.f_entry, values=[
            "1. [TCP] Recon Rápido OS (-sS -O -Pn)",
            "2. [TCP] Puertos Totales (-sS -p- -Pn --min-rate 5000)",
            "3. [TCP] Agresivo Completo (-A -Pn)",
            "4. [TCP] Enumeración Servicios (-sSCV -Pn)",
            "5. [VULN] Escaneo Vulnerabilidades (--script vuln)",
            "6. [EVASION] Mapeo Firewall (ACK Scan)",
            "7. [EVASION] Bypass (Señuelos + DNS Src)",
            "8. [UDP] Discovery Rápido (Top 20)",
            "9. [UDP] Investigación Profunda Versiones",
            "10. [WEB] Recon Básico (Enum, Robots, Title)",
            "11. [WEB] Recon Completo (Vulns Web)"
        ])
        self.nmap_opt.set("Selecciona modo Nmap...")
        self.nmap_opt.pack(side="left")
        tk.Button(nmap_frame, text="Ejecutar", command=self.run_nmap_submenu, bg="#444", fg="white", font=self.f_btn).pack(side="left", padx=10)

        # Windows Submenu
        win_frame = tk.Frame(bottom_tools, bg=self.bg_panel)
        win_frame.pack(side="left", padx=(40, 10))
        tk.Label(win_frame, text="Opciones para Entornos WINDOWS:", bg=self.bg_panel, font=self.f_label).pack(anchor="w")
        
        self.win_opt = ttk.Combobox(win_frame, width=50, state="readonly", font=self.f_entry, values=[
            "1. [Nmap] Enumeración SMB Básica",
            "2. [Nmap] Enumeración NetBIOS (UDP 137)",
            "3. [Nmap] Vulnerabilidades SMB",
            "4. [SMBClient] Listar recursos (Sesión Nula)",
            "5. [Nbtscan] Escaneo NetBIOS rápido",
            "6. [Enum4Linux] Enumeración completa"
        ])
        self.win_opt.set("Selecciona modo Windows...")
        self.win_opt.pack(side="left")
        tk.Button(win_frame, text="Ejecutar", command=self.run_win_submenu, bg="#005fb8", fg="white", font=self.f_btn).pack(side="left", padx=10)

        # --- 4. CONSOLA DE SALIDA ---
        console_frame = tk.Frame(self.root, bg=self.bg_main)
        console_frame.pack(expand=True, fill="both", padx=30, pady=(10, 20))

        tk.Label(console_frame, text=" 🖥️ Consola de Ejecución y Logs", bg=self.bg_main, fg=self.fg_text, font=self.f_title).pack(anchor="w")
        
        self.output = scrolledtext.ScrolledText(console_frame, bg="#1e1e1e", fg="#00ff00", font=self.f_console, insertbackground="white", highlightthickness=2, highlightbackground="#555")
        self.output.pack(expand=True, fill="both", pady=5)

    def create_tool_btn(self, parent, title, desc, cmd, color):
        frame = tk.Frame(parent, bg=self.bg_panel)
        frame.pack(side="left", padx=15)
        btn = tk.Button(frame, text=title, command=cmd, bg=color, fg="white", width=20, height=2, font=self.f_btn, relief="groove", cursor="hand2")
        btn.pack()
        tk.Label(frame, text=desc, bg=self.bg_panel, fg="#666", font=("Segoe UI", 10, "italic")).pack(pady=2)

    # --- NÚCLEO ROBUSTO DE EJECUCIÓN ---

    def get_safe_target_name(self):
        """Sanitiza IPs, URLs o CIDR para que no corrompan la creación de carpetas."""
        raw_target = self.target.get().strip()
        if not raw_target: return "Unknown_Target"
        # Eliminar http:// o https:// y sustituir caracteres prohibidos en rutas
        clean_name = re.sub(r'^https?://', '', raw_target)
        return re.sub(r'[\\/*?:"<>|]', "_", clean_name)

    def write_log(self, text):
        """Escribe en la consola visual y guarda en .txt de forma segura."""
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        
        if self.txt_status.get() and self.folder:
            safe_target = self.get_safe_target_name()
            log_path = os.path.join(self.folder, f"Auditoria_Completa_{safe_target}.txt")
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(text + "\n")
            except Exception as e:
                self.output.insert(tk.END, f"[!] Aviso: No se pudo guardar en TXT ({e})\n")

    def sync_log(self, text):
        """Método puente seguro Tkinter <-> Hilos"""
        self.root.after(0, self.write_log, text)

    def init_folder(self):
        """Crea la estructura de carpetas usando nombres seguros."""
        target = self.target.get().strip()
        if not target:
            messagebox.showwarning("Error", "¡Debes indicar un objetivo (IP o Dominio)!")
            return False
            
        safe_target = self.get_safe_target_name()
        date_str = datetime.now().strftime("%d-%m-%Y")
        self.folder = f"Auditoria_{safe_target}_{date_str}"
        
        try:
            os.makedirs(self.folder, exist_ok=True)
            return True
        except Exception as e:
            messagebox.showerror("Error Fichero", f"No se pudo crear la carpeta: {e}")
            return False

    def run_command(self, cmd, callback=None):
        if not self.init_folder(): 
            return

        if self.is_scanning:
            messagebox.showinfo("Aviso", "Ya hay un escaneo en progreso. Por favor espera.")
            return

        self.is_scanning = True # Bloqueamos nuevos comandos hasta que acabe

        def task():
            separator = "="*70
            time_str = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            self.sync_log(f"\n{separator}\n🕒 INICIO: {time_str}\n🚀 COMANDO: {cmd}\n{separator}")
            
            try:
                # Usamos /bin/bash directo para garantizar que tuberías (pipes) y awk funcionen
                shell_executable = '/bin/bash' if os.name != 'nt' else None
                
                # Leemos en formato RAW bytes y evitamos los buffers con iter()
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                         shell=True, executable=shell_executable)
                
                output_content = []
                while True:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break
                    if line:
                        # Decodificamos 'replace' previene crasheos por tildes o codificación extraña de Nmap
                        clean_line = line.decode('utf-8', errors='replace').rstrip('\r\n')
                        self.sync_log(clean_line)
                        output_content.append(clean_line)
                
                full_output = "\n".join(output_content)
                self.sync_log(f"{separator}\n✅ Tarea finalizada.\n")
                
                if callback:
                    self.root.after(0, callback, full_output)
                    
            except Exception as e:
                self.sync_log(f"❌ ERROR CRÍTICO: {str(e)}")
            finally:
                self.is_scanning = False # Liberamos el escaner

        threading.Thread(target=task, daemon=True).start()

    # --- LÓGICAS ESPECÍFICAS ---

    def run_network_discovery(self):
        if not self.target.get().strip():
            self.target.set("Red_Local")
            
        cmd = """
        echo '=== [FASE 1] ARP-SCAN en la red local ==='
        arp-scan --localnet --ignoredups 2>/dev/null
        
        echo ''
        echo '=== [FASE 2] PING SWEEP Rápido (Nmap) ==='
        if command -v ip >/dev/null 2>&1; then
            subnets=$(ip -o -4 addr show | awk '{print $4}' | grep -v '127.0.0.1' || true)
        else
            subnets=$(ifconfig | awk '/inet / {print $2}' | grep -v '127.0.0.1' || true)
        fi
        
        if [ -z "$subnets" ]; then
            echo "❌ No se encontraron interfaces de red locales válidas."
        else
            for subnet in $subnets; do
                echo ""
                echo "[*] Escaneando subred: $subnet..."
                nmap -sn -PS22,80,443,445 -PE --min-rate 5000 --max-rtt-timeout 20ms --host-timeout 1s "$subnet"
            done
        fi
        """
        self.run_command(cmd)

    def start_auto_scan(self):
        target = self.target.get().strip()
        if not self.init_folder(): return
        self.sync_log(f"\n[🚀 FASE 1] Iniciando Auto-Scan en {target} (Mínimo 5000 pkts/s)...")
        self.run_command(f"nmap -sS -p- -n -Pn --open --min-rate 5000 {target}", callback=self.fase_1_callback)

    def fase_1_callback(self, output):
        ports = re.findall(r"(\d+)/tcp\s+open", output)
        target = self.target.get().strip()
        
        if not ports:
            self.sync_log("⚠️ No se detectaron puertos abiertos. Lanzando Evasión Sigilosa...")
            self.run_command(f"nmap -sF --top-ports 1000 -Pn -n --open -T3 --data-length 25 --spoof-mac cisco {target}", callback=self.fase_1_stealth_callback)
            return

        self.lanzar_fase_2(ports)

    def fase_1_stealth_callback(self, output):
        ports = re.findall(r"(\d+)/tcp\s+open", output)
        if not ports:
            self.sync_log("❌ Tampoco se detectaron puertos con sigilo. Host caído o totalmente protegido.")
            return
        self.lanzar_fase_2(ports)

    def lanzar_fase_2(self, ports):
        port_list = ",".join(ports)
        target = self.target.get().strip()
        safe_t = self.get_safe_target_name()
        
        self.sync_log(f"\n✅ Puertos confirmados: {port_list}\n[🚀 FASE 2] Extrayendo Versiones y Servicios...")
        
        time_mark = datetime.now().strftime("%H%M%S")
        self.current_fase2_base = f"{self.folder}/nmap_auto_{safe_t}_{time_mark}_fase2"
        self.current_fase3_base = f"{self.folder}/nmap_auto_{safe_t}_{time_mark}_fase3"
        
        cmd = f"nmap -sSCV -Pn -n -v -p {port_list} {target}"
        if self.xml_status.get():
            cmd += f" -oA {self.current_fase2_base}"

        self.run_command(cmd, callback=lambda _: self.lanzar_fase_3(port_list, target))

    def lanzar_fase_3(self, port_list, target):
        self.sync_log(f"\n[🚀 FASE 3] Buscando Vulnerabilidades Conocidas (Scripts)...")
        cmd = f"nmap --script vuln -v -p {port_list} {target}"
        if self.xml_status.get():
            cmd += f" -oA {self.current_fase3_base}"

        self.run_command(cmd, callback=self.procesar_reportes)

    def procesar_reportes(self, _=None):
        if not self.xml_status.get():
            self.sync_log("✅ Escaneo CTF Finalizado (Archivos no requeridos).")
            return

        self.sync_log("\n[⚙️] Generando Reportes Inteligentes (Markdown, HTML, Prompt IA)...")
        target = self.target.get().strip()
        safe_t = self.get_safe_target_name()
        timestamp = datetime.now().strftime("%H%M%S")
        
        nmap_f2 = f"{self.current_fase2_base}.nmap"
        nmap_f3 = f"{self.current_fase3_base}.nmap"
        xml_f2 = f"{self.current_fase2_base}.xml"
        
        html_out = f"{self.folder}/Writeup_{safe_t}_{timestamp}.html"
        md_out = f"{self.folder}/Writeup_{safe_t}_{timestamp}.md"
        ia_out = f"{self.folder}/ia_prompt_{safe_t}.txt"

        if os.path.exists(xml_f2):
            try:
                subprocess.run(["xsltproc", xml_f2, "-o", html_out], stderr=subprocess.DEVNULL)
                self.sync_log(f"   ✔️ Reporte HTML generado.")
            except: pass

        if os.path.exists(nmap_f2):
            try:
                with open(nmap_f2, 'r', encoding='utf-8', errors='replace') as f:
                    data_f2 = f.read()
                
                md_content = f"# 🎯 CTF Writeup / Auto-Report: {target}\n"
                md_content += f"📅 **Fecha:** {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n\n"
                md_content += "## 🚪 Puertos y Servicios Detectados\n```text\n"
                ports_block = re.search(r'(PORT\s+STATE\s+SERVICE.*?\n\n)', data_f2, re.DOTALL)
                if ports_block: md_content += ports_block.group(1)
                md_content += "```\n\n## ⚡ Vulnerabilidades (Nmap Vuln)\n"
                
                if os.path.exists(nmap_f3):
                    with open(nmap_f3, 'r', encoding='utf-8', errors='replace') as f3:
                        md_content += "```text\n"
                        vuln_block = re.search(r'(PORT\s+STATE\s+SERVICE.*?\n\n)', f3.read(), re.DOTALL)
                        if vuln_block: md_content += vuln_block.group(1)
                        md_content += "```\n"

                with open(md_out, 'w', encoding='utf-8') as f: f.write(md_content)
                self.sync_log(f"   ✔️ Writeup Markdown estructurado.")
                
                ia_content = f"Actúa como tutor de CTF. Objetivo: {target}\n\n{md_content}"
                with open(ia_out, 'w', encoding='utf-8') as f: f.write(ia_content)
                self.sync_log(f"   ✔️ Prompt de IA guardado.")

            except Exception as e:
                self.sync_log(f"   ⚠️ Error de parseo MD: {e}")

        # Limpieza de temporales
        for ext in ['.xml', '.nmap', '.gnmap']:
            try:
                if os.path.exists(self.current_fase2_base + ext): os.remove(self.current_fase2_base + ext)
                if os.path.exists(self.current_fase3_base + ext): os.remove(self.current_fase3_base + ext)
            except: pass
        self.sync_log("\n✅ Limpieza lista. Resultados en la carpeta generada.")

    def run_nmap_submenu(self):
        choice = self.nmap_opt.get()
        target = self.target.get().strip()
        safe_t = self.get_safe_target_name()
        
        cmds = {
            "1.": f"nmap -sS -O -Pn -n -vvv -T4 {target}",
            "2.": f"nmap -sS -p- -Pn -n --min-rate 5000 {target}",
            "3.": f"nmap -A -Pn -v {target}",
            "4.": f"nmap -sS -sCV -Pn -v {target}",
            "5.": f"nmap --script vuln -v -Pn {target}",
            "6.": f"nmap -sA -Pn -vv -T4 {target}",
            "7.": f"nmap -sS -Pn -vv -f -D RND:5 -g 53 --data-length 25 {target}",
            "8.": f"nmap -sU -Pn --top-ports 20 -T4 {target}",
            "9.": f"nmap -sU -sV -Pn {target}",
            "10.": f"nmap --script http-enum,http-robots.txt,http-title -p 80,443 -Pn {target}",
            "11.": f"nmap --script http-vuln-* -p 80,443 -v -Pn {target}"
        }

        for key, cmd in cmds.items():
            if choice.startswith(key):
                if self.xml_status.get() and self.init_folder():
                    cmd += f" -oX {self.folder}/nmap_{safe_t}_{datetime.now().strftime('%H%M%S')}.xml"
                self.run_command(cmd)
                return
        messagebox.showinfo("Info", "Selecciona una opción válida del menú desplegable.")

    def run_win_submenu(self):
        choice = self.win_opt.get()
        target = self.target.get().strip()
        
        cmds = {
            "1.": f"nmap --script smb-os-discovery,smb-enum-shares -p 139,445 -Pn {target}",
            "2.": f"nmap -sU -p 137 --script nbstat -Pn {target}",
            "3.": f"nmap --script smb-vuln* -p 139,445 -Pn {target}",
            "4.": f"smbclient -L //{target} -N",
            "5.": f"nbtscan -r {target}",
            "6.": f"enum4linux -a {target}"
        }

        for key, cmd in cmds.items():
            if choice.startswith(key):
                self.run_command(cmd)
                return
        messagebox.showinfo("Info", "Selecciona una opción de Windows válida.")

    def run_whatweb(self):
        target = self.target.get().strip()
        self.run_command(f"whatweb -a 1 -t 1 -v --no-errors --open-timeout=5 --read-timeout=5 {target}")

    def run_ferox(self):
        target = self.target.get().strip()
        url = target if target.startswith("http") else f"http://{target}"
        
        real_home = os.path.expanduser("~")
        if 'SUDO_USER' in os.environ:
            real_home = os.path.expanduser(f"~{os.environ['SUDO_USER']}")
            
        possible_paths = [
            f"{real_home}/seclists/Discovery/Web-Content/common.txt",
            "/usr/share/seclists/Discovery/Web-Content/common.txt",
            "/snap/seclists/current/Discovery/Web-Content/common.txt"
        ]
        wordlist = next((w for w in possible_paths if os.path.exists(w)), "common.txt")
        
        self.run_command(f"feroxbuster --url {url} --wordlist {wordlist} --extensions bak,zip,txt,sql,old,php.bak --no-recursion --filter-size 0 --threads 50 --timeout 5")

    def run_wpscan(self):
        target = self.target.get().strip()
        sub = self.sub_path.get().strip()
        
        url = target if target.startswith("http") else f"http://{target}"
        if sub: 
            url = f"{url.rstrip('/')}/{sub.lstrip('/')}"
            
        self.run_command(f"wpscan --url {url} -e u,ap --detection-mode aggressive --force")

if __name__ == "__main__":
    root = tk.Tk()
    app = Scan4MeApp(root)
    root.mainloop()