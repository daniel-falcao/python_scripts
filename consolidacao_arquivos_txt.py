"""CONSOLIDAÇÃO DE ARQUIVOS TXT:
- Consolida vários arquivos .txt de uma pasta
- Gera um único arquivo .txt delimitado por ponto e vírgula
- Para cada linha, lê o 5º campo (CODIGO)
- Procura equivalência na coluna A do Excel DExPARA.xlsx
- Ao encontrar, copia o valor da coluna C e grava no novo campo NOVO_CODIGO
- Inclui log detalhado e barra de progresso com tqdm
- DEPENDÊNCIA: pip install pandas openpyxl tqdm"""


import pandas as pd
from tqdm import tqdm
from pathlib import Path
import logging

# ==============================
# 1. CONFIGURAÇÃO DE DIRETÓRIOS
# ==============================

CHOME = Path.home()
PASTA_TXT = Path(CHOME / 'Cursos' / 'Proj' / 'Consolid_TXT' / 'Arq_TXT')
ARQ_EXCEL = Path(CHOME / 'Cursos' / 'Proj' / 'Consolid_TXT' / 'DExPARA' /
                 'DExPARA.xlsx')
PASTA_SAIDA = Path(CHOME / 'Cursos' / 'Proj' / 'Consolid_TXT' / 'Saida')

ARQUIVO_SAIDA = Path(PASTA_SAIDA, 'arquivo_consolidado.txt')
ARQUIVO_LOG = Path(PASTA_SAIDA, 'processo_log.txt')


# ================================
# 2. FUNÇÃO PARA CONFIGURAR O LOG
# ================================
def configurar_log():
    logging.basicConfig(
        filename=ARQUIVO_LOG,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    )
    logging.info("==== Início do processo ====")


# ==========================================
# 3. CARREGAR MAPA DE EQUIVALÊNCIA DO EXCEL
# ==========================================
def carregar_equivalencias():
    logging.info("Carregando arquivo Excel de equivalências...")

    df = pd.read_excel(ARQ_EXCEL, dtype=str)

    # Cria um dicionário: chave = coluna A / valor = coluna C
    mapa = dict(zip(df.iloc[:, 0], df.iloc[:, 2]))

    logging.info(f"Mapa de equivalência carregado. Total de registros: \
        {len(mapa)}")
    return mapa


# -----------------------------------------------------
# 4. CONSOLIDAR ARQUIVOS TXT
# -----------------------------------------------------
def consolidar_arquivos_txt(mapa_equivalencia):
    logging.info("Iniciando consolidação dos arquivos TXT...")

    arquivos_txt = list(PASTA_TXT.glob("*.txt"))
    logging.info(f"Encontrados {len(arquivos_txt)} arquivos TXT.")

    linhas_saida = []

    # Processa cada arquivo com barra de progresso
    for arquivo in tqdm(arquivos_txt, desc="Processando arquivos TXT"):
        with open(arquivo, "r", encoding="utf-8", errors="ignore") as f:
            for linha in f:
                linha = linha.strip()

                if not linha:
                    continue

                campos = linha.split(";")

                # Garante que existam ao menos 5 campos
                if len(campos) < 5:
                    logging.warning(f"Linha ignorada (menos de 5 campos) em \
                        {arquivo}: {linha}")
                    continue

                codigo = campos[4].strip()

                # Busca equivalência
                cod_equivalente = mapa_equivalencia.get(codigo, "")

                campos.append(cod_equivalente)
                linhas_saida.append(";".join(campos))

    return linhas_saida


# -----------------------------------------------------
# 5. SALVAR ARQUIVO CONSOLIDADO
# -----------------------------------------------------
def salvar_arquivo(linhas):
    logging.info(f"Salvando arquivo final em: {ARQUIVO_SAIDA}")

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        for linha in linhas:
            f.write(linha + "\n")

    logging.info("Arquivo salvo com sucesso.")


# -----------------------------------------------------
# 6. EXECUÇÃO PRINCIPAL
# -----------------------------------------------------
def main():
    configurar_log()

    try:
        mapa = carregar_equivalencias()
        linhas = consolidar_arquivos_txt(mapa)
        salvar_arquivo(linhas)

        logging.info("==== Processo concluído com sucesso ====")
        print("\nProcesso concluído com sucesso!")
    except Exception as e:
        logging.error(f"Erro durante o processo: {e}")
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
