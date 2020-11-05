# WebCrawlerRedesI

Nesse trabalho, o web crawler desenvolvido terá por objetivo de criar uma cópia de uma página especificada pelo usuário no sistema de arquivos local. Assim, o programa deverá requisitar o arquivo HTML base apontado pelo endereço especificado pelo usuário, deverá fazer um parsing (simplificado) do código HTML e, posteriormente, requisitar os demais objetos referenciados pelo HTML base. Como forma de simplificar o trabalho, além do HTML base, o programa deverá baixar e salvar apenas as imagens referenciadas na página (i.e., tags <img>): outros objetos (e.g., arquivos CSS, arquivos Javascript, vídeos, áudios) podem ser ignorados. Note que, exceto por identificar os elementos <img> no HTML base, o programa não precisa realizar qualquer tipo de processamento ou interpretação do HTML base.

## Utilização
#### Execute utilizando um dos comandos abaixo:
1. `python webCrawler.py -a <address> -p <port>`
2. `python webCrawler.py --address <address> --port <port>`

#### Observações
- O argumento port é opcional, seu valor default é 80.
- O html base será baixado e salvo num arquivo de nome "htmlBase.html".
- Para as imagens será criado um diretório imagens, e lá serão guardadas as imagens utilizando o mesmo nome e extensão originais.

**A cada execução o html e as imagens existentes serão substituídos!**

## Endereços testados
- http://www.ic.uff.br/index.php/pt
- http://wotvffbe.gamea.co
- http://www.capital.sp.gov.br/cidadao
- http://www.rondonopolis.mt.gov.br
- http://www.londrina.pr.gov.br
- http://www.rebeccaguay.com
