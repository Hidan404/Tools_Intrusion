import socket
import threading


def Scanner_portas(ip, portas):
    """
    Função que escaneia portas de um IP específico.
    :param ip: IP a ser escaneado
    :param portas: Lista de portas a serem escaneadas
    :return: None
    """
    for porta in portas:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            resultado = s.connect_ex((ip, porta))
            if resultado == 0:
                print(f"Porta {porta} está aberta.")
            else:
                print(f"Porta {porta} está fechada.")
            s.close()
        except socket.error as e:
            print(f"Erro ao conectar na porta {porta}: {e}")