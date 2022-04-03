from flask import Config, Flask, jsonify,request
from decouple import config
import firebase_admin
import requests
from flask_cors import CORS
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
from firebase_admin import auth ,exceptions
import cloudinary
import cloudinary.uploader
import cloudinary
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Inicializar Cloudinary
cloudinary.config( 
  cloud_name = config("CLOUD_NAME"), 
  api_key = config("API_KEY"), 
  api_secret = config("API_SECRET_KEY"),
  secure = True
)
# Inicializar JSONBin
key_json=config('KEY')
url = config('URL_CREDENTIALS_FIREBASE')
headers = {
  'X-Master-Key': key_json
}
req = requests.get(url, json=None, headers=headers)
data=req.json()["record"]

# Credenciales Firebase
cred = credentials.Certificate(data)
url=config('URL_FIREBASE')

#Inicializar Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': url,
})

# API Email SendGrid

def sendEmail(email,name,case):
  
  if case==1:
    subject=f'Bienvenido a Nuovent {name} '
    content='<strong>Bienvenido  ahora podras crear nuevos anuncios o alojamientos </strong>'
  else:
   subject=f'Nuevo anuncio creado'
   content=f'<strong> Se creo un nuevo anuncio {name} </strong>'

  message = Mail(
    from_email='cedioza@gmail.com',
    to_emails=email,
    subject=subject,
    html_content=content)
  try:
      sg = SendGridAPIClient(config('KEY_SENDGRID'))
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
  except Exception as e:
      print(e)



# Home
@app.route('/home')
def anuncios():
    anuncios=db.reference("/anuncios").order_by_key().limit_to_last(6).get()
    datos=anuncios.items()
    # datos=anuncios.values()
    return jsonify(list(datos))

#Login Usuario

@app.route('/login',methods=['POST'])
def login(): 
  try:  
    data=request.json
    email=data['email']
    password=data['password']
    user=auth.get_user_by_email(email)
    #Validación sí existe usuario 
    if(user):
      usuario=db.reference("/usuarios").child(user.uid).get()
      print(usuario)
      if(usuario["password"]== password):
        token=str(auth.create_custom_token(user.uid,usuario)).split("'")[1]
        return jsonify({"token":token})
      else:
        return jsonify({"Message":"Contraseña Erronea intente nuevamente"})
    else:
      return jsonify({"Message":"Usuario No esta registrado"})
  except :
    return jsonify({"Message":"Datos Incorrectos"})
  # Registro Usuarios

@app.route('/registro',methods=['POST'])
def registroUsuarios():
  reference=db.reference("/usuarios")
  data=request.json
  usuarios={
  "nombre":data["nombre"],
  "typeDoc":data["typeDoc"],
  "numDoc":data["numDoc"],
  "userName":data["userName"],
  "password":data["password"],
  "email":data["email"],
  "phone":data["phone"],
  "state":"1"
  }  
  try:
    if(validarExisteUsuario(reference,usuarios)):
      return jsonify({"Mensaje":"Ya existe un usuario creado con ese cedula"})
    else:
      create=auth.create_user(email=data["email"],password=data["password"])
      reference.child(create.uid).set(usuarios)
      sendEmail(data["email"],data["nombre"],1)
      return jsonify({"Mensaje":"usuario Creado satisfactoriamente","UID":create.uid})
  except auth.EmailAlreadyExistsError:
    return jsonify({"Mensaje":"Ya existe un usuario creado con ese correo"})
    

#Buscar Anuncion
@app.route('/obteneranuncio/<string:uid>',methods=['GET'])
def obtenerAnuncio(uid):
  anuncio=db.reference('/anuncios').child(uid).get()
  alojamiento=db.reference('/alojamiento').child(anuncio["uidAlojamiento"]).get()

  anuncio["telefono"]=alojamiento["telefono"]
  anuncio["email"]=alojamiento["email"]
  anuncioP=[]
  anuncioP.append(anuncio)
   
  return jsonify(anuncioP)

#Crear Anuncio

@app.route('/anuncio',methods=['POST'])
def registroAnuncios():
  try:
    reference=db.reference("/anuncios")
    data=request.form
    imagen=request.files 
    anuncios={
    "nomAnounce":data["nomAnounce"],
    "description":data["description"],
    "numCapacity":data["numCapacity"],
    "location":data["location"],
    "available":"available",
    "uidAlojamiento":data["uid"]
    }

    for i in range(1,len(imagen)+1):
      if(imagen.get(f"file{i}")):
        url=cloudinary.uploader.upload(imagen.get(f"file{i}"))
        anuncios[f"picture{i}"]= url["url"]
    reference.push(anuncios)

    return jsonify({"Mensaje":"Anuncio creado"})
  except Exception as  e:
    reference=db.reference("/error").push(e)
    return jsonify({"Mensaje":"Error creando anuncio"})

#crear un alojamineto con uid enviado


#Documentacion Relacionada Postman
@app.route("/")

def index():
  return jsonify({"Message":"""Ver  solamente 4 anuncios  /home
  Trae todos los eventos /zonaevento """})

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

#Alojamiento datos con uid dado

@app.route('/registrarAlojamiento/<string:uid>',  methods=['POST'])
def registrarAlojamiento(uid):

  reference=db.reference("/alojamientos").child(uid)
  data=request.json
  alojamiento={
  "nombrealojamiento":data["nombrealojamiento"],
  "nit":data["nit"],
  "email":data["email"],
  "telefono":data["telefono"],
  "responsable":data["responsable"],
  "categoria":data["categoria"],
  "descripcion":data["descripcion"],
  "ciudad":data["ciudad"],
  "direccion":data["direccion"],
  "proveedor":data["proveedor"]
  }
  if(validarExisteAlojamiento(reference,alojamiento)):
    return jsonify({"Mensaje":"Ya existe un alojamiento  creado con ese nit"})
  else:
    reference.set(alojamiento)
    db.reference('/usuarios').child(uid).update({"state":"2"})
    print("usuario cambio de estado ")
    return jsonify({"Mensaje":"Alojamiento  Creado satisfactoriamente","UID":uid})

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
        
# mis anuncios en base al uid del anuncio con el parametro del alojamiento


@app.route('/misanuncios/<string:uid>')
def misAnuncios(uid):
  anuncios=db.reference('/anuncios').get()
  misAnuncios=[]
  anuncioTotal=[]
  if(anuncios):
     for key, value in anuncios.items():
       print(value["uidAlojamiento"])
       print(uid)
       if(value["uidAlojamiento"] == uid):
         misAnuncios.append(key)


  for anuncio in misAnuncios:
    data=db.reference('/anuncios').child(anuncio).get()
    data["uid"]=anuncio
    print(data)
    anuncioTotal.append(data)


  return jsonify(list(anuncioTotal))
  

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

@app.route('/zonaevento')
def zonaEvento():
  eventos=db.reference("/eventos").get()
  return jsonify(eventos)


@app.route('/anuncios')
def zona_anuncios():
  anuncios=db.reference("/anuncios").get()
  datos=anuncios.items()
  return jsonify(list(datos))

  
  
  

@app.route('/evento',methods=['POST'])
def registroEvento():
  reference=db.reference("/eventos")
  data=request.json
  request.headers["nombre de la cabecera "]
  evento={
  "tipoEvento":data["tipoEvento"],
  "descripcion":data["descripcion"],
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
    if(database):
      for key, value in database.items():
        if(value["numDoc"] == data["numDoc"]):
          return True

    return False

def validarExisteAlojamiento(reference,data):
    database = reference.get()
    if(database):
      for key, value in database.items():
        if(value["nit"] == data["nit"]):
          return True

def validarExisteEvento(reference,data):
    database = reference.get()
    if(database):
      for key, value in database.items():
        if(value["cliente"] == data["cliente"]):
          return True
        else:
          return False
    else:
      return False

#Correr la Aplicación

# def sendEmail(email):
#   message = Mail(
#     from_email='cedioza@misena.edu.co',
#     to_emails=[email,'flaskemail2022@gmail.com'],
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content="""""")
#   try:
#     sg = SendGridAPIClient(Config("KEY_SENDGRID"))
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
#   except Exception as e:
#     print(e.body)

if __name__ == '__main__':
    app.run(debug=True)
