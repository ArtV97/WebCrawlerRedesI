# WebCrawlerRedesI

Nesse trabalho, o web crawler desenvolvido terá por objetivo de criar uma cópia de uma página especificada pelo usuário no sistema de arquivos local. Assim, o programa deverá requisitar o arquivo HTML base apontado pelo endereço especificado pelo usuário, deverá fazer um parsing (simplificado) do código HTML e, posteriormente, requisitar os demais objetos referenciados pelo HTML base. Como forma de simplificar o trabalho, além do HTML base, o programa deverá baixar e salvar apenas as imagens referenciadas na página (i.e., tags <img>): outros objetos (e.g., arquivos CSS, arquivos Javascript, vídeos, áudios) podem ser ignorados. Note que, exceto por identificar os elementos <img> no HTML base, o programa não precisa realizar qualquer tipo de processamento ou interpretação do HTML base.

## Utilização
`python3 webCrawler.py -a <address> -p <port>`
o argumento port é opcional, o default é 80