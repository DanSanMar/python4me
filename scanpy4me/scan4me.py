import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import os
import re
from datetime import datetime

class Scan4Me:
    def __init__(self, root):
        self.root = root
        self.root.title("ALL 4 ME - Pentest Suite v3.5.2")
        self.root.geometry("1000x750")
        self.root.configure(bg="#121212")

        self.target = tk.StringVar()
        self.xml_status = tk.BooleanVar(value=False)
        self.folder = ""
        
        self.setup_ui()

    def setup_ui(self):
        # --- Estilos ---
        style = ttk.Style()
        style.theme_use('clam')
        
        # --- Banner ASCII ---
        banner = tk.Text(self.root, height=8, bg="#121212", fg="#00f2ff", font=("Courier New", 9), borderwidth=0)
        banner.insert(tk.END, """
      █████╗ ██╗      ██╗      ██╗  ██╗███╗   ███╗███████╗
     ██╔══██╗██║      ██║      ██║  ██║████╗ ████║██╔════╝
     ███████║██║      ██║      ███████║██╔████╔██║█████╗  
     ██╔══██║██║      ██║      ╚════██║██║╚██╔╝██║██╔══╝  
     ██║  ██║███████╗███████╗      ██║██║ ╚═╝ ██║███████╗
     ╚═╝  ╚═╝╚══════╝╚══════╝      ╚═╝╚═╝     ╚═╝╚══════╝""")
        banner.tag_configure("center", justify='center')
        banner.tag_add("center", "1.0", "end")
        banner.pack(fill="x", pady=5)

        # --- Panel de Entrada ---
        input_frame = tk.Frame(self.root, bg="#1c1c1c", padx=10, pady=10)
        input_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(input_frame, text="TARGET IP/URL:", fg="white", bg="#1c1c1c", font=("Consolas", 10, "bold")).pack(side="left")
        tk.Entry(input_frame, textvariable=self.target, width=30, bg="#333", fg="white", insertbackground="white").pack(side="left", padx=10)
        
        tk.Checkbutton(input_frame, text="XML REPORT", variable=self.xml_status, fg="#00ff00", bg="#1c1c1c", selectcolor="black").pack(side="left", padx=10)

        # --- Botonera Principal ---
        btn_frame = tk.Frame(self.root, bg="#121212")
        btn_frame.pack(fill="x", padx=20, pady=10)

        # Definición de botones (Texto, Comando, Color)
        actions = [
            ("AUTO SCAN (NMAP)", self.start_auto_scan, "#0078d7"),
            ("WEB RECON", self.run_whatweb, "#5f378a"),
            ("FUZZING", self.run_ferox, "#c1272d"),
            ("WPSCAN", self.run_wpscan, "#217346"),
            ("CLEAN LOGS", self.clear_console, "#444")
        ]

        for text, cmd, color in actions:
            btn = tk.Button(btn_frame, text=text, command=cmd, bg=color, fg="white", width=15, relief="flat", font=("Consolas", 9, "bold"))
            btn.pack(side="left", padx=5)

        # --- Consola de Salida ---
        self.output = scrolledtext.ScrolledText(self.root, bg="black", fg="#00ff00", font=("Consolas", 10))
        self.output.pack(expand=True, fill="both", padx=20, pady=10)

    def write_log(self, text, color="#00ff00"):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        # Guardar en archivo
        if self.folder:
            with open(f"{self.folder}/auditoria.log", "a", encoding="utf-8") as f:
                f.write(text + "\n")

    def clear_console(self):
        self.output.delete('1.0', tk.END)

    def run_command(self, cmd_list, callback=None):
        """ Ejecuta comandos de forma asíncrona para no congelar la ventana """
        def task():
            try:
                # En Windows es vital shell=True para comandos del sistema
                process = subprocess.Popen(
                    cmd_list, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, 
                    text=True, 
                    shell=True,
                    encoding='utf-8',
                    errors='replace'
                )
                full_output = []
                for line in process.stdout:
                    clean_line = line.strip()
                    self.write_log(clean_line)
                    full_output.append(clean_line)
                
                process.wait()
                if callback:
                    callback("\n".join(full_output))
            except Exception as e:
                self.write_log(f"ERROR: {str(e)}", "red")

        threading.Thread(target=task, daemon=True).start()

    # --- Lógica de Escaneo Automático (La más compleja) ---
    def start_auto_scan(self):
        target = self.target.get()
        if not target: return messagebox.showwarning("Falta Target", "Escribe una IP o Dominio")
        
        # Preparar carpeta
        date_str = datetime.now().strftime("%d-%m-%Y")
        self.folder = f"Auditoria_{target}_{date_str}"
        if not os.path.exists(self.folder): os.makedirs(self.folder)

        self.write_log(f"--- INICIANDO FASE 1: DESCUBRIMIENTO DE PUERTOS EN {target} ---", "#00ffff")
        
        # Paso 1: Descubrir puertos (Equivalente al logic del script Bash)
        # Usamos -oG - para que sea fácil de parsear con Regex
        cmd = f"nmap -sS -p- --open -T4 -Pn -n {target}"
        self.run_command(cmd, callback=self.fase_2_scan)

    def fase_2_scan(self, output):
        # Extraer puertos usando Regex (busca números antes de /tcp)
        ports = re.findall(r"(\d+)/tcp\s+open", output)
        if not ports:
            self.write_log("[-] No se encontraron puertos abiertos.", "red")
            return
        
        port_list = ",".join(ports)
        self.write_log(f"[+] Puertos detectados: {port_list}", "#00ff00")
        self.write_log(f"--- INICIANDO FASE 2: VERSIONES Y SCRIPTS ---", "#00ffff")
        
        xml_cmd = ""
        if self.xml_status.get():
            xml_path = f"{self.folder}/nmap_report_{datetime.now().strftime('%H%M%S')}.xml"
            xml_cmd = f"-oX {xml_path}"

        cmd = f"nmap -sSCV -Pn -p {port_list} {xml_cmd} {self.target.get()}"
        self.run_command(cmd, callback=lambda _: self.write_log("--- ESCANEO FINALIZADO ---", "#00ff00"))

    # --- Otras Herramientas ---
    def run_whatweb(self):
        target = self.target.get()
        self.write_log(f"--- WHATWEB RECON: {target} ---", "#5f378a")
        # Nota: Whatweb suele requerir Ruby en Windows, asegúrate que esté en el PATH
        self.run_command(f"whatweb -a 3 -v {target}")

    def run_ferox(self):
        target = self.target.get()
        url = target if target.startswith("http") else f"http://{target}"
        # Buscamos wordlist en carpeta actual para el .exe
        wordlist = "common.txt" 
        self.write_log(f"--- FEROXBUSTER FUZZING: {url} ---", "#c1272d")
        self.run_command(f"feroxbuster --url {url} -w {wordlist} -t 50 --no-recursion")

    def run_wpscan(self):
        target = self.target.get()
        url = target if target.startswith("http") else f"http://{target}"
        self.write_log(f"--- WPSCAN ENUMERATION: {url} ---", "#217346")
        self.run_command(f"wpscan --url {url} --enumerate u,ap --detection-mode aggressive --force")

if __name__ == "__main__":
    root = tk.Tk()
    app = Scan4Me(root)
    root.mainloop()