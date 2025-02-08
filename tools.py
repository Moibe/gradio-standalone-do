import random
import gradio as gr
import globales
from huggingface_hub import HfApi
import bridges
import sulkuPypi
import importlib

def theme_selector():
    temas_posibles = [
        gr.themes.Base(),
        gr.themes.Default(),
        gr.themes.Glass(),
        gr.themes.Monochrome(),
        gr.themes.Soft()
    ]
    tema = random.choice(temas_posibles)
    return tema

def eligeAPI(opcion):

    funciones = {
        "eligeQuotaOCosto": eligeQuotaOCosto,
        "eligeAOB": eligeAOB,
        "eligeGratisOCosto": eligeGratisOCosto
    }
    
    if opcion in funciones:
        funcion_elegida = funciones[opcion]
        api, tipo_api = funcion_elegida()
    else:
        print("Opción no válida")

    return api, tipo_api

#Los tipos de elección son diferentes porque tienen diferentes reglas de negocio.

def eligeGratisOCosto():
#Se eligirá en los casos en los que sin costo funciona bien como Astroblend pero por si se quiere mejorar hacia Costo.
#Por ahora funcionará exactamente igual que eligeAoB, en el futuro se basará en reglas de membresía.
    apis = [globales.api_a, globales.api_b]
    api_elegida = random.choice(apis)
    api, tipo_api = api_elegida
    return api, tipo_api

def eligeAOB():
#Se eligirá cuando se tenga un control sobre la cantidad en queu y se redirija hacia una segunda fuente alternativa.
    # Lista con las opciones
    apis = [globales.api_a, globales.api_b]
    api_elegida = random.choice(apis)
    api, tipo_api = api_elegida
    return api, tipo_api

def eligeQuotaOCosto():
#Se eligirá en los casos en los que se use Zero, para extender las posibilidades de Quota y después usar Costo.
    diferencia = sulkuPypi.getQuota() - globales.process_cost

    if diferencia >= 0:
        #Entonces puedes usar Zero.
        api, tipo_api = globales.api_zero
        #Además Si el resultado puede usar la Zero "por última vez", debe de ir prendiendo la otra.
        #if diferencia es menor que el costo de un sig.  del proceso, ve iniciando ya la otra API.
        if diferencia < globales.process_cost:
            print("Preventivamente iremos prendiendo la otra.")
            initAPI(globales.api_cost) 
    else:
        api, tipo_api = globales.api_cost

    print("La API elegida es: ", api)
    return api, tipo_api

def initAPI(api):
    
    global result_from_initAPI

    try:
        repo_id = api
        llave = HfApi(token=bridges.hug)
        runtime = api.get_space_runtime(repo_id=repo_id)
        print("Stage: ", runtime.stage)
        #"RUNNING_BUILDING", "APP_STARTING", "SLEEPING", "RUNNING", "PAUSED", "RUNTIME_ERROR"
        if runtime.stage == "SLEEPING" or runtime.stage == "PAUSED":
            llave.restart_space(repo_id=repo_id)
            
        print("Hardware: ", runtime.hardware)
        result_from_initAPI = runtime.stage

    except Exception as e:
        #Creo que ya no debería de llegar aquí.
        print("No api, encendiendo: ", e)
        result_from_initAPI = str(e)    
    
    return result_from_initAPI

def titulizaExcepDeAPI(e):   
    print("El e recibido por tituliza es: ", e) 
     #Resume una excepción a un título manejable.
    if "RUNTIME_ERROR" in str(e):
        resultado = "RUNTIME_ERROR" #api mal construida tiene error.
    elif "PAUSED" in str(e):
        resultado = "PAUSED" 
    elif "The read operation timed out" in str(e): #IMPORTANTE, ESTO TAMBIÉN SUCEDE CUANDO LA DESPIERTAS Y ES INSTANTÁNEO.
        resultado = "STARTING"
    elif "GPU quota" in str(e): 
        resultado = recortadorQuota(str(e)) #Cuando se trata de quota regresa el resultado completo convertido a string.
    elif "handshake operation timed out" in str(e):
        resultado = "HANDSHAKE_ERROR"
    elif "File None does not exist on local filesystem and is not a valid URL." in str(e):
        resultado = "NO_FILE"
    #A partir de aquí son casos propios de cada aplicación.
    #image-blend
    elif "no-source-face" in str(e):
        resultado = "NO_FACE"
    #splashmix
    elif "Unable to detect a face" in str(e):
        resultado = "NO_FACE"
    else: 
        resultado = "GENERAL"

    return resultado

def recortadorQuota(texto_quota):
    # Encontrar el índice de inicio (después de "exception:")
    indice_inicio = texto_quota.find("exception:") + len("exception:")
    # Encontrar el índice de final (antes de "<a")
    indice_final = texto_quota.find("<a")
    
    if indice_final == -1: #Significa que no encontró el texto "<a" entonces buscará Sign-Up.
        indice_final = texto_quota.find("Sign-up")
    
    #Extraer la subcadena
    subcadena = texto_quota[indice_inicio:indice_final]

    #Y si el objetivo es nunca desplegar el texto Hugging Face, éste es el plan de escape final.
    if "Hugging" in subcadena: 
        nuevo_mensaje = "Your quota is exceeded, try again in few hours please."
        return nuevo_mensaje
    else:
        print("El recorte quedó: ")
        print(subcadena)
    
    return subcadena

#En gradio-standalone no se usa, pero el destuplador podría servir para otras apps que salgan de ésta app general. 
def desTuplaResultado(resultado):
    #Procesa la tupla recibida y la convierte ya sea en imagen(path) o error(string)       
    if isinstance(resultado, tuple):

        print("El resultado fue una tupla, ésta tupla:")
        print(resultado)
        ruta_imagen_local = resultado[0]
        print("Ésto es resultado ruta imagen local: ", ruta_imagen_local)
        return ruta_imagen_local        

    #NO PROCESO CORRECTAMENTE NO GENERA UNA TUPLA.
    #CORRIGE IMPORTANTE: QUE NO SE SALGA DEL CICLO DE ESA IMAGEN AL ENCONTRAR ERROR.
    else:
        #NO ES UNA TUPLA:
        print("El tipo del resultado cuando no fue una tupla es: ", type(resultado))                
        texto = str(resultado)
        segmentado = texto.split('exception:')
        print("Segmentado es una posible causa de error, analiza segmentado es: ", segmentado)
        #FUTURE: Agregar que si tuvo problemas con la imagen de referencia, agregue en un 
        #Log de errores porque ya no lo hará en el excel, porque le dará la oportunidad con otra 
        #imagen de posición.
        try:
            #Lo pongo en try porque si no hay segmentado[1], suspende toda la operación. 
            print("Segmentado[1] es: ", segmentado[1])
            mensaje = segmentado[1]
            return mensaje
        except Exception as e:
            print("Error en el segmentado: ", e)
            # mensaje = "concurrent.futures._base.CancelledError"
            # concurrents = concurrents + 1
        finally: 
            pass

def get_mensajes(idioma):
    """
    Obtiene el módulo de mensajes correspondiente al idioma especificado.

    Args:
        idioma (str): Código del idioma (ej: 'es', 'en').

    Returns:
        module: Módulo de mensajes cargado dinámicamente.
    """
    #Primero el módulo normal de mensajes.
    try:
        # Intenta cargar el módulo correspondiente
        module_mensajes = importlib.import_module(f"messages.{idioma}")
        
    except ImportError:
        # Si ocurre un error al importar, carga un módulo por defecto (opcional)
        print(f"Idioma '{idioma}' no encontrado. Cargando módulo por defecto.")
        module_mensajes = importlib.import_module("messages.en")  # Por ejemplo, inglés como defecto

    #Y después el módulo de Sulku.
    try:
        # Intenta cargar el módulo correspondiente
        module_sulku = importlib.import_module(f"messages_sulku.{idioma}")
        
    except ImportError:
        # Si ocurre un error al importar, carga un módulo por defecto (opcional)
        print(f"Idioma '{idioma}' no encontrado. Cargando módulo por defecto.")
        module_sulku = importlib.import_module("messages_sulku.en")  # Por ejemplo, inglés como defecto 
    
    return module_mensajes, module_sulku        