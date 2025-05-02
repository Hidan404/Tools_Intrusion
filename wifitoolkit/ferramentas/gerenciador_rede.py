import subprocess

class GerenciadorRede:
    def __init__(self, interface):
        self.interface = interface

    def iniciar_modo_monitor(self):
        try:
            subprocess.run(
                ['sudo', 'airmon-ng', 'start', self.interface, '&&', 'airmon-ng', 'check', 'kill'],
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def parar_modo_monitor(self):
        try:
            subprocess.run(
                ['sudo', 'airmon-ng', 'stop', self.interface, '&&', 'systemctl', 'restart', 'NetworkManager'],
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def escanear_redes(self):
        try:
            resultado = subprocess.run(
                ['sudo', 'airodump-ng', self.interface, '-M'],
                capture_output=True,
                text=True,
                check=True
            )
            return resultado.stdout
        except subprocess.CalledProcessError:
            return None