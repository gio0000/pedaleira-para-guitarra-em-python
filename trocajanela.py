import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget
from PyQt5.uic import loadUi

class Janela2(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Janela2.ui",self)
        self.pushButton.clicked.connect(self.fechar)

    def fechar(self):
        self.close()

class Janela1(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Janela1.ui",self)
        self.pushButton.clicked.connect(self.mudaJanela)
        self.janela2=Janela2()

    def mudaJanela(self):
        self.janela2.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = Janela1()
    janela.show()
    sys.exit(app.exec_())
