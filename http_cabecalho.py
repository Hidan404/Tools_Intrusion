import requests
import random
import time
from urllib.parse import urlparse

# ========== CONFIGURAÇÕES ==========

TOR_PROXY = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Firefox/115.0",
    "curl/7.68.0"
]

# ========== FUNÇÃO DE ENUMERAÇÃO ==========

def analisar_headers(url, usar_tor=False):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "*/*",
        "Connection": "close"
    }

    proxies = TOR_PROXY if usar_tor else None

    try:
        print(f"\n[~] Analisando cabeçalhos de: {url}")
        response = requests.get(url, headers=headers, proxies=proxies, timeout=7)

        print(f"\n[+] Status: {response.status_code}")
        print("[+] Cabeçalhos HTTP:")
        for k, v in response.headers.items():
            print(f"  {k}: {v}")

        print("\n[~] Verificando possíveis tecnologias e segurança:")

        server = response.headers.get("Server", "Desconhecido")
        powered_by = response.headers.get("X-Powered-By", "")
        waf = "cloudflare" in server.lower() or "sucuri" in server.lower()

        print(f"  - Servidor: {server}")
        print(f"  - Powered By: {powered_by if powered_by else 'N/A'}")
        print(f"  - WAF Detectado: {'Sim' if waf else 'Não'}")

        if "Strict-Transport-Security" not in response.headers:
            print("  ⚠️ HSTS NÃO habilitado (risco de downgrade attack)")
        if "X-Frame-Options" not in response.headers:
            print("  ⚠️ Sem proteção contra clickjacking")
        if "Access-Control-Allow-Origin" in response.headers:
            print("  ⚠️ CORS exposto: ", response.headers["Access-Control-Allow-Origin"])

        cookies = response.cookies
        if cookies:
            print("\n[+] Cookies identificados:")
            for c in cookies:
                print(f"  - {c.name}: HttpOnly={c._rest.get('HttpOnly', False)}, Secure={c.secure}")
        else:
            print("  - Nenhum cookie identificado.")

        salvar_log(url, response)

    except requests.exceptions.RequestException as e:
        print(f"[!] Erro ao acessar {url}: {e}")

# ========== FUNÇÃO DE LOG ==========

def salvar_log(url, resp):
    parsed = urlparse(url)
    dominio = parsed.netloc.replace(".", "_")
    nome_arquivo = f"header_log_{dominio}.txt"

    with open(nome_arquivo, "w") as f:
        f.write(f"URL: {url}\nStatus: {resp.status_code}\n\n")
        f.write("=== Cabeçalhos HTTP ===\n")
        for k, v in resp.headers.items():
            f.write(f"{k}: {v}\n")

        f.write("\n=== Cookies ===\n")
        for c in resp.cookies:
            f.write(f"{c.name}: HttpOnly={c._rest.get('HttpOnly', False)}, Secure={c.secure}\n")

    print(f"\n[✓] Log salvo em: {nome_arquivo}")

# ========== EXECUÇÃO ==========

def main():
    print("==== 🔍 HTTP Header Recon ====")
    alvo = input("URL do alvo (ex: https://site.com): ").strip()
    usar_tor = input("Usar TOR? (s/n): ").strip().lower() == 's'

    analisar_headers(alvo, usar_tor)
