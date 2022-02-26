from ctypes import util
from weakref import ref
from flask import Flask, jsonify,request
from decouple import config
import firebase_admin
import requests
from flask_cors import CORS
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
from firebase_admin import auth ,exceptions

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

#module key file
# Fetch the service account key JSON file contents
key_json=config('KEY')

url = config('URL_CREDENTIALS_FIREBASE')
headers = {
  'X-Master-Key': key_json
}
req = requests.get(url, json=None, headers=headers)
data=req.json()["record"]

cred = credentials.Certificate(data)
url=config('URL_FIREBASE')

# #firebase = firebase.FirebaseApplication('https://'+url, None)

# # Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': url,
})

# As an admin, the app has access to read and write all data, regradless of Security Rules

@app.route('/')
def index():
    alojamientos=db.reference("/alojamientos").order_by_key().limit_to_last(4).get()
    return jsonify(alojamientos)

#Loguear

@app.route('/login',methods=['POST'])
def login():   
  data=request.json
  
  email=data['email']
  password=data['password']

  user=auth.get_user_by_email(email)
  if(user):
    usuario=db.reference("/usuarios").child(user.uid).get()
    token=str(auth.create_custom_token(user.uid,usuario)).split("'")[1]
    
    if(usuario["password"]== data["password"]):
      return jsonify({"token":token})
    else:
      return jsonify({"Message":"Contraseña Erronea intente nuevamente"})
  else:
    return jsonify({"Message":"Usuario No esta registrado"})

# Tabla Usuarios

@app.route('/registro',methods=['POST'])
def registroUsuarios():
  reference=db.reference("/usuarios")
  data=request.json
  usuarios={
  "nombre":data["nombre"],
  "typeDoc":data["typeDoc"],
  "numDoc":data["numDoc"],
  "userName":data["userName"],
  "password":data["password"]
  }

  if(validarExisteUsuario(reference,usuarios)):
    return jsonify({"Mensaje":"Ya existe un usuario creado con ese nit"})
  else:
    create=reference.push(usuarios)
    return jsonify({"Mensaje":"usuario Creado satisfactoriamente","UID":create.key})


#listado de usuarios con credenciales
@app.route('/listadoUsuarios')
def list_usuarios():
  page=auth.list_users()
  data={}
  for user in page.users:
    data={"user": user.uid}
    user
  return (data)

# Obtener todos los  usuarios
@app.route('/usuarios')
def listaUsuarios():
  database = db.reference("/usuarios").get()
  return jsonify(database)

# Obtener usuario en especifico
@app.route('/usuarios<string:uid>')
def listaUsuariosUid(uid):
  database = db.reference("/usuarios").child(uid).get()
  return jsonify(database)


#colocar escuchadores  db.reference('/').listen()
@app.route('/actualizarUsuario',methods=['PUT'])      
def validarActualizarUsuario():
    database = db.reference("/usuarios")
    for key, value in database.items():
      if(value["numDoc"] == data["numDoc"]):
        database.child(key).update(data)
        return True
      else:
        return False   
        
@app.route('/eliminarUsuario',methods=['PUT'])      
def eliminarUsuarios():
    database = db.reference("/usuarios")
    for key, value in database.items():
      if(value["numDoc"] == data["numDoc"]):
        database.child(key).update({})
        return True
      else:
        return False     

#Alojamiento datos

@app.route('/registrarEvento',methods=['POST'])
def registroAlojamientos():
  reference=db.reference("/evento")
  data=request.json
  alojamiento={
  "tipoEvento":data["tipoEvento"],
  "descricion":data["descricion"],
  "fecha":data["fecha"],
  "hora":data["hora"],
  "numpax":data["numpax"],
  "v_unitario":data["v_unitario"],
  "v_total":data["v_total"],
  "cliente":data["cliente"],
  "alojamiento":data["alojamiento"],
  "proveedor":data["proveedor"]
  }

  if(validarExisteAlojamiento(reference,alojamiento)):
    return jsonify({"Mensaje":"Ya existe un vento creado con ese nit"})
  else:
    create=reference.push(alojamiento)
    return jsonify({"Mensaje":"Evento Creado satisfactoriamente","UID":create.key})

#lista de productos

@app.route('/actualizarAlojamiento',methods=['PUT'])      
def actualizarAlojamiento():
    database = db.reference("/alojamientos")
    for key, value in database.items():
      if(value["nit"] == data["nit"]):
        database.child(key).update(data)
        return True
      else:
        return False   
        
@app.route('/eliminarAlojamiento',methods=['POST'])      
def eliminarAlojamiento():
    database = db.reference("/usuarios")
    for key, value in database.items():
      if(value["nit"] == data["nit"]):
        database.child(key).update({})
        return True
      else:
        return False     

# Eventos 

@app.route('/evento',methods=['POST'])
def registroEvento():
  reference=db.reference("/eventos")
  data=request.json
  evento={
  "tipoEvento":data["tipoEvento"],
  "descricion":data["descricion"],
  "fecha":data["fecha"],
  "hora":data["hora"],
  "numpax":data["numpax"],
  "v_unitario":data["v_unitario"],
  "v_total":data["v_total"],
  "cliente":data["cliente"],
  "alojamiento":data["alojamiento"],
  "proveedor":data["proveedor"]
  }

  if(validarExisteEvento(reference,evento)):
    return jsonify({"Mensaje":"Ya existe un alojamiento creado con ese nit"})
  else:
    create=reference.push(alojamiento)
    return jsonify({"Mensaje":"Alojamiento Creado satisfactoriamente","UID":create.key})

#lista de productos

@app.route('/actualizarEventos',methods=['PUT'])      
def actualizarEvento():
    database = db.reference("/eventos")
    for key, value in database.items():
      if(value["alojamiento"] == data["alojamiento"]):
        database.child(key).update(data)
        return True
      else:
        return False   
        
@app.route('/eliminarEventos',methods=['POST'])      
def eliminarEvento():
    database = db.reference("/usuarios")
    for key, value in database.items():
      if(value["alojamiento"] == data["alojamiento"]):
        database.child(key).update({})
        return True
      else:
        return False     


#metodo validar con una referencia y con una data a almacenar
# retornando true en caso de que si exista 

@app.route('/product')
def product():
  data=db.reference('/product')
  return jsonify(data)

@app.route('/validar')
def validar():
  validar=db.reference('/product').get()
  if(len(validar)>=1):
    for clave in validar:
      if(True):
        print(validar[clave])
        
        print(len(db.reference('/product').child('-MvqvI_TTUbrDctEB7Ow').get()))
  else:
    validar={"Message":"No hay datos"}

  return jsonify(db.reference('/product').child('-MvqvI_TTUbrDctEB7Ow').get())


# metodos 

  #jsonify(db.reference("/users").child(create.uid).get()) buscamos por el create uid

def validarExisteUsuario(reference,data):
    database = reference.get()
    for key, value in database.items():
      if(value["numDoc"] == data["numDoc"]):
        return True
      else:
        return False

def validarExisteAlojamiento(reference,data):
    database = reference.get()
    if(database):
      for key, value in database.items():
        if(value["numDoc"] == data["numDoc"]):
          return True
        else:
          return False
    else:
      return False

def validarExisteAlojamiento(reference,data):
    database = reference.get()
    if(database):
      for key, value in database.items():
        if(value["alojamiento"] == data["alojamiento"]):
          return True
        else:
          return False
    else:
      return False



#Correr la Aplicación

if __name__ == '__main__':
    app.run(debug=True)
