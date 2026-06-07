# 🛡️ scan4me, ahora en versión python

**scan4me** es una herramienta de escaneo interactivo diseñada para agilizar la fase de reconocimiento en auditorías de seguridad y entornos de CTF. Esta versión en Python ofrece una interfaz gráfica profesional y está optimizada para ejecutarse en entornos Linux (con soporte nativo para `bash` y herramientas de red) y Windows.

![Versión](https://img.shields.io/badge/Versión-5.6-blue)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Características Principales

* **Interfaz Gráfica Intuitiva:** Diseño limpio y moderno con soporte para maximizado.
* **Descubrimiento de Red (Nuevo):** Botón `DISCOVER HOSTS` para enumerar hosts activos en tu red mediante `arp-scan` y `ping sweep` de Nmap antes de empezar.
* **Escaneo Automático en Fases (CTF Mode):**
    * **Fase 1:** Descubrimiento agresivo de puertos (5000+ pkts/s).
    * **Fase 2:** Enumeración detallada de servicios y versiones (`-sSCV`).
    * **Fase 3:** Detección de vulnerabilidades con scripts NSE (`--script vuln`).
* **Sistemas Especializados:** Submenús dedicados para **Nmap** (múltiples técnicas de evasión y escaneo) y **Windows/SMB** (Enumeración, `smbclient`, `enum4linux`).
* **Integración Multi-Herramienta:** Acceso directo a `WhatWeb`, `Feroxbuster` (con búsqueda automática de wordlists) y `WPScan`.
* **Gestión de Reportes:** Creación automática de estructuras de carpetas, generación de archivos **Markdown**, **HTML** y prompts listos para IA.

---

## 📸 Vista Previa
> El programa ahora se abre a pantalla completa para mejorar la visibilidad de todos los elementos.

---

## 🛠️ Instalación y Requisitos

### Dependencias del Sistema
Para que todas las funciones de scan4me operen correctamente, el sistema debe tener instaladas las siguientes herramientas:

1. Reconocimiento de Red
nmap: Motor principal para escaneo de puertos, detección de servicios, versiones y scripts de vulnerabilidades (NSE).

arp-scan: Utilizado para el descubrimiento rápido de hosts en redes locales (Fase ARP).

2. Auditoría Web
whatweb: Identificación de tecnologías web, CMS, librerías y versiones de servidores.

feroxbuster: Herramienta de fuzzing de directorios de alto rendimiento.

wpscan: Escáner especializado en vulnerabilidades de WordPress.

3. Enumeración Windows / SMB
enum4linux: Enumeración de información en sistemas Windows (usuarios, grupos, shares).

nbtscan: Escaneo de nombres NetBIOS para identificar máquinas en la red.

smbclient: Interacción con recursos compartidos de Windows (incluyendo sesiones nulas).

4. Utilidades de Sistema (Requisito GUI)
python3-tk: Librería necesaria para visualizar la interfaz gráfica en sistemas Linux.

xsltproc: (Opcional) Necesario para procesar los reportes XML de Nmap y convertirlos a formatos legibles.

📥 Comando de Instalación (Kali/Debian/Ubuntu)
Puedes instalar la mayoría de estas dependencias ejecutando el siguiente comando en tu terminal:

Bash
sudo apt update && sudo apt install nmap arp-scan whatweb feroxbuster wpscan enum4linux nbtscan samba-common-bin xsltproc python3-tk -y
Nota: Si utilizas otra distribución (Arch, Fedora, etc.), asegúrate de instalar los paquetes equivalentes a través de tu gestor de paquetes (dnf, pacman, etc.).

### Ejecución en Linux (Kali/Parrot)
1. Instalar soporte de interfaz gráfica:
   ```bash
   sudo apt install python3-tk -y
   ```

Ejecutar el script:


```Bash
sudo python3 scan4me.py
```

Ejecución en Windows

Descarga el ejecutable desde la sección de Releases.

O ejecuta el script con Python instalado:


```Bash
python scan4me.py
```

📦 Compilación a .exe (Windows)
Si deseas generar tu propio ejecutable para Windows sin dependencias externas de Python:

Instala PyInstaller:

```Bash
pip install pyinstaller
```

Compila el proyecto:

```Bash
pyinstaller --noconsole --onefile scan4me.py
```

El archivo resultante estará en la carpeta ==dist/.==

⚖️ Descargo de Responsabilidad
Esta herramienta ha sido creada exclusivamente para fines educativos y auditorías de seguridad autorizadas. El uso de esta herramienta contra objetivos sin consentimiento previo es ilegal. El autor no se hace responsable del mal uso de este software.
