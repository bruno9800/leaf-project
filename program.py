import sys
import subprocess
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QFileDialog, QTabWidget, QScrollArea,
    QGridLayout, QMessageBox
)
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt

# =======================================================
# Janela Principal (Interface de Execução)
# =======================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface de Execução")
        self.setGeometry(100, 100, 600, 400)
        self.csv_path = ""
        
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout(centralWidget)
        
        # Linha para importar o CSV e normalizar
        csvLayout = QHBoxLayout()
        self.csvLineEdit = QLineEdit()
        self.csvLineEdit.setPlaceholderText("Caminho do CSV")
        btnImportCSV = QPushButton("Import CSV")
        btnImportCSV.clicked.connect(self.import_csv)
        btnNormalize = QPushButton("Normalize Data")
        btnNormalize.clicked.connect(self.normalize_data)
        csvLayout.addWidget(QLabel("CSV File:"))
        csvLayout.addWidget(self.csvLineEdit)
        csvLayout.addWidget(btnImportCSV)
        csvLayout.addWidget(btnNormalize)
        mainLayout.addLayout(csvLayout)
        
        # Feedback visual de normalização
        self.feedbackLabel = QLabel("")
        mainLayout.addWidget(self.feedbackLabel)
        
        # Inputs para parâmetros: Layout e Bench
        paramsLayout = QHBoxLayout()
        self.layoutLineEdit = QLineEdit()
        self.layoutLineEdit.setPlaceholderText("Ex: (9,20)")
        self.benchLineEdit = QLineEdit()
        self.benchLineEdit.setPlaceholderText("Ex: (4,2)")
        paramsLayout.addWidget(QLabel("Layout Size:"))
        paramsLayout.addWidget(self.layoutLineEdit)
        paramsLayout.addWidget(QLabel("Bench Size:"))
        paramsLayout.addWidget(self.benchLineEdit)
        mainLayout.addLayout(paramsLayout)
        
        # Botão para rodar o algoritmo genético
        btnRunAlgorithm = QPushButton("Run Algorithm")
        btnRunAlgorithm.clicked.connect(self.run_algorithm)
        mainLayout.addWidget(btnRunAlgorithm)
    
    def import_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if path:
            self.csv_path = path
            self.csvLineEdit.setText(path)
    
    def normalize_data(self):
        if not self.csv_path:
            QMessageBox.critical(self, "Erro", "Por favor, selecione um CSV primeiro.")
            return
        try:
            # Chama o script normalize-data-program.py passando o caminho do CSV.
            # Este script deve gerar o arquivo "result-program.csv" como resultado.
            subprocess.run(["python", "normalize-data-program.py", self.csv_path], check=True)
            self.feedbackLabel.setText("CSV normalizado com sucesso!")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Erro", f"Erro ao normalizar CSV: {str(e)}")
    
    def run_algorithm(self):
    # Coleta os parâmetros dos inputs
      layout_str = self.layoutLineEdit.text()
      bench_str = self.benchLineEdit.text()
      try:
          layout_dim = eval(layout_str)  # Exemplo: (9,20)
          bench_dim = eval(bench_str)    # Exemplo: (4,2)
      except Exception as e:
          QMessageBox.critical(self, "Erro", "Formato inválido para layout ou bench.")
          return

      # Em vez de usar o arquivo importado, usa o arquivo normalizado "result-program.csv"
      try:
          data = pd.read_csv("result-program.csv")
      except Exception as e:
          QMessageBox.critical(self, "Erro", f"Erro ao ler o arquivo result-program.csv: {str(e)}")
          return

      # Verifica se o layout comporta todas as plantas
      num_plants = data.shape[0]
      total_positions = layout_dim[0] * layout_dim[1]
      if total_positions < num_plants:
          QMessageBox.critical(self, "Erro", f"O layout precisa ter pelo menos {num_plants} posições. "
                                              f"Seu layout atual possui {total_positions} posições.")
          return

      # Calcula o número de colunas PDSID presentes no DataFrame
      num_pdsid_columns = sum(col.startswith("PDSID") for col in data.columns)

      # Atualiza o feedback visual
      self.feedbackLabel.setText("Executando o algoritmo genético...")
      QApplication.processEvents()

      # Importa as funções do algoritmo genético do módulo core (certifique-se do caminho correto)
      from core.mainProgram import genetic_algorithm
      from core.aux import map_ids_to_functions

      # Executa o algoritmo genético
      best_solution, best_fitness = genetic_algorithm(data, layout_dim, bench_dim, num_pdsid_columns)
      print("Melhor fitness:", best_fitness)

      # Converte a melhor solução em uma "function matrix"
      function_matrix = map_ids_to_functions(best_solution, data)
      print("Function Matrix:\n", function_matrix)

      # Filtra os doadores (onde 'Pollination Gender' == 'M')
      df_donors = data[data["Pollination Gender"] == "M"]

      # Abre a janela de resultados com a matriz final
      self.resultWindow = ResultWindow(function_matrix, df_donors, data)
      self.resultWindow.show()


# =======================================================
# Janela de Resultados (Exibição dos Resultados do Algoritmo)
# =======================================================
class ResultWindow(QWidget):
    def __init__(self, matrix, df_donors, data):
        super().__init__()
        self.setWindowTitle("Matriz com Destaques")
        self.resize(1200, 1200)  # Tamanho máximo semelhante ao exemplo Tkinter
        self.matrix = matrix
        self.df_donors = df_donors
        self.data = data
        
        layout = QVBoxLayout(self)
        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget)
        
        # Para cada doador, cria uma aba
        for idx, row in self.df_donors.iterrows():
            tab = QWidget()
            tabLayout = QVBoxLayout(tab)
            
            # Label com o nome do item (índice)
            item_label = QLabel(f"Item: {idx}")
            font = QFont("Arial", 14, QFont.Bold)
            item_label.setFont(font)
            tabLayout.addWidget(item_label)
            
            # Exibe as informações do doador com wrap e largura limitada
            donor_info = QLabel("Informações do Doador:\n" + str(row.to_dict()))
            donor_info.setWordWrap(True)
            donor_info.setMaximumWidth(600)
            donor_info.setMaximumHeight(300)
            tabLayout.addWidget(donor_info)
            
            # Cria um QScrollArea para conter a matriz e os BIDs relacionados
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            container = QWidget()
            hLayout = QHBoxLayout(container)
            
            # Obtém os índices relacionados para este doador
            related_indexes = self.get_related_indexes(row)
            # Cria o widget da matriz (usando QGridLayout) com destaque
            matrix_widget = self.createMatrixWidget(self.matrix, idx, related_indexes)
            hLayout.addWidget(matrix_widget)
            
            # Cria um QLabel com as informações dos BIDs relacionados
            related_info_str = self.get_related_info(row)
            related_label = QLabel("Doadores Relacionados:\n" + related_info_str)
            related_label.setWordWrap(True)
            related_label.setStyleSheet("color: blue;")
            related_label.setMaximumWidth(200)
            hLayout.addWidget(related_label)
            
            container.setLayout(hLayout)
            scroll_area.setWidget(container)
            tabLayout.addWidget(scroll_area)
            
            self.tabWidget.addTab(tab, f"Item {idx}")
        
        self.setLayout(layout)
    
    def createMatrixWidget(self, matrix, highlight_index, related_indexes):
        """
        Cria um widget para exibir a matriz em um layout de grade.
        As células cuja string seja igual ao highlight_index serão pintadas de amarelo,
        e as que estiverem em related_indexes (convertidos para string) serão pintadas de azul claro.
        """
        widget = QWidget()
        grid = QGridLayout(widget)
        rows, cols = matrix.shape
        related_str = {str(x) for x in related_indexes}
        for i in range(rows):
            for j in range(cols):
                cell_value = matrix[i, j]
                cell_str = str(cell_value)
                label = QLabel(cell_str)
                label.setAlignment(Qt.AlignCenter)
                if highlight_index is not None and cell_str == str(highlight_index):
                    label.setStyleSheet("background-color: yellow; border: 1px solid black; padding: 5px;")
                elif cell_str in related_str:
                    label.setStyleSheet("background-color: lightblue; border: 1px solid black; padding: 5px;")
                else:
                    label.setStyleSheet("background-color: white; border: 1px solid black; padding: 5px;")
                grid.addWidget(label, i, j)
        return widget
    
    def get_related_indexes(self, donor_row):
      related_indexes = set()
      # Obtém todas as colunas que começam com "PDSID" do DataFrame completo
      pdsid_cols_data = [col for col in self.data.columns if col.startswith("PDSID")]
      # Para cada valor de PDSID presente no doador (em qualquer coluna), procure em todas as colunas PDSID
      for col in donor_row.index:
          if col.startswith("PDSID") and pd.notnull(donor_row[col]):
              pdsid_value = donor_row[col]
              for pdsid_col in pdsid_cols_data:
                  matches = self.data[(self.data[pdsid_col] == pdsid_value) &
                                      (self.data["Inventory BID"] != donor_row["Inventory BID"])]
                  related_indexes.update(matches.index.tolist())
      return related_indexes

    
    def get_related_info(self, donor_row):
        """
        Retorna uma string com os índices relacionados e seus respectivos "Inventory BID".
        """
        related_indexes = self.get_related_indexes(donor_row)
        info_list = []
        for idx in sorted(related_indexes):
            bid = self.data.loc[idx, "Inventory BID"]
            info_list.append(f"Index: {idx}, BID: {bid}")
        return "\n".join(info_list) if info_list else "Nenhum relacionado encontrado."

# =======================================================
# Execução do Aplicativo
# =======================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
