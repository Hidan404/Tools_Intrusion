import requests


def diretorio_bruteforce(url, wordlist):
    """
    Função para realizar brute force em diretórios de um site.

    :param url: URL do site alvo
    :param wordlist: Lista de palavras para brute force
    :return: None
    """
    for word in wordlist:
        # Monta a URL com o diretório atual
        target_url = f"{url}/{word.strip()}"
        try:
            response = requests.get(target_url)
            if response.status_code == 200:
                print(f"[+] Encontrado: {target_url}")
            else:
                print(f"[-] Não encontrado: {target_url} (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {target_url}: {e}")