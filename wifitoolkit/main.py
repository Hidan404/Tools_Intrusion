from ferramentas.instalador import FedoraInstaller
from ferramentas.gerenciador_rede import GerenciadorRede
from utils.interface import exibir_menu, obter_entrada

class WifiToolkitApp:
    def __init__(self):
        self.interface = None
        self.gerenciador = None

    def executar(self):
        FedoraInstaller.instalar_todas()
        while True:
            escolha = exibir_menu()
            self.processar_escolha(escolha)

    def processar_escolha(self, escolha):
        if escolha == '1':
            self.iniciar_modo_monitor()
        elif escolha == '2':
            self.parar_modo_monitor()
        # ... outros casos

    def iniciar_modo_monitor(self):
        interface = obter_entrada("Digite a interface (padrão: wlan0): ")
        self.gerenciador = GerenciadorRede(interface)
        if self.gerenciador.iniciar_modo_monitor():
            print("Modo monitor iniciado com sucesso!")
        else:
            print("Erro ao iniciar modo monitor")

if __name__ == "__main__":
    app = WifiToolkitApp()
    app.executar()