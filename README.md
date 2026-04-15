Markdown
# 🛡️ scan4me, ahora en versión python (Estamos en obras)

**scan4me** es una herramienta de escaneo interactivo diseñada para agilizar la fase de reconocimiento en auditorías de seguridad y entornos de CTF. Esta versión en Python ofrece una interfaz gráfica clara (Light Mode) y está optimizada para ejecutarse en Windows y Linux.

![Versión](https://img.shields.io/badge/Versión-3.5.2-blue)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Características Principales

* **Interfaz Gráfica Intuitiva:** Diseño limpio con tipografía optimizada para lectura de logs técnicos.
* **Escaneo Automático en Fases:**
    * **Fase 1:** Descubrimiento rápido de puertos abiertos.
    * **Fase 2:** Enumeración detallada de servicios y versiones.
    * **Fase 3:** Escaneo automático de vulnerabilidades con scripts de Nmap.
* **Submenú de Nmap:** Selección rápida de modos (UDP, Puertos totales, Web Recon, etc.).
* **Integración Multi-Herramienta:** Acceso directo a `WhatWeb`, `Feroxbuster` y `WPScan`.
* **Gestión de Reportes:** Creación automática de carpetas por objetivo con logs detallados y reportes XML opcionales.
* **Soporte para Subdominios/Rutas:** Campo específico para auditar carpetas como `/wordpress` o `/dev`.

---

## 📸 Vista Previa
> El programa cuenta con un banner ASCII clásico de la versión original y una consola de alta legibilidad con fuente *Consolas* tamaño 12 para evitar la fatiga visual.

---

## 🛠️ Instalación y Requisitos

### Dependencias del Sistema
Para que el script ejecute las herramientas correctamente, debes tener instalado:
* [Nmap](https://nmap.org/)
* [Feroxbuster](https://github.com/epi052/feroxbuster)
* [WPScan](https://wpscan.com/)
* [WhatWeb](https://github.com/urbanadventurer/WhatWeb)

### Ejecución en Linux (Kali/Parrot)
1. Instalar soporte de interfaz gráfica:
   ```bash
   sudo apt install python3-tk -y
Ejecutar el script:

Bash
sudo python3 scan4me.py
Ejecución en Windows
Descarga el ejecutable desde la sección de Releases.

O ejecuta el script con Python instalado:

Bash
python scan4me.py
📦 Compilación a .exe (Windows)
Si deseas generar tu propio ejecutable para Windows sin dependencias externas de Python:

Instala PyInstaller:

Bash
pip install pyinstaller
Compila el proyecto:

Bash
pyinstaller --noconsole --onefile scan4me.py
El archivo resultante estará en la carpeta dist/.

⚖️ Descargo de Responsabilidad
Esta herramienta ha sido creada exclusivamente para fines educativos y auditorías de seguridad autorizadas. El uso de esta herramienta contra objetivos sin consentimiento previo es ilegal. El autor no se hace responsable del mal uso de este software.
