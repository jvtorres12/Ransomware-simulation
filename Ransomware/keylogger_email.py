# demo_email_simulator.py
import smtplib
from email.mime.text import MIMEText
from threading import Timer
from datetime import datetime
import os

# CONFIGURAÇÕES DE E-MAIL (use senha de app)
EMAIL_ORIGEM = "seu_email@gmail.com"
EMAIL_DESTINO = "seu_email@gmail.com"
SENHA_EMAIL = "senha_de_app"  # crie em: Conta Google > Segurança > Senhas de app

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

# “Log” SIMULADO (não lê teclado do sistema)
log_buffer = []

def gerar_log_falso():
    # Simula eventos de aplicação (não captura teclas reais)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_buffer.append(f"[{ts}] Evento de demonstração\n")

def enviar_email():
    global log_buffer
    try:
        if not log_buffer:
            agendar_envio()
            return

        corpo = "".join(log_buffer)
        msg = MIMEText(corpo, "plain", "utf-8")
        msg["Subject"] = "Demo: dados simulados do laboratório"
        msg["From"] = EMAIL_ORIGEM
        msg["To"] = EMAIL_DESTINO

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30)
        server.starttls()
        server.login(EMAIL_ORIGEM, SENHA_EMAIL)
        server.send_message(msg)
        server.quit()

        print(f"[OK] E-mail enviado às {datetime.now().strftime('%H:%M:%S')}")
        log_buffer = []  # limpa após envio
    except Exception as e:
        print("[ERRO] Falha ao enviar:", e)
    finally:
        agendar_envio()

def agendar_envio():
    # agenda novo envio em 60s
    Timer(60, enviar_email).start()

def main():
    print("Simulador iniciado. Envio a cada 60s. Pressione Ctrl+C para sair.")
    agendar_envio()
    # Gera eventos simulados continuamente
    try:
        while True:
            gerar_log_falso()
            # intervalo curto apenas para simulação
            import time; time.sleep(5)
    except KeyboardInterrupt:
        print("\nEncerrado.")

if __name__ == "__main__":
    main()
