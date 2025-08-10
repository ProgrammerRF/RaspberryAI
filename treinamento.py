#!/usr/bin/env python
#-*- coding:utf8 -*-
#qpy:3
#qpy:kivy

__Author__ = "Rafael Moraes De Oliveira"
__Date__ = "Segunda-Feira (30/06/2025)"

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.lang import Builder

# Carrega as variaveis do dotenv
from dotenv import load_dotenv

# Carrega o conteudo do arquivo .dotenv para as variaveis de ambiente
load_dotenv() # Esse comando procura o arquivo env e carrega suas variaveis no sistema

# Pega as variaveis usando nomes definidos no .env
API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')

print(API_KEY)

IGU = Builder.load_string("""
<Menu>:
	FloatLayout:
		pos_hint:{'right':1,'top':1}
		size_hint:1,1
		Label:
			id:label_api
			text:''
			pos_hint:{'right':1,'top':1.30}
			size_hint:1,1
			color:1,1,1,1
		Button:
			text:"Mostra URL da API"
			pos_hint:{"right":1,"top":0.60}
			size_hint:1,0.10
			background_color:0,1,0,1
			on_press:root.mostrarurl()
		Label:
			id:label_url
			text:'Teste'
			pos_hint:{'right':1,'top':0.40}
			size_hint:1,0.10
""")

class Menu(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
	
	def on_pre_enter(self):
		chave_oculta = API_KEY[:20] if API_KEY else "Chave não encontrada"
		self.ids['label_api'].text = f'API_Key: \n {chave_oculta}'
		
	def mostrarurl(self):
		self.ids['label_url'].text = API_URL

class MyApp(App):
	def build(self):
		sm = ScreenManager()
		sm.add_widget(Menu(name='menu'))
		return sm
		
if __name__ == '__main__':
	MyApp().run()



