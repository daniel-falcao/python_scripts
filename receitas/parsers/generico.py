"""Parser genérico de receitas culinárias."""

# from readability import Document
from bs4 import BeautifulSoup
import requests
from http_client import session
from logger import logger
# import re

# HEADERS = {"User-Agent": "Mozilla/5.0"}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
    "Upgrade-Insecure-Requests": "1",
}


PALAVRAS_ING = ["ingrediente", "ingredientes"]
PALAVRAS_PREP = ["modo de preparo", "preparo", "modo"]


def extrair(url):
    try:
        r = session.get(url, timeout=20)
        r.raise_for_status()
    except requests.HTTPError as e:
        logger.error(f"ERRO | URL='{url}' | {e}")
    # return [], []
    soup = BeautifulSoup(r.text, "html.parser")

    # ==============================
    # 1. MAPA SEMÂNTICO
    # ==============================

    TEXT_ING = ("ingrediente", "ingredients")
    TEXT_PREP = ("preparo", "modo", "instructions", "directions")

    ingredientes = []
    preparo = []

    current_section = None

    # Percorre o HTML NA ORDEM NATURAL
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
        text = tag.get_text(" ", strip=True).lower()

        if not text:
            continue

        # Detecta mudança de seção
        if any(k in text for k in TEXT_ING):
            current_section = "ING"
            continue

        if any(k in text for k in TEXT_PREP):
            current_section = "PREP"
            continue

        # Coleta conteúdo conforme seção ativa
        if current_section == "ING":
            ingredientes.append(tag.get_text(" ", strip=True))

        elif current_section == "PREP":
            preparo.append(tag.get_text(" ", strip=True))

    # ==============================
    # 2. LIMPEZA DE SOBREPOSIÇÃO
    # ==============================

    set_ing = set(ingredientes)
    set_prep = set(preparo)

    intersecao = set_ing & set_prep
    if intersecao:
        logger.warning(
            f"OVERLAP DETECTADO | Removendo {len(intersecao)} itens duplicados"
        )
        ingredientes = [i for i in ingredientes if i not in intersecao]
        preparo = [p for p in preparo if p not in intersecao]

    logger.debug(
        f"PARSER FINAL | Ingredientes={len(ingredientes)} | Preparo={
            len(preparo)}"
    )

    return ingredientes, preparo
