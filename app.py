from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, storage, firestore
import datetime
from collections import defaultdict

app = Flask(__name__)

# --- CONFIGURAÇÃO ---
nome_do_bucket = 'meustreaming-94cda.firebasestorage.app'
caminho_chave = 'firebase_key.json'

if not firebase_admin._apps:
    cred = credentials.Certificate(caminho_chave)
    firebase_admin.initialize_app(cred, {
        'storageBucket': nome_do_bucket
    })

bucket = storage.bucket()
db = firestore.client()

# --- FUNÇÃO AUXILIAR ---
def get_nomes_playlists():
    docs = db.collection('musicas').stream()
    nomes = set()
    for doc in docs:
        dados = doc.to_dict()
        playlist = dados.get('playlist', 'GERAL').upper()
        nomes.add(playlist)
    return sorted(list(nomes))

@app.route('/')
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

    nomes_existentes = get_nomes_playlists()
    return render_template('upload.html', sugestoes=nomes_existentes)

@app.route('/atualizar', methods=['POST'])
def atualizar_playlist():
    id_musica = request.form['id_musica']
    nova_playlist = request.form['nova_playlist'].upper()
    doc_ref = db.collection('musicas').document(id_musica)
    doc_ref.update({'playlist': nova_playlist})
    return redirect(url_for('index'))

# --- NOVA ROTA DE EXCLUSÃO ---
@app.route('/deletar', methods=['POST'])
def deletar_musica():
    id_musica = request.form['id_musica'] # O ID é o nome do arquivo
    
    # 1. Tenta apagar o arquivo do Storage (Nuvem)
    try:
        bucket.blob(id_musica).delete()
    except:
        print("Arquivo não encontrado no Storage, apagando apenas do banco.")

    # 2. Apaga o registro do Banco de Dados
    db.collection('musicas').document(id_musica).delete()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)