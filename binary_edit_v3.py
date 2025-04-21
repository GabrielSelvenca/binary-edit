import os
import re
import time
import random
import sys

def editar_arquivo(caminho):
    try:
        with open(caminho, 'rb') as arquivo:
            conteudo = arquivo.read()

        padrao = re.search(rb'\b\w{9}\b', conteudo)
        if padrao:
            numero_antigo = padrao.group()
            num_chars_to_change = random.choice([4, 5])
            indices = random.sample(range(9), num_chars_to_change)
            novo_numero = list(numero_antigo.decode().upper())

            for i in indices:
                novo_numero[i] = random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            novo_numero = ''.join(novo_numero)

            while novo_numero == numero_antigo.decode().upper():
                for i in indices:
                    novo_numero[i] = random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                novo_numero = ''.join(novo_numero)

            conteudo = conteudo.replace(numero_antigo, novo_numero.encode())

            with open(caminho, 'wb') as arquivo:
                arquivo.write(conteudo)

            return True
        else:
            return False
    except:
        return False

def mostrar_titulo():
    titulo = (
        "╔══════════════════════════════════════╗\n"
        "║   BINARY EDIT - V3 • MONITORAMENTO   ║\n"
        "╚══════════════════════════════════════╝\n\n\n"
    )
    sys.stdout.write(titulo + "\n")
    sys.stdout.flush()

def mostrar_status(mensagem):
    sys.stdout.write(mensagem + '\r')
    sys.stdout.flush()

caminho = os.path.join(os.path.dirname(__file__), "proinfo.bin")

mostrar_titulo()

tempo_inicio_erro = None
falhas_consecutivas = 0
alteracoes = 0

while True:
    alteracoes += 1
    if os.path.exists(caminho):
        sucesso = editar_arquivo(caminho)
        if sucesso:
            falhas_consecutivas = 0
            tempo_inicio_erro = None
            status = f"[🟢] Status: OK | Alterações: {alteracoes} | Falhas consecutivas: {falhas_consecutivas}"
        else:
            falhas_consecutivas += 1
            if tempo_inicio_erro is None:
                tempo_inicio_erro = time.time()
            duracao = int(time.time() - tempo_inicio_erro)
            status = f"[🟡] Status: Falhando há {duracao}s | Alterações: {alteracoes} | Falhas consecutivas: {falhas_consecutivas}"
    else:
        status = f"[🔴] Arquivo não encontrado: {caminho}"
        falhas_consecutivas += 1
        time.sleep(1)

    mostrar_status(status)
    time.sleep(0.5)