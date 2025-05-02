import subprocess

class QuebradorSenha:
    def __init__(self, arquivo_handshake):
        self.arquivo = arquivo_handshake

    def quebrar_com_rockyou(self):
        try:
            resultado = subprocess.run(
                ['aircrack-ng', self.arquivo, '-w', '/usr/share/wordlists/rockyou.txt'],
                capture_output=True,
                text=True,
                check=True
            )
            return resultado.stdout
        except subprocess.CalledProcessError:
            return None

    def quebrar_com_wordlist(self, wordlist):
        try:
            resultado = subprocess.run(
                ['aircrack-ng', self.arquivo, '-w', wordlist],
                capture_output=True,
                text=True,
                check=True
            )
            return resultado.stdout
        except subprocess.CalledProcessError:
            return None