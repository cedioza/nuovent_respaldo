from ctypes import util
from weakref import ref
from flask import Flask, abort, jsonify,request,redirect
from decouple import config
import firebase_admin
import requests
from flask_cors import CORS
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
from firebase_admin import auth ,exceptions
from datetime import datetime, timedelta
import cloudinary
import cloudinary.uploader
import cloudinary.api
app = Flask(__name__)





#module key file
# Fetch the service account key JSON file contents
key_json=config('KEY')

url = config('URL_CREDENTIALS_FIREBASE')
headers = {
  'X-Master-Key': key_json
}
req = requests.get(url, json=None, headers=headers)
data=req.json()["record"]


cloudinary.config( 
  cloud_name = config("CLOUD_NAME"), 
  api_key = config("API_KEY"), 
  api_secret = config("API_SECRET_KEY"),
  secure = True
)


@app.route("/imagen",methods=["POST"])
def enviarImagen():
  #resp=cloudinary.uploader.upload(request.files['file'])
  print((request.form['data']))
  print((request.files['file']))
  return ({"data":"buenas"})


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
  "email":data["email"],
  "password":data["password"],
  "state":1
  }

  if(validarExisteUsuario(reference,usuarios)):
    return jsonify({"Mensaje":"Ya existe un usuario creado con ese correo"})
  else:
    user=auth.create_user(email=data["email"],password=data["password"])
    reference.update({user.uid:usuarios})
  
    #retornamos el uID
    return jsonify({"Message":"Usuario Creado"})


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
@app.route('/usuarios/<string:uid>')
def listaUsuariosUid(uid):
  database = db.reference("/usuarios").child(uid).get()
  return jsonify(database)


#colocar escuchadores  db.reference('/').listen()
@app.route('/actualizarUsuario',methods=['PUT'])      
def validarActualizarUsuario():
    database = db.reference("/usuarios")
    for key, value in database.items():
      if(value["numDoc"] == data["numDoc"]):
        database.child(key).update(data["numDoc"])
        return True
      else:
        return False   
        
@app.route('/eliminarUsuario',methods=['DELETE'])      
def eliminarUsuarios():
    
    database = db.reference("/usuarios")
    data=request.json
    users=database.get()
    for key, value in users.items():
      if(value["numDoc"] == data["numDoc"]):
        
        database.child(key).set({})
        #auth.disable(key)
        return True
      else:
        return False     

#Alojamiento datos

@app.route('/registrarAlojamiento',methods=['POST'])
def registroAlojamientos():
  reference=db.reference("/alojamientos")
  uid=request.headers["uid"]
  data=request.json
  alojamiento={
  "nombrealojamiento":data["nombrealojamiento"],
  "nit":data["nit"],
  "email":data["email"],
  "telefono":data["telefono"],
  "responsable":data["responsable"],
  "descripcion":data["descripcion"],
  "ciudad":data["ciudad"],
  "direccion":data["direccion"],
  "alojamiento":data["alojamiento"],
  "password":data["password"]
  }

  if(validarExisteAlojamiento(reference,alojamiento)):
    return jsonify({"Mensaje":"Ya existe un vento creado con ese nit"})
  else:
    create=reference.update({uid:alojamiento})
    return jsonify({"Mensaje":"Evento Creado satisfactoriamente","UID":uid})

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
    create=reference.push(evento)
    return jsonify({"Mensaje":"Alojamiento Creado satisfactoriamente","UID":create.key})

#lista de productos

@app.route('/actualizarEventos',methods=['PUT'])      
def actualizarEvento():
    database = db.reference("/eventos")
    if(database):
      return False
    else:
       for key, value in database.items():
        if(value["alojamiento"] == data["alojamiento"]):
          database.child(key).update(data)
          return True
        else:
          return False


@app.route('/eliminarEventos',methods=['POST'])      
def eliminarEvento():
    database = db.reference("/Eventos")
    for key, value in database.items():
      if(value["alojamiento"] == data["alojamiento"]):
        database.child(key).update({})
        return True
      else:
        return False     

#Anuncios 

@app.route('/anuncio',methods=['POST'])
def registroAnuncio():
  reference=db.reference("/anuncio")
  data=request.json
  anuncio={
  "nomAnounce":data["nomAnounce"],
  "description":data["description"],
  "numCapacity":data["numCapacity"],
  "location":data["location"],
  "arrayImages":data["arrayImages"],
  }
  create=reference.push(anuncio)

  return jsonify({"message":"anuncio creado satisfactoriamente"})

  # if(validarExisteEvento(reference,evento)):
  #   return jsonify({"Mensaje":"Ya existe un alojamiento creado con ese nit"})
  # else:
  #   create=reference.push(anuncio)
  #   return jsonify({"Mensaje":"Alojamiento Creado satisfactoriamente","UID":create.key})

#lista de productos

@app.route('/actualizarAnuncios',methods=['PUT'])      
def actualizarAnuncio():
    database = db.reference("/anuncios")
    if(database):
      return False
    else:
       for key, value in database.items():
        if(value["alojamiento"] == data["alojamiento"]):
          database.child(key).update(data)
          return True
        else:
          return False


@app.route('/eliminarAnuncios',methods=['POST'])      
def eliminarAnuncio():
    database = db.reference("/anuncios")
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


# metodos 

  #jsonify(db.reference("/users").child(create.uid).get()) buscamos por el create uid



def validarExisteUsuario(reference,data):
    database = reference.get()
    if(database):
      for key, value in database.items():
        if(value["numDoc"] == data["numDoc"]):
          return True
        else:
          return False
    else:
      return False


def validarContraseñaUsuario(reference,data):
    database = reference.get()
    if(database):
      for key, value in database.items():
        if(value["password"] == data["password"]):
          return True
        else:
          return False
    else:
      return False

def validarExisteAlojamiento(reference,data):
    database = reference.get()
    if(database):
      for key, value in database.items():
        if(value["nit"] == data["nit"]):
          return True
        else:
          return False
    else:
      return False

def validarExisteEvento(reference,data):
    database = reference.get()
    if(database):
      for key, value in database.items():
        if(value["alojamiento"] == data["alojamiento"]):
          return True
        else:
          return False
    else:
      return False



@app.route('/sessionLogin', methods=['POST'])
def session_login():
    # Get the ID token sent by the client
    id_token = request.json['idToken']
    # Set session expiration to 5 days.
    expires_in = timedelta(days=5)
    try:
        # Create the session cookie. This will also verify the ID token in the process.
        # The session cookie will have the same claims as the ID token.
        session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
        response = jsonify({'status': 'success'})
        # Set cookie policy for session cookie.
        expires = datetime.datetime.now() + expires_in
        response.set_cookie(
            'session', session_cookie, expires=expires, httponly=True, secure=True)
        return response
    except exceptions.FirebaseError:
        return abort(401, 'Failed to create a session cookie')


# @app.route('/profile', methods=['POST'])
# def access_restricted_content():
#     session_cookie = request.cookies.get('session')
#     if not session_cookie:
#         # Session cookie is unavailable. Force user to login.
#         return redirect('/login')

#     # Verify the session cookie. In this case an additional check is added to detect
#     # if the user's Firebase session was revoked, user deleted/disabled, etc.
#     try:
#         decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
#         return serve_content_for_user(decoded_claims)
#     except auth.InvalidSessionCookieError:
#         # Session cookie is invalid, expired or revoked. Force user to login.
#         return redirect('/login')

#Correr la Aplicación


if __name__ == '__main__':
    app.run(debug=True)



