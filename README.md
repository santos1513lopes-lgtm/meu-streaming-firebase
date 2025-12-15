# 🎵 Streaming Pessoal - Firebase & Flask

Este é um projeto de **Streaming de Áudio Profissional** desenvolvido com Python (Flask) e Firebase. O sistema permite ouvir músicas, organizar playlists, pesquisar em tempo real e fazer upload de novos arquivos MP3 diretamente pelo navegador, sem necessidade de tocar no código.

## 🚀 Funcionalidades

* **Player de Áudio HTML5:** Interface moderna e responsiva (estilo Spotify).
* **Gestão de Playlists:** Músicas agrupadas automaticamente (ex: "GERAL", "FORRÓ", "ROCK").
* **Mover Músicas:** Possibilidade de trocar a playlist de uma música com um clique.
* **Upload Web:** Página dedicada para enviar arquivos MP3 diretamente para a nuvem.
* **Autoplay Inteligente:** Toca a próxima música da lista automaticamente.
* **Pesquisa em Tempo Real:** Filtre músicas instantaneamente usando a lupa.
* **Modo Escuro:** Interface "Dark Mode" com ícones SVG verdes.

---

## 📂 Estrutura do Projeto

Abaixo, a organização dos arquivos principais:

```text
MEU-STREAMING/
│
├── app.py                # O Cérebro. Controla o site, banco de dados e rotas.
├── requirements.txt      # Lista de bibliotecas necessárias (Flask, Firebase, Gunicorn).
├── .gitignore            # Arquivo de segurança (impede o envio da chave secreta).
│
└── templates/            # Pasta com as páginas HTML (Front-end)
    ├── index.html        # Página Principal (Player, Listas e Pesquisa).
    └── upload.html       # Página de Envio de Arquivos.

#Parceiro de Programacao
Com certeza, meu parceiro! Essa é uma ideia excelente. 💡

Ter um README.md bem escrito é essencial. Ele serve como o "Manual de Instruções" do seu projeto. Se daqui a 6 meses você (ou outra pessoa) precisar mexer no código, vai saber exatamente como tudo funciona.

Preparei um arquivo completo, profissional e formatado com Markdown. Ele explica a estrutura, como instalar, como funciona o Upload e os cuidados de segurança.

Como criar o arquivo:
No VS Code, crie um novo arquivo chamado README.md (tem que ser maiúsculo).

Copie o código abaixo e cole dentro dele.

Salve, faça o commit e envie para o GitHub!

Conteúdo do README.md (Copie e Cole)
Markdown
# 🎵 Streaming Pessoal - Firebase & Flask

Este é um projeto de **Streaming de Áudio Profissional** desenvolvido com Python (Flask) e Firebase. O sistema permite ouvir músicas, organizar playlists, pesquisar em tempo real e fazer upload de novos arquivos MP3 diretamente pelo navegador, sem necessidade de tocar no código.

## 🚀 Funcionalidades

* **Player de Áudio HTML5:** Interface moderna e responsiva (estilo Spotify).
* **Gestão de Playlists:** Músicas agrupadas automaticamente (ex: "GERAL", "FORRÓ", "ROCK").
* **Mover Músicas:** Possibilidade de trocar a playlist de uma música com um clique.
* **Upload Web:** Página dedicada para enviar arquivos MP3 diretamente para a nuvem.
* **Autoplay Inteligente:** Toca a próxima música da lista automaticamente.
* **Pesquisa em Tempo Real:** Filtre músicas instantaneamente usando a lupa.
* **Modo Escuro:** Interface "Dark Mode" com ícones SVG verdes.

---

## 📂 Estrutura do Projeto

Abaixo, a organização dos arquivos principais:

```text
MEU-STREAMING/
│
├── app.py                # O Cérebro. Controla o site, banco de dados e rotas.
├── requirements.txt      # Lista de bibliotecas necessárias (Flask, Firebase, Gunicorn).
├── .gitignore            # Arquivo de segurança (impede o envio da chave secreta).
│
└── templates/            # Pasta com as páginas HTML (Front-end)
    ├── index.html        # Página Principal (Player, Listas e Pesquisa).
    └── upload.html       # Página de Envio de Arquivos.
🛠️ Tecnologias Utilizadas
Backend: Python 3 + Flask.

Banco de Dados: Google Firestore (NoSQL).

Armazenamento: Google Firebase Storage (para os arquivos .mp3).

Frontend: HTML5, CSS3, JavaScript puro.

Deploy: Render (Hospedagem em nuvem).

##🔒 Configuração de Segurança (Importante)
Este projeto utiliza uma chave privada do Firebase (firebase_key.json) para acessar o banco de dados.

⚠️ ATENÇÃO: O arquivo firebase_key.json NUNCA deve ser enviado para o GitHub ou compartilhado publicamente.

Certifique-se de que o arquivo .gitignore contenha a linha:

Plaintext

firebase_key.json
Como configurar no Render (Produção):
Ao hospedar o site, adicione o conteúdo do seu JSON como um "Secret File":

Filename: firebase_key.json

Content: Cole o conteúdo inteiro da sua chave privada.

▶️ Como Rodar Localmente (No seu PC)
Clone o repositório:

Bash

git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
cd SEU-REPOSITORIO
Instale as dependências:

Bash

pip install -r requirements.txt
Adicione a Chave: Coloque o seu arquivo firebase_key.json na raiz da pasta do projeto.

Execute o servidor:

Bash

python app.py
O site estará disponível em: http://127.0.0.1:5000

📝 Histórico de Atualizações
v1.0: Listagem simples de músicas do Storage.

v2.0: Integração com Banco de Dados (Firestore) e nomes corrigidos.

v3.0: Criação de Playlists dinâmicas e botão "Mover".

v4.0: Adição de Lupa de Pesquisa e Autoplay sequencial.

v5.0: Página de Upload Web com sugestão de playlists (Sistema Autônomo).##
