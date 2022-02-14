from flask import Flask, jsonify,request
from decouple import config
import firebase_admin
import requests
from firebase_admin import credentials
from firebase_admin import firestore
import json
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
            #data = firebase.get('/', None)
    db=firestore.client()
    db.collection('usuarios').add({"name":"matusalen","Age":"500s"})

    
    return "buenas"

# @app.route('/users')
# def users():

#     users = firebase.get('/users', None)
#     return jsonify(users)


# @app.route('/productos')
# def productos():

#     users = firebase.get('/product', None)
#     return jsonify(users)

# @app.route('/registro')
# def registro_usuarios():

#     data={
#     "nombre":request["nombre"],
#     "typeDoc":request["typeDoc"],
#     "numDoc":request["numDoc"],
#     "userName":request["userName"],
#     "password":request["password"]
#     } 

#     crear = firebase.post('/users',data)
#     return jsonify("datos")


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
    app.run()