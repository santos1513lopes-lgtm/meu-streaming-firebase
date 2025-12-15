from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, storage, firestore
import datetime

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
    # Busca todas as músicas e ordena pela playlist para ficar organizado
    docs = db.collection('musicas').order_by('playlist').stream()
    
    lista_musicas = []
    for doc in docs:
        dados = doc.to_dict()
        nome_arquivo = dados['nome']
        # Pega o ID do documento para podermos editá-lo depois
        doc_id = doc.id 
        playlist_nome = dados.get('playlist', 'Geral')
        
        blob = bucket.blob(nome_arquivo)
        url_assinada = blob.generate_signed_url(expiration=datetime.timedelta(hours=1))
        
        lista_musicas.append({
            'id': doc_id,
            'nome': nome_arquivo,
            'playlist': playlist_nome,
            'url': url_assinada
        })

    return render_template('index.html', musicas=lista_musicas)

# --- NOVA FUNÇÃO: ATUALIZAR PLAYLIST ---
@app.route('/atualizar', methods=['POST'])
def atualizar_playlist():
    # Recebe os dados do formulário do site
    id_musica = request.form['id_musica']
    nova_playlist = request.form['nova_playlist']
    
    # Atualiza no Banco de Dados
    doc_ref = db.collection('musicas').document(id_musica)
    doc_ref.update({
        'playlist': nova_playlist
    })
    
    # Recarrega a página para mostrar a mudança
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)