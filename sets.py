import gradio as gr
import globales
import tools

mensajes, sulkuMessages = tools.get_mensajes(globales.mensajes_lang)

# Diccionario para mapear los sets a sus respectivas configuraciones
configuraciones = {
    "image-blend": {
        "input1": gr.Image(label=mensajes.label_input1, type="filepath", elem_classes="container1 animate__animated"),
        "input2": gr.Image(label=mensajes.label_input2, type="filepath", elem_classes="container1 animate__animated"),
        "result": gr.Image(label=mensajes.label_resultado, elem_classes="container1 animate__animated"),
    },
    "video-blend": {
        "input1": gr.Image(label=mensajes.label_input1, type="filepath"),
        "input2": gr.Video(label=mensajes.label_input2),
        "result": gr.Video(label=mensajes.label_resultado) 
    },
    "sampler": {
        "input1": gr.Audio(label=mensajes.label_input1),
        "input2": gr.Audio(label=mensajes.label_input2),
        "result": gr.Audio(label=mensajes.label_resultado) 
    },
    "splashmix": {
        "input1": gr.Image(label=mensajes.label_input1, type="filepath"),
        "result": gr.Image(label=mensajes.label_resultado, type="filepath"),
    },
    "txt2image": {
        "input1": gr.Textbox(label=mensajes.label_input1),
        "result": gr.Image(label=mensajes.label_resultado, type="filepath"),
    },
    "txt2video": {
        "input1": gr.Textbox(label=mensajes.label_input1),
        "result": gr.Video(mensajes.label_resultado),
    },
    "zhi": {
        "input1": gr.Image(label=mensajes.label_input1, type="filepath"),
        "input2": gr.Textbox(label= mensajes.label_input2),
        "result": gr.Image(label=mensajes.label_resultado),
    },
}