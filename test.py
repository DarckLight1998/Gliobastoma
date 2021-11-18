# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import imagetools
import sys
import socket
from six.moves import urllib
import os

# Ruta de la Imagen
b = (sys.argv[1])
a= (b.split('.'))
print (a)
ruta = a[1]+'.'+a[2]+'.'+a[3]+'.'+a[4]
print (ruta)
# print (todo)



# ruta = '127.0.0.1'

# Obtener IP publica para que no realicen mas pruebas de la IA, solo 1 por IP
# external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
# external_ip = "192.168.1.9"
# Importar Letras a usar
letra_negrita = ImageFont.truetype("Lekton-Bold.ttf",20)
letra_negrita_score = ImageFont.truetype("Lekton-Bold.ttf",10)
letra_normal = ImageFont.truetype("Lekton-Regular.ttf", 10)


ruta_si = 'C:/xampp/htdocs/TESIS'+'/'+str(ruta)



# im = Image.open(/+str(ruta))
listar = os.listdir(ruta_si)

def IA(i):
	path = 'C:/xampp/htdocs/TESIS'+'/'+str(ruta)+'/'+str(i)
	im = Image.open(path)
	print (im)
	ancho, alto = im.size
	draw = ImageDraw.Draw(im)
	x1_1= ancho*0.5737983
	x2_1= ancho*0.8191304
	y1_1= alto*0.4094614
	y2_1= alto*0.6375127
	valor = str(98)

	x1 = ancho+100
	y1 = alto+100

	x2 = ancho/2
	y2 = alto/2

	x3=x1_1+3
	y3=y2_1+3

	x4=x3+30
	x5 = (x1/2)-50
	y5 = (y1/2)+150

	draw.rectangle((x1_1-1,y1_1-1,x2_1+1,y2_1+1), outline=(0, 0, 0), width=1)
	draw.rectangle((x1_1,y1_1,x2_1,y2_1), outline=(57,255,20), width=1)
	draw.rectangle((x1_1+1,y1_1+1,x2_1-1,y2_1-1), outline=(0, 0, 0), width=1)
	draw.text((x3,y3),"Score: ",(248,0,0), font=letra_negrita_score)
	draw.text((x4,y3),valor+'%',(57,255,20), font=letra_negrita_score)

	nuevo = Image.new(im.mode,(x1,y1),color=(10,10,10))

	dibujar = ImageDraw.Draw(nuevo)
	dibujar.text((x5,y5),"GLIOBLASTOMA",(253, 254, 254), font=letra_negrita)
	nuevo.paste(im,(50,50))
	# nuevo.save('C:/xampp/htdocs/TESIS/brain-tumor/data_cleaned/test/')

	nuevo.show()


for i in listar:
	IA(i)




"""
# Obtener Tamano de la Imagen
ancho, alto = im.size 
draw = ImageDraw.Draw(im)
x1_1= ancho*0.5737983
x2_1= ancho*0.8191304
y1_1= alto*0.4094614
y2_1= alto*0.6375127
valor = str(98)

x1 = ancho+100
y1 = alto+100

x2 = ancho/2
y2 = alto/2

x3=x1_1+3
y3=y2_1+3

x4=x3+30
x5 = (x1/2)-50
y5 = (y1/2)+150

draw.rectangle((x1_1-1,y1_1-1,x2_1+1,y2_1+1), outline=(0, 0, 0), width=1)
draw.rectangle((x1_1,y1_1,x2_1,y2_1), outline=(57,255,20), width=1)
draw.rectangle((x1_1+1,y1_1+1,x2_1-1,y2_1-1), outline=(0, 0, 0), width=1)
draw.text((x3,y3),"Score: ",(248,0,0), font=letra_negrita_score)
draw.text((x4,y3),valor+'%',(57,255,20), font=letra_negrita_score)

nuevo = Image.new(im.mode,(x1,y1),color=(10,10,10))

dibujar = ImageDraw.Draw(nuevo)
dibujar.text((x5,y5),"GLIOBLASTOMA",(253, 254, 254), font=letra_negrita)
nuevo.paste(im,(50,50))
# nuevo.save('C:/xampp/htdocs/TESIS/brain-tumor/data_cleaned/test/')

nuevo.show()











# im.show()



"""