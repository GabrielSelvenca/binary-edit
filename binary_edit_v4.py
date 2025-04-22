import os
import re
import time
import secrets
import random
import sys

def gerar_codigo_distinto(anterior, usados, tentativas=100):
    caracteres = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    anterior = anterior.upper()
    for _ in range(tentativas):
        novo = list(anterior)
        indices = random.sample(range(9), secrets.choice([4, 5]))
        for i in indices:
            novo[i] = secrets.choice(caracteres)
        novo_codigo = ''.join(novo)

        if novo_codigo != anterior and novo_codigo not in usados:
            diferenca = sum(1 for a, b in zip(anterior, novo_codigo) if a != b)
            if diferenca >= 4:
                return novo_codigo
    return None

def editar_arquivo(caminho, usados_codigos):
    try:
        with open(caminho, 'rb') as arquivo:
            conteudo = arquivo.read()
            
        inicio = conteudo[:9]

        padrao = re.search(rb'[A-Za-z0-9]{9}', inicio)
        if padrao:
            numero_antigo_bytes = padrao.group()
            numero_antigo = numero_antigo_bytes.decode()
            novo_codigo = gerar_codigo_distinto(numero_antigo, usados_codigos)

            if not novo_codigo:
                return False
            
            conteudo = novo_codigo.encode() + conteudo[9:]
            
            with open(caminho, 'wb') as arquivo:
                arquivo.write(conteudo)

            usados_codigos.add(novo_codigo)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def mostrar_titulo():
    titulo = (
        "╔══════════════════════════════════════╗\n"
        "║      BINARY EDIT - V4 • LOOPING      ║\n"
        "╚══════════════════════════════════════╝\n\n\n"
    )
    sys.stdout.write(titulo + "\n")
    sys.stdout.flush()

def mostrar_status(mensagem):
    largura_terminal = os.get_terminal_size().columns
    sys.stdout.write(' ' * largura_terminal + '\r')
    sys.stdout.write(mensagem + '\r')
    sys.stdout.flush()

caminho = os.path.join(os.path.dirname(__file__), "proinfo.bin")

mostrar_titulo()

tempo_inicio_erro = None
falhas_consecutivas = 0
alteracoes = 0
codigos_usados = set()

while True:
    if os.path.exists(caminho):
        sucesso = editar_arquivo(caminho, codigos_usados)
        if sucesso:
            alteracoes += 1
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
        status = f"[🔴] Arquivo não encontrado: {caminho} | Falha fatal"
        falhas_consecutivas += 1
        time.sleep(1)

    mostrar_status(status)
    time.sleep(15)