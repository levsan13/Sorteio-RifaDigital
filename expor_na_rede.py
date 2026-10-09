"""Expõe a página do sorteio da rifa na rede local.

Uso:
    python expor_na_rede.py          # porta 8000
    python expor_na_rede.py 8080     # outra porta

Deixe esta janela aberta enquanto a página estiver em uso. Ctrl+C encerra.
Só usa a biblioteca padrão do Python (3.7 ou mais novo).
"""
import socket
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PAGINA = Path(__file__).resolve().parent / "sorteio-rifa-ibvb.html"
PORTA_PADRAO = 8000


class Pagina(BaseHTTPRequestHandler):
    """Entrega só a página do sorteio; nenhum outro arquivo da pasta fica acessível."""

    def do_GET(self):
        self._responder(com_corpo=True)

    def do_HEAD(self):
        self._responder(com_corpo=False)

    def _responder(self, com_corpo):
        caminho = self.path.split("?", 1)[0].split("#", 1)[0]
        if caminho not in ("/", "/" + PAGINA.name):
            self.send_error(404, "Nada aqui")
            return
        try:
            conteudo = PAGINA.read_bytes()
        except OSError:
            self.send_error(500, "Pagina do sorteio nao encontrada")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(conteudo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if com_corpo:
            self.wfile.write(conteudo)


def ip_na_rede():
    """Endereço deste computador na rede local, ou None se ele não estiver em rede."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Não envia nada: só faz o sistema dizer por qual interface sairia.
            s.connect(("10.255.255.255", 1))
            ip = s.getsockname()[0]
    except OSError:
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except OSError:
            return None
    return None if ip.startswith("127.") else ip


def main():
    try:
        porta = int(sys.argv[1]) if len(sys.argv) > 1 else PORTA_PADRAO
    except ValueError:
        sys.exit(f"Porta inválida: {sys.argv[1]}. Uso: python {Path(__file__).name} [porta]")
    if not PAGINA.is_file():
        sys.exit(f"Não encontrei {PAGINA.name} na mesma pasta deste script.")
    try:
        servidor = ThreadingHTTPServer(("0.0.0.0", porta), Pagina)
    except OSError as erro:
        sys.exit(f"Não consegui usar a porta {porta} ({erro}). Tente outra: python {Path(__file__).name} 8080")

    ip = ip_na_rede()
    print("Sorteio da rifa no ar.")
    print(f"  Neste computador:        http://localhost:{porta}")
    if ip:
        print(f"  Outros aparelhos na rede: http://{ip}:{porta}")
    else:
        print("  Não encontrei um endereço de rede. Confira se o computador está no Wi-Fi ou no cabo.")
    print("Ctrl+C encerra.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrado.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
