from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('carregarefeitos.ui', self)

        self.pushButton.clicked.connect(self.carregar_efeitos)
       # self.comboBox=comboBox

    def carregar_efeitos(self):
        efeito_selecionado=self.combobox
        conexao=sqlite3.connect("efeitos.db")
        cursor=conexao.cursor()

        cursor.execute("SELECT * FROM SALVOS WHERE id = {efeito_selecionado};")
        efeitos = cursor.fetchone()
        

        conexao.close()

        return efeitos
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = MainWindow()
    janela.show()
    sys.exit(app.exec_())
