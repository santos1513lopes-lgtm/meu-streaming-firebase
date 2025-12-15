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

@app.route('/')
def index():
    docs = db.collection('musicas').stream()
    playlists_agrupadas = defaultdict(list)
    
    for doc in docs:
        dados = doc.to_dict()
        nome_arquivo = dados['nome']
        doc_id = doc.id 
        playlist_nome = dados.get('playlist', 'Geral').upper()
        
        blob = bucket.blob(nome_arquivo)
        url_assinada = blob.generate_signed_url(expiration=datetime.timedelta(hours=1))
        
        musica_obj = {
            'id': doc_id,
            'nome': nome_arquivo,
            'playlist': playlist_nome,
            'url': url_assinada
        }
        playlists_agrupadas[playlist_nome].append(musica_obj)

    return render_template('index.html', playlists=dict(playlists_agrupadas))

# --- ROTA DE UPLOAD (A MÁGICA ACONTECE AQUI) ---
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # 1. Recebe o arquivo e o nome da playlist do formulário
        arquivo = request.files['arquivo']
        playlist = request.form['playlist']
        
        if arquivo:
            # 2. Envia o arquivo MP3 para o Storage (Nuvem)
            blob = bucket.blob(arquivo.filename)
            blob.upload_from_file(arquivo)
            
            # 3. Salva os dados no Banco de Dados
            db.collection('musicas').document(arquivo.filename).set({
                'nome': arquivo.filename,
                'tipo': 'mp3',
                'playlist': playlist,
                'adicionado_em': firestore.SERVER_TIMESTAMP
            })
            
            # 4. Volta para a página inicial
            return redirect(url_for('index'))

    # Se for GET, só mostra a página de upload
    return render_template('upload.html')

@app.route('/atualizar', methods=['POST'])
def atualizar_playlist():
    id_musica = request.form['id_musica']
    nova_playlist = request.form['nova_playlist']
    doc_ref = db.collection('musicas').document(id_musica)
    doc_ref.update({'playlist': nova_playlist})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)