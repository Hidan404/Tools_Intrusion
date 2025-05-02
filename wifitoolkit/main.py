from ferramentas.instalador import FedoraInstaller
from ferramentas.gerenciador_rede import GerenciadorRede
from ferramentas.captura_handshake import CapturadorHandshake
from ferramentas.quebrador_senha import QuebradorSenha
from ferramentas.ataque_wps import AtaqueWPS
from utils.interface import exibir_menu, obter_entrada

class WifiToolkitApp:
    def __init__(self):
        self.interface = None
        self.gerenciador = None
        self.arquivo_handshake = None

    def executar(self):
        FedoraInstaller.instalar_todas()
        while True:
            escolha = exibir_menu()
            self.processar_escolha(escolha)
    
    def processar_escolha(self, escolha):
        try:
            if escolha == '1':
                self.iniciar_modo_monitor()
            elif escolha == '2':
                self.parar_modo_monitor()
            elif escolha == '3':
                self.escanear_redes()
            elif escolha == '4':
                self.capturar_handshake()
            elif escolha == '5':
                self.quebrar_senha_rockyou()
            elif escolha == '6':
                self.quebrar_senha_wordlist()
            elif escolha == '7':
                self.ataque_wps()
            elif escolha == '00':
                exit()
            else:
                print("\nOpção inválida! Tente novamente.")
        except Exception as e:
            print(f"\nErro: {str(e)}")
        input("\nPressione Enter para continuar...")

    def iniciar_modo_monitor(self):
        self.interface = obter_entrada("Digite a interface (ex: wlan0): ")
        self.gerenciador = GerenciadorRede(self.interface)
        if self.gerenciador.iniciar_modo_monitor():
            print(f"\nModo monitor iniciado em {self.interface}mon")
            self.interface += "mon"  # Atualiza interface para modo monitor
        else:
            print("\nFalha ao iniciar modo monitor!")

    def parar_modo_monitor(self):
        if self.gerenciador and self.gerenciador.parar_modo_monitor():
            print("\nModo monitor desativado!")
            self.interface = None
        else:
            print("\nNenhum modo monitor ativo!")

    def escanear_redes(self):
        if not self.interface:
            print("\nInicie o modo monitor primeiro!")
            return
            
        print("\nEscaneando redes... (Pressione Ctrl+C para parar)")
        redes = self.gerenciador.escanear_redes()
        print(redes)

    def capturar_handshake(self):
        if not self.interface:
            print("\nInicie o modo monitor primeiro!")
            return

        bssid = obter_entrada("Digite o BSSID alvo: ")
        canal = obter_entrada("Digite o canal: ")
        arquivo = obter_entrada("Nome do arquivo de saída: ")
        pacotes = obter_entrada("Número de pacotes de desautenticação (0 para contínuo): ")

        capturador = CapturadorHandshake(
            interface=self.interface,
            bssid=bssid,
            canal=canal,
            arquivo_saida=arquivo
        )
        
        if capturador.capturar(pacotes=int(pacotes)):
            self.arquivo_handshake = f"{arquivo}-01.cap"
            print("\nHandshake capturado com sucesso!")
        else:
            print("\nFalha ao capturar handshake!")

    def quebrar_senha_rockyou(self):
        if not self.arquivo_handshake:
            print("\nCapture um handshake primeiro!")
            return
            
        quebrador = QuebradorSenha(self.arquivo_handshake)
        resultado = quebrador.quebrar_com_rockyou()
        print(resultado or "\nSenha não encontrada na wordlist!")

    def quebrar_senha_wordlist(self):
        if not self.arquivo_handshake:
            print("\nCapture um handshake primeiro!")
            return
            
        wordlist = obter_entrada("Caminho completo da wordlist: ")
        quebrador = QuebradorSenha(self.arquivo_handshake)
        resultado = quebrador.quebrar_com_wordlist(wordlist)
        print(resultado or "\nSenha não encontrada na wordlist!")

    def ataque_wps(self):
        if not self.interface:
            print("\nInicie o modo monitor primeiro!")
            return
            
        bssid = obter_entrada("Digite o BSSID alvo: ")
        ataque = AtaqueWPS(self.interface, bssid)
        print("\nIniciando ataque WPS...")
        resultado = ataque.executar()
        print(resultado or "\nAtaque WPS falhou!")

if __name__ == "__main__":
    app = WifiToolkitApp()
    app.executar()