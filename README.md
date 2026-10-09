# Sorteio da Rifa IBVB Santa Cecília

Página de sorteio da Grande Rifa Online em prol da festa do Dia das Crianças da IBVB Santa Cecília. Você carrega o relatório `.xlsx` da [rifa.digital](https://rifa.digital), informa quantos pontos a rifa tem, e a página sorteia um ponto ao acaso e revela o número e o nome de quem comprou, com fogos e confete.

A página não traz dados de ninguém e não guarda nada. Ela trabalha só com a planilha carregada naquele momento.

## Arquivos

| Arquivo | O que é |
|---|---|
| `sorteio-rifa-ibvb.html` | A aplicação inteira em um único arquivo: página, estilo, código e imagens. |
| `expor_na_rede.py` | Servidor opcional: abre a página em outros aparelhos da mesma rede e compartilha com eles os dados carregados. |
| `.gitignore` | Mantém planilhas `.xlsx` fora do repositório. |

## Como usar

Abra `sorteio-rifa-ibvb.html` em um navegador atualizado (Chrome, Edge, Firefox ou Safari). Não é preciso instalar nada.

### Tela 1: carregar os dados

1. Arraste o relatório `.xlsx` exportado pela rifa.digital para a área indicada, ou clique em **Escolher arquivo**.
2. Informe a **quantidade de pontos da rifa**, de 2 a 10000. Há atalhos para 50, 100, 200, 500 e 1000. Os pontos vão de 0 até a quantidade menos 1: uma rifa de 200 pontos vai de 0 a 199.
3. Clique em **IR PARA O SORTEIO**.

A página confere a planilha antes de liberar o botão:

- Lê só as colunas `Nome` e `Cotas`. Telefone e e-mail não são lidos.
- Se a planilha tiver ponto acima do limite escolhido, o sorteio fica bloqueado e a página diz qual é a quantidade mínima.
- Se um ponto aparecer mais de uma vez, a página avisa e vale a primeira linha.

### Tela 2: o sorteio

1. Clique em **SORTEAR**. Depois da contagem, a tela mostra o ponto sorteado e o nome de quem comprou.
2. Para continuar, clique em **Sortear o próximo** ou feche a revelação e sorteie de novo.

Os botões no canto superior direito voltam para a tela de dados, ligam e desligam o som, colocam a página em tela cheia e levam à lista de participantes.

Voltar para a tela de dados sem mudar nada mantém os sorteios já feitos. Com outra planilha ou outra quantidade de pontos, o sorteio recomeça do zero.

Sem internet a página funciona do mesmo jeito. Só as fontes mudam, porque vêm do Google Fonts.

## Regras do sorteio

- **Quem concorre:** só os pontos vendidos. Cada ponto tem a mesma chance, então quem comprou mais pontos tem mais chances.
- **Ponto sorteado sai da disputa.** Ele aparece riscado no quadro e não volta a concorrer. Quem tem outros pontos continua concorrendo com eles.
- **Recomeçar:** devolve todos os pontos à disputa e apaga a lista de sorteios. Pede um segundo clique para confirmar.
- **Todos os pontos:** opção que inclui os pontos sem dono. Se sair um deles, a tela avisa, não solta fogos, e o ponto também sai da disputa.
- **Aleatoriedade:** o ponto é escolhido por `crypto.getRandomValues` no instante do clique, descartando a sobra da divisão para não favorecer nenhum ponto. A contagem na tela só revela o resultado.

O quadro de pontos tem 10 colunas. Rifas de até 200 pontos cabem inteiras na tela; nas maiores, o quadro rola por dentro e pula para o ponto sorteado.

## Nada fica guardado

- A página não usa `localStorage` nem cookies. A planilha, a quantidade de pontos e a lista de sorteios ficam só na memória dela.
- Aberta direto do arquivo, os dados não saem do navegador. Fechar ou recarregar a página apaga tudo, e é preciso carregar a planilha de novo.
- Servida pelo `expor_na_rede.py`, os dados carregados ficam também na memória do script, enquanto ele estiver aberto. Nada é gravado em disco. Recarregar a página traz os dados de volta, mas a lista de sorteios se perde.
- Se já houver sorteios feitos, o navegador pede confirmação antes de fechar ou recarregar.

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

Com o script, os dados carregados na página valem para a rede toda:

- **Quem carrega primeiro compartilha.** Ao clicar em **IR PARA O SORTEIO**, os nomes, os pontos e a quantidade de pontos vão para a memória do script.
- **Os outros aparelhos abrem direto no sorteio**, sem precisar da planilha. Quem já estava com a página aberta precisa recarregar.
- **Só o aparelho que carregou, ou o computador que roda o script, pode trocar a planilha ou a quantidade.** Nos outros, a tela de dados fica só para consulta.
- **Cada aparelho faz o próprio sorteio.** Os resultados e a lista de pontos sorteados não são compartilhados. O sorteio oficial é o da tela de quem apresenta.
- **Nada é gravado em disco.** Encerrar o script apaga os dados. Para começar com outra rifa, basta reiniciá-lo.
- Se o envio dos dados falhar, a página avisa e oferece seguir só naquele aparelho.

Sobre o acesso pela rede:

- **Quem abrir o endereço vê os nomes dos participantes e os pontos de cada um.** Telefones e e-mails não saem da planilha.
- O script entrega só a página e esses dados. Nenhum arquivo da pasta fica acessível.
- No Windows, o firewall pode perguntar se permite o Python na rede. Sem permitir em redes privadas, os outros aparelhos não conseguem abrir a página.

## Dados e privacidade

- O repositório não contém nomes, telefones nem pontos de ninguém.
- O relatório da rifa.digital traz nomes, telefones e e-mails. Não coloque a planilha no repositório. O `.gitignore` já ignora arquivos `.xlsx`.

## Adaptar para outra rifa

A quantidade de pontos e os participantes vêm da tela de dados. O resto fica em `sorteio-rifa-ibvb.html`:

| Onde | O que define |
|---|---|
| `PREMIO`, no `<script>` do fim | Texto do prêmio na tela de revelação. |
| `QTD_MIN` e `QTD_MAX`, no mesmo `<script>` | Limites da quantidade de pontos. |
| `IMAGENS`, no `<script>` anterior | Arte do título, foto do prêmio e logo da igreja, recortadas do cartaz da campanha e embutidas em base64. |
| HTML | Nome da igreja, texto do prêmio na tela do sorteio, atalhos de quantidade e frase do rodapé. |
