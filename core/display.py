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
    # Converte os índices relacionados para strings (para comparação com o valor da célula)
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

def create_notebook_with_matrix(matrix, df_doadores, data):
    """
    Cria uma janela com abas, onde cada aba representa um doador (linha) de df_doadores.
    
    Em cada aba:
      - Exibe as informações do doador.
      - Exibe uma lista dos índices relacionados e seus respectivos "Inventory BID"
        (os quais serão destacados na matriz em azul).
      - Exibe a matriz, onde a célula cujo valor corresponde ao índice do doador é destacada em amarelo
        e os relacionados (obtidos pelos PDSID) em azul.
    """
    root = tk.Tk()
    root.title("Matriz com Destaques")
    
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    
    # Lista de colunas de PDSID no dataframe 'data'
    pdsid_cols_data = [col for col in data.columns if col.startswith("PDSID")]
    
    for idx, row in df_doadores.iterrows():
        # Extrai os PDSIDs do doador atual (todas as colunas que começam com "PDSID")
        current_pdsids = [row[col] for col in row.index if col.startswith("PDSID") and pd.notnull(row[col])]
        
        # Conjunto para armazenar os índices relacionados (dos outros itens em data)
        related_indexes = set()
        for pdsid in current_pdsids:
            for col in pdsid_cols_data:
                # Filtra as linhas onde o valor da coluna é igual ao PDSID e o índice é diferente do doador atual
                matches = data[(data[col] == pdsid) & (data.index != idx)]
                related_indexes.update(matches.index.tolist())
        
        # Cria uma lista de strings com as informações dos índices relacionados e seus respectivos BIDs
        related_info = []
        for r in sorted(related_indexes):
            bid = data.loc[r, "Inventory BID"]
            related_info.append(f"Index: {r}, BID: {bid}")
        related_info_str = "\n".join(related_info) if related_info else "Nenhum relacionado encontrado."
        
        # Cria um frame para a aba
        tab = tk.Frame(notebook)
        notebook.add(tab, text=f"Item {idx+1}")
        
        # Exibe as informações do doador
        donor_info = tk.Label(tab, text=f"Informações do Doador:\n{row.to_dict()}",
                              justify="left", anchor="w")
        donor_info.pack(pady=(5,2), padx=5, anchor="w")
        
        # Exibe a lista de doadores relacionados (índices e seus respectivos BIDs)
        related_label = tk.Label(tab, text=f"Doadores Relacionados:\n{related_info_str}",
                                 justify="left", anchor="w", fg="blue")
        related_label.pack(pady=(0,5), padx=5, anchor="w")
        
        # Cria e adiciona o frame da matriz
        matrix_frame = create_matrix_frame(tab, matrix,
                                           highlight_index=idx,
                                           related_indexes=related_indexes)
        matrix_frame.pack(pady=5, padx=5)
    
    return root


    

