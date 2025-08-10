#!/user/bin/env python3 # O comando env procura a localização do interpretador no dispositivo
#-*-coding:utf-8-*- # Define a codificação UTF-8. opcional no python3
#qpy:3 # Define o uso do python3
#qpy:kivy # Define o uso do kivy para criar interface gráfica

# Versão Raspberry pi

# Metadados
__Author__ = "Rafael Moraes De Oliveira"
__Date__ = "Sábado (08/03/2025)"

#Importa modulos necessários
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
import os
import requests
import socket
from firebase import firebase
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from gtts import gTTS
import falas
import texto
from texto import parar_audio
import time

#Carrega as variaveis do .env
from dotenv import load_dotenv

# Carrega o conteudo do arquivo .dotenv para as variaveis de sistema
load_dotenv() # Procura o comando .env e carrega suas variaveis no sistema

# Sua chave da API Together
API_KEY = os.getenv('API_KEY') 
API_URL = os.getenv('API_URL')

#Integração com o firebase
firebase_app = firebase.FirebaseApplication("https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/",None)

"""
A lista user_name inicia vazia, porém conforme o usuario interage com o aplicativo armazena o nome do usuario que é fornecido após uma consulta no firebase através do email quando o usuario faz login ou se cadastra.

A lista photo_profile tambem inicializa vazia, porém quando o usuario faz login a lista armazena o numero e o tipo da foto que está registrada no firebase.

E a lista user_email tambem inicializa vazia, porém quando o usuario faz login ou se cadastra armazena o email do usuario.

essas listas tem o objetivo de manter os dados persistentes no app sem ter que fazer excessivas consultas no banco de dados.
"""

user_name = []
photo_profile = []
user_email = []
historico_nome = []
historico_conteudo = []

class Menu(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        """Assim que o usuario inicializa o programa a tecla voltar do android recebe a funcionalidade de apresentar um popup antes de encerrar o app perguntando se o usuario quer realmente fechar o programa"""
        Window.bind(on_keyboard=self.tecla_voltar)
        
        texto.fala(3,'Olá. para acessar a plataforma faça Login','frases/resposta_ia.mp3',3)

    def tecla_voltar(self,window,key,*args):
        """ 27 é o numero correspondente a tecla voltar do android. quando o usuario pressiona essa tecla chama a função sair que abre um Popup perguntando se o usuario realmente quer sair.
        """
        if key == 27:
        	self.sair()
        	return True
       
    def sair(self):
        float = FloatLayout()
        titulo = Label(text='Você quer realmente sair?',pos_hint={'right':0.70,'top':1},font_size=(45),size_hint=(0.40,0.30),color=(0,1,0,1))
        bt1 = Button(text='Sim',pos_hint={'right':0.42,'top':0.6},size_hint=(0.40,0.30),background_color=(0,0,0,0))
        bt1.bind(on_press=self.saida)
        
        bt1_image = Image(source='fotos/Botao.png',pos_hint={'right':0.42,'top':0.6},size_hint=(0.40,0.30))
        
        bt2 = Button(text='Não',pos_hint={'right':0.95,'top':0.6},size_hint=(0.40,0.30),background_color=(0,0,0,0))
        bt2.bind(on_press=self.dispensar)
        
        bt2_image = Image(source='fotos/Botao.png',pos_hint={'right':0.95,'top':0.6},size_hint=(0.40,0.30))
        
        float.add_widget(titulo)
        
        float.add_widget(bt1_image)
        float.add_widget(bt1)
        
        float.add_widget(bt2_image)
        float.add_widget(bt2)
        
        self.popup = Popup(title=''.center(90),content=float,pos_hint={'right':1,'top':0.7},size_hint=(1,0.30),background="fotos/fundo_preto.png")
        
        self.popup.open()
        
        parar_audio(3)
        
        texto.fala(3,'Você realmente deseja sair ','frases/resposta_ia.mp3',3)
    
    def formatar_email(self,email,*args):
        return email.replace('.',',').replace('@','_')
    
    def mostrarsenha(self):
        self.ids['senha_user'].password = False
        
    def ocultarsenha(self):
        self.ids['senha_user'].password = True
        
    def verificar_conexao(self):
    	try:
    		socket.create_connection(('www.google.com',443),timeout=5)
    		return True
    	except:
    	   return False
    	   
    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.tecla_voltar)
        self.ids['label_error'].text = ''
        
    def login(self,**kwargs):
        email = self.ids['email_user'].text
        senha = self.ids['senha_user'].text
        
        if self.verificar_conexao():
        	print(':&&&')
        else:
         	print('Errro')
         	self.ids['label_error'].text = 'Você não està conectado a internet'
         	self.ids['label_error'].color = 1,0,0,1
         	falas.fala(3,'Você não está conectado a internet')
        
        if email == '':
        	self.ids['label_error'].text = 'Digite seu E-mail'
        	parar_audio(3)
        	falas.fala(3,'Digite seu E-mail',3)
        elif '@' not in email:
        	self.ids['label_error'].text = 'E-mail deve conter @'
        	parar_audio(3)
        	falas.fala(3,'Seu E-mail deve conter @',3)
        elif '.com' not in email:
        	self.ids['label_error'].text = 'E-mail deve conter .com'
        	parar_audio(3)
        	falas.fala(3,'Seu E-mail deve conter .com',3)
        elif senha == '':
        	self.ids['label_error'].text = 'Digite uma senha'
        	parar_audio(3)
        	falas.fala(3,'Digite sua senha',3)
        elif len(senha) < 6:
        	self.ids['label_error'].text = 'A senha deve conter pelo menos 6 digitos'
        	parar_audio(3)
        	falas.fala(3,'Sua senha deve conter pelo menos 6 digitos',3)
        else:
        	try:
        		email_formatado = self.formatar_email(email)
        		
        		nome_usuario = firebase_app.get(f'/Usuarios/{email_formatado}/nome',None)
        	
	        	validacao_email = firebase_app.get(f'/Usuarios/{email_formatado}/email',None)
	        	
	        	validacao_senha = firebase_app.get(f'/Usuarios/{email_formatado}/senha',None)
	        	
	        	foto_perfil = firebase_app.get(f'/Usuarios/{email_formatado}/foto_perfil',None)
	        	
	        	print(email_formatado)
	        	print(validacao_email)
	        	
	        	if email == validacao_email:
	        		if senha == validacao_senha:
	        			self.ids['label_error'].text = ''
	        			self.ids['email_user'].text = ''
	        			self.ids['senha_user'].text = ''
	        			
	        			user_name.append(nome_usuario)
	        			user_email.append(email_formatado)
	        			photo_profile.append(foto_perfil)
	        			
	        			self.manager.current = 'homepage'
	        			parar_audio(3)
	        			texto.fala(3,f'Olá, {nome_usuario}, Seja bem vindo a ascenção. Como posso te ajudar hoje','frases/resposta_ia.mp3',3)
	        		else:
	        			self.ids['label_error'].text = 'Senha Incorreta'
	        			parar_audio(3)
	        			falas.fala(3,'Sua senha está incorreta',3)
	        	else:
	        	    	self.ids['label_error'].text = 'Email não cadastrado'
	        	    	parar_audio(3)
	        	    	falas.fala(3,'Seu E-mail não está cadastrado',3)
        		
        	except Exception as c:
        		print(c)
        
    def saida(self,*args):
        parar_audio(3)
        texto.fala(3,'Vá em paz. Volte sempre.','frases/resposta_ia.mp3',3)
        time.sleep(3)
        exit()
        
    def dispensar(self,*args):
       parar_audio(3)
       falas.fala(3,'Fico feliz por ter decidido ficar',3)
       self.popup.dismiss()
         	
        
class LabelButton(ButtonBehavior,Label):
        def __init__(self,**kwargs):
        	super().__init__(**kwargs)
        
class Cadastro(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
		Window.bind(on_keyboard=self.tecla_voltar)
		
		parar_audio(3)
		texto.fala(3,'Para se cadastrar na plataforma, preencha o formulário','frases/resposta_ia.mp3',3)
	
	def tecla_voltar(self,window,key,*args):
		if key == 27:
			self.manager.current = 'menu'
			return True
	
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.tecla_voltar)
			
		
	def formatar_email(self,email,*args):
		return email.replace('.',',').replace('@','_')
		
	def mostrarsenha1(self):
		self.ids['senha1_input'].password = False
	
	def mostrarsenha2(self):
		self.ids['senha2_input'].password = False
	
	def ocultarsenha1(self):
		self.ids['senha1_input'].password = True
	
	def ocultarsenha2(self):
		self.ids['senha2_input'].password = True
		
	def verificar_conexao(self,*args):
		try:
			socket.create_connection(('www.google.com',443),timeout=5)
			return True
		except:
			return False
			
	def on_pre_leave(self):
		self.ids['label_error'].text = ''
		
	def enviar(self):
		email = self.ids['email_input'].text
		nome = self.ids['nome_input'].text
		senha1 = self.ids['senha1_input'].text
		senha2 = self.ids['senha2_input'].text
		
		if self.verificar_conexao():
			pass
		else:
			self.ids['label_error'].text = 'Você não está conectado a internet'
			self.ids['label_error'].color = 1,0,0,1
			
		
		print("""

{}

{}

{}

		""".format(email,senha1,senha2))
		
		if email == '':
			self.ids['label_error'].text = 'Digite seu E-mail'
			self.ids['label_error'].color = 1,0,0,1
		elif '@' not in email:
			self.ids['label_error'].text = 'E-mail deve conter @'
			self.ids['label_error'].color = 1,0,0,1
		elif '.com' not in email:
			self.ids['label_error'].text = 'E-mail deve conter .com'
			self.ids['label_error'].color = 1,0,0,1
		elif nome == '':
			self.ids['label_error'].text = 'Digite seu nome'
			self.ids['label_error'].color = 1,0,0,1
		elif senha1 == '':
			self.ids['label_error'].text = 'Digite uma senha'
			self.ids['label_error'].color = 1,0,0,1
		elif len(senha1) < 6:
			self.ids['label_error'].text = 'A senha deve conter pelo menos 6 digitos'
			self.ids['label_error'].color = 1,0,0,1
		elif senha2 == '':
			self.ids['label_error'].text = 'Digite a senha novamente'
			self.ids['label_error'].color = 1,0,0,1
		elif senha1 != senha2:
			self.ids['label_error'].text = 'As senhas não conferem'
			self.ids['label_error'].color = 1,0,0,1
		else:
			self.ids['label_error'].text = ''
			self.ids['nome_input'].text = ''
			self.ids['email_input'].text = ''
			self.ids['senha1_input'].text = ''
			self.ids['senha2_input'].text = ''
			
			try:
				email_formatado = self.formatar_email(email)
				
				validacao = firebase_app.get(f'/Usuarios/{email_formatado}',None)
				
				if validacao:
					self.ids['label_error'].color = 1,0,0,1
					self.ids['label_error'].text = 'Email já cadastrado'
				else:
					dados_cliente = {
					'email':email,
					'nome':nome,
					'senha':senha1,
					'foto_perfil':'foto1.png'
					}
					user_email.append(email_formatado)
					user_name.append(nome)
					photo_profile.append('foto1.png')
					resultado = firebase_app.put('/Usuarios',email_formatado,dados_cliente)
					
					parar_audio(3)
					texto.fala(3,f'Olá, {nome}. Seja bem vindo a ascenção. Como posso te ajudar hoje ','frases/resposta_ia.mp3',3)
					
					self.manager.current = 'homepage'
			except:
				self.ids['label_error'].text = 'Você não está conectado a internet'
				self.ids['label_error'].color = 1,0,0,1
				pass
	   
class HomePage(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
	    Window.bind(on_keyboard=self.tecla_voltar)
	    
	    nome_do_usuario = str(user_name)
	    self.ids['user_name'].text = nome_do_usuario.replace('[','').replace(']','').replace("'",'')
	    #self.ids['resposta_ia'].text = 'Como posso te ajudar ? ' #'teste '*250
	    
	    if len(historico_nome) == 0:
	    	resposta = self.ids['resposta_ia'].text
	    	print("BET")
	    else:
	    	try:
	    		self.ids['resposta_ia'].text = str(historico_conteudo[0])
	    		texto.fala(3,historico_conteudo[0],'frases/resposta_ia.mp3',3)
	    	except Exception as erro:
	    		print(erro)
	    		
	    	resposta = self.ids['resposta_ia'].text
	    	print()
	    	print('what are you selling?')
	    	print(resposta)
	    	print()
	    	
	    	separar = resposta.split()
	    	
	    	if len(separar) < 100:
	    		self.ids['resposta_ia'].size_hint = (1,3.90)
	    		
	    	elif len(separar) == 100:
	    	 	self.ids['resposta_ia'].size_hint = (1,3.90)
	    	 	
	    	elif len(separar) < 250 and len(separar) > 100:
	    	 	self.ids['resposta_ia'].size_hint = (1,3.90)
	    	 	
	    	elif len(separar) == 250:
	    	 	self.ids['resposta_ia'].size_hint = (1,3.90)
	    	 	
	    	elif len(separar) < 500 and len(separar) > 250:
	    	 	self.ids['resposta_ia'].size_hint = (1,5.10)
	    	
	    	elif len(separar) == 500:
	    	 	self.ids['resposta_ia'].size_hint = (1,5.10)
	    	 	
	    	elif len(separar) < 750 and len(separar) > 500:
	    	 	self.ids['resposta_ia'].size_hint = (1,5.10)
	    	
	    	elif len(separar) == 750:
	    		self.ids['resposta_ia'].size_hint = (1,5.10)
	    		
	    	elif len(separar) < 1000 and len(separar) > 750:
	    	    self.ids['resposta_ia'].size_hint = (1,5.10)
	    	    
	    	elif len(separar) == 1000:
	    	 	self.ids['resposta_ia'].size_hint = (1,5.10)
	    	 	
	    	elif len(separar) < 1250 and len(separar) > 1000:
	    	 	self.ids['resposta_ia'].size_hint = (1,5.20)
	    	
	    	elif len(separar) == 1250:
	    	 	self.ids['resposta_ia'].size_hint = (1,5.20)
	    	 	
	    	elif len(separar) < 1500 and len(separar) > 1250:
	    	 	self.ids['resposta_ia'].size_hint = (1,6.20)
	    	 	
	    	elif len(separar) == 1500:
	    	 	self.ids['resposta_ia'].size_hint = (1,6.20)
	    	 	
	    	elif len(separar) < 1750 and len(separar) > 1500:
	    	 	self.ids['resposta_ia'].size_hint = (1,7.10)
	    	
	    	elif len(separar) == 1750:
	    	 	self.ids['resposta_ia'].size_hint = (1,7.10)
	    	 	
	    	elif len(separar) < 2000 and len(separar) > 1750:
	    	 	self.ids['resposta_ia'].size_hint = (1,8.20)
	    	 	
	    	elif len(separar) == 2000:
	    	 	self.ids['resposta_ia'].size_hint = (1,8.20)
	    	 	
	    	elif len(separar) < 2232 and len(separar) > 2000:
	    	 	self.ids['resposta_ia'].size_hint = (1,9)
	    	 	
	    	elif len(separar) == 2232:
	    		self.ids['resposta_ia'].size_hint = (1,9)
	    	
	    	linhas = []
	    	for i in range(0, len(separar), 6):
		    	linha = ' '.join(separar[i:i+6])
		    	linhas.append(linha)
		    	self.ids['resposta_ia'].text = '\n'.join(linhas).replace('.','\n\n').strip()
		    

	    
	    try:
		    email = user_email[0]
		  	    
		    email_formatado = email.replace("@",'_').replace(".",',').replace(']','').replace('[','').replace("'",'')
		    
		    print('_'*30)
		    print(email_formatado)
		    
		    foto = firebase_app.get(f'/Usuarios/{email_formatado}/foto_perfil',None)
		    nome = firebase_app.get(f'/Usuarios/{email_formatado}/nome',None)
		    
		    print("WHERE IS THE ERROR")
		    print(nome)
		    
		    self.ids['user_name'].text = nome or ''
		    
		    print(email)
		    print()
		    print(foto)
		    
		    foto_perfil = str(photo_profile)
		    foto_perfil_formatada = foto_perfil.replace('[','').replace("]",'').replace("'",'')
		    
		    print(os.getcwd())
		    
		    self.ids['foto_usuario'].source = f'foto_usuario/{foto}'
	    	
	    except Exception as erro:
	    	print(erro)
	    	
	    	self.ids['label_error'].text = 'Você não está conectado a internet'
	    	self.ids['label_error'].color = 1,0,0,1
	    	
	def tecla_voltar(self,window,key,*args):
		if key == 27:
			self.sair()
			return True

	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.tecla_voltar)
		self.ids['label_error'].text = ''
		
	def sair(self):
	       float = FloatLayout()
	       titulo = Label(text='Você quer realmente sair?',pos_hint={'right':0.70,'top':1},font_size=(45),size_hint=(0.40,0.30),color=(0,1,0,1))
	       bt1 = Button(text='Sim',pos_hint={'right':0.42,'top':0.6},size_hint=(0.40,0.30),background_color=(0,0,0,0))
	       bt1.bind(on_press=self.saida)
	       
	       parar_audio(3)
	       texto.fala(3,'Você realmente deseja sair, ','frases/resposta_ia.mp3',3)
	       
	       bt1_image = Image(source='fotos/Botao.png',pos_hint={'right':0.42,'top':0.6},size_hint=(0.40,0.30))
	       
	       bt2 = Button(text='Não',pos_hint={'right':0.95,'top':0.6},size_hint=(0.40,0.30),background_color=(0,0,0,0))
	       bt2.bind(on_press=self.dispensar)
	       
	       bt2_image = Image(source='fotos/Botao.png',pos_hint={'right':0.95,'top':0.6},size_hint=(0.40,0.30))
	       
	       float.add_widget(titulo)
	       float.add_widget(bt1_image)
	       float.add_widget(bt1)
	       float.add_widget(bt2_image)
	       float.add_widget(bt2)
	       
	       self.popup = Popup(title=''.center(90),content=float,pos_hint={'right':1,'top':0.7},size_hint=(1,0.30),background="fotos/fundo_preto.png")
	       
	       self.popup.open()
	       
	       
	def saida(self,*args):
		self.popup.dismiss()
		user_email.clear()
		self.ids['resposta_ia'].text = 'Como posso ajudar você?'
		self.ids['resposta_ia'].size_hint = (1,0.40)
		self.manager.current = 'menu'
		
	def dispensar(self,*args):
		falas.fala(3,'Como posso ajudar',3)
		self.popup.dismiss() 
		
	def formatar_pergunta(self,pergunta,*args):
		return pergunta.replace('.','').replace('@','').replace('#','').replace('[','').replace(']','').replace('/','').replace('$','').replace('?','')
		
	
	def send_question(self, *args):
		pergunta = self.ids['entrada_usuario'].text
		
		if pergunta == '':
			pergunta = 'Oque posso perguntar ?'
		
		headers = { "Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json",}
		
		data = {"model": "Qwen/Qwen2.5-7B-Instruct-Turbo","messages": [{"role": "user", "content": pergunta}]}
		
		response = requests.post(API_URL, headers=headers, json=data)
		
		self.ids['entrada_usuario'].text = ''
		
		if response.status_code == 200:
		    resposta = response.json()['choices'][0]['message']['content']
		    self.ids['resposta_ia'].text = "Resposta: " + resposta
		    
		    resposta = self.ids['resposta_ia'].text
		    
		    resposta_voz = resposta.replace('?','')
		    
		    parar_audio(3)
		    texto.fala(3,resposta_voz,'frases/resposta_ia.mp3',3)
		    
		    pergunta_formatada = self.formatar_pergunta(pergunta)
		    
		    email = str(user_email[0])
		    
		    email_formatado = email.replace('.',',').replace('@','_')
		    
		    info = {
		    f'{pergunta_formatada}': f"{resposta}"
		    }
		    
		    historico_conversa = firebase_app.patch(f'/Usuarios/{email_formatado}/historico',info)
	
		    separar = resposta.split()
		    
		    print(len(separar))
		    
		    if len(separar) < 100:
		    	self.ids['resposta_ia'].size_hint = (1,3.90)
		    	
		    elif len(separar) == 100:
		    	self.ids['resposta_ia'].size_hint = (1,3.90)
		    
		    elif len(separar) < 250 and len(separar) > 100:
		    	self.ids['resposta_ia'].size_hint = (1,3.90)
		    
		    elif len(separar) == 250:
		    	self.ids['resposta_ia'].size_hint = (1,3.90)
		    	
		    elif len(separar) < 500 and len(separar) > 250:
		    	self.ids['resposta_ia'].size_hint = (1,5.10)
		    
		    elif len(separar) == 500:
		    	self.ids['resposta_ia'].size_hint = (1,5.10)
		    	
		    elif len(separar) < 750 and len(separar) > 500:
		    	self.ids['resposta_ia'].size_hint = (1,5.10)	    		
		    elif len(separar) == 750:
		    	self.ids['resposta_ia'].size_hint = (1,5.10)
		    	
		    elif len(separar) < 1000 and len(separar) > 750:
		    	self.ids['resposta_ia'].size_hint = (1,5.10)
		    	
		    elif len(separar) == 1000:
		    	self.ids['resposta_ia'].size_hint = (1,5.10)
		    	
		    elif len(separar) < 1250 and len(separar) > 1000:
		    	self.ids['resposta_ia'].size_hint = (1,5.20)
		    	
		    elif len(separar) == 1250:
		    	self.ids['resposta_ia'].size_hint = (1,5.20)
		    	
		    elif len(separar) < 1500 and len(separar) > 1250:
		    	self.ids['resposta_ia'].size_hint = (1,6.20)
		    	
		    elif len(separar) == 1500:
		    	self.ids['resposta_ia'].size_hint = (1,6.20)
		    
		    elif len(separar) < 1750 and len(separar) > 1500:
		    	self.ids['resposta_ia'].size_hint = (1,7.10)
		    	
		    elif len(separar) == 1750:
		    	self.ids['resposta_ia'].size_hint = (1,7.10)
		    	
		    elif len(separar) < 2000 and len(separar) > 1750:
		    	self.ids['resposta_ia'].size_hint = (1,8.20)
		    	
		    elif len(separar) == 2000:
		    	self.ids['resposta_ia'].size_hint = (1,8.20)
		    	
		    elif len(separar) < 2232 and len(separar) > 2000:
		    	self.ids['resposta_ia'].size_hint = (1,9)
		    	
		    elif len(separar) == 2232:
		    	self.ids['resposta_ia'].size_hint = (1,9)
	
	
	
	
		    
		    print(len(separar))
		    # 500
		    
		    # Organizando em linhas de 8 palavras
		    linhas = []
		    for i in range(0, len(separar), 6):
		        linha = ' '.join(separar[i:i+6])
		        linhas.append(linha)
		    
		    self.ids['resposta_ia'].text = '\n'.join(linhas).replace('.','\n\n').strip()
		else:
			self.ids['resposta_ia'].text = "Erro: " + str(response.json())
		
			
		
		
		
	def alterar_posicao(self):
		if self.ids['entrada_usuario'].focus == True:
			self.ids['entrada_usuario'].pos_hint = {'right':1,'top':0.40}
		else:
			self.ids['entrada_usuario'].pos_hint = {'right':1,'top':0.18}
			
class Configuracoes(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
		parar_audio(3)
		texto.fala(3,'Tela de configurações','frases/resposta_ia.mp3',3)
		Window.bind(on_keyboard=self.tecla_voltar)
	
	def tecla_voltar(self,window,key,*args):
		if key == 27:
			self.manager.current = 'homepage'
			return True
	
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.tecla_voltar)
		
class Mudar_Foto(Screen,Image,FloatLayout):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
class ImageButton(ButtonBehavior,Image):
	pass

class Mudar_Foto(Screen):
    def on_pre_enter(self):
        Window.bind(on_keyboard=self.tecla_voltar)
        
        parar_audio(3)
        texto.fala(3,'Você deseja mudar sua foto de perfil. Se sim, selecione uma das fotos disponíveis','frases/resposta_ia.mp3',3)
        
        scroll = self.ids['teste']

        # Grid para mostrar 3 imagens por linha
        grid = GridLayout(cols=3, spacing=10, padding=10, size_hint_y=None)#10
        grid.bind(minimum_height=grid.setter('height'))
        
        print(os.getcwd())

        os.chdir(os.getcwd() + "/foto_usuario")
        fotos = sorted(os.listdir())

        for foto in fotos:
            if foto.endswith('.png') or foto.endswith('.jpg'):
                img = ImageButton(source=os.path.join(os.getcwd(), foto),
                            size_hint_y=None,
                            height=200, 
                            allow_stretch=True,
                            keep_ratio=True)
                img.bind(on_press=lambda instance, foto=foto:self.mudar_foto_perfil(foto))
                grid.add_widget(img)
                

        scroll.clear_widgets()
        scroll.add_widget(grid)
        
    def mudar_foto_perfil(self,foto,**args):
    	try:
    		info = f'{{"foto_perfil": "{foto}"}}'
	    	print(info)
	    	nome_usuario = str(user_email)
	    	nome_usuario_formatado = nome_usuario.replace('[','').replace(']','').replace("'",'')
	    	print(nome_usuario_formatado)
	    	requisicao = requests.patch(f"https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/Usuarios/{nome_usuario_formatado}.json",data=info)
	    	print(requisicao.status_code)
	    	print(requisicao.text)
	    	os.chdir(os.getcwd() + '/..')
	    	self.manager.current = 'homepage'
	    	
	    	parar_audio(3)
	    	texto.fala(3,'Foto alterada com sucesso','frases/resposta_ia.mp3',3)
    	except:
    		self.ids["label_error"].text = 'Você não está conectado a internet'
    		self.ids['label_error'].color = 1,0,0,1
    		
    def on_pre_leave(self):
    	Window.unbind(on_keyboard=self.tecla_voltar)
    	self.ids['label_error'].text = ''
    
    def tecla_voltar(self,window,key,*args):
    	if key == 27:
    		self.manager.current = 'configuracoes'
    		return True
    	
class Mudar_Nome(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
		Window.bind(on_keyboard=self.tecla_voltar)
		parar_audio(3)
		texto.fala(3,'Você deseja alterar seu nome. Se sim, digite seu novo nome e pressione validar','frases/resposta_ia.mp3',3)
		
	def mudar_nome_perfil(self,**args):
	    self.nome = self.ids['campo_alterar_nome'].text
	    try:
    		info = f'{{"nome": "{self.nome}"}}'
	    	print(info)
	    	nome_usuario = str(user_email)
	    	nome_usuario_formatado = nome_usuario.replace('[','').replace(']','').replace("'",'')
	    	print(nome_usuario_formatado)
	    	requisicao = requests.patch(f"https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/Usuarios/{nome_usuario_formatado}.json",data=info)
	    	print(requisicao.status_code)
	    	print(requisicao.text)
	    	parar_audio(3)
	    	texto.fala(3,'Nome alterado com sucesso','resposta_ia.mp3',3)
	    	self.manager.current = 'homepage'
	    except Exception as erro:
	    	print(erro)
    		self.ids["label_error"].text = 'Você não está conectado a internet'
    		self.ids['label_error'].color = 1,0,0,1
    
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.tecla_voltar)
		self.ids['label_error'].text = ''
		self.ids['campo_alterar_nome'].text = ''
	
	def tecla_voltar(self,window,key,*args):
		if key == 27:
			self.manager.current = "configuracoes"
			return True

class Mudar_Senha(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
		Window.bind(on_keyboard=self.tecla_voltar)
		parar_audio(3)
		texto.fala(3,'Se você deseja alterar sua senha preencha os campos do formulário','frases/resposta_ia.mp3',3)
		
	def tecla_voltar(self,window,key,*args):
		if key == 27:
			self.manager.current = 'configuracoes'
			return True
	
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.tecla_voltar)
		
	def formatar_email(self,email,*args):
		email = str(email)
		return email.replace('.',',').replace('@','_')
		
	def mostrarsenha1(self):
		self.ids['senha1_input'].password = False
	
	def mostrarsenha2(self):
		self.ids['senha2_input'].password = False
		
	def mostrarsenha3(self):
		self.ids['senha3_input'].password = False
	
	def ocultarsenha1(self):
		self.ids['senha1_input'].password = True
	
	def ocultarsenha2(self):
		self.ids['senha2_input'].password = True
		
	def ocultarsenha3(self):
		self.ids['senha3_input'].password = True
		
	def mudar_senha(self):
		email_formatado = str(user_email[0])
		
		validacao_senha = firebase_app.get(f'/Usuarios/{email_formatado}/senha',None)
		
		if self.ids['senha1_input'].text == '':
			self.ids['label_error'].text = 'Digite sua senha antiga'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			texto.fala(3,'Digite sua senha antiga','frases/resposta_ia.mp3',3)
			
		elif len(self.ids['senha1_input'].text) < 6:
			self.ids['label_error'].text = 'Sua senha antiga deve ter pelo menos 6 caracteres'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			texto.fala(3,'Sua senha deve conter pelo menos 6 caracteres','frases/resposta_ia.mp3',3)
			
		elif self.ids['senha2_input'].text == '':
			self.ids['label_error'].text = 'Digite sua nova senha'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			texto.fala(3,'Digite sua nova senha','frases/resposta_ia.mp3',3)
			
		elif len(self.ids['senha2_input'].text) < 6:
			self.ids['label_error'].text = 'Sua nova senha deve ter pelo menos 6 caracteres'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			texto.fala(3,'Sua nova senha deve conter pelo menos 6 caracteres','frases/resposta_ia.mp3',3)
			
		elif self.ids['senha3_input'].text == '':
			self.ids['label_error'].text = 'Digite sua nova senha novamente'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			texto.fala(3,'Digite sua nova senha novamente','frases/resposta_ia.mp3',3)
			
		elif len(self.ids['senha3_input'].text) < 6:
			self.ids['label_error'].text = 'Sua nova senha deve ter pelo menos 6 caracteres'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			texto.fala(3,'Sua senha deve ter pelo menos 6 caracteres','frases/resposta_ia.mp3',3)
			
		elif self.ids['senha2_input'].text != self.ids['senha3_input'].text:
			self.ids['label_error'].text = 'As senhas não conferem'
			parar_audio(3)
			texto.fala(3,'As senhas não conferem','frases/resposta_ia.mp3',3)
		
		elif self.ids['senha1_input'].text == self.ids['senha2_input'].text and self.ids['senha3_input'].text:
			self.ids['label_error'].text = 'Sua nova senha deve ser diferente da antiga'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			texto.fala(3,'Sua nova senha deve ser diferente da antiga','frases/resposta_ia.mp3',3)
			
		elif self.ids['senha1_input'].text != validacao_senha:
			self.ids['label_error'].text = 'Senha antiga está incorreta'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			texto.fala(3,'Sua senha antiga está incorreta','frases/resposta_ia.mp3',3)
			
		else:
		    self.senha = self.ids['senha2_input'].text
		    try:
	    		info = f'{{"senha": "{self.senha}"}}'
		    	print(info)
		    	nome_usuario = str(user_email)
		    	nome_usuario_formatado = nome_usuario.replace('[','').replace(']','').replace("'",'')
		    	print(nome_usuario_formatado)
		    	requisicao = requests.patch(f"https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/Usuarios/{nome_usuario_formatado}.json",data=info)
		    	print(requisicao.status_code)
		    	print(requisicao.text)
		    	print('Acerttoy')
		    	self.ids['senha1_input'].text = ''
		    	self.ids['senha2_input'].text = ''
		    	self.ids['senha3_input'].text = ''
		    	self.ids['label_error'].text = ''
		    	parar_audio(3)
		    	texto.fala(3,'Senha alterada com sucesso','frases/resposta_ia.mp3',3)
		    	self.manager.current = 'homepage'
		    except Exception as erro:
		    	print(erro)
	    		self.ids["label_error"].text = 'Você não está conectado a internet'
	    		self.ids['label_error'].color = 1,0,0,1
    		
	def on_pre_leave(self):
		self.ids['label_error'].text = ''
		
class Mudar_Email(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
		Window.bind(on_keyboard=self.tecla_voltar)
		parar_audio(3)
		texto.fala(3,'Se você deseja alterar o endereço de E-mail preencha os campos do formulário','frases/resposta_ia.mp3',3)
		
	def tecla_voltar(self,window,key,*args):
		if key == 27:
			self.manager.current = 'configuracoes'
			return True
			
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.tecla_voltar)
		
	def mudar_email(self):
		email = self.ids['campo_alterar_email'].text
		email_formatado = self.formatar_email(email)
		validacao_email = firebase_app.get(f'/Usuarios/{email_formatado}/email',None)
		
		if email == '':
			self.ids['label_error'].text = 'Digite o novo E-mail'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			texto.fala(3,'Digite seu novo E-mail','frases/resposta_ia.mp3',3)
			
		elif '@' not in email:
			self.ids['label_error'].text = 'O email deve conter @'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			texto.fala(3,'Seu E-mail deve conter @','frases/resposta_ia.mp3',3)
			
		elif '.com' not in email:
			self.ids['label_error'].text = 'O email deve conter .com'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			texto.fala(3,'Seu E-mail deve conter .com','frases/resposta_ia.mp3',3)
		
		elif email == validacao_email:
			self.ids['label_error'].text = 'O novo E-mail deve ser diferente do antigo'
			parar_audio(3)
			texto.fala(3,'Seu novo E-mail deve ser diferente do antigo','frases/resposta_ia.mp3',3)
			
		else:
			self.email = self.ids['campo_alterar_email'].text
			try:
				email = user_email[0]
				email_formatado = self.formatar_email(email)
				
				print(email_formatado)
				
				email = firebase_app.get(f'/Usuarios/{email_formatado}/email',None)
				
				foto_perfil = firebase_app.get(f'/Usuarios/{email_formatado}/foto_perfil',None)
				
				try:
					self.historico = firebase_app.get(f'/Usuarios/{email_formatado}/historico',None)
				except:
					pass
				
				nome = firebase_app.get(f'/Usuarios/{email_formatado}/nome',None)
				
				senha = firebase_app.get(f'/Usuarios/{email_formatado}/senha',None)
				
				print("OVER HERE, STRANGER")
				print(email)
				print(foto_perfil)
				print(nome)
				print(senha)
				
				url = f"https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/Usuarios/{email_formatado}.json"
				
				res = requests.delete(url)
				
				novo_email = self.formatar_email(self.ids['campo_alterar_email'].text)
				
				dados_cliente = {
				'email': self.ids['campo_alterar_email'].text,
				'foto_perfil': foto_perfil,
				'historico':self.historico,
				'nome': nome,
				'senha': senha
				}
				
				resultado = firebase_app.put('/Usuarios',novo_email,dados_cliente)
				
				user_email.clear()
				
				user_email.append(novo_email)
				
				self.ids['label_error'].text = ''
				self.ids['campo_alterar_email'].text = ''
				
				parar_audio(3)
				texto.fala(3,'E-mail alterado com sucesso','frases/resposta_ia.mp3',3)
				
				self.manager.current = 'homepage'
				
			except Exception as erro:
				print(erro)
				self.ids["label_error"].text = 'Você não está conectado a internet'
				self.ids['label_error'].color = 1,0,0,1
		

	def formatar_email(self,email,*args):
		email = str(email)
		return email.replace('.',',').replace('@','_')

class Historico_Conversas(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
		Window.bind(on_keyboard=self.voltar)
		parar_audio(3)
		texto.fala(3,'Histórico de conversas. Nessa tela você pode selecionar uma das conversas anteriores para ser carregada na HomePage ou deletar uma conversa anterior preesionando o botão vermelho','frases/resposta_ia.mp3',3)
		
		email = str(user_email[0])
		
		email_formatado = email.replace('@','_').replace('.',',')
		
		try:
			self.historico = firebase_app.get(f'/Usuarios/{email_formatado}/historico',None)
			
			for palavra in self.historico.keys():
				if self.historico.keys == None:
					pass
				else:
					grid = FloatLayout(size_hint_y=None,height=140)
					self.button = Button(text=str(palavra),pos_hint={'center_x':0.5,'center_y':0.2},size_hint=(0.5,None),size_hint_y=None,background_color=(0,0,0,0),height=100)
					self.button.bind(on_press=self.conversa_arquivada)
					self.botao_excluir = Button(text=str(palavra),color=(0,0,0,0),pos_hint={'center_x':0.9,'center_y':0.2},size_hint=(0.1,None),size_hint_y=None,height=80,background_color=(0,0,0,0))
					self.botao_excluir.bind(on_press=self.excluir_conversa_arquivada)
					self.foto_excluir = Image(pos_hint={'center_x':0.9,'center_y':0.2},size_hint=(0.1,None),size_hint_y=None,height=80,source='fotos/excluir2.png')
					grid.add_widget(self.botao_excluir)
					grid.add_widget(self.button)
					grid.add_widget(self.foto_excluir)
					self.ids['float'].add_widget(grid)
		except Exception as erro:
			print('Erro')
			
	def on_leave(self):
		self.ids['float'].clear_widgets()
		
	def voltar(self,window,key,*args):
		print('*'*30)
		print(key)
		print('*'*30)
		if key == 27:
			self.manager.current = 'configuracoes'
			return True
			
	def excluir_conversa_arquivada(self,instance,*args):
			historico_nome.clear()
			historico_conteudo.clear()
			historico_nome.append(instance.text)
			
			print()
			print('EXCLUIR CONVERSA')
			print(instance.text)
			print()
			
			email = str(user_email[0])
			
			email_formatado = email.replace('.',',').replace('@','_')
			
			print()
			print(historico_nome[0])
			print()
			
			url = f"https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/Usuarios/{email_formatado}/historico/{historico_nome[0]}.json" 
			requests.delete(url)
			
			parar_audio(3)
			texto.fala(3,'Conversa excluida com sucesso','frases/resposta_ia.mp3',3)
			
			self.manager.current = 'homepage'
			
			#teste = firebase_app.get(f'/Usuarios/{email_formatado}/historico/{historico_nome[0]}',None)
			
			#print(teste)
			
	def conversa_arquivada(self,instance,*args):
		try:
			historico_nome.clear()
			historico_conteudo.clear()
			historico_nome.append(instance.text)
			
			print("""
			OVER HERE STRANGER
			{}
			""".format(historico_nome))
			
			email = str(user_email[0])
			email_formatado = email.replace('@','_').replace('.',',')
			
			pergunta = instance.text
			self.historico_conteudo = firebase_app.get(f'/Usuarios/{email_formatado}/historico/{historico_nome[0]}',None)
			historico_conteudo.append(self.historico_conteudo)
			
			print(f"""
			!!!!!
			{self.historico_conteudo}
			!!!!!
			""")
		except Exception as erro:
			print(erro)
		
		self.manager.current = 'homepage'

	def formatar_pergunta(self,pergunta,*args):
		return pergunta.replace('.',',').replace('@','_').replace('#','').replace('[','').replace(']','').replace('/','').replace('$','').replace(' ','')
		
class Configuracoes_Raspberry(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
		Window.bind(on_keyboard=self.mudar_tecla)
		parar_audio(3)
		texto.fala(3,'Configurações do raspberry PI','frases/resposta_ia.mp3',3)
		
	def mudar_tecla(self,window,key,*args):
		if key == 27:
			self.manager.current = 'configuracoes'
			return True
			
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.mudar_tecla)
		
Gui = Builder.load_file('main.kv')

class Inteligencia_Artificial(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Menu(name='menu'))
        sm.add_widget(Cadastro(name='cadastro'))
        sm.add_widget(HomePage(name='homepage'))
        sm.add_widget(Configuracoes(name='configuracoes'))
        sm.add_widget(Mudar_Foto(name='mudar_foto'))
        sm.add_widget(Mudar_Nome(name='mudar_nome'))
        sm.add_widget(Mudar_Senha(name='mudar_senha'))
        sm.add_widget(Mudar_Email(name='mudar_email'))
        sm.add_widget(Historico_Conversas(name='historico_conversas'))
        sm.add_widget(Configuracoes_Raspberry(name='configuracoes_raspberry'))
        return sm

if __name__ == '__main__':
	Inteligencia_Artificial().run()





