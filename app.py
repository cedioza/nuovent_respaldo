from ctypes import util
from flask import Flask, jsonify,request
from decouple import config
import firebase_admin
import requests
from flask_cors import CORS
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
from firebase_admin import auth ,exceptions

cors = CORS(app, resources={r"/*": {"origins": "*"}})

app = Flask(__name__)



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
    
    ref=db.reference("/product")
    prueba=db.reference('/').child('product').order_by_key().limit_to_last(2).get()
    return jsonify(prueba)


#Loguear
@app.route('/login',methods=['POST'])
def login():   
  data=request.json
  usuario=data['usuario']
  contraseña=data['contraseña']
  mensaje=""
  #user=auth.create_user(email=usuario,password=contraseña)
  user=auth.get_user_by_email(usuario)
  
  return jsonify({"id":user.uid,"email":user.email})

#Registrar Usuarios

@app.route('/registro',methods=['POST'])
def registro_usuarios():
  ref=db.reference("/usuarios")
  data=request.json
  user={
  "nombre":data["nombre"],
  "typeDoc":data["typeDoc"],
  "numDoc":data["numDoc"],
  "userName":data["userName"],
  "password":data["password"]
  } 
  create=ref.push(user)  
  return jsonify({"Mensaje":"Usuario Creado satisfactoriamente","UID":create.key})
  #jsonify(db.reference("/users").child(create.uid).get())

@app.route('/product')
def product():
  data=db.reference('/product').child('-MvqvI_TTUbrDctEB7Ow').get()
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