# Sorteio da Rifa IBVB Santa Cecília

Página de sorteio da Grande Rifa Online em prol da festa do Dia das Crianças da IBVB Santa Cecília. Ela usa os pontos vendidos no relatório da [rifa.digital](https://rifa.digital), sorteia um deles ao acaso e revela o número e o nome de quem comprou, com fogos e confete.

A rifa tem 200 pontos, numerados de 0 a 199.

## Arquivos

| Arquivo | O que é |
|---|---|
| `sorteio-rifa-ibvb.html` | A aplicação inteira em um único arquivo: página, estilo, código, imagens e os dados da rifa. |
| `expor_na_rede.py` | Servidor opcional para abrir a página em outros aparelhos da mesma rede. |

## Como usar

1. Abra `sorteio-rifa-ibvb.html` em um navegador atualizado (Chrome, Edge, Firefox ou Safari). Não é preciso instalar nada.
2. Clique em **SORTEAR**. Depois da contagem, a tela mostra o ponto sorteado e o nome de quem comprou.
3. Para continuar, clique em **Sortear o próximo** ou feche a revelação e sorteie de novo.

Os botões no canto superior direito ligam e desligam o som, colocam a página em tela cheia e levam à lista de participantes.

Sem internet a página funciona do mesmo jeito. Só as fontes mudam, porque vêm do Google Fonts.

## Regras do sorteio

- **Quem concorre:** só os pontos vendidos. Cada ponto tem a mesma chance, então quem comprou mais pontos tem mais chances.
- **Ponto sorteado sai da disputa.** Ele aparece riscado no quadro e não volta a concorrer. Quem tem outros pontos continua concorrendo com eles.
- **Recomeçar:** devolve todos os pontos à disputa e apaga o registro dos sorteios. Pede um segundo clique para confirmar.
- **Todos os 200:** opção que inclui os pontos sem dono. Se sair um deles, a tela avisa, não solta fogos, e o ponto também sai da disputa.
- **Aleatoriedade:** o ponto é escolhido por `crypto.getRandomValues` no instante do clique, descartando a sobra da divisão para não favorecer nenhum ponto. A contagem na tela só revela o resultado.
- **Registro:** os sorteios ficam gravados no `localStorage` do navegador. Recarregar a página não perde o resultado, mas sorteios de teste também contam. Clique em **Recomeçar** antes do sorteio oficial.

## Atualizar os dados da rifa

Os dados embutidos vêm do relatório com contribuições até 06/10/2026 às 17:19: 19 contribuições e 54 pontos vendidos.

Há dois jeitos de atualizar:

- **Na página:** no fim dela, clique em **Carregar planilha atualizada** e escolha o `.xlsx` exportado pela rifa.digital. A leitura acontece no navegador e usa só as colunas `Nome` e `Cotas`. A planilha carregada vale apenas para aquele navegador; **Voltar à planilha original** desfaz.
- **No código:** edite a lista `ORIGINAL`, no `<script>` do fim do HTML. Assim a mudança vale para todo mundo que abrir o arquivo.

Ao ler uma planilha, números fora de 0 a 199 são ignorados. Se um ponto aparecer em mais de uma linha, vale a primeira.

## Abrir em outros aparelhos da rede

Requer Python 3.7 ou mais novo. Dentro da pasta do projeto:

```bash
python expor_na_rede.py
```

O script mostra o endereço para este computador e o endereço para os outros aparelhos da mesma rede. Para usar outra porta no lugar da 8000:

```bash
python expor_na_rede.py 8080
```

Deixe a janela aberta enquanto a página estiver em uso. `Ctrl+C` encerra.

- **Cada aparelho faz o próprio sorteio.** Os resultados e o registro não são compartilhados entre aparelhos. O sorteio oficial é o da tela de quem apresenta.
- O script entrega só a página do sorteio. Nenhum outro arquivo da pasta fica acessível.
- No Windows, o firewall pode perguntar se permite o Python na rede. Sem permitir em redes privadas, os outros aparelhos não conseguem abrir a página.

## Dados e privacidade

- O HTML traz embutidos os nomes de quem contribuiu e os pontos de cada pessoa. Telefones e e-mails do relatório não entram. **Em um repositório público, esses nomes ficam públicos.**
- A planilha carregada pela página e o registro dos sorteios ficam só no `localStorage` do navegador. Nada é enviado para fora.
- Quem estiver na mesma rede, com o servidor ligado, consegue ver os nomes dos participantes.

## Adaptar para outra rifa

Tudo fica no `<script>` do fim de `sorteio-rifa-ibvb.html`:

| Constante | O que define |
|---|---|
| `TOTAL` | Quantidade de pontos da rifa. |
| `PREMIO` | Texto do prêmio na tela de revelação. |
| `CHAVE` | Nome usado no `localStorage`. Troque para não misturar o registro de rifas diferentes. |
| `ORIGINAL` | Nome do relatório, data da última contribuição e a lista de nomes com seus pontos. |
| `IMAGENS` | Arte do título, foto do prêmio e logo da igreja, recortadas do cartaz da campanha e embutidas em base64. |

O nome da igreja, o texto do prêmio na tela principal, o rótulo "Todos os 200" e a frase do rodapé estão no HTML.
