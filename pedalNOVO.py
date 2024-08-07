from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLCDNumber, QLineEdit, QDial, QMessageBox, QTableWidgetItem, QComboBox, QTableWidget, QDialog,QSlider
import sys, sqlite3
import sounddevice as sd
import numpy as np
from pedalboard import Pedalboard, Reverb, Chorus, Compressor, Distortion, Gain, Delay, PitchShift
import threading


class BancoEfeitos(QMainWindow): #funçao que carrega a tela do banco de dados
    def __init__(self):
        super().__init__()
        uic.loadUi('carregarefeitos.ui', self)
        self.tableWidget = self.tableWidget
        self.botaoCarregar.clicked.connect(self.carregarEfeitos)
        self.pedalUI = TelaEfeitos()
        self.comboEfeitos = self.comboBox

    def gerarTabela(self): #funcao que gera a ateblada tela carregar efeitos
        conexao = sqlite3.connect("efeitos.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM SALVOS")
        efeitos = cursor.fetchall()
        self.tableWidget.setRowCount(len(efeitos))
        self.tableWidget.setColumnCount(len(efeitos[0]))
        for linha, registro in enumerate(efeitos):
            for coluna, valor in enumerate(registro):
                self.tableWidget.setItem(linha, coluna, QTableWidgetItem(str(valor)))

    def carregarCombo(self): # carregando comboBox
        conexao = sqlite3.connect("efeitos.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM SALVOS")
        efeitos = cursor.fetchall()
        for item in efeitos:
            self.comboEfeitos.addItem(str(item[0]))

    def carregarEfeitos(self): #funçao que puxa os valores do bd para a tela da pedaleira
        efeito_id = self.comboEfeitos.currentText()
        if not efeito_id:
            QMessageBox.warning(self,"Selecione um efeito do ComboBox.")
            return

        conexao = sqlite3.connect("efeitos.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM SALVOS WHERE id = ?", (efeito_id,))
        efeito = cursor.fetchone()
        conexao.close()

        if efeito:
            
            self.pedalUI.dial_compressor.setValue(efeito[4])
            self.pedalUI.dial_pitch.setValue(efeito[1])
            self.pedalUI.dial_reverb.setValue(efeito[2])
            self.pedalUI.dial_delay.setValue(efeito[3])
            self.pedalUI.dial_distorcao.setValue(efeito[5])
            self.pedalUI.dial_ganho.setValue(efeito[6])
            self.pedalUI.dial_razao.setValue(efeito[7])

            self.pedalUI.lcdCompressor.display(efeito[4])
            self.pedalUI.lcdPitch.display(efeito[1])
            self.pedalUI.lcdReverb.display(efeito[2])
            self.pedalUI.lcdDelay.display(efeito[3])
            self.pedalUI.lcdDistorcao.display(efeito[5])
            self.pedalUI.lcdGanho.display(efeito[6])
            self.pedalUI.lcdRazao.display(efeito[7])

            self.pedalUI.show()
        else:
            QMessageBox.warning(self, "Efeito Não Encontrado", "Não foi possível encontrar o efeito selecionado.")

class TelaEfeitos(QMainWindow): # carrega tela dos efeitos
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('pedalUI.ui', self)


        self.lcdCompressor = self.findChild(QLCDNumber, "lcdCompressor")
        self.dial_compressor = self.findChild(QDial, "dial_compressor")
        self.dial_compressor.valueChanged.connect(self.alterar_dial_compressor)
        self.janelaSalvar = self.JanelaSalvar(self)

        self.botaoLigar.clicked.connect(self.botao_ligar) # carregando botao ligar

        self.botaoDesligar.clicked.connect(self.botao_desligar) # carregando botao desligar

        self.pushButton_3.clicked.connect(self.mostrar_salvar) # carreagndo botao de sdalvar

        self.lcdGanho = self.findChild(QLCDNumber, "lcdGanho") # carregando botao de ganho
        self.dial_ganho = self.findChild(QDial, "dial_ganho")
        self.dial_ganho.valueChanged.connect(self.alterar_dial_ganho)

        self.lcdPitch = self.findChild(QLCDNumber, "lcdPitch") #carregando botao de pitch
        self.dial_pitch = self.findChild(QDial, "dial_pitch")
        self.dial_pitch.valueChanged.connect(self.alterar_dial_pitch)

        self.lcdDistorcao = self.findChild(QLCDNumber, "lcdDistorcao") # careegando botao de distorcao
        self.dial_distorcao = self.findChild(QDial, "dial_distorcao")
        self.dial_distorcao.valueChanged.connect(self.alterar_dial_distorcao)

        self.lcdReverb = self.findChild(QLCDNumber, "lcdReverb") #carregando botao do reverb
        self.dial_reverb = self.findChild(QDial, "dial_reverb")
        self.dial_reverb.valueChanged.connect(self.alterar_dial_reverb)

        self.lcdRazao = self.findChild(QLCDNumber, "lcdRazao") # carregando botao da razao
        self.dial_razao = self.findChild(QDial, "dial_razao")
        self.dial_razao.valueChanged.connect(self.alterar_dial_razao)

        self.lcdDelay = self.findChild(QLCDNumber, "lcdDelay") #carregando botao do delay
        self.dial_delay = self.findChild(QDial, "dial_delay")
        self.dial_delay.valueChanged.connect(self.alterar_dial_delay)

        self.compressor = (self.dial_compressor.value() *-1)
        self.pitch = self.dial_pitch.value()
        #self.volume = self.volume.value()
        self.reverb = (self.dial_reverb.value()/10)
        self.delay = (self.dial_delay.value()/10)
        self.distorcao = (self.dial_distorcao.value()/10)
        self.ganho = (self.dial_ganho.value()/10)
        self.razao = (self.dial_razao.value()/10)

    
    def botao_ligar(self):

        print("a pedaleira está ligada")
        self.process_audio(input_device=9, output_device=1, reverb_amount=self.reverb, chorus_rate=self.razao, compressor_threshold=self.compressor, distortion_amount=self.distorcao, gain_db=self.ganho, delay_time=self.delay, pitch_shift_semitones=self.pitch)

    def botao_desligar(self):
       
        print("a pedaleira está desligada")

    def process_audio(self, input_device, output_device, sample_rate=22050, buffer_size=512, reverb_amount=0.5, chorus_rate=1.0, compressor_threshold=-20.0, distortion_amount=0.5, gain_db=0.0, delay_time=0.5, pitch_shift_semitones=0):
        # Initialize the Pedalboard with desired effects
        board = Pedalboard([
            Reverb(room_size=reverb_amount),
            Chorus(rate_hz=chorus_rate),
            Compressor(threshold_db=compressor_threshold),
            Distortion(drive_db=distortion_amount),
            Gain(gain_db=gain_db),
            Delay(delay_seconds=delay_time),
            PitchShift(semitones=pitch_shift_semitones),
        ])

        def callback(indata, outdata, frames, time, status):
            if status:
                print(status)
            # Process the audio data
            processed = board(indata, sample_rate=sample_rate)
            outdata[:] = processed

        with sd.Stream(device=(input_device, output_device), samplerate=sample_rate, blocksize=buffer_size, dtype='float32', channels=1, callback=callback, latency="high"):
            print("Processing audio... Press Ctrl+C to stop.")
            try:
                while True:
                    sd.sleep(1000)
            except KeyboardInterrupt:
                print("Stopping audio processing.")

    def alterar_dial_ganho(self, valor):
        print(f'O ganho está em: {valor}')
        self.lcdGanho.display(valor)
        self.ganho = valor
        if valor < 5:
            self.lcdGanho.setStyleSheet("color: green;")
        elif 5 <= valor < 8:
            self.lcdGanho.setStyleSheet("color: yellow;")
        else:
            self.lcdGanho.setStyleSheet("color: red;")

    def alterar_dial_delay(self, valor):
        print(f'a saturação do delay está em: {valor}')
        self.lcdDelay.display(valor)
        self.delay = valor
        if valor < 5:
            self.lcdDelay.setStyleSheet("color: green;")
        elif 5 <= valor < 8:
            self.lcdDelay.setStyleSheet("color: yellow;")
        else:
            self.lcdDelay.setStyleSheet("color: red;")

    def alterar_dial_pitch(self, valor):
        print(f'O pitch está em: {valor}')
        self.lcdPitch.display(valor)
        self.pitch = valor
        if valor < 5:
            self.lcdPitch.setStyleSheet("color: green;")
        elif 5 <= valor < 8:
            self.lcdPitch.setStyleSheet("color: yellow;")
        else:
            self.lcdPitch.setStyleSheet("color: red;")

    def alterar_dial_distorcao(self, valor):
        print(f'a saturação da distorcao está em: {valor}')
        self.lcdDistorcao.display(valor)
        self.distorcao = valor
        if valor < 5:
            self.lcdDistorcao.setStyleSheet("color: green;")
        elif 5 <= valor < 8:
            self.lcdDistorcao.setStyleSheet("color: yellow;")
        else:
            self.lcdDistorcao.setStyleSheet("color: red;")

    def alterar_dial_compressor(self, valor):
        print(f'o compressor está em: {valor}')
        self.lcdCompressor.display(valor)
        self.compressor = valor
        if valor < 5:
            self.lcdCompressor.setStyleSheet("color: green;")
        elif 5 <= valor < 8:
            self.lcdCompressor.setStyleSheet("color: yellow;")
        else:
            self.lcdCompressor.setStyleSheet("color: red;")

    def alterar_dial_reverb(self, valor):
        print(f'a saturação do reverb está em: {valor}')
        self.lcdReverb.display(valor)
        self.reverb = valor
        if valor < 5:
            self.lcdReverb.setStyleSheet("color: green;")
        elif 5 <= valor < 8:
            self.lcdReverb.setStyleSheet("color: yellow;")
        else:
            self.lcdReverb.setStyleSheet("color: red;")

    def alterar_dial_razao(self, valor):
        print(f'a saturação da razao está em: {valor}')
        self.lcdRazao.display(valor)
        self.razao = valor
        if valor < 5:
            self.lcdRazao.setStyleSheet("color: green;")
        elif 5 <= valor < 8:
            self.lcdRazao.setStyleSheet("color: yellow;")
        else:
            self.lcdRazao.setStyleSheet("color: red;")

    def salvar_efeito(self, nome):
        id = nome
        compressor = self.dial_compressor.value()
        pitch = self.dial_pitch.value()
        
        reverb = self.dial_reverb.value()
        delay = self.dial_delay.value()
        distorcao = self.dial_distorcao.value()
        ganho = self.dial_ganho.value()
        razao = self.dial_razao.value()

        conexao = sqlite3.connect("efeitos.db")
        cursor = conexao.cursor()
        cursor.execute("""INSERT INTO SALVOS(id, pitch, reverb, delay, compressor, distorcao, ganho, razao, volume) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (id, pitch, reverb, delay, compressor, distorcao, ganho, razao, 0))
        conexao.commit()
        conexao.close()
        QMessageBox.information(self, "Efeito salvo", "Efeito salvo com sucesso!")

    def mostrar_salvar(self):
        self.janelaSalvar.show()

    class JanelaSalvar(QDialog):
        def __init__(self, main_window):
            super().__init__()
            uic.loadUi('salvarNome.ui', self)
            self.lineEdit = self.findChild(QLineEdit, "lineEdit")
            self.buttonBox.accepted.connect(self.salvar)
            self.buttonBox.rejected.connect(self.reject)
            self.main_window = main_window

        def salvar(self):
            nome = self.lineEdit.text()
            if nome:
                self.main_window.salvar_efeito(nome)
                self.accept()


class TelaInicial(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pedalinicio.ui', self)
        self.telaEfeitos = TelaEfeitos(parent=self)
        self.pushButton.clicked.connect(self.mostrar_tela)
        self.bancoEfeitos = BancoEfeitos()
        self.pushButton_2.clicked.connect(self.mostrar_banco)

    def mostrar_tela(self):
        self.telaEfeitos.show()

    def mostrar_banco(self):
        self.bancoEfeitos.carregarCombo()
        self.bancoEfeitos.gerarTabela()
        self.bancoEfeitos.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = TelaInicial()
    janela.show()
    sys.exit(app.exec_())
