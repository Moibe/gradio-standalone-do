import globales
#import sulkuPypi
import tools
import fireWhale

def authenticate(username, password):   

    print("Entré al autorizador")

    #(Colección, dato índice, campo buscado.)
    contrasena = fireWhale.obtenDato('usuarios', username, 'password')

    if contrasena == password:
        api, tipo_api = tools.eligeAPI(globales.seleccion_api)                                           
        return True
    else:
        return False