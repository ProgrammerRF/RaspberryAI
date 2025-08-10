import pyrebase

config = {
  "apiKey": "AIzaSyAAEOHK7Iuq54tqRosWnoZgSYXvPYv0p6M",
  "authDomain": "inteligencia-artificial-37d91.firebaseapp.com",
  "databaseURL": "https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/",
  "storageBucket": "inteligencia-artificial-37d91.appspot.com"
}


firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Escrevendo
db.child("Usuarios").child("rafael").set({"nome": "Rafael", "email": "rafael@email.com"})

# Lendo
dados = db.child("Usuarios").child("rafael").get()
print(dados.val())  
# {'nome': 'Rafael', 'email': 'rafael@email.com'}

