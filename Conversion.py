#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 15:38:47 2021

Conversion de imagen Dicom a JPG

@author: germanzan
"""

"""
Generalmente las imagenes DICOM son imagenes de 16 bits por lo tanto no es legible por los visores de imagenes es 
por eso que es necesario convertir esa imagen de 16 bits a 8 bits
"""


# This program is written by Abubakr Shafique (abubakr.shafique@gmail.com) 
import os
import cv2 as cv
import numpy as np
import pydicom as PDCM
import subprocess
import sys

def Dicom_to_Image(Path):
    
    # Se leera el archivo de entrada DICOM
    DCM_Img = PDCM.read_file(Path)

    # Obtiene el numero de filas y columnas (mierntras mas informacion mejor)
    rows = DCM_Img.get(0x00280010).value # Obtener el numero de filas desde el tag (0028, 0010)
    cols = DCM_Img.get(0x00280011).value # Obtener el numero de columnas desde el tag (0028, 0011)

    # 
    Instance_Number = int(DCM_Img.get(0x00200013).value) # Obtener el numero de instancia de segmento real desde el tag (0020, 0013)

    Window_Center = int(DCM_Img.get(0x00281050).value) # Obtener el centro de la ventana desde el tag (0028, 1050)
    Window_Width = int(DCM_Img.get(0x00281051).value) # Obtener el ancho de la ventana desde el tag (0028, 1051)

    Window_Max = int(Window_Center + Window_Width / 2)
    Window_Min = int(Window_Center - Window_Width / 2)

    # Despues de obtener la informacion necesaria se hara el reescalado
    if (DCM_Img.get(0x00281052) is None):
        Rescale_Intercept = 0
    else:
        Rescale_Intercept = int(DCM_Img.get(0x00281052).value)

    if (DCM_Img.get(0x00281053) is None):
        Rescale_Slope = 1
    else:
        Rescale_Slope = int(DCM_Img.get(0x00281053).value)

    # Ahora se inicializara una nueva imagen de 8 bits con ceros y obtener la matriz de pixeles del DICOM
    New_Img = np.zeros((rows, cols), np.uint8)
    Pixels = DCM_Img.pixel_array

    for i in range(0, rows):
        for j in range(0, cols):
            
            # Se normalizara y se pondran nuevas intensidades de pixeles en la nueva imagen
            Pix_Val = Pixels[i][j]
            Rescale_Pix_Val = Pix_Val * Rescale_Slope + Rescale_Intercept

            if (Rescale_Pix_Val > Window_Max): # Si la intensidad es mayor que el maximo de pantalla
                New_Img[i][j] = 255
            elif (Rescale_Pix_Val < Window_Min): # Si la intensidad es menor que el minimo de pantalla
                New_Img[i][j] = 0
            else:
                New_Img[i][j] = int(((Rescale_Pix_Val - Window_Min) / (Window_Max - Window_Min)) * 255) # Normaliza la intensidad
    
    # Devolver el numero de instancia de corte de imagen final a nuestra funcion principal
    return New_Img, Instance_Number

def main(content):
    # Se procesara una archivo lleno de imagenes DICOM
    Input_Folder = str(content)
    Output_Folder = str(content)+'_JPG'
    
    Input_Image_List = os.listdir(Input_Folder)
    contador = 0
    if os.path.isdir(Output_Folder) is False:
        os.mkdir(Output_Folder)
        
    for i in range (0, len(Input_Image_List)):
        contador= contador+1
        # Funcion para pocesar el archivo y devuelve una imagen de 8 bits 
        nombre_archivo, extension = os.path.splitext(Input_Image_List[i])
        #print("El archivo '{}' se llama '{}' y tiene la extension '{}'".format(Input_Image_List[i], nombre_archivo, extension))

        if extension==".dcm":
            #print ("Formato Correcto")
            Output_Image, Instance_Number = Dicom_to_Image(Input_Folder + '/' + Input_Image_List[i])
        
            # Se guardara la nueva imagen con su respectivo segmento
            cv.imwrite(Output_Folder + '/' + str(contador - 1).zfill(4) + '.jpg', Output_Image)
        else:
            print ("<html><script language='javascript'>alert('Un archivo no posee la extension .dcm, pero los demas se pudieron convertir')</script></html>")

    print ("""<!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="css/estilo_python.css">
        </head>
        <body>
            <a href="index.html">VOLVER</a>
            <div id="particles-js"></div>
            <script language='javascript'>alert('Conversion Realizada Exitosamente')</script>
            <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
            <script src="js/app.js"></script>
        </body>
        </html>""")
    
if __name__ == "__main__":
    b = (sys.argv[1])
    a= (b.split('.'))
    ruta = a[1]+'.'+a[2]+'.'+a[3]+'.'+a[4]
    print (ruta)
    content = 'C:/xampp/htdocs/TESIS'+'/'+str(ruta)
    main(content)
