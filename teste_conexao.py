import firebase_admin
from firebase_admin import credentials, storage

# --- CONFIGURAÇÃO ---
# Nome do seu bucket (já configurado)
nome_do_bucket = 'meustreaming-94cda.firebasestorage.app'

# Caminho para a sua chave
caminho_chave = 'firebase_key.json'

try:
    # --- CONEXÃO ---
    # Verifica se já existe uma conexão para não dar erro ao rodar duas vezes
    if not firebase_admin._apps:
        cred = credentials.Certificate(caminho_chave)
        firebase_admin.initialize_app(cred, {
            'storageBucket': nome_do_bucket
        })

    # --- TESTE ---
    # Acessa o bucket e lista os arquivos
    bucket = storage.bucket()
    blobs = list(bucket.list_blobs())

    print("\n" + "="*50)
    print("SUCESSO! CONEXÃO REALIZADA COM O FIREBASE.")
    print(f"Bucket: {nome_do_bucket}")
    print("="*50)
    
    if len(blobs) == 0:
        print(">> O bucket está vazio. Tente subir uma música no site do Firebase.")
    else:
        print(f">> Encontrei {len(blobs)} arquivo(s):")
        for blob in blobs:
            print(f"   - {blob.name}")
            # Gera um link temporário só para testar se conseguimos ler
            link = blob.generate_signed_url(expiration=3600)
            print(f"   - Link de teste: {link}")
    print("="*50 + "\n")

except Exception as e:
    print("\n" + "="*50)
    print("ERRO NA CONEXÃO:")
    print(e)
    print("="*50 + "\n")