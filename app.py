from flask import Flask, render_template, request, redirect, url_for, session, flash
import firebase_admin
from firebase_admin import credentials, storage, firestore
import datetime
from collections import defaultdict
from functools import wraps

app = Flask(__name__)

# --- CONFIGURAÇÃO DE SEGURANÇA ---
app.secret_key = 'uma_chave_secreta_muito_dificil' # Necessário para o login funcionar

# 🔴 DEFINA SEU LOGIN AQUI:
USUARIO_ADM = "santos1513.lopes@gmail.com"
SENHA_ADM = "191414"

# --- CONFIGURAÇÃO FIREBASE ---
nome_do_bucket = 'meustreaming-94cda.firebasestorage.app'
caminho_chave = 'firebase_key.json'

if not firebase_admin._apps:
    cred = credentials.Certificate(caminho_chave)
    firebase_admin.initialize_app(cred, {
        'storageBucket': nome_do_bucket
    })

bucket = storage.bucket()
db = firestore.client()

# --- BLOQUEADOR (Protege as páginas) ---
def login_obrigatorio(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_logado' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROTA DE LOGIN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        if email == USUARIO_ADM and senha == SENHA_ADM:
            session['usuario_logado'] = True
            return redirect(url_for('index'))
        else:
            flash('Login ou senha incorretos!')
            
    return render_template('login.html')

# --- ROTA DE SAIR ---
@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('login'))

# --- ROTAS DO SITE (Agora Protegidas) ---
@app.route('/')
@login_obrigatorio
def index():
    docs = db.collection('musicas').stream()
    playlists_agrupadas = defaultdict(list)
    nomes_playlists = set()

    for doc in docs:
        dados = doc.to_dict()
        nome_arquivo = dados['nome']
        doc_id = doc.id 
        playlist_nome = dados.get('playlist', 'Geral').upper()
        
        nomes_playlists.add(playlist_nome)
        
        blob = bucket.blob(nome_arquivo)
        url_assinada = blob.generate_signed_url(expiration=datetime.timedelta(hours=1))
        
        musica_obj = {
            'id': doc_id,
            'nome': nome_arquivo,
            'playlist': playlist_nome,
            'url': url_assinada
        }
        playlists_agrupadas[playlist_nome].append(musica_obj)

    return render_template('index.html', 
                         playlists=dict(playlists_agrupadas),
                         lista_opcoes=sorted(list(nomes_playlists)))

@app.route('/upload', methods=['GET', 'POST'])
@login_obrigatorio
def upload():
    if request.method == 'POST':
        arquivo = request.files['arquivo']
        playlist = request.form.get('playlist') or 'GERAL'
        playlist = playlist.upper()
        
        if arquivo:
            blob = bucket.blob(arquivo.filename)
            blob.upload_from_file(arquivo)
            
            db.collection('musicas').document(arquivo.filename).set({
                'nome': arquivo.filename,
                'tipo': 'mp3',
                'playlist': playlist,
                'adicionado_em': firestore.SERVER_TIMESTAMP
            })
            return redirect(url_for('index'))

    # Pega nomes para sugestão
    docs = db.collection('musicas').stream()
    nomes = set()
    for doc in docs:
        dados = doc.to_dict()
        nomes.add(dados.get('playlist', 'GERAL').upper())
        
    return render_template('upload.html', sugestoes=sorted(list(nomes)))

@app.route('/atualizar', methods=['POST'])
@login_obrigatorio
def atualizar_playlist():
    id_musica = request.form['id_musica']
    nova_playlist = request.form['nova_playlist'].upper()
    doc_ref = db.collection('musicas').document(id_musica)
    doc_ref.update({'playlist': nova_playlist})
    return redirect(url_for('index'))

@app.route('/deletar', methods=['POST'])
@login_obrigatorio
def deletar_musica():
    id_musica = request.form['id_musica']
    try:
        bucket.blob(id_musica).delete()
    except:
        pass
    db.collection('musicas').document(id_musica).delete()
    return redirect(url_for('index'))
# --- NOVAS ROTAS DE GERENCIAMENTO DE PLAYLIST ---

@app.route('/renomear_playlist', methods=['POST'])
@login_obrigatorio
def renomear_playlist():
    nome_antigo = request.form['nome_antigo']
    nome_novo = request.form['nome_novo'].upper() # Força maiúsculo para padronizar
    
    # 1. Busca todas as músicas daquela playlist
    docs = db.collection('musicas').where('playlist', '==', nome_antigo).stream()
    
    # 2. Atualiza uma por uma
    for doc in docs:
        doc.reference.update({'playlist': nome_novo})
        
    return redirect(url_for('index'))

@app.route('/deletar_playlist', methods=['POST'])
@login_obrigatorio
def deletar_playlist():
    nome_playlist = request.form['nome_playlist']
    
    # 1. Busca todas as músicas
    docs = db.collection('musicas').where('playlist', '==', nome_playlist).stream()
    
    for doc in docs:
        dados = doc.to_dict()
        nome_arquivo = dados['nome']
        
        # 2. Deleta o arquivo MP3 da Nuvem
        try:
            bucket.blob(nome_arquivo).delete()
        except:
            print(f"Erro ao deletar arquivo {nome_arquivo} do Storage")
            
        # 3. Deleta o registro do Banco de Dados
        doc.reference.delete()
        
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)