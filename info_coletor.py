import whois
import socket
import dns.resolver


def coletar_informacoes_dominio(dominio):
    print(f"Coletando informações para o domínio: {dominio}")
    try:
        w = whois.whois(dominio)
        print("Informações do domínio:")
        print(f"Nome do domínio: {w.domain_name}")
    except Exception as e:
        print(f"Erro ao coletar informações do domínio: {e}")
        return
    
    try:
        ip = socket.gethostbyname(dominio)
        print(f"IP do domínio: {ip}")
    except socket.gaierror as e:
        print(f"Erro ao resolver o domínio: {e}")
        return
    
    try:
        resolver = dns.resolver.Resolver()
        resposta = resolver.resolve(dominio, 'A')
        print(f"Endereço IP: {resposta[0]}")
    except dns.resolver.NoAnswer as e:
        print(f"Erro ao resolver o domínio: {e}")
        return
    except dns.resolver.NXDOMAIN as e:
        print(f"Erro ao resolver o domínio: {e}")
        return
    except dns.exception.Timeout as e:
        print(f"Erro ao resolver o domínio: {e}")
        return
    except Exception as e:
        print(f"Erro ao resolver o domínio: {e}")
        return    