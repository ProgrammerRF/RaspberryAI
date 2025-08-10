from kivy.core.audio import SoundLoader
from gtts import gTTS
import os
import time

som = None

def fala(self,texto,caminho,instance):
	global som
	try:
		if som and som.state == 'play':
			som.stop()
			
		frase = texto
		salvar_arquivo = caminho
		fala = gTTS(text=frase,lang='pt-br')
		fala.save(caminho)
		
		som = SoundLoader.load(caminho)
		
		if som.state != 'play':
			som.play()
		
	except Exception as erro:
		print('Qual é o erro? ', erro)
		pass
		
def parar_audio(self):
		global som
		if som and som.state == 'play':
			som.stop()
		
		
