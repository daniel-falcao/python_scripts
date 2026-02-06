"""Script principal do aplicativo de receitas."""

# pip install requests beautifulsoup4 readability-lxml
# fpdf2 duckduckgo-search tkinter

import tkinter as tk
from tkinter import messagebox
from scraper import executar_lote
from logger import set_debug
from models import Receita
from exporters.pdf_exporter import exportar_pdf
from exporters.word_exporter import exportar_word
from pathlib import Path


def executar():
    set_debug(debug_mode.get())
    receitas = entrada_receitas.get("1.0", tk.END).strip().splitlines()
    sites = entrada_sites.get("1.0", tk.END).strip().splitlines()

    if not receitas:
        messagebox.showerror("Erro", "Informe ao menos uma receita.")
        return

    if not sites:
        messagebox.showerror("Erro", "Informe ao menos um site.")
        return

    status.set("Processando...")
    janela.update()

    dados = executar_lote(receitas, sites, estrategia=estrategia.get(),
                          max_sites=5)

    if not dados:
        messagebox.showwarning("Aviso", "Nenhuma receita válida encontrada.")
        status.set("")
        return

    saida = Path("saida")
    saida.mkdir(exist_ok=True)

    for r in dados:
        receita = Receita(
            titulo=r["termo"],
            ingredientes=r["ingredientes"],
            preparo=r["preparo"],
            fonte=r["site"],
            url=r["url"]
        )

    nome = receita.titulo.lower().replace(" ", "_")

    exportar_pdf(receita, saida / f"{nome}.pdf")

    exportar_word(receita, saida / f"{nome}.docx")

    status.set("Finalizado")
    messagebox.showinfo("Sucesso", "PDF e Word gerados com sucesso.")


janela = tk.Tk()
debug_mode = tk.BooleanVar(value=False)
janela.title("Coletor de Receitas Fit")
janela.geometry("600x500")
estrategia = tk.StringVar(value="MELHOR")


tk.Label(janela, text="Receitas (uma por linha):").pack(anchor="w", padx=10)
entrada_receitas = tk.Text(janela, height=7)
entrada_receitas.pack(fill="x", padx=10, pady=5)

tk.Label(janela, text="Sites para pesquisa (um por linha):").pack(
    anchor="w", padx=10)
entrada_sites = tk.Text(janela, height=6)
entrada_sites.pack(fill="x", padx=10, pady=5)

tk.Label(janela, text="Estratégia de seleção:").pack(anchor="w", padx=10)

tk.Radiobutton(
    janela,
    text="Melhor pontuada (recomendado)",
    variable=estrategia,
    value="MELHOR"
).pack(anchor="w", padx=30)

tk.Radiobutton(
    janela,
    text="Primeiro resultado válido",
    variable=estrategia,
    value="PRIMEIRO"
).pack(anchor="w", padx=30)

tk.Radiobutton(
    janela,
    text="Todos os resultados",
    variable=estrategia,
    value="TODOS"
).pack(anchor="w", padx=30)


tk.Checkbutton(
    janela,
    text="Modo DEBUG (log detalhado)",
    variable=debug_mode
).pack(anchor="w", padx=30, pady=5)


botao = tk.Button(janela, text="Executar", command=executar)
botao.pack(pady=15)

status = tk.StringVar()
tk.Label(janela, textvariable=status).pack()

janela.mainloop()
