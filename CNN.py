#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 19:39:49 2021

@author: germanzan
"""
"""
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
"""
from IPython.display import clear_output
import os
import sys
from tqdm import tqdm
import cv2
import numpy as np
import json
import skimage.draw
import matplotlib
import matplotlib.pyplot as plt
import random

# Root directory of the project
ROOT_DIR = os.path.abspath('Mask_RCNN/')
# Import Mask RCNN
sys.path.append(ROOT_DIR)
from mrcnn.config import Config
from mrcnn import utils
from mrcnn.model import log
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, 'samples/coco/'))
import coco

plt.rcParams['figure.facecolor'] = 'white'

clear_output()

def get_ax(rows=1, cols=1, size=7):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.
    Change the default size attribute to control the size
    of rendered images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    return ax

MODEL_DIR = os.path.join(ROOT_DIR, 'logs') # Directorio para guardar registros y modelo entrenado
# ANNOTATIONS_DIR = 'brain-tumor/data/new/annotations/' # directory with annotations for train/val sets
DATASET_DIR = 'brain-tumor/data_cleaned/' # Directorio con datos de imagenes
DEFAULT_LOGS_DIR = 'logs'

# Ruta local al archivo de pesos entrenados
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Descargar los pesos de COCO si es necesario
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

class TumorConfig(Config):
    """
    Configuracion para el entrenamiento en el conjunto de datos de tumores cerebrales
    """
    # Dar a la configuracionun nombre reconocible
    NAME = 'Detector_Tumor_Cerebral'
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 1 + 1  # background + tumor
    DETECTION_MIN_CONFIDENCE = 0.85
    STEPS_PER_EPOCH = 100
    LEARNING_RATE = 0.001

config = TumorConfig()
config.display()

class BrainScanDataset(utils.Dataset):

    def load_brain_scan(self, dataset_dir, subset):
        """
        Load a subset of the FarmCow dataset.
        dataset_dir: Root directory of the dataset.
        subset: Subset to load: train or val
        """
        # Agregar clases, solamente hay 1
        self.add_class("tumor", 1, "tumor")

        # Entrenamiento o conjunto de datos de validacion
        assert subset in ["train", "val", 'test']
        dataset_dir = os.path.join(dataset_dir, subset)

        annotations = json.load(open(os.path.join(DATASET_DIR, subset, 'annotations_'+subset+'.json')))
        annotations = list(annotations.values())  # No se necesitan las claves de dictado

        # La herramienta VIA guarda imagenes en JSON incluso si no tiene ninguna
        # anotaciones, omitir imagines sin anotar
        annotations = [a for a in annotations if a['regions']]

        # Anadir imagenes
        for a in annotations:
            """
            # 
            Obtener coordenadas X, Y de los puntos de los pligonos que forman
            el contorno de cada instancia de objeto
            Estas son instancias en Shape_attributes (vea el formato json de arriba)
            La condicion If es necesaria para adminir las versiones 1.x y 2.x de VIA
            """
            if type(a['regions']) is dict:
                polygons = [r['shape_attributes'] for r in a['regions'].values()]
            else:
                polygons = [r['shape_attributes'] for r in a['regions']]
            """
            load_mask() necesita el tamano de la imagen para convertir poligonos
            en mascara
            Desafortunadamente, VIA np lo incluye en JSON por lo que debemos leer
            la imagen.
            Esto solo se puede administrar ya que el conjunto de datos es pequeno
            """
            image_path = os.path.join(dataset_dir, a['filename'])
            image = skimage.io.imread(image_path)
            height, width = image.shape[:2]

            self.add_image(
                "tumor",
                image_id=a['filename'],  # Use el nombre del archivo como una identificacion de imagen unica
                path=image_path,
                width=width,
                height=height,
                polygons=polygons
            )

    def load_mask(self, image_id):
        """
        Genera mascaras de instancia para una imagen
       Returns:
        masks: Variable de forma booleana [alto, ancho, recuento de instancia] 
            con una mascara por instancia
        class_ids: Una matriz de 1D de ID de las clases de las mascaras de instancia
        """
        # Si no es una imagen de conjunto de datos farm-cow, delegue en la clase principal
        image_info = self.image_info[image_id]
        if image_info["source"] != "tumor":
            return super(self.__class__, self).load_mask(image_id)

        # Convertir poligonos en una mascara de forma de mapa de bits
        # [alto, ancho, recuento de instancia]
        info = self.image_info[image_id]
        mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                        dtype=np.uint8)
        for i, p in enumerate(info["polygons"]):
            # Obtenga indices de pixeles dentro del poligono y configurelos en 1
            rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
            mask[rr, cc, i] = 1
        """
         Devuelve la máscara y la matriz de ID de clase de cada instancia. 
         Como solo tenemos una ID de clase, devolvemos una matriz de 1s
        """
        return mask.astype(np.bool), np.ones([mask.shape[-1]], dtype=np.int32)

    def image_reference(self, image_id):
        """Devuelve el Directorio de la imagen."""
        info = self.image_info[image_id]
        if info["source"] == "tumor":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)
"""
Devido a que se usaran datos muy pequenos y se usaran pesos ya entrenados,
no es necesario entrenar demasiado, por lo tanto, se excluye las ultimas
capas del entrenamiento 
"""


model = modellib.MaskRCNN(
    mode='training',
    config=config,
    model_dir=DEFAULT_LOGS_DIR
)

model.load_weights(
    COCO_MODEL_PATH,
    by_name=True,
    exclude=["mrcnn_class_logits", "mrcnn_bbox_fc", "mrcnn_bbox", "mrcnn_mask"]
)


"""
Cargue el conjunto de datos y entrene su modelo durante 15 epocas con la tasa
de aprendizaje de 0,001
"""
# Conjunto de datos de entrenamiento
dataset_train = BrainScanDataset()
dataset_train.load_brain_scan(DATASET_DIR, 'train')
dataset_train.prepare()

# Conjunto de datos de validacion
dataset_val = BrainScanDataset()
dataset_val.load_brain_scan(DATASET_DIR, 'val')
dataset_val.prepare()

dataset_test = BrainScanDataset()
dataset_test.load_brain_scan(DATASET_DIR, 'test')
dataset_test.prepare()

print("Training network heads")
model.train(
    dataset_train, dataset_val,
    learning_rate=config.LEARNING_RATE,
    epochs=15,
    layers='heads'
)

# Recrear el modelo en modo de inferencia
model = modellib.MaskRCNN(
    mode="inference",
    config=config,
    model_dir=DEFAULT_LOGS_DIR
)
"""
Obtener la ruta de los pesos guardados Establezca una ruta específica o 
busque los últimos pesos entrenados.
model_path = os.path.join(ROOT_DIR,".h5 file name here")
"""
model_path = model.find_last()

# Cargar pesos entrenados
print("Loading weights from ", model_path)
model.load_weights(model_path, by_name=True)

# Funciones para mostrar los resultados
def predict_and_plot_differences(dataset, img_id):
    original_image, image_meta, gt_class_id, gt_box, gt_mask =\
        modellib.load_image_gt(dataset, config,
                               img_id, use_mini_mask=False)

    results = model.detect([original_image], verbose=0)
    r = results[0]

    visualize.display_differences(
        original_image,
        gt_box, gt_class_id, gt_mask,
        r['rois'], r['class_ids'], r['scores'], r['masks'],
        class_names = ['tumor'], title="", ax=get_ax(),
        show_mask=True, show_box=True)


def display_image(dataset, ind):
    plt.figure(figsize=(5,5))
    plt.imshow(dataset.load_image(ind))
    plt.xticks([])
    plt.yticks([])
    plt.title('Original Image')
    plt.show()

"""
Pruebe la prediccion de su modelo en el conjunto de validacion
"""
# Conjunto de validacion
ind = 9
display_image(dataset_val, ind)
predict_and_plot_differences(dataset_val, ind)

ind = 6
display_image(dataset_val, ind)
predict_and_plot_differences(dataset_val, ind)

"""
Ahora pruebe el modelo en el conjunto de prueba
"""
# Conjunto de prueba
ind = 1
display_image(dataset_test, ind)
predict_and_plot_differences(dataset_test, ind)
ind = 0
display_image(dataset_test, ind)
predict_and_plot_differences(dataset_test, ind)
