import time
import globales
import sulkuPypi
import gradio as gr
import threading
import tools
import fireWhale

# import modulo_correspondiente
mensajes, sulkuMessages = tools.get_mensajes(globales.mensajes_lang)

result_from_displayTokens = None
result_from_initAPI = None    

def displayTokens(usuario):

    global result_from_displayTokens    

    print("El usuario es: ", usuario)
    novelty = fireWhale.obtenDato('usuarios', usuario, 'novelty' )
     
    if novelty == "new_user": 
        display = gr.Textbox(visible=False)
    else: 
        tokens = fireWhale.obtenDato('usuarios', usuario, 'tokens')
        display = visualizar_creditos(tokens, usuario) 
    
    result_from_displayTokens = display 


def precarga(request: gr.Request):

    # global result_from_initAPI
    # global result_from_displayTokens

    if globales.acceso == "login": 
        usuario = request.username
    else:        
        usuario = globales.usuario
    
    #thread1 = threading.Thread(target=initAPI)
    #IMPORTANTE FUTURE: displaytokens no se debería llevar a cabo si estamos en el modo libre. 
    thread2 = threading.Thread(target=displayTokens, args=(usuario,))

    #thread1.start()
    thread2.start()

    #thread1.join()  # Espera a que el hilo 1 termine
    thread2.join()  # Espera a que el hilo 2 termine

    return result_from_displayTokens  
  

def visualizar_creditos(nuevos_creditos, usuario):

    html_credits = f"""
    <div>
    <div style="text-align: left;">👤<b>Username: </b> {usuario}</div><div style="text-align: right;">💶<b>Credits Available: </b> {nuevos_creditos}</div>
    </div>
                    """    
     
    return html_credits

#Controla lo que se depliega en el frontend y que tiene que ver con llamados a Sulku.
def noCredit(usuario):
    info_window = sulkuMessages.out_of_credits
    path = 'images/no-credits.png'
    tokens = 0
    html_credits = visualizar_creditos(tokens, usuario)
    return info_window, path, html_credits

def aError(usuario, tokens, excepcion):
    #aError se usa para llenar todos los elementos visuales en el front.
    info_window = manejadorExcepciones(excepcion)
    path = 'images/error.png'
    tokens = tokens
    html_credits = visualizar_creditos(tokens, usuario)   
    return info_window, path, html_credits

def manejadorExcepciones(excepcion):
    #El parámetro que recibe es el texto despliega ante determinada excepción:
    if excepcion == "PAUSED": 
        info_window = sulkuMessages.PAUSED
    elif excepcion == "RUNTIME_ERROR":
        info_window = sulkuMessages.RUNTIME_ERROR
    elif excepcion == "STARTING":
        info_window = sulkuMessages.STARTING
    elif excepcion == "HANDSHAKE_ERROR":
        info_window = sulkuMessages.HANDSHAKE_ERROR
    elif excepcion == "GENERAL":
        info_window = sulkuMessages.GENERAL
    elif excepcion == "NO_FACE":
        info_window = sulkuMessages.NO_FACE
    elif excepcion == "NO_FILE":
        info_window = sulkuMessages.NO_FILE
    elif "quota" in excepcion: #Caso especial porque el texto cambiará citando la cuota.
        info_window = excepcion
    else:
        info_window = sulkuMessages.ELSE

    return info_window

def presentacionFinal(usuario, accion):
        
    if accion == "debita": 
        tokens = fireWhale.obtenDato('usuarios', usuario, 'tokens') #obtienes
        tokens = tokens - globales.costo_work #debitas
        fireWhale.editaDato('usuarios', usuario, 'tokens', tokens) #editas
        print(f"Después de debitar tienes {tokens} tokens.")
        info_window = sulkuMessages.result_ok
    elif accion == "no-debitar": #Aquí llega si está en modo libre.
        info_window = sulkuMessages.result_ok
        tokens = "Free"        
    else: 
        info_window = "No face in source path detected."
        tokens = fireWhale.obtenDato('usuarios', usuario, 'tokens') #obtienes
    
    html_credits = visualizar_creditos(tokens, usuario)       
    
    return html_credits, info_window