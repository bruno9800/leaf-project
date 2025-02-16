import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd

def create_matrix_frame(parent, matrix, highlight_index=None, related_indexes=None):
    """
    Cria um frame que renderiza uma matriz 2D usando uma grade de Labels.
    
    - matrix: numpy.array contendo a matriz.
    - highlight_index: valor (geralmente o índice do doador) a ser destacado em amarelo.
    - related_indexes: conjunto de valores (índices) a serem destacados em azul claro.
    """
    frame = tk.Frame(parent)
    rows, cols = matrix.shape
    related_str = {str(idx) for idx in related_indexes} if related_indexes is not None else set()

    for i in range(rows):
        for j in range(cols):
            cell_value = matrix[i, j]
            cell_str = str(cell_value)
            if highlight_index is not None and cell_str == str(highlight_index):
                bg = "yellow"
            elif cell_str in related_str:
                bg = "lightblue"
            else:
                bg = "white"
            label = tk.Label(frame, text=str(cell_value),
                             borderwidth=1, relief="solid",
                             bg=bg, padx=5, pady=5)
            label.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
    return frame

def create_scrollable_frame(parent):
    """
    Cria um frame com um canvas e uma scrollbar horizontal, retornando
    o frame interno onde o conteúdo pode ser adicionado.
    """
    container = tk.Frame(parent)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, borderwidth=0, height=300)
    h_scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
    canvas.configure(xscrollcommand=h_scrollbar.set)

    h_scrollbar.pack(side="bottom", fill="x")
    canvas.pack(side="top", fill="both", expand=True)

    scroll_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    # Atualiza a região rolável quando o conteúdo mudar
    scroll_frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    return scroll_frame

def create_notebook_with_matrix(matrix, df_doadores, data):
    """
    Cria uma janela com abas. Em cada aba:
      - Exibe o nome do item (índice), as informações do doador e
      - Exibe, dentro de um frame com scroll horizontal, a matriz e ao lado as informações dos BIDs relacionados.
    """
    root = tk.Tk()
    root.title("Matriz com Destaques")
    root.geometry("1200x1200")  # Define um tamanho máximo para a janela
    
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    
    # Lista de colunas de PDSID no dataframe 'data'
    pdsid_cols_data = [col for col in data.columns if col.startswith("PDSID")]
    
    for idx, row in df_doadores.iterrows():
        # Extrai os PDSIDs do doador atual (todas as colunas que começam com "PDSID")
        current_pdsids = [row[col] for col in row.index if col.startswith("PDSID") and pd.notnull(row[col])]
        related_indexes = set()
        for pdsid in current_pdsids:
            for col in pdsid_cols_data:
                matches = data[(data[col] == pdsid) & (data.index != idx)]
                related_indexes.update(matches.index.tolist())
                
        # Cria uma lista com as informações dos índices relacionados e seus respectivos BIDs
        related_info = []
        for r in sorted(related_indexes):
            bid = data.loc[r, "Inventory BID"]
            related_info.append(f"Index: {r}, BID: {bid}")
        related_info_str = "\n".join(related_info) if related_info else "Nenhum relacionado encontrado."
        
        # Cria o frame da aba
        tab = tk.Frame(notebook)
        notebook.add(tab, text=f"Item {idx}")  # Label da aba com o índice real
        
        # Label com o nome do item (dentro da aba)
        item_label = tk.Label(tab, text=f"Item: {idx}", font=("Arial", 14, "bold"))
        item_label.pack(pady=5, padx=5, anchor="w")
        
        # Exibe as informações do doador com limite de largura
        donor_info = tk.Label(tab, text=f"Informações do Doador:\n{row.to_dict()}",
                              justify="left", anchor="w", wraplength=300)
        donor_info.pack(pady=(5,2), padx=5, anchor="w")
        
        # Cria um frame scrollable para conter a matriz e os BIDs relacionados
        scroll_frame = create_scrollable_frame(tab)
        
        # Coloca a matriz à esquerda
        matrix_frame = create_matrix_frame(scroll_frame, matrix,
                                           highlight_index=idx,
                                           related_indexes=related_indexes)
        matrix_frame.grid(row=0, column=0, padx=5, pady=5)
        
        # Coloca as informações dos BIDs relacionados à direita
        related_label = tk.Label(scroll_frame, text=f"Doadores Relacionados:\n{related_info_str}",
                                 justify="left", anchor="w", fg="blue", wraplength=200)
        related_label.grid(row=0, column=1, padx=5, pady=5, sticky="n")
    
    return root
