# RaspberryAI

Sistema embarcado desenvolvido em Python utilizando [Kivy](https://kivy.org/) para interface gráfica, integração com Firebase para armazenamento e API de inteligência artificial para respostas dinâmicas.  
O projeto também utiliza recursos de síntese de voz para interação por áudio, permitindo que o assistente leia informações e responda perguntas.

## 📌 Funcionalidades

- Interface gráfica responsiva desenvolvida com Kivy e `.kv` language.
- Integração com **Firebase** para gerenciamento de dados.
- Comunicação com API de IA (Together AI).
- Leitura em voz alta com **Google TTS** (`gtts`).
- Reprodução de áudio via `kivy.core.audio.SoundLoader`.
- Modularização do código para fácil manutenção.
- Suporte a múltiplas telas com mudança dinâmica de conteúdo.

## 🛠 Tecnologias utilizadas

- **Python 3**
- **Kivy** (Interface gráfica)
- **Firebase** (Banco de dados e autenticação)
- **gtts** (Google Text-to-Speech)
- **SoundLoader** (Reprodução de áudio)
- **API Together AI** (Integração de IA)
- **Git/GitHub** (Controle de versão)

## 📂 Estrutura do projeto

. ├── .kivy/                 # Arquivos de configuração do Kivy ├── frases/                # Áudios e textos pré-definidos ├── fotos/                 # Imagens utilizadas no app ├── foto_usuario/          # Fotos tiradas pelo usuário ├── usuarios/              # Diretório de usuários registrados ├── main.py                # Arquivo principal da aplicação ├── main.kv                # Layout Kivy ├── texto.py               # Funções relacionadas à geração e leitura de texto ├── falas.py               # Funções para manipulação de falas ├── buildozer.spec         # Configuração para empacotamento ├── .env                   # Variáveis de ambiente └── README.md              # Documentação do projeto

## 🚀 Como executar o projeto

### Pré-requisitos
- **Python 3.8+**
- Pip atualizado
- Instalar dependências:

```bash
pip install -r requirements.txt

Executando

python main.py

Para Android (via Buildozer)

buildozer android debug
