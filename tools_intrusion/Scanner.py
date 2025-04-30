import socket
import threading
from queue import Queue
import time
import random
import os

# Configurações
NUM_THREADS = 100
TIMEOUT = 1
portas_abertas = []
lock = threading.Lock()

# ======== FINGERPRINT OS VIA TTL ========
def fingerprint_ttl(ip):
    print("\n[+] Realizando fingerprint do sistema operacional via TTL...")
    try:
        if os.name == "posix":
            output = os.popen(f"ping -c 1 {ip}").read()
        else:
            output = os.popen(f"ping -n 1 {ip}").read()

        for linha in output.splitlines():
            if "ttl=" in linha.lower():
                ttl = int([seg for seg in linha.lower().split() if "ttl=" in seg][0].split("=")[1])
                if ttl <= 64:
                    sistema = "Provavelmente Linux/Unix"
                elif ttl <= 128:
                    sistema = "Provavelmente Windows"
                elif ttl <= 255:
                    sistema = "Provavelmente Cisco/Unix BSD"
                else:
                    sistema = "Desconhecido"
                print(f"[✓] TTL identificado: {ttl} ➜ {sistema}")
                return
        print("[-] TTL não identificado.")
    except Exception as e:
        print(f"[!] Erro ao obter TTL: {e}")

# ======== FUZZING BANNER DE SERVIÇO ========
def banner_fuzz(ip, porta):
    try:
        payloads = [b"\n", b"HEAD / HTTP/1.0\r\n\r\n", b"HELP\r\n"]
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, porta))
        for payload in payloads:
            try:
                s.send(payload)
                resposta = s.recv(1024).decode(errors="ignore").strip()
                if resposta:
                    return resposta
            except:
                continue
        return "Nenhuma resposta"
    except:
        return "Conexão falhou"
    finally:
        s.close()

# ======== SCAN DE PORTA COM OU SEM MODO STEALTH ========
def escanear(ip, porta, stealth=False):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        resultado = s.connect_ex((ip, porta))
        s.close()
        if resultado == 0:
            banner = banner_fuzz(ip, porta)
            with lock:
                portas_abertas.append((porta, banner))
                print(f"[+] Porta {porta} aberta ➜ Banner: {banner}")
        if stealth:
            time.sleep(random.uniform(0.5, 2.0))  # Atraso aleatório entre scans
    except Exception as e:
        with lock:
            print(f"[!] Erro ao escanear porta {porta}: {e}")

# ======== WORKER THREAD ========
def worker(ip, fila, stealth=False):
    while not fila.empty():
        porta = fila.get()
        escanear(ip, porta, stealth)
        fila.task_done()

# ======== EXECUTA O SCAN ========
def executar_scan(ip, portas, stealth=False):
    print(f"\n[~] Iniciando scan em {ip} (stealth={stealth}) - Portas {portas[0]} até {portas[-1]}")
    fila = Queue()
    for porta in portas:
        fila.put(porta)

    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(ip, fila, stealth))
        t.daemon = True
        t.start()

    fila.join()

    print("\n[✓] Scan finalizado.")
    if portas_abertas:
        print("\n[+] Portas abertas detectadas:")
        for porta, banner in portas_abertas:
            print(f"  → Porta {porta}: {banner}")
    else:
        print("[-] Nenhuma porta aberta encontrada.")

# ======== MAIN ========
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("==== Scanner de Portas com Fingerprinting de Sistema e Fuzz de Banners ====")
    alvo = input("Digite o IP ou hostname do alvo: ").strip()

    porta_inicio = int(input("Porta inicial (ex: 1): ").strip())
    porta_fim = int(input("Porta final (ex: 1024): ").strip())
    modo_stealth = input("Modo stealth (s/n)? ").strip().lower() == 's'

    fingerprint_ttl(alvo)
    portas = list(range(porta_inicio, porta_fim + 1))
    executar_scan(alvo, portas, stealth=modo_stealth)
