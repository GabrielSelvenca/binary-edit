import os
import re
import time
import random

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

            print(f"[✓] Alterado: {numero_antigo.decode()} → {novo_numero}")
            return True
        else:
            print("[!] Nenhum número válido encontrado.")
            return False

    except Exception as e:
        return False

caminho = os.path.join(os.path.dirname(__file__), "proinfo.bin")

print("Iniciando loop infinito de edição...")
tempo_inicio_erro = None

while True:
    if os.path.exists(caminho):
        sucesso = editar_arquivo(caminho)
        if sucesso:
            tempo_inicio_erro = None
        else:
            if tempo_inicio_erro is None:
                tempo_inicio_erro = time.time()
            else:
                duracao_erro = time.time() - tempo_inicio_erro
                if duracao_erro >= 60:
                    print("⚠️  WARN: Mais de 1 minuto com erro ao editar o arquivo.")
    else:
        print(f"[!] Arquivo não encontrado: {caminho}")
        time.sleep(1)