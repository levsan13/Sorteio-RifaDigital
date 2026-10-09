"""Expõe a página do sorteio da rifa na rede local e compartilha os dados carregados nela.

Uso:
    python expor_na_rede.py          # porta 8000
    python expor_na_rede.py 8080     # outra porta

Quando alguém carrega a planilha na página e vai para o sorteio, os nomes e os
pontos ficam na memória deste script. Os outros aparelhos da rede que abrirem a
página recebem esses dados e entram direto no sorteio. Nada é gravado em disco:
ao encerrar o script, os dados somem.

Deixe esta janela aberta enquanto a página estiver em uso. Ctrl+C encerra.
Só usa a biblioteca padrão do Python (3.7 ou mais novo).
"""
import json
import socket
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PAGINA = Path(__file__).resolve().parent / "sorteio-rifa-ibvb.html"
PORTA_PADRAO = 8000
QTD_MIN, QTD_MAX = 2, 10000    # os mesmos limites de quantidade de pontos da página
TAMANHO_MAX = 2 * 1024 * 1024  # maior corpo aceito ao receber os dados

# Dados carregados na página. Ficam só na memória deste processo.
_trava = threading.Lock()
_dados = None                   # {"arquivo": str, "total": int, "linhas": [{"nome": str, "numeros": [int]}]}
_dono = None                    # endereço do aparelho que carregou os dados
_locais = {"127.0.0.1", "::1"}  # endereços deste computador, que sempre pode trocar os dados


def validar(corpo):
    """Devolve os dados limpos, ou None se o corpo não tiver o formato esperado."""
    if not isinstance(corpo, dict):
        return None
    arquivo, total, linhas = corpo.get("arquivo"), corpo.get("total"), corpo.get("linhas")
    if not isinstance(arquivo, str) or type(total) is not int or not isinstance(linhas, list):
        return None
    if not QTD_MIN <= total <= QTD_MAX or not 0 < len(linhas) <= QTD_MAX:
        return None
    limpas = []
    for linha in linhas:
        if not isinstance(linha, dict):
            return None
        nome, numeros = linha.get("nome"), linha.get("numeros")
        if not isinstance(nome, str) or not isinstance(numeros, list) or not numeros:
            return None
        if any(type(n) is not int or not 0 <= n < total for n in numeros):
            return None
        limpas.append({"nome": nome[:200], "numeros": numeros})
    return {"arquivo": arquivo[:200], "total": total, "linhas": limpas}


class Pagina(BaseHTTPRequestHandler):
    """Entrega a página do sorteio e os dados carregados nela; nenhum arquivo da pasta fica acessível."""

    def do_GET(self):
        caminho = self._caminho()
        if caminho in ("/", "/" + PAGINA.name):
            self._pagina(com_corpo=True)
        elif caminho == "/dados":
            with _trava:
                resposta = {"dados": _dados, "podeTrocar": self._pode_trocar()}
            self._json(200, resposta)
        else:
            self.send_error(404, "Nada aqui")

    def do_HEAD(self):
        if self._caminho() in ("/", "/" + PAGINA.name):
            self._pagina(com_corpo=False)
        else:
            self.send_error(404, "Nada aqui")

    def do_PUT(self):
        global _dados, _dono
        if self._caminho() != "/dados":
            self.send_error(404, "Nada aqui")
            return
        # Exigir JSON impede que outro site, aberto no navegador de alguém da rede, troque os dados por formulário.
        if self.headers.get_content_type() != "application/json":
            self.send_error(415, "Envie JSON")
            return
        try:
            tamanho = int(self.headers.get("Content-Length", ""))
        except ValueError:
            tamanho = 0
        if not 0 < tamanho <= TAMANHO_MAX:
            self.send_error(413 if tamanho > TAMANHO_MAX else 411, "Tamanho invalido")
            return
        try:
            novos = validar(json.loads(self.rfile.read(tamanho).decode("utf-8")))
        except (ValueError, RecursionError):
            novos = None
        if novos is None:
            self.send_error(400, "Dados fora do formato")
            return
        with _trava:
            aceito = self._pode_trocar()
            if aceito:
                _dados, _dono = novos, self.client_address[0]
            resposta = {"dados": _dados, "podeTrocar": aceito}
        # 409: outro aparelho já carregou os dados desta rede, e valem os dele.
        self._json(200 if aceito else 409, resposta)

    def _caminho(self):
        return self.path.split("?", 1)[0].split("#", 1)[0]

    def _pode_trocar(self):
        """Carrega quem chegar primeiro; depois, só esse aparelho ou este computador trocam os dados."""
        aparelho = self.client_address[0]
        return _dados is None or aparelho == _dono or aparelho in _locais

    def _pagina(self, com_corpo):
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

    def _json(self, codigo, objeto):
        conteudo = json.dumps(objeto, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(conteudo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
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
    if ip:
        _locais.add(ip)
    print("Sorteio da rifa no ar.")
    print(f"  Neste computador:        http://localhost:{porta}")
    if ip:
        print(f"  Outros aparelhos na rede: http://{ip}:{porta}")
    else:
        print("  Não encontrei um endereço de rede. Confira se o computador está no Wi-Fi ou no cabo.")
    print("Os dados carregados na página ficam na memória deste script e somem ao encerrar.")
    print("Ctrl+C encerra.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrado.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
