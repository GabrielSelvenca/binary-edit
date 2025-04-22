import os
import re
import time
import secrets
import sys

def gerar_codigo_distinto(anterior, usados, tentativas=100):
    caracteres = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    anterior = anterior.upper()
    for _ in range(tentativas):
        novo = list(anterior)
        indices = secrets.sample(range(9), secrets.choice([4, 5]))
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

        padrao = re.search(rb'\b\w{9}\b', conteudo)
        print("Padrão encontrado:", padrao.group() if padrao else "Nenhum")
        if padrao:
            numero_antigo = padrao.group().decode().upper()
            novo_codigo = gerar_codigo_distinto(numero_antigo, usados_codigos)

            if not novo_codigo:
                return False

            conteudo = conteudo.replace(numero_antigo.encode(), novo_codigo.encode())

            with open(caminho, 'wb') as arquivo:
                arquivo.write(conteudo)

            usados_codigos.add(novo_codigo)
            return True
        else:
            return False
    except:
        return False

def mostrar_titulo():
    titulo = (
        "╔══════════════════════════════════════╗\n"
        "║   BINARY EDIT - V4 • MONITORAMENTO   ║\n"
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
codigos_usados = set()

while True:
    alteracoes += 1
    if os.path.exists(caminho):
        sucesso = editar_arquivo(caminho, codigos_usados)
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
    time.sleep(10)