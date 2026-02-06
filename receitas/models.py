"""Modelos de documentos para exportação de receitas em PDF e Word"""

from dataclasses import dataclass
from typing import List


@dataclass
class Receita:
    titulo: str
    ingredientes: List[str]
    preparo: List[str]
    fonte: str
    url: str
