# GCOTT - Get Control Of The Target

[![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.12+](https://img.shields.io/badge/Python-3.12+-blueviolet.svg)](https://www.python.org/downloads/)
[![Maintenance: Active](https://img.shields.io/badge/Maintenance-Active-success.svg)](https://github.com/cihaneray/GCOTT)
[![OS](https://img.shields.io/badge/OS-Linux%20%7C%20Windows%20%7C%20macOS-orange.svg)]()

## Overview

**GCOTT** (pronounced "jee-cott") is a command and control framework designed for security professionals and system administrators. It enables authorized users to establish secure connections to remote systems for command execution, file transfer, and system management.

> **IMPORTANT**: This tool is intended for authorized security assessments and legitimate system administration only. Unauthorized use is strictly prohibited and may be illegal.

## Features

- **Interactive Command Console:** Execute shell commands on target systems with real-time output
- **File Transfer:** Upload and download files between control and target systems
- **Directory Navigation:** Browse and traverse the target file system
- **System Intelligence:** Gather information about the target operating system and user context
- **Desktop Surveillance:** Capture and retrieve screenshots from the target machine
- **Interactive Shell:** Establish fully interactive shell sessions on the target
- **Custom Payload Generation:** Create Python payloads with configurable connection parameters
- **Password Decryption Module:** Attempt to crack hashed passwords using various algorithms and wordlists
- **Firewall Bypass Capabilities:** Configure firewall rules to facilitate outbound communication (experimental)
- **User-Friendly Interface:** Clear prompts and color-coded output for improved usability
- **Modular Architecture:** Well-structured codebase designed for extensibility

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/username/GCOTT.git
   cd GCOTT
   ```

2. **Verify Python installation:**
   ```bash
   python3 --version
   ```
   Ensure you have Python 3.12 or higher installed.

3. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

## Usage Guide

GCOTT operates on a client-server model with a **listener** (your control system) and a **payload** (the target system).

### Payload Generation

1. Launch GCOTT:
   ```bash
   python3 gcott.py
   ```

2. Access the payload generator:
   ```
   GCOTT -> generate
   ```

3. View available payloads:
   ```
   GCOTT@Payload -> list
   ```

4. Configure your payload:
   ```
   GCOTT@Payload -> set reverseShell.py
   GCOTT@reverseShell -> set host_ip [your_listening_ip]
   GCOTT@reverseShell -> set host_port [your_listening_port]
   ```

5. Generate the payload:
   ```
   GCOTT@reverseShell -> generate
   ```
   This creates a `payload.py` file in the GCOTT directory.

### Listener Setup

1. Launch GCOTT:
   ```bash
   python3 gcott.py
   ```

2. Start the listener:
   ```
   GCOTT -> listen
   ```

3. Configure listener settings:
   ```
   GCOTT@Listen -> show
   GCOTT@Listen -> set host_ip [your_listening_ip]
   GCOTT@Listen -> set host_port [your_listening_port]
   ```

4. Activate the listener:
   ```
   GCOTT@Listen -> execute
   ```

### Payload Deployment

1. Transfer the generated `payload.py` to the target system using an authorized method.

2. Execute the payload on the target system:
   ```bash
   python3 payload.py
   ```

### Target Interaction

Once connected, your prompt will display the target's IP address:
```
[target_ip]@GCOTT->
```

Use the `help` command to view available options:
```
[target_ip]@GCOTT-> help
```

### Password Cracking Module

1. Launch GCOTT:
   ```bash
   python3 gcott.py
   ```

2. Access the password module:
   ```
   GCOTT -> password
   ```

3. Follow the interactive prompts to input hash data and configuration options.

## Payloads Repository

The `payloads` directory contains example Python scripts that can be used as templates. Contributions of additional custom payloads are welcome.

## Contributing

We welcome contributions to GCOTT. Please submit pull requests for bug fixes, new features, or improvements to the existing codebase.

## License

This project is licensed under the MIT License.

## Acknowledgements

- The `art` library for ASCII banner generation
- The `termcolor` library for terminal output coloring
- The `pyautogui` library for screenshot capabilities

---

**Reminder**: Always use this tool responsibly and only with proper authorization.
```

This version maintains all the key information while presenting it in a more professional, concise manner. I've reduced some of the flowery language while keeping the important details about installation, usage, and legal considerations.