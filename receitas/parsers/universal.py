"""Parser universal de receitas culinárias."""

# import requests
import re
from bs4 import BeautifulSoup
from http_client import session
# from logger import logger

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


UNIDADES = [
    "g", "kg", "ml", "l",
    "xícara", "xícaras",
    "colher", "colheres",
    "unidade", "unidades"
]

VERBOS = [
    "misture", "adicione", "leve", "asse", "cozinhe",
    "refogue", "bata", "misturar", "assar"
]

TIT_ING = ["ingrediente", "ingredientes"]
TIT_PREP = ["modo de preparo", "preparo", "modo"]


def score_lista(itens):
    score = 0
    for i in itens:
        if any(u in i.lower() for u in UNIDADES):
            score += 2
        if re.search(r"\d", i):
            score += 1
    return score


def extrair(url):
    r = session.get(url, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    candidatos_ing = []
    candidatos_prep = []

    # 1️⃣ Busca por títulos semânticos
    for tag in soup.find_all(["h2", "h3", "h4"]):
        texto = tag.get_text(strip=True).lower()

        if any(t in texto for t in TIT_ING):
            ul = tag.find_next(["ul", "ol"])
            if ul:
                candidatos_ing.append(
                    [li.get_text(strip=True) for li in ul.find_all("li")]
                )

        if any(t in texto for t in TIT_PREP):
            ol = tag.find_next(["ol", "ul"])
            if ol:
                candidatos_prep.append(
                    [li.get_text(strip=True) for li in ol.find_all("li")]
                )

    # 2️⃣ Busca por listas gerais (fallback)
    for lista in soup.find_all(["ul", "ol"]):
        itens = [li.get_text(strip=True) for li in lista.find_all("li")]
        if len(itens) < 3:
            continue

        if score_lista(itens) >= 4:
            candidatos_ing.append(itens)

        if any(v in " ".join(itens).lower() for v in VERBOS):
            candidatos_prep.append(itens)

    ingredientes = max(candidatos_ing, key=score_lista, default=[])
    preparo = max(candidatos_prep, key=len, default=[])

    return ingredientes, preparo
