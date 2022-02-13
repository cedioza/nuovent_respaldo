from flask import Flask, jsonify,request
import requests
from decouple import config
from firebase import firebase


app = Flask(__name__)
url=config('URL_FIREBASE')
firebase = firebase.FirebaseApplication('https://'+url, None)


@app.route('/')
def index():
    data = firebase.get('/', None)
    return data

@app.route('/users')
def users():

    users = firebase.get('/users', None)
    return jsonify(users)


@app.route('/productos')
def users():

    users = firebase.get('/product', None)
    return jsonify(users)

@app.route('/registro')
def registro_usuarios():

    data={
    "nombre":request["nombre"],
    "typeDoc":request["typeDoc"],
    "numDoc":request["numDoc"],
    "userName":request["userName"],
    "password":request["password"]
    }

    crear = firebase.post('/users',data)
    return jsonify("datos")


app.route('/eliminar<string:numDoc>')
def delete(numDoc):
     
    data=(firebase.get('/users',None))

    # for clave in data:
    #     if data[clave] == numDoc:
        
    #     firebase.delete('/users',clave)
    
    return jsonify({"message": "User Delete"})

#actualizar datos
#print(firebase.put('/product','-MveibFb9AzLgX3e5JQm"',data2))

if __name__ == '__main__':
    app.run(debug=True)


#  for clave in data:
        
#         print(data[clave])
#         print("name :" +clave)
#         firebase.delete('/users',clave)
        

        
