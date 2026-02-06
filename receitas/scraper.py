"""SCRAPER DE RECEITAS CULINÁRIAS"""

# from duckduckgo_search import DDGS
from ddgs import DDGS
import time
import random
from logger import logger
from parsers import (
    tudo_gostoso,
    panelinha,
    receitas_globo,
    cybercook,
    generico,
    universal
)


# def escolher_parser(url):
#     if "tudogostoso" in url:
#         return tudo_gostoso
#     if "panelinha" in url:
#         return panelinha
#     if "globo" in url:
#         return receitas_globo
#     if "cybercook" in url:
#         return cybercook
#     return generico


def escolher_parser(url):
    if "tudogostoso.com.br" in url:
        logger.debug("PARSER | TudoGostoso")
        return tudo_gostoso
    if "panelinha.com.br" in url:
        logger.debug("PARSER | Panelinha")
        return panelinha
    if "receitas.globo.com" in url:
        logger.debug("PARSER | Receitas Globo")
        return receitas_globo
    if "cybercook.com.br" in url:
        logger.debug("PARSER | CyberCook")
        return cybercook

    logger.debug("PARSER | Genérico")
    return generico


# def buscar_links(receita, site, max_sites):
#     termo = f"{receita} site:{site}"
#     with DDGS() as ddgs:
#         resultados = list(ddgs.text(termo, max_results=max_sites))
#     return [r["href"] for r in resultados if "href" in r]
#

def buscar_links(receita, site, max_sites):
    termo = f"{receita} site:{site}"
    logger.debug(f"BUSCA | Termo='{termo}'")

    with DDGS() as ddgs:
        resultados = list(ddgs.text(termo, max_results=max_sites))

    logger.debug(
        f"RESULTADOS | Receita='{receita}' | Site='{site}' | "
        f"Links encontrados={len(resultados) if resultados else 0}"
    )

    return [r["href"] for r in resultados or [] if "href" in r]


def pontuar_receita(url, ingredientes, preparo, termo):
    score = 0

    score += min(len(ingredientes), 15) * 2
    score += min(len(preparo), 20)

    palavras = termo.lower().split()
    texto = " ".join(ingredientes + preparo).lower()

    for p in palavras:
        if p in texto:
            score += 3

    if len(url) < 120:
        score += 2

    logger.debug(
        f"PONTUAÇÃO | URL='{url}' | Score={score}"
    )
    logger.info(
        f"PONTUAÇÃO | Receita='{termo}' | URL='{url}' | "
        f"Ingredientes={len(ingredientes)} | Passos={len(preparo)} | Score={
            score}"
    )

    return score


def executar_lote(receitas, sites, estrategia="MELHOR", max_sites=5):
    resultados_finais = []

    for receita in receitas:
        for site in sites:
            links = buscar_links(receita, site, max_sites)
            candidatos = []

            for link in links:
                try:
                    parser = escolher_parser(link)
                    ingredientes, preparo = parser.extrair(link)

                    if not ingredientes or not preparo:
                        logger.debug("FALLBACK | Parser específico falhou")
                        ingredientes, preparo = generico.extrair(link)

                    if not ingredientes or not preparo:
                        logger.debug("FALLBACK | Parser genérico falhou")
                        ingredientes, preparo = universal.extrair(link)

                    if not ingredientes or not preparo:
                        logger.debug(
                            "DESCARTE FINAL | Parser universal falhou")
                        continue

                    if estrategia == "PRIMEIRO":
                        logger.info(
                            f"SELEÇÃO | Estratégia=PRIMEIRO | "
                            f"Receita='{receita}' | URL='{link}'"
                        )
                        resultados_finais.append({
                            "termo": receita,
                            "site": site,
                            "url": link,
                            "ingredientes": ingredientes,
                            "preparo": preparo
                        })
                        break

                    if estrategia == "MELHOR":
                        score = pontuar_receita(
                            link, ingredientes, preparo, receita
                        )
                        candidatos.append({
                            "termo": receita,
                            "site": site,
                            "url": link,
                            "ingredientes": ingredientes,
                            "preparo": preparo,
                            "score": score
                        })

                    if estrategia == "TODOS":
                        resultados_finais.append({
                            "termo": receita,
                            "site": site,
                            "url": link,
                            "ingredientes": ingredientes,
                            "preparo": preparo
                        })

                except Exception as e:
                    logger.error(f"ERRO | URL='{link}' | {e}")

                time.sleep(random.uniform(1.5, 3.5))

            if estrategia == "MELHOR" and candidatos:
                vencedor = max(candidatos, key=lambda x: x["score"])

                logger.info(
                    f"VENCEDOR | Receita='{receita}' | Site='{site}' | "
                    f"URL='{vencedor['url']}' | Score={vencedor['score']}"
                )

                resultados_finais.append(vencedor)

    return resultados_finais
