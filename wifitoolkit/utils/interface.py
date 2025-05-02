def exibir_menu():
    print("""\033[1;32m
    [Menu principal]
    1. Iniciar modo monitor
    2. Parar modo monitor
    ...
    00. Sair
    """)
    return input("Escolha uma opção: ").strip()

def obter_entrada(mensagem):
    return input(mensagem).strip()