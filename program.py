import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import pandas as pd
import numpy as np

# --- Funções da interface de visualização (já desenvolvidas anteriormente) ---

def create_matrix_frame(parent, matrix, highlight_index=None, related_indexes=None):
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
    container = tk.Frame(parent)
    container.pack(fill="both", expand=True)
    canvas = tk.Canvas(container, borderwidth=0, height=300)
    h_scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
    canvas.configure(xscrollcommand=h_scrollbar.set)
    h_scrollbar.pack(side="bottom", fill="x")
    canvas.pack(side="top", fill="both", expand=True)
    scroll_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    scroll_frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
    return scroll_frame

def create_notebook_with_matrix(matrix, df_doadores, data):
    root = tk.Toplevel()
    root.title("Matriz com Destaques")
    root.geometry("800x600")
    
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")
    
    pdsid_cols_data = [col for col in data.columns if col.startswith("PDSID")]
    
    for idx, row in df_doadores.iterrows():
        current_pdsids = [row[col] for col in row.index if col.startswith("PDSID") and pd.notnull(row[col])]
        related_indexes = set()
        for pdsid in current_pdsids:
            for col in pdsid_cols_data:
                matches = data[(data[col] == pdsid) & (data.index != idx)]
                related_indexes.update(matches.index.tolist())
                
        related_info = []
        for r in sorted(related_indexes):
            bid = data.loc[r, "Inventory BID"]
            related_info.append(f"Index: {r}, BID: {bid}")
        related_info_str = "\n".join(related_info) if related_info else "Nenhum relacionado encontrado."
        
        tab = tk.Frame(notebook)
        notebook.add(tab, text=f"Item {idx}")  # Índice real
        
        # Nome do item
        item_label = tk.Label(tab, text=f"Item: {idx}", font=("Arial", 14, "bold"))
        item_label.pack(pady=5, padx=5, anchor="w")
        
        donor_info = tk.Label(tab, text=f"Informações do Doador:\n{row.to_dict()}",
                              justify="left", anchor="w", wraplength=300)
        donor_info.pack(pady=(5,2), padx=5, anchor="w")
        
        scroll_frame = create_scrollable_frame(tab)
        matrix_frame = create_matrix_frame(scroll_frame, matrix,
                                           highlight_index=idx,
                                           related_indexes=related_indexes)
        matrix_frame.grid(row=0, column=0, padx=5, pady=5)
        
        related_label = tk.Label(scroll_frame, text=f"Doadores Relacionados:\n{related_info_str}",
                                 justify="left", anchor="w", fg="blue", wraplength=200)
        related_label.grid(row=0, column=1, padx=5, pady=5, sticky="n")
    
    return root

# --- Funções de apoio para a interface principal ---

def import_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        entry_csv_path.delete(0, tk.END)
        entry_csv_path.insert(0, file_path)

def run_normalization():
    file_path = entry_csv_path.get()
    if not file_path:
        messagebox.showerror("Erro", "Por favor, importe um arquivo CSV primeiro.")
        return
    try:
        # Chama o script normalize-data.py com o caminho do CSV
        subprocess.run(["python", "normalize-data.py", file_path], check=True)
        messagebox.showinfo("Sucesso", "CSV normalizado com sucesso.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"A normalização falhou: {str(e)}")

def run_algorithm():
    layout_str = entry_layout.get()
    bench_str = entry_bench.get()
    try:
        layout = eval(layout_str)  # Exemplo: (9,20)
        bench = eval(bench_str)    # Exemplo: (4,2)
    except Exception as e:
        messagebox.showerror("Erro", "Formato inválido para layout ou bench.")
        return
    
    file_path = entry_csv_path.get()
    if not file_path:
        messagebox.showerror("Erro", "Por favor, importe um arquivo CSV.")
        return
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao ler o CSV: {str(e)}")
        return
    
    # Aqui você pode integrar a execução do seu algoritmo que gera a população
    # e otimiza a disposição. Para demonstração, criaremos uma matriz dummy com o layout.
    matrix = np.arange(layout[0] * layout[1]).reshape(layout)
    
    # Filtra os doadores (exemplo: "Pollination Gender" igual a "M")
    df_doadores = data[data["Pollination Gender"] == "M"]
    
    # Abre uma nova janela com o notebook de matrizes
    notebook_window = create_notebook_with_matrix(matrix, df_doadores, data)
    notebook_window.mainloop()

# --- Interface Principal ---

root = tk.Tk()
root.title("Interface de Execução")
root.geometry("600x400")

# Frame para importação do CSV
frame_csv = tk.Frame(root)
frame_csv.pack(pady=10, padx=10, fill="x")

tk.Label(frame_csv, text="CSV File:").pack(side="left")
entry_csv_path = tk.Entry(frame_csv, width=40)
entry_csv_path.pack(side="left", padx=5)
tk.Button(frame_csv, text="Import CSV", command=import_csv).pack(side="left", padx=5)
tk.Button(frame_csv, text="Normalize Data", command=run_normalization).pack(side="left", padx=5)

# Frame para parâmetros de layout e bench
frame_params = tk.Frame(root)
frame_params.pack(pady=10, padx=10, fill="x")

tk.Label(frame_params, text="Layout Size (ex: (9,20)):", anchor="w").pack(side="left")
entry_layout = tk.Entry(frame_params, width=15)
entry_layout.pack(side="left", padx=5)

tk.Label(frame_params, text="Bench Size (ex: (4,2)):", anchor="w").pack(side="left")
entry_bench = tk.Entry(frame_params, width=10)
entry_bench.pack(side="left", padx=5)

# Botão para executar o algoritmo
tk.Button(root, text="Run Algorithm", command=run_algorithm).pack(pady=20)

root.mainloop()
