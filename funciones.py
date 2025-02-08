import time
import tools
import bridges
import globales
import sulkuPypi
import sulkuFront
import gradio as gr
import gradio_client
import fireWhale

mensajes, sulkuMessages = tools.get_mensajes(globales.mensajes_lang)

btn_buy = gr.Button("Get Credits", visible=False, size='lg')

#PERFORM es la app INTERNA que llamará a la app externa.
def perform(input1, input2, request: gr.Request):

    #Future: Maneja una excepción para el concurrent.futures._base.CancelledError
    #Future: Que no se vea el resultado anterior al cargar el nuevo resultado! (aunque solo se ven los resultados propios.)         

    #tokens = sulkuPypi.getTokens(sulkuPypi.encripta(request.username).decode("utf-8"), globales.env)
    tokens = fireWhale.obtenDato('usuarios', request.username, 'tokens')

    #1: Reglas sobre autorización si se tiene el crédito suficiente.
    #Básicamente consiste en preguntar si tiene suficientes tokens para ejecutar la tarea.
    autorizacion = sulkuPypi.authorize(tokens, globales.work)
    #if autorizacion is True: #La autorización ya no se gestionará llendo a un api, se definirá en globales. 
    #Quizá en el futuro cuando diferentes tareas tengan diferentes costos use api, o vaya directo a firebase.
    if tokens >= globales.costo_work:    
        try: 
            resultado = mass(input1, input2)
        except Exception as e:
            print("Éste es el except de perform...")            
            info_window, resultado, html_credits = sulkuFront.aError(request.username, tokens, excepcion = tools.titulizaExcepDeAPI(e))
            return resultado, info_window, html_credits, btn_buy
    else:
        info_window, resultado, html_credits = sulkuFront.noCredit(request.username)
        return resultado, info_window, html_credits, btn_buy    
    
    #Primero revisa si es imagen!: 
    if "result.png" in resultado:
        #Si es imagen, debitarás.
        html_credits, info_window = sulkuFront.presentacionFinal(request.username, "debita")
    else: 
        #Si no es imagen es un texto que nos dice algo.
        info_window, resultado, html_credits = sulkuFront.aError(request.username, tokens, excepcion = tools.titulizaExcepDeAPI(resultado))
        return resultado, info_window, html_credits, btn_buy      
    
    # #2: ¿El resultado es debitable?
    # if debit_rules.debita(resultado) == True:
    #     html_credits, info_window = sulkuFront.presentacionFinal(request.username, "debita")
    # else:
    #     html_credits, info_window = sulkuFront.presentacionFinal(request.username, "no debita") 
            
    #Lo que se le regresa oficialmente al entorno.
    return resultado, info_window, html_credits, btn_buy

#MASS es la que ejecuta la aplicación EXTERNA
def mass(input1, input2):
    
    api, tipo_api = tools.eligeAPI(globales.seleccion_api)
    print("Una vez elegido API, el tipo api es: ", tipo_api)

    client = gradio_client.Client(api, hf_token=bridges.hug)
    #client = gradio_client.Client("https://058d1a6dcdbaca0dcf.gradio.live/")  #MiniProxy

    imagenSource = gradio_client.handle_file(input1) 
    imagenDestiny = gradio_client.handle_file(input2)       
    
    try: 
        result = client.predict(imagenSource, imagenDestiny, api_name=globales.interface_api_name)
                
        #(Si llega aquí, debes debitar de la quota, incluso si detecto no-face o algo.)
        if tipo_api == "quota":
            print("Como el tipo api fue gratis, si debitaremos la quota.")
            sulkuPypi.updateQuota(globales.process_cost)
        #No debitas la cuota si no era gratis, solo aplica para Zero.         
        
        #result = splash_tools.desTuplaResultado(result)
        return result

    except Exception as e:
            #La no detección de un rostro es mandado aquí?! Siempre?
            mensaje = tools.titulizaExcepDeAPI(e)        
            return mensaje

def mass_zhi(input1, input2): 

    imagenSource = gradio_client.handle_file(input1) 
    #imagenDestiny = gradio_client.handle_file(input2)       

    client = gradio_client.Client(globales.api)
    #result = client.predict(imagenSource, imagenDestiny, api_name="/predict")

    result = client.predict(
		prompt="A hot girl in sexy cocktail dress.",
		person_img=imagenSource,
		seed=486992,
		randomize_seed=False,
		height=1024,
		width=1024,
		api_name="/character_gen"
        )
    
    print(result)
    print(result[0])    

    return result[0]