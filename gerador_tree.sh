#!/bin/bash

# Criar a estrutura de diretórios
mkdir -p wifitoolkit/ferramentas wifitoolkit/utils

# Criar arquivos principais
touch wifitoolkit/main.py

# Criar arquivos na pasta ferramentas
touch wifitoolkit/ferramentas/{__init__.py,instalador.py,gerenciador_rede.py,captura_handshake.py,quebrador_senha.py,ataque_wps.py,gerador_wordlist.py}

# Criar arquivos na pasta utils
touch wifitoolkit/utils/{__init__.py,interface.py}

echo "Estrutura do projeto criada com sucesso!"