from kivy.core.audio import SoundLoader
import os
from gtts import gTTS
import time
from som import som

def fala(self,msg,instance):
	global som
	try:
		if som and som.state == 'play':
			som.stop()
			
		texto = msg
		caminho = f'frases/{msg}.mp3'
		fala = gTTS(text=texto,lang='pt-br')
		
		fala.save(caminho)
		
		som = SoundLoader.load(caminho)
		
		print(som)
		
		if som:
			som.play()
	except Exception as erro:
		print(erro)
		
