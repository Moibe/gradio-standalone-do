import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials.
cred = credentials.Certificate('config.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


##Vamos

#Primero debemos definir la referencia al documento, o sea a la hoja de usuario.
doc_ref = db.collection('usuarios').document('ella')
#Éste es el documento que tiene los datos de ella.
documento = doc_ref.get()

#Recuerda la conversión a diccionario.
diccionario = documento.to_dict()


print("Documento:")
print(diccionario.get('password'))