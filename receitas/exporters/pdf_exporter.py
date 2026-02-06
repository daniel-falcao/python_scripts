"""PDF exporter"""

from fpdf import FPDF
from pathlib import Path

FONT_PATH = Path(__file__).parent / "fonts" / "DejaVuSans.ttf"


class ReceitaPDF(FPDF):

    # def __init__(self):
    #     super().__init__()

    #     # REGISTRAR FONTES ANTES DE QUALQUER add_page()
    #     self.add_font("DejaVu", "", FONT_PATH, uni=True)
    #     self.add_font("DejaVu", "B", FONT_PATH, uni=True)

    def header(self):
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 10, "Receita", align="C", new_y="NEXT")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", size=8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


def exportar_pdf(receita, destino):
    pdf = ReceitaPDF()

    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.add_font("DejaVu", "B", FONT_PATH, uni=True)

    pdf.add_page()

    # Título
    pdf.set_font("DejaVu", "B", 18)
    pdf.set_x(pdf.l_margin)
    largura = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.multi_cell(largura, 10, receita.titulo)
    pdf.ln(4)

    # Fonte
    pdf.set_font("DejaVu", size=10)
    pdf.set_x(pdf.l_margin)
    largura = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.multi_cell(largura, 6, f"Fonte: {receita.fonte}")

    pdf.ln(1)

    pdf.set_x(pdf.l_margin)
    largura = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.multi_cell(largura, 6, f"URL: {receita.url}")
    pdf.ln(4)

    # Ingredientes
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "Ingredientes", new_y="NEXT")
    pdf.set_font("DejaVu", size=11)

    for ing in receita.ingredientes:
        pdf.set_x(pdf.l_margin)
        largura = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.multi_cell(largura, 6, f"• {ing}")

    pdf.ln(3)

    # Preparo
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "Modo de preparo", new_y="NEXT")
    pdf.set_font("DejaVu", size=11)

    for i, passo in enumerate(receita.preparo, start=1):
        pdf.set_x(pdf.l_margin)
        largura = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.multi_cell(largura, 6, f"{i}. {passo}")

    pdf.output(destino)
