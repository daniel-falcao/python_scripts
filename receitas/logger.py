"""Gerar LOGs da aplicação de receitas."""

# import logging

# logging.basicConfig(
#     filename="receitas.txt",
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(message)s",
#     encoding="utf-8"
# )

# logger = logging.getLogger("receitas")

import logging

logger = logging.getLogger("receitas")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler = logging.FileHandler("receitas.log", encoding="utf-8")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def set_debug(debug: bool):
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("MODO DEBUG ATIVADO")
    else:
        logger.setLevel(logging.INFO)
