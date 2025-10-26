from cryptography.fernet import Fernet
import os

def carregar_chave():
    """Carrega a chave de descriptografia salva anteriormente"""
    return open("chave.key", "rb").read()

def descriptografar_arquivo(arquivo, chave):
    """Descriptografa um único arquivo"""
    f = Fernet(chave)
    with open(arquivo, "rb") as file:
        dados_encriptados = file.read()
    
    try:
        dados_originais = f.decrypt(dados_encriptados)
        with open(arquivo, "wb") as file:
            file.write(dados_originais)
        print(f" Arquivo descriptografado: {arquivo}")
    except Exception as e:
        print(f" Erro ao descriptografar {arquivo}: {e}")

def encontrar_arquivos(diretorio):
    """Encontra todos os arquivos no diretório"""
    lista = []
    for raiz, _, arquivos in os.walk(diretorio):
        for nome in arquivos:
            caminho = os.path.join(raiz, nome)
            if caminho != "decryptor.py" and not nome.endswith(".key"):
                lista.append(caminho)
    return lista

def main():
    """Função principal de descriptografia"""
    print(" Iniciando descriptografia de arquivos...")
    
    # Verifica se a chave existe
    if not os.path.exists("chave.key"):
        print(" ERRO: Arquivo chave.key não encontrado!")
        print("Sem a chave, não é possível recuperar os arquivos.")
        return
    
    # Carrega a chave
    chave = carregar_chave()
    print(" Chave carregada com sucesso!")
    
    # Encontra e descriptografa os arquivos
    arquivos = encontrar_arquivos("test_files")
    print(f" {len(arquivos)} arquivo(s) encontrado(s)")
    
    for arquivo in arquivos:
        descriptografar_arquivo(arquivo, chave)
    
    # Remove a mensagem de resgate
    if os.path.exists("LEIA ISSO.txt"):
        os.remove("LEIA ISSO.txt")
        print(" Mensagem de resgate removida")
    
    print("\n Descriptografia concluída! Arquivos restaurados.")

if __name__ == "__main__":
    main()
