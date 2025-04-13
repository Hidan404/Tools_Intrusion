import requests

def mostraar_cabecalho(url):
    """
    Função para mostrar o cabeçalho HTTP de uma URL.

    :param url: URL alvo
    :return: None
    """
    try:
        response = requests.get(url)
        print(f"URL: {url}")
        print("Cabeçalho HTTP:")
        for key, value in response.headers.items():
            print(f"{key}: {value}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")