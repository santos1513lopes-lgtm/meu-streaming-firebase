import firebase_admin
from firebase_admin import credentials, storage, firestore

# --- CONFIGURAÇÃO ---
nome_do_bucket = 'meustreaming-94cda.firebasestorage.app' # Seu bucket
caminho_chave = 'firebase_key.json'

# Inicializa (se já não estiver inicializado)
if not firebase_admin._apps:
    cred = credentials.Certificate(caminho_chave)
    firebase_admin.initialize_app(cred, {
        'storageBucket': nome_do_bucket
    })

# Conecta aos dois sistemas
bucket = storage.bucket()
db = firestore.client()

print("--- INICIANDO CATALOGAÇÃO ---")

# 1. Busca todas as músicas no Storage
blobs = list(bucket.list_blobs())
print(f"Encontrei {len(blobs)} arquivos no Storage.")

# 2. Salva cada uma no Banco de Dados
for blob in blobs:
    # Vamos usar o nome do arquivo como ID para facilitar
    nome_arquivo = blob.name
    
    # Cria uma referência no banco de dados na coleção "musicas"
    # Se a música já existir, ele atualiza. Se não, ele cria.
    doc_ref = db.collection('musicas').document(nome_arquivo)
    
    doc_ref.set({
        'nome': nome_arquivo,
        'tipo': 'mp3',
        'adicionado_em': firestore.SERVER_TIMESTAMP, # Data de hoje
        'playlist': 'Geral' # Por enquanto, todas vão para "Geral"
    })
    
    print(f"✔ Catalogado: {nome_arquivo}")

print("--- SUCESSO! SEU BANCO DE DADOS ESTÁ ATUALIZADO ---")