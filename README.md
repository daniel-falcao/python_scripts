# python_scripts

### conferencia_registros.py
- Script para ler arquivos txt posicionais criar chaves de busca usando as posições fornecidas e armazenar essas chaves em um arquivo txt (arq1).
- Após consolidação das chaves criadas, usar outro arquivo txt (arq2) separado por ponto e vírgula e procurar os registros deste arquivo no arquivo arq1.
- Quando o registo do arq2 for encontrado no arq1, marcar como "OK" e quando não encontrar, marcar como "CANCELAR"

### consolidacao_arquivos_txt.py
- Script para consolidar diversos arquivos txt em um único arquivo.
- Após a consolidação, procurar o quinto registro do arquivo consolidado na coluna A de uma planilha Excel e inserir na última coluna do arquivo txt consolidado o valor correspondente da coluna C do arquivo Excel.

### de_x_para_registros.py
- Scrip para usar uma base de dados em excel como dataset para machine learning.
- Abrir um a um todos os arquivos Excel contidos na pasta informada e buscar a descrição presente na coluna informada dentro ddo dataset e procurar descrições similares semanticamente utilizando processamento de linguagem natural (NLP) uma vez que as descrição nem sempre serão idênticas mas podem significar a mesma coisa.
- Quando encontrar um registro similar, inserir no arquivo em análise nas duas últimas colunas o código e a descrição encontrados na base de dados.

### Projeto receitas
- Este projeto cria um app para rodar python sem a necessidade de tê-lo instalado no computador, criando versões para Windows ou Mac.
- Consiste em um app para buscar receitas culinárias na internet. O usuário deve informar as receitas e os sites onde buscar as receitas.
- Após a execução, o app irá salvar as receitas escolhidas em Word e PDF.
- Para criação do app, executar o script build_exe.py.
- Para rodar direto da IDE, executar o script app.py.
