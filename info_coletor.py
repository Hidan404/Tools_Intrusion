import whois
import socket
import dns.resolver
from urllib.parse import urlparse

def entrada_dominio():
    dominio = input("Digite o domínio (exemplo: www.exemplo.com): ").strip()
    if dominio.startswith("http://") or dominio.startswith("https://"):
        dominio = urlparse(dominio).netloc
    return dominio

def printar_whois_info(w):
    print("\n[+] Informações WHOIS:")
    try:
        print(f"  - Nome do domínio: {w.domain_name}")
        print(f"  - Organização: {w.org}")
        print(f"  - Criado em: {w.creation_date}")
        print(f"  - Expira em: {w.expiration_date}")
        print(f"  - Servidores DNS: {w.name_servers}")
    except Exception as e:
        print(f"  [!] Erro ao interpretar WHOIS: {e}")

def consultar_dns(dominio):
    print("\n[+] Resolvendo registros DNS:")
    tipos = ['A', 'AAAA', 'MX', 'NS', 'TXT']
    for tipo in tipos:
        try:
            respostas = dns.resolver.resolve(dominio, tipo)
            print(f"\n  Registros {tipo}:")
            for rdata in respostas:
                print(f"    - {rdata.to_text()}")
        except Exception:
            continue

def coletar_informacoes_dominio(dominio):
    print(f"\n[~] Coletando informações para: {dominio}")

    # WHOIS
    try:
        w = whois.whois(dominio)
        printar_whois_info(w)
    except Exception as e:
        print(f"[!] Erro WHOIS: {e}")

    # IP
    try:
        ip = socket.gethostbyname(dominio)
        print(f"\n[+] IP do domínio: {ip}")
    except Exception as e:
        print(f"[!] Erro ao resolver IP: {e}")

    # DNS
    consultar_dns(dominio)


