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

url = config('URL_CREDENTIALS')
headers = {
  'X-Master-Key': key_json
}
req = requests.get(url, json=None, headers=headers)
data=req.json()["record"]

cred = credentials.Certificate(data)
url=config('URL_FIREBASE_PRUEBAS')

# #firebase = firebase.FirebaseApplication('https://'+url, None)

# # Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': url,
})

# As an admin, the app has access to read and write all data, regradless of Security Rules

@app.route('/')
def index():
    # ref=db.reference("/product")
    # prueba=db.reference('/').child('product').order_by_key().limit_to_last(2).get()
    # return jsonify(prueba)
    ref = db.reference("/product")
    product = ref.get()
    print(product)
    for key, value in product.items():
      print(key, value["message"])
    return jsonify({"message":"mundo"})

#Loguear
@app.route('/login',methods=['POST'])
def login():   
  data=request.json
  usuario=data['usuario']
  contraseña=data['contraseña']
  user=auth.get_user_by_email(usuario)
  if(user):
    print ("bienvenido")
  else:
    user=auth.create_user(email=usuario,password=contraseña)
  
  return jsonify({"id":user.uid,"email":user.email})

#Metodos utiles

def validarExisteUsuario(reference,data):
    database = reference.get()
    for key, value in database.items():
      if(value["numDoc"] == data["numDoc"]):
        return True
      else:
        return False

#listado de usuarios
@app.route('/list')
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


@app.route('/registro',methods=['POST'])
def registroUsuarios():
  reference=db.reference("/usuarios")
  data=request.json
  user={
  "nombre":data["nombre"],
  "typeDoc":data["typeDoc"],
  "numDoc":data["numDoc"],
  "userName":data["userName"],
  "password":data["password"]
  }

#Alojamiento datos

def validarExisteAlojamiento(reference,data):
    database = reference.get()
    for key, value in database.items():
      if(value["numDoc"] == data["numDoc"]):
        return True
      else:
        return False

@app.route('/alojamiento',methods=['POST'])
def registroAlojamientos():
  reference=db.reference("/usuarios")
  data=request.json
  alojamiento={
  "nombreAlojamiento":data["nombreAlojamiento"],
  "nit":data["typeDoc"],
  "email":data["numDoc"],
  "telefono":data["userName"],
  "responsable":data["password"],
  "categoria":data["password"],
  "descricion":data["password"],
  "ciudad":data["password"],
  "password":data["password"],
  }

  if(validarExisteAlojamiento(reference,user)):
    return jsonify({"Mensaje":"Ya existe un alojamiento creado con ese nit"})
  else:
    create=reference.push(alojamiento)
    return jsonify({"Mensaje":"Alojamiento Creado satisfactoriamente","UID":create.key})

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


  #jsonify(db.reference("/users").child(create.uid).get())

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
















# @app.route('/users')
# def users():

#     users = firebase.get('/users', None)
#     return jsonify(users)


# @app.route('/productos')
# def productos():

#     users = firebase.get('/product', None)
#     return jsonify(users)


# app.route('/eliminar<string:numDoc>')
# def delete(numDoc):
     
#     data=(firebase.get('/users',None))

#     # for clave in data:
#     #     if data[clave] == numDoc:
        
#     #     firebase.delete('/users',clave)
    
#     return jsonify({"message": "User Delete"})

# #actualizar datos
# #print(firebase.put('/product','-MveibFb9AzLgX3e5JQm"',data2))

if __name__ == '__main__':
    app.run(debug=True)