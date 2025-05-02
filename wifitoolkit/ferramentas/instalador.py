import subprocess
import platform

class FedoraInstaller:
    FERRAMENTAS = {
        'aircrack-ng': ['aircrack-ng'],
        'crunch': ['crunch'],
        'wifite': ['python3-wifite'],
        'reaver': ['reaver', 'pixiewps'],
        'bully': ['bully']
    }

    @classmethod
    def instalar_ferramentas(cls, ferramenta):
        sistema = platform.freedesktop_os_release()
        if sistema['ID'] != 'fedora' or int(sistema['VERSION_ID']) < 42:
            raise OSError("Este script só é compatível com Fedora 42 ou superior")

        if ferramenta not in cls.FERRAMENTAS:
            raise ValueError(f"Ferramenta não suportada: {ferramenta}")

        pacotes = cls.FERRAMENTAS[ferramenta]
        try:
            subprocess.run(
                ['sudo', 'dnf', 'install', '-y'] + pacotes,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except subprocess.CalledProcessError:
            return False

    @classmethod
    def instalar_todas(cls):
        for ferramenta in cls.FERRAMENTAS:
            if not cls.instalar_ferramentas(ferramenta):
                return False
        return True