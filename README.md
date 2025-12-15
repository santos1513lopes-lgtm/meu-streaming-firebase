# 🎵 Meu Streaming Premium - Firebase & Flask

Aplicação web profissional de streaming de áudio pessoal. Sistema completo com player avançado, gestão administrativa de playlists e proteção por login.

---

## 🚀 Funcionalidades

### 🔐 Administração & Segurança
* **Login Seguro:** Acesso protegido por e-mail e senha.
* **Gestão de Playlists:** * **Renomear:** Corrija nomes de playlists inteiras com um clique.
    * **Excluir:** Remova playlists e todas as suas músicas do banco de dados e nuvem.
* **Upload:** Envio de arquivos MP3 com barra de progresso em tempo real.

### 🎧 Player & Reprodução
* **Loop Mode:** Opção de repetir a playlist infinitamente.
* **Background Play:** Funciona com a tela do celular bloqueada.
* **Controles na Tela de Bloqueio:** Pause/Pule músicas sem desbloquear o celular.
* **Autoplay:** Toca a próxima faixa automaticamente.

### 📂 Organização & Interface
* **Menu Sanfona (Acordeão):** Playlists abrem e fecham para limpar o visual.
* **Header Fixo:** Barra de pesquisa e controles sempre visíveis no topo.
* **Mobile First:** Design perfeitamente adaptado para celulares.
* **Pesquisa Global:** Filtre por nome da música ou da playlist.

---

## 🛠️ Instalação e Configuração

1.  **Dependências:** `pip install -r requirements.txt`
2.  **Chave Firebase:** Coloque o arquivo `firebase_key.json` na raiz.
3.  **Configurar Login:**
    * Abra o `app.py`.
    * Edite as variáveis `USUARIO_ADM` e `SENHA_ADM`.
4.  **Rodar:** `python app.py`

---

Desenvolvido com Python, Flask e dedicação. 🚀