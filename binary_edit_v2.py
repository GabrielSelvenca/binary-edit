import os
import re
import time
import random
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

ARQUIVO = "proinfo.bin"

def editar_arquivo(caminho):
    if not os.path.exists(caminho):
        print(f"[!] Arquivo '{caminho}' não encontrado.")
        return

    print(f"\n[+] Editando: {caminho}")
    with open(caminho, 'rb') as f:
        conteudo = f.read()

    padrao = re.search(rb'\b\w{9}\b', conteudo)
    if padrao:
        numero_antigo = padrao.group()
        print("Número antigo:", numero_antigo.decode().upper())

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

        print("Novo número:", novo_numero)
        conteudo = conteudo.replace(numero_antigo, novo_numero.encode())

        with open(caminho, 'wb') as f:
            f.write(conteudo)
        print("[✓] Número substituído com sucesso!")

class MonitorArquivo(FileSystemEventHandler):
    def __init__(self, arquivo):
        self.arquivo = os.path.abspath(arquivo)
        self.hash_anterior = None
        self.mod_time = None

    def on_modified(self, event):
        if os.path.abspath(event.src_path) == self.arquivo:
            print("\n[*] Detecção de modificação!")
            editar_arquivo(self.arquivo)

    def on_created(self, event):
        if os.path.abspath(event.src_path) == self.arquivo:
            print("\n[*] Arquivo criado ou restaurado!")
            editar_arquivo(self.arquivo)

    def on_moved(self, event):
        if os.path.abspath(event.dest_path) == self.arquivo:
            print("\n[*] Arquivo movido de volta!")
            editar_arquivo(self.arquivo)

    def on_deleted(self, event):
        if os.path.abspath(event.src_path) == self.arquivo:
            print("\n[!] Arquivo deletado!")

if __name__ == "__main__":
    caminho_completo = os.path.abspath(ARQUIVO)
    pasta = os.path.dirname(caminho_completo)

    if os.path.exists(caminho_completo):
        editar_arquivo(caminho_completo)

    print("\n[*] Monitorando alterações no arquivo...")

    evento = MonitorArquivo(caminho_completo)
    observador = Observer()
    observador.schedule(evento, pasta, recursive=False)
    observador.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observador.stop()

    observador.join()