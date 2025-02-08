import gradio as gr

#MAIN
version = "6.11.14"
env = "dev"
aplicacion = "astroblend-dev"

seleccion_api = "eligeAOB" #eligeGratisOCosto , eligeAOB o eligeGratisOCosto
max_size = 20
#Quota o Costo
api_zero = ("Moibe/image-blend", "quota")
api_cost = ("Moibe/image-blend", "costo")
#A o B
api_a = ("Moibe/image-blend", "gratis")
api_b = ("Moibe/image-blend", "gratis")
#Gratis o Costo
api_gratis = ("Moibe/image-blend", "gratis")
api_costo = ("Moibe/image-blend", "costo")

interface_api_name = "/predict" #El endpoint al que llamará client.

process_cost = 0
seto = "image-blend"
work = "picswap" #Se dejará de usar, pero en el futuro se reutilizará cuando en base definamos diferentes tareas a diferentes costos.
costo_work = 1 #Se integró costo_work para definir aquí directamente lo que cueta picswap, y dejar de usar la var work.
app_path = "/boilerplate"
server_port=7860
#tema = tools.theme_selector()
tema = gr.themes.Default()
flag = "auto"

#Future: Put age to cookies.

neural_wait = 3
mensajes_lang = "es"