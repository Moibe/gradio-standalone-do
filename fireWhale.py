import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials.
cred = credentials.Certificate('config.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def obtenDato(coleccion, dato, info):
    #Colección es la base donde está, dato es el índice con el que buscaremos e info es el resultado que estamos buscando. 

    print("Si ent´re a firewhale...")
    print("Y ésto es usuario: ", dato)
    print("Y su tipo es: ", type(dato))
   
    #Primero debemos definir la referencia al documento, o sea a la hoja de usuario.
    doc_ref = db.collection(coleccion).document(dato)
    #Éste es el documento que tiene los datos de ella.
    documento = doc_ref.get()

    #Recuerda la conversión a diccionario.
    diccionario = documento.to_dict()

    return diccionario.get(info)

