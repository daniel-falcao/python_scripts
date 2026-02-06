"""Código para conferir chaves em arquivos de
texto e atualizar um arquivo txt."""

import os


def main():
    """Código para conferir chaves em arquivos de
    texto e atualizar um arquivo txt."""

    # Pasta com os arquivos
    pasta = r"C:\Users\Usuario\Documents\Conferência Registros\Arquivos"

    # Arquivo principal
    arquivo_registros = os.path.join(pasta, "REGISTROS_ATIVOS_VIA_CARGA.txt")

    # Listas de arquivos posicionais por regra
    arquivos_regra1 = [
        "r1a_18092025.txt",
        "r1b_18092025.txt",
        "r1c_19082025.TXT",
        "r1d_18092025.txt",
        "r1e_18092025.TXT",
        "r1f_18092025.txt"]
    arquivos_regra2 = [
        "r2a_20250918.txt",
        "r2b_19092025.txt"]

    # Função para carregar as chaves de cada arquivo posicional

    def carregar_chaves(arquivo, regra):
        """ Carrega chaves de um arquivo posicional baseado
        na regra especificada. """

        chaves = set()
        with open(os.path.join(pasta, arquivo),
                  encoding="iso-8859-1", errors="ignore") as f:
            for linhac in f:
                if regra == 1:
                    chave = linhac[0:2] + linhac[234:245]  # pos 1-2 e 235-245
                else:
                    chave = linhac[0:2] + linhac[236:247]  # pos 1-2 e 237-247
                chaves.add(chave.strip())
        return chaves

    # Carregar todas as chaves válidas
    chaves_validas = set()
    for arq in arquivos_regra1:
        chaves_validas.update(carregar_chaves(arq, regra=1))
    for arq in arquivos_regra2:
        chaves_validas.update(carregar_chaves(arq, regra=2))

    # Salvar chaves válidas em um txt para conferência
    arquivo_chaves = os.path.join(pasta, "chaves_validas.txt")
    with open(arquivo_chaves, "w", encoding="iso-8859-1") as fc:
        for chavec in sorted(chaves_validas):
            fc.write(chavec + "\n")

    print(f"Arquivo de chaves válidas gerado em: {arquivo_chaves}")

    # Contadores
    cont_ok = 0
    cont_cancelar = 0
    total = 0

    # Processar beneficiarios_ativos.txt
    saida = os.path.join(pasta, "registros_ativos_processado.txt")
    with (open(arquivo_registros, encoding="iso-8859-1", errors="ignore")
          as fin, open(saida, "w", encoding="iso-8859-1") as fout):

        for linha in fin:
            partes = linha.strip().split(";")
            if len(partes) >= 5:
                chaveb = partes[4].strip() + partes[2].strip()
                total += 1
                if chaveb in chaves_validas:
                    nova_linha = linha.strip() + ";OK\n"
                    cont_ok += 1
                else:
                    nova_linha = linha.strip() + ";CANCELAR\n"
                    cont_cancelar += 1
                fout.write(nova_linha)

    # Resumo
    print(f"Processo concluído! Arquivo gerado em: {saida}")
    print(f"Total de linhas processadas: {total}")
    print(f"Marcadas como OK: {cont_ok}")
    print(f"Marcadas como CANCELAR: {cont_cancelar}")


main()
