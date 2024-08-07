

from pedalboard import Distortion,Pedalboard, Chorus, Compressor, Gain, Reverb, Phaser, Delay, PitchShift
from pedalboard.io import AudioStream
import random
import time
import tkinter as tk
import threading

delay_inicial = 0.0 
3
pitch_inicial = 0.0

entrada = AudioStream.input_device_names[0]
saida = AudioStream.output_device_names[0]
print(entrada, saida)

limiteCompressor = 0.0
razao = 1.0
ganho = 0.0
reverb = 0.0
distorcao = 0.0

# Adjust functions
def attDelay(delay):
    global delay_inicial
    delay_inicial = float(delay)

def attPitch(pitch):
    global pitch_inicial
    pitch_inicial = float(pitch)

def attCompressao(compressao):
    global limiteCompressor
    limiteCompressor = float(compressao)

def attRazao(novaRazao):
    global razao
    razao = float(novaRazao)

def attGanho(novoGanho):
    global ganho
    ganho = float(novoGanho)

def attReverb(novoReverb):
    global reverb
    reverb = float(novoReverb)


def attDistorcao(novaDist):
    global distorcao
    distorcao = float(novaDist)


# funcoes dos efeitos
def janela():
    janela = tk.Tk()
    janela.title("Pedaleira gio 1.0")

    # Delay slider
    rotulo_delay = tk.Label(janela, text="Delay")
    rotulo_delay.grid(column=0, row=0, padx=10)
    slider_delay = tk.Scale(janela, from_=5.0, to=0.0, orient=tk.VERTICAL,
                            resolution=0.1, command=attDelay)
    slider_delay.grid(column=0, row=1, padx=10)
   

    # Pitch slider
    rotulo_pitch = tk.Label(janela, text="Pitch")
    rotulo_pitch.grid(column=1, row=0, padx=10)
    slider_pitch = tk.Scale(janela, from_=1.0, to=0.0, orient=tk.VERTICAL,
                            resolution=0.1, command=attPitch)
    slider_pitch.grid(column=1, row=1, padx=10)

    # Compression slider
    rotulo_compressao = tk.Label(janela, text="Compressao")
    rotulo_compressao.grid(column=2, row=0, padx=10)
    slider_compressao = tk.Scale(janela, from_=-50.0, to=1.0, orient=tk.VERTICAL,
                                 resolution=0.1, command=attCompressao)
    slider_compressao.grid(column=2, row=1, padx=10)

    # Ratio slider
    rotulo_razao = tk.Label(janela, text="Razao")
    rotulo_razao.grid(column=3, row=0, padx=10)
    slider_razao = tk.Scale(janela, from_=50.0, to=1.0, orient=tk.VERTICAL,
                            resolution=0.1, command=attRazao)
    slider_razao.grid(column=3, row=1, padx=10)

    # Gain slider
    rotulo_ganho = tk.Label(janela, text="Ganho")
    rotulo_ganho.grid(column=4, row=0, padx=10)
    slider_ganho = tk.Scale(janela, from_=30.0, to=0.0, orient=tk.VERTICAL,
                            resolution=0.1, command=attGanho)
    slider_ganho.grid(column=4, row=1, padx=10)

    # Reverb slider
    rotulo_reverb = tk.Label(janela, text="Reverb")
    rotulo_reverb.grid(column=5, row=0, padx=10)
    slider_reverb = tk.Scale(janela, from_=1.0, to=0.0, orient=tk.VERTICAL,
                             resolution=0.1, command=attReverb)
    slider_reverb.grid(column=5, row=1, padx=10)

     # Distorcao slider
    rotulo_dist = tk.Label(janela, text="Distorção")
    rotulo_dist.grid(column=6, row=0, padx=10)
    slider_dist = tk.Scale(janela, from_=1.0, to=0.0, orient=tk.VERTICAL,
                             resolution=0.1, command=attReverb)
    slider_dist.grid(column=6, row=1, padx=10)


    janela.mainloop()

# processamento do audio funcao
def audio_processing():
    global delay_inicial, pitch_inicial, limiteCompressor, razao, ganho, reverb

    buffer= 128 # Smaller buffer size for lower latency
    sample= 48000.00  # Standard sample rate, adjust as needed



    with AudioStream(entrada, saida, buffer_size=buffer, sample_rate=sample,allow_feedback=True) as stream:
        # Create empty pedalboard
        pedalboard = Pedalboard()

        # Add plugins to the pedalboard
        compressor_plugin = Compressor(threshold_db=limiteCompressor, ratio=razao)
        gain_plugin = Gain(gain_db=ganho)
        chorus_plugin = Chorus()
        phaser_plugin = Phaser()
        reverb_plugin = Reverb(room_size=reverb)
        delay_plugin = Delay(delay_seconds=delay_inicial)
        pitch_plugin = PitchShift(semitones=pitch_inicial)
        distortion_plugin=Distortion(drive_db=distorcao)

        pedalboard.append(compressor_plugin)
        pedalboard.append(gain_plugin)
        pedalboard.append(chorus_plugin)
        pedalboard.append(phaser_plugin)
        pedalboard.append(reverb_plugin)
        pedalboard.append(delay_plugin)
        pedalboard.append(pitch_plugin)
        pedalboard.append(distortion_plugin)

        # Set the pedalboard as plugins in the audio stream
        stream.plugins = pedalboard

        # Loop for updating delay time during audio playback
        while True:
            # Update plugin parameters
            compressor_plugin.threshold_db = limiteCompressor
            compressor_plugin.ratio = razao
            gain_plugin.gain_db = ganho
            reverb_plugin.room_size = reverb
            delay_plugin.delay_seconds = delay_inicial
            pitch_plugin.semitones = pitch_inicial

            # Sleep for some time
            print(f"Delay: {delay_inicial}, Pitch: {pitch_inicial}, Compressor: {limiteCompressor}/{razao}, Gain: {ganho}, Reverb: {reverb}")
            time.sleep(1.0)

# Run GUI in a separate thread
threading.Thread(target=janela).start()

# Start audio processing
audio_processing()




#Criar botões para ativar/desativar os efeitos
#criar funcoao de gravação de audio