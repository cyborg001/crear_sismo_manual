# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:03:02 2019

@author: el_in
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 11:50:37 2017
version 1.2

@author: Cgrs scripts
"""


import sys
import os
import os.path
import codigo.funciones_sismicas2 as fc
import json
import requests

PYTHON_VERSION = sys.version_info.major

PYTHON_VERSION

if PYTHON_VERSION < 3:
    try:
        import Tkinter as tk
    except ImportError:
        raise ImportError("Se requiere el modulo Tkinter")
else:
    try:
        import tkinter as tk
    except ImportError:
        raise ImportError("se requiere el modulo tkinter")
from tkinter import font
from tkinter import ttk
#################################################################################
## esta funcion genera el comentario y lo envia a la pagina, ademas de enviar
## los correos al sini automaticamente y la opcion de enviar correo a las partes
## interesadas.
##
## internaente necesita los archivos paths.txt de donde tomara las direcciones
## paths.txt tiene tres lineas:la primera de donde esta localizado el hyper.out
## la segunda  a donde enviara el dummyX.dat
## y la tercera a donde ira el dummyX.copy
##
## tambien tomara el archivo contactos.txt donde estaran los correos electroni
## cos de las partes interesadas, y contactos_sini.txt donde estaran los corre-
## os que se enviaran automaticamente al sini
##
################################################################################

def crear_hyper(formato,sentido,paths):

    '''
    # formato es el arreglo que contiene la informacion del sismo: latitud, longitud, comentario etc...
    # sentido es el valor dado al checkbox sentido para saber si el sismo fue sentido o no y publicarlo
    # en la pagina
    # paths es la variable que contiene las rutas necesarias para el programa
    '''
    '''aqui se crea el archivo en seisan con comentario'''
    url = paths[7][:-1]
    # print(url)
    print(f'*** Enviando el sismo a la direccion {url}')
    headers = {'Content-Length': '3477',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'python-requests/2.25.1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'token': "2#gi5@s=3y@#23+6@q^tq=2#=rdqqju#47_q(cawbcqzs"
        }
    r = requests.post(url,data = formato, headers = headers)
    if r.status_code == 200:
        print(f'*** Enviado exitosamente!')
    else:
        print(f'*** Error {r.status_code}, el sismo no pudo ser enviado!')
    
def mensaje():
    print(entry_fecha.get())
    if bool_sentido.get():
        sentido = True
        sentido_local = ' (Sentido).'
    else:
        sentido = False
        sentido_local = ''
    
    paths = open(os.path.join('utiles',"paths.txt")).readlines()
    path_poligonos = 'provinciascsv'
    path_ciudades = os.path.join('utiles','localidades_2mundo.dat')
    hyp_path = paths[0][:-1]#'hyp.out'#r'Z:\seismo\WOR\hyp.out'
    fpath = open(os.path.join('utiles',hyp_path))
    analista = entry_analista.get()
    fecha = entry_fecha.get() 
    hora = entry_hora.get() 
    latitud = entry_latitud.get() 
    longitud = entry_longitud.get() 
    depth = '10.0' 
    mag = entry_coda.get() 
    i_d = fecha+hora[:-2]
    ciudades = fc.get_ciudades(path_ciudades)
    # sustituimos linea por lineas para prueba
    comentario = fc.generar_comentario(ciudades,float(latitud),float(longitud),path_poligonos)
    poligonos_acuaticos =['Canal de la Mona','Canal du Sud','Mar Caribe','Oceano Atlantico','Golfo de Gonaive']
    for n in poligonos_acuaticos:
        if n in comentario:
            print(f'{n} is in {comentario}')
            if float(depth) < 1:
                # print('es menor')
                depth = ' 10.0'
            break
    fecha = f"{fecha[:4]}-{fecha[4:6]}-{fecha[6:]}"
    hora = f"{hora[:2]}:{hora[2:4]}:{hora[4:]}"
    sal=i_d+ '  '+fecha+'  '+hora+'  '+latitud+'  '+longitud+'  '+depth+'  '+mag+'  '
    #json = "{'i_d':'"+i_d+"','fecha':'"+fecha+"','hora':'"+hora+"','lat':'"+lat+"','lon':'"+lon+"','deph':'"+deph+"','mag':'"+mag+"','comentario':'"+comentario+"}"

    obj = {'id':i_d,
    'analista':analista,
    "fecha":fecha,
    "hora":hora,
    "lat":latitud,
    "lon":longitud,
    "depth":depth,
    "mag":mag,
    "magC":mag,
    "rms":1,
    "magL":mag,
    "magW":mag,
    "comentario":comentario,
    "salida":sal,
    "tipo_magni":"",
    "gapInfo":[''],
    "focalInfo":[''],
    'sentido':sentido,
    'data_estaciones':"",
    }
    #print (json.dumps(obj))
    print(obj)

    from tkinter import messagebox
    datos = obj['salida']+obj['comentario']+sentido_local
    # mensaje = f'{datos} \n\nEstas de acuerdo con los datos mostrados?'
    mensaje = '%s \n\nEstas de acuerdo con los datos mostrados?'%(datos)
    respuesta = messagebox.askyesno(message=mensaje,title='Validar Datos')
    if respuesta == True:
        crear_hyper(obj,sentido,paths)


#parte que crea la aplicacion grafica
root = tk.Tk()
root.title('Hyper')
root.geometry('540x320')
root.resizable(width=False, height=False)
font_size = font.Font(weight='bold',size=12)

bool_sentido = tk.BooleanVar()
backcolor='white smoke'
root.configure(background=backcolor)
#font_size=17
entry_analista = ttk.Entry(takefocus=True)
entry_fecha = ttk.Entry()
entry_hora = ttk.Entry()
entry_latitud = ttk.Entry()
entry_longitud = ttk.Entry()
entry_coda = ttk.Entry()

etiqueta_analista = tk.Label(root,text='Analista: ', font=font_size, justify=tk.LEFT,)
etiqueta_fecha = tk.Label(root,text='Fecha: (aaaammdd)', font=font_size, justify=tk.LEFT)
etiqueta_hora = tk.Label(root,text='Hora: (hhmmss)', font=font_size, justify=tk.LEFT)
etiqueta_latitud = tk.Label(root,text='Latitud: ', font=font_size, justify=tk.LEFT)
etiqueta_longitud = tk.Label(root,text='Longitud: ', font=font_size, justify=tk.LEFT)
etiqueta_coda = tk.Label(root,text='Magnitud: ', font=font_size, justify=tk.LEFT)
etiqueta_espacio = tk.Label(root,text='')
etiqueta2 = tk.Label(root,text='hola mundo')
boton = tk.Button(root,text='Enviar Datos',font=font_size,background='forest green',
                  foreground='yellow',command=mensaje)
ch_sentido = tk.Checkbutton(root,text='Sentido             ',font=font_size,background=backcolor,
                         variable=bool_sentido,foreground='red')
# etiqueta_status = tk.Label(root,text='Status:')
# status = tk.Label(root,text=var_status)
etiqueta_espacio.grid(row=1,column=1)
etiqueta_analista.grid(row=3,column=0)
entry_analista.grid(row=3,column=1)
etiqueta_fecha.grid(row=4,column=0)
entry_fecha.grid(row=4,column=1)
etiqueta_hora.grid(row=5,column=0)
entry_hora.grid(row=5,column=1)
etiqueta_latitud.grid(row=6,column=0)
entry_latitud.grid(row=6,column=1)
etiqueta_longitud.grid(row=7,column=0)
entry_longitud.grid(row=7,column=1)
etiqueta_coda.grid(row=8,column=0)
entry_coda.grid(row=8,column=1)
ch_sentido.grid(row=9,column=1)
etiqueta2.grid(row=9,column=1)
boton.grid(row=12,column=1)

root.mainloop()
