#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 19:39:49 2021

@author: germanzan
"""

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# Importar las librerias necesarias

import os
import sys
# Directorio del proyecto Mask
ROOT_DIR = os.path.abspath('Mask_RCNN/')
# Importar Mask
sys.path.append(ROOT_DIR)
from mrcnn.config import Config
from mrcnn import model as modellib
from mrcnn import visualize
import mrcnn
import numpy as np
import colorsys
import argparse
import imutils
import random
import cv2
import tqdm

from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mrcnn.visualize import display_instances
from mrcnn import utils

import matplotlib.patches as patches
import matplotlib.lines as lines
from matplotlib.patches import Polygon
from tqdm import tqdm 
from time import sleep
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array


b = (sys.argv[1])
a= (b.split('.'))
ruta = a[1]+'.'+a[2]+'.'+a[3]+'.'+a[4]

content = 'C:/xampp/htdocs/TESIS/'+str(ruta)+'_JPG'

ruta_prediccion = str(ruta)+'_PREDICCION_JPG/imagen_1.png'

class myMaskRCNNConfig(Config):
    # Darle a la configuracion un nombre reconocible
    NAME = "MaskRCNN_inference"
 
    # Establecer la cantidad de GPU que se utilizarán junto con la cantidad de imágenes por GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
 
    # número de clases (normalmente agregaríamos +1 para el fondo, pero la clase de fondo * ya * está incluida en los nombres de las clases)
    NUM_CLASSES = 1+1

# Crear la instancia
config = myMaskRCNNConfig()

# inicializar el modelo Mask R-CNN para inferencia

model = modellib.MaskRCNN(mode="inference", config=config, model_dir='./')
# Cargar los pesos
model.load_weights('logs/ia_entrenada.h5', by_name=True)
os.getcwd()
# definir 81 clases que el modelo coco conoce junto con antecedentes
class_names = ['person', 'tumor', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']
# cargue la imagen en una matriz numpy y muestre la imagen original
# Abrir archivo
path = str(content)
dirs = os.listdir(path)

# Esto imprimiría todos los archivos y directorios.
contador = 1
if contador <= len(dirs):
    for file in dirs:
        #print(file)
        img = load_img(path+'/'+file)
        img = img_to_array(img)

        pyplot.imshow(img/255)

        # dibujar una imagen con objetos detectados
        def draw_image_with_boxes(filename, boxes_list):
             # Cargar imagen
             data = pyplot.imread(filename)
             # Trazar la imagen
             pyplot.imshow(data)
             # obtener el contexto para dibujar cuadros
             ax = pyplot.gca()
             # trazar cada caja
             for box in boxes_list:
                  # Obtener coordenadas
                  y1, x1, y2, x2 = box
                  # calcular el ancho y alto de la caja
                  width, height = x2 - x1, y2 - y1
                  # crea la forma
                  rect = Rectangle((x1, y1), width, height, fill=False, color='red', lw=5)
                  # Dibujar la caja
                  ax.add_patch(rect)
             # Mostrar la trama
             #pyplot.show()


        # Hacer la prediccion
        results = model.detect([img], verbose=0)

        r = results[0]
        # mostrar foto con cuadros delimitadores, máscaras, etiquetas de clase y puntajes

        display_instances(img, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])
        pyplot.savefig('imagen.jpg',bbox_inches='tight', pad_inches=-0.5,orientation= 'landscape')
        
        porcentaje = str(r['scores']*100)[1:-1]
        tipo = str(class_names)
        contador = contador + 1
        
        
        print (f"""<!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="css/boton.css">
        </head>
        <body style="background: url(css/fondo.jpg)">
            
            <script language='javascript'>alert('IA Realizada Exitosamente')</script>
            <div id="particles-js"></div>
                
            <div class="caja" style="width:100%; max-width:1000px; margin:auto; padding:60px; margin-top:100px; border-top: 6px solid #65d6a6; overflow: hidden;">
                <h1 class="title" style="color:#FFFFFF; font-size:40px; margin-bottom: 60px;">RESULTADO</h1>
                <img src="{ruta_prediccion}" alt="" style="width:300px; float:left; margin-right:20px; margin-bottom:20px">
                <h2 class="tipo_tumor" style="color:#FFFFFF; font-size:30px; font-weight:400; margin-top:20px;">Glioblastoma Multiple</h2>
                <h2 class="porcentaje_asertividad" style="color:#FFFFFF; font-size:30px; font-weight:400; margin-top:20px">Con un {porcentaje}% de Asertividad</h2>
                    
                <a href="index.html">VOLVER</a>
            </div>
            
            
            <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
            <script src="js/app.js"></script>

        </body>
        </html>""")

