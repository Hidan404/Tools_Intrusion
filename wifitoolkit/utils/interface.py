def exibir_menu():
    print("""\033[1;32m
    [MENU PRINCIPAL]
    1. Iniciar modo monitor
    2. Parar modo monitor
    3. Escanear redes
    4. Capturar handshake
    5. Quebrar senha com rockyou.txt
    6. Quebrar senha com wordlist personalizada
    7. Ataque WPS (Reaver)
    
    00. Sair
    \033[0m""")
    return input("Escolha uma opção: ").strip()

def obter_entrada(mensagem):
    return input(f"\n{mensagem}: ").strip()