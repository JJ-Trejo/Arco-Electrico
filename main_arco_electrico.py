import tkinter as tk
from functools import partial #para usar la funcion partial y pasar datos a funciones
from tkinter import ttk #De tikinter se importa el modula ttk
from tkinter import *
from IEEE_std_1584_2018 import main, main_afp, main_afp_min
from ecuaciones_2002 import main_2002, main_afp_2002, main_afpmin_2002

# ******************** VENTANA PRINCIPAL ********************
ventana = tk.Tk()
ventana.title("Cálculo de arco eléctrico")
ventana.geometry("800x640+30+30") #Dimensiones de la ventana | 30+30 indica las coordenadas X Y donde aparece la ventana
ventana.iconbitmap("icono.ico") #Imagen icono de la ventana
ventana.resizable(False, False) #Evita que la ventana cambie de tamaño
#ventana.configure(bg="lightblue")
#ventana.resizable(False, False) #Evita que la ventana cambie de tamaño
ventana.attributes("-alpha", 0.95) #Transparencia de la ventana

################################## TABLAS | IEEE 1584 2018 ##################################
# Diccionario Método de cálculo
dic_metodo = {
    1: "IEEE 1584-2002",
    2: "IEEE 1584-2018"
}
# Diccionario Enclosure type
dic_ET = {
    1: "OA",
    2: "BOX"
}
#Diccionaro datos tipicos de acuerdo al tipo de equipo
typical_data = {
    "1": { #DATOS PARA VOLTAJES MENORES O IGUAL A 1 kV
        "Switchgear": {"gap": 32, "height": 508, "width": 508, "depth": 508, "workd": 609.6},
        "MCC_shallow": {"gap": 25, "height": 355.6, "width": 304.8, "depth": 203.2, "workd": 457.2},
        "MCC_deep": {"gap": 25, "height": 355.6, "width": 304.8, "depth": 204, "workd": 457.2},
        "Panelboard_shallow": {"gap": 25, "height": 355.6, "width": 304.8, "depth": 203.2, "workd": 457.2},
        "Panelboard_deep": {"gap": 25, "height": 355.6, "width": 304.8, "depth": 204, "workd": 457.2},
        "Cable_junction_box_shallow": {"gap": 13, "height": 355.6, "width": 304.8, "depth": 203.2, "workd": 457.2},
        "Cable_junction_box_deep": {"gap": 13, "height": 355.6, "width": 304.8, "depth": 204, "workd": 457.2},
    },
    "5": { #DATOS PARA VOLTAJES MENORES O IGUAL A 5 kV
        "Switchgear_large": {"gap": 104, "height": 914.4, "width": 914.4, "depth": 914.4, "workd": 914.4},
        "Switchgear_small": {"gap": 104, "height": 1143, "width": 762, "depth": 762, "workd": 914.4},
        "MCC": {"gap": 104, "height": 660.4, "width": 660.4, "depth": 660.4, "workd": 914.4},
        "Cable_junction_box_shallow": {"gap": 13, "height": 355.6, "width": 304.8, "depth": 203.2, "workd": 457.2},
        "Cable_junction_box_deep": {"gap": 13, "height": 355.6, "width": 304.8, "depth": 204, "workd": 457.2},
    },
    "15": { #DATOS PARA VOLTAJES MENORES O IGUAL A 15 kV
        "Switchgear": {"gap": 152, "height": 1143, "width": 762, "depth": 762, "workd": 914.4},
        "MCC": {"gap": 152, "height": 914.4, "width": 914.4, "depth": 914.4, "workd": 914.4},
        "Cable_junction_box_shallow": {"gap": 13, "height": 355.6, "width": 304.8, "depth": 203.2, "workd": 457.2},
        "Cable_junction_box_deep": {"gap": 13, "height": 355.6, "width": 304.8, "depth": 204, "workd": 457.2},
    }
}

typical_data_2002 = {
    "1": { #DATOS PARA VOLTAJES MENORES O IGUAL A 1 kV
        "Switchgear": {"gap": 32, "workd": 610, "xfactor":1.473},
        "MCC":        {"gap": 25, "workd": 455, "xfactor":1.641},
        "Panelboard": {"gap": 25, "workd": 455, "xfactor":1.641},
        "Cable":      {"gap": 13, "workd": 455, "xfactor":2.0},
        "Other_'OA'": {"gap": 25, "workd": "" , "xfactor":2.0},
    },
    "5": { #DATOS PARA VOLTAJES MENORES O IGUAL A 5 kV
        "Switchgear": {"gap": 104, "workd": 910, "xfactor":0.973},
        "Cable":      {"gap": 13, "workd": 455,  "xfactor":2.0},
        "Other_'OA'": {"gap": 102, "workd": "",  "xfactor":2.0},
    },
    "15": { #DATOS PARA VOLTAJES MENORES O IGUAL A 15 kV
        "Switchgear": {"gap": 152, "workd": 910, "xfactor":0.973},
        "Cable":      {"gap": 13,  "workd": 455, "xfactor":2.0},
        "Other_'OA'": {"gap": 70,  "workd": "",  "xfactor":2.0},
    }
}

# ******************** FUNCIONES ********************
# Función para mostrar el frame "metodo seleccionado"
def show_frame():
    if var_radiobutton.get() == 1:
        frame6.grid_remove()  # Oculta "#IEEE 1584-2018"
        frame5.grid()  # Muestra frame5 "#IEEE 1584-2002"
    elif var_radiobutton.get() == 2:
        frame5.grid_remove()  # Oculta #IEEE 1584-2002
        frame6.grid()  # Muestra #IEEE 1584-2018

# Función para resetear los checkbutton seleccionados cuando se cambia de "ENCLOSURE TYPE" OA & BOX
def show_frame_EC():
    if var_EC.get() == 1: # 'OA'
        cont_BOX_2018.grid_remove() # Oculta 'BOX'
        #RESETEA LOS VALORES DE "BOX"
        variable_VCB.set(False)
        variable_VCBB.set(False)
        variable_HCB.set(False)
        cont_OA_2018.grid()  # Muestra 'OA'
    elif var_EC.get() == 2: #'BOX'
        cont_OA_2018.grid_remove()  # Oculta 'OA'
        #RESETEA LOS VALORES DE "OA"
        variable_VOA.set(False)
        variable_HOA.set(False)
        cont_BOX_2018.grid()  # Muestra 'BOX'

# Se activa cuando cambia el voltaje de entrada "var_entrada_v2018" o "entrada_v2018"
# Funcion para establecer los "tipos de equipo" tipicos de acuerdo al nivel de voltaje
def rellena_typicalequipment_2018 (*args):
    check_equipo_2018.set('') #Limpia el tipo de equipo seleccionado (quita seleccion)
    verifica_rango_icc_2018() #Llama a la función que verifica el rango de corriente de corto circuito
    verifica_rango_gap_2018() #Llama a la función que verifica el rango de corriente de distancia entre electrodos "gap"
    try:
        Voc = float(var_entrada_v2018.get())
        if Voc >= 0.208 and Voc <= 1:    
            lista_equipo_2018= ["Switchgear", "MCC_shallow", "MCC_deep", "Panelboard_shallow", "Panelboard_deep", "Cable_junction_box_shallow", "Cable_junction_box_deep"]  # Elementos de la lista nueva
            check_equipo_2018["values"] = lista_equipo_2018  # Se cambia la lista de elementos usando combobox["values"]
            entrada_v2018.configure(bg="SpringGreen3") # La casilla de voltaje se torna color verde
        elif Voc > 1 and Voc <= 5:
            lista_equipo_2018 = ["Switchgear_large", "Switchgear_small", "MCC", "Cable_junction_box_shallow", "Cable_junction_box_deep"]  # Elementos de la lista nueva
            check_equipo_2018["values"] = lista_equipo_2018  # Se cambia la lista de elementos
            entrada_v2018.configure(bg="SpringGreen3")
        elif Voc > 5 and Voc <= 15:
            lista_equipo_2018 = ["Switchgear", "MCC", "Cable_junction_box_shallow", "Cable_junction_box_deep"]  # Elementos de la lista nueva
            check_equipo_2018["values"] = lista_equipo_2018  # Se cambia la lista de elementos
            entrada_v2018.configure(bg="SpringGreen3")
        else: #Si el voltaje ingresado está fuera del rango
            check_equipo_2018["values"] = []  # Limpia la lista de "tipos de equipo" | valores del combobox
            entrada_v2018.configure(bg="OrangeRed2") # La casilla de voltaje se torna color Rojo
    except ValueError:
        check_equipo_2018["values"] = []  # Limpiar los valores del combobox
        entrada_v2018.configure(bg="OrangeRed2") #La casilla de voltaje se torna color Rojo

# Se activa cuando cambia el tipo de equipo seleccionado "var_equipo_2018" o "check_equipo_2018"
#Funcion para establecer los datos tipicos de acuerdo al tipo de equipo y nivel de voltaje seleccionado
def rellena_typicaldata_2018 (*args):
    try:
        Voc = float(var_entrada_v2018.get()) #Obtiene el voltaje ingresado
        equipo = var_equipo_2018.get() #Obtiene el equipo seleccionado
        if Voc >= 0.208 and Voc <= 1:
            var_dis_2018.set(typical_data["1"][equipo]["workd"]) #Distancia de trabajo
            var_gap_2018.set(typical_data["1"][equipo]["gap"])   #Distancia entre conductores
            var_w_2018.set(typical_data["1"][equipo]["width"])   #Width
            var_h_2018.set(typical_data["1"][equipo]["height"])  #Height
            var_d_2018.set(typical_data["1"][equipo]["depth"])   #Depth
        elif Voc > 1 and Voc <= 5:
            var_dis_2018.set(typical_data["5"][equipo]["workd"]) #Distancia de trabajo
            var_gap_2018.set(typical_data["5"][equipo]["gap"])   #Distancia entre conductores
            var_w_2018.set(typical_data["5"][equipo]["width"])   #Width
            var_h_2018.set(typical_data["5"][equipo]["height"])  #Height
            var_d_2018.set(typical_data["5"][equipo]["depth"])   #Depth
        elif Voc > 5 and Voc <= 15:
            var_dis_2018.set(typical_data["15"][equipo]["workd"]) #Distancia de trabajo
            var_gap_2018.set(typical_data["15"][equipo]["gap"])   #Distancia entre conductores
            var_w_2018.set(typical_data["15"][equipo]["width"])   #Width
            var_h_2018.set(typical_data["15"][equipo]["height"])  #Height
            var_d_2018.set(typical_data["15"][equipo]["depth"])   #Depth
        else:
            pass
    except (KeyError, ValueError):
        # KeyError: Se lanza cuando intentas acceder a una clave que no existe en un diccionario.
        # ValueError: Se lanza cuando intentas realizar una operación con un valor inapropiado, como convertir una cadena no numérica en número.
        pass

def verifica_rango_icc_2018(*args):
    try:
        icc = float(var_icc_2018.get())
        Voc = float(var_entrada_v2018.get()) #Obtiene el voltaje ingresado
        if Voc >= 0.208 and Voc <= 0.600 and icc >= 0.5 and icc <= 106:
            entrada_icc_2018.configure(bg="SpringGreen3")
        elif Voc > 0.600 and Voc <= 15 and icc >= 0.2 and icc <= 65:
            entrada_icc_2018.configure(bg="SpringGreen3")
        else:
            entrada_icc_2018.configure(bg="OrangeRed2")
    except ValueError:
        entrada_icc_2018.configure(bg="OrangeRed2")

def verifica_rango_gap_2018(*args):        ################################# VERIFICAR RANGO DEL TIPO D EQUIPO "Cable_junction_box" QUE ES IGUAL A 13
    try:
        gap = float(var_gap_2018.get())
        Voc = float(var_entrada_v2018.get()) #Obtiene el voltaje ingresado
        if Voc >= 0.208 and Voc <= 0.600 and gap >= 6.35 and gap <= 76.2:
            entrada_gap_2018.configure(bg="sky blue")
        elif Voc > 0.600 and Voc <= 15 and gap >= 19.05 and gap <= 254:
            entrada_gap_2018.configure(bg="sky blue")
        else:
            entrada_gap_2018.configure(bg="OrangeRed2")
    except ValueError:
        entrada_gap_2018.configure(bg="OrangeRed2")

#distancia de trabajo
def verifica_rango_dis_2018(*args):
    try:
        dis = float(var_dis_2018.get())
        if dis >= 305:
            entrada_dis_2018.configure(bg="sky blue")
        else:
            entrada_dis_2018.configure(bg="OrangeRed2")
    except ValueError:
        entrada_dis_2018.configure(bg="OrangeRed2")

def verifica_rango_height_2018(*args):
    try:
        height = float(var_h_2018.get())
        if height <= 1244.6:
            entrada_h.configure(bg="sky blue")
        else:
            entrada_h.configure(bg="OrangeRed2")
    except ValueError:
        entrada_h.configure(bg="OrangeRed2")

def verifica_rango_width_2018(*args):
    try:
        width = float(var_w_2018.get())
        gap = float(var_gap_2018.get())
        if width >= gap*4 and width <= 1244.6:
            entrada_w.configure(bg="sky blue")
        else:
            entrada_w.configure(bg="OrangeRed2")
    except ValueError:
        entrada_w.configure(bg="OrangeRed2")

def verifica_rango_icc_2002(*args):
    try:
        icc = float(var_icc_2002.get())
        if icc >= 0.7 and icc <= 106:
            entrada_icc_2002.configure(bg="SpringGreen3")
        else:
            entrada_icc_2002.configure(bg="OrangeRed2")

    except ValueError:
        entrada_icc_2002.configure(bg="OrangeRed2")

def verifica_rango_gap_2002(*args):
    try:
        gap = float(var_gap_2002.get())
        if gap >= 13 and gap <= 152:
            entrada_gap_2002.configure(bg="sky blue")
        else:
            entrada_gap_2002.configure(bg="OrangeRed2")
    except ValueError:
        entrada_gap_2002.configure(bg="OrangeRed2")

# Se activa cuando cambia el voltaje de entrada "var_entrada_v2002" o "entrada_v2002"
# Funcion para establecer los "tipos de equipo" tipicos de acuerdo al nivel de voltaje
def rellena_typicalequipment_2002 (*args):
    check_equipo_2002.set('') #Limpia el tipo de equipo seleccionado (quita seleccion)
    try:
        Voc = float(var_entrada_v2002.get())
        if Voc >= 0.208 and Voc <= 1:    
            lista_equipo_2002= ["Switchgear", "MCC", "Panelboard", "Cable", "Other_'OA'"]  # Elementos de la lista nueva
            check_equipo_2002["values"] = lista_equipo_2002  # Se cambia la lista de elementos usando combobox["values"]
            entrada_v2002.configure(bg="SpringGreen3") # La casilla de voltaje se torna color verde
        elif Voc > 1 and Voc <= 5:
            lista_equipo_2002 = ["Switchgear", "Cable", "Other_'OA'"]  # Elementos de la lista nueva
            check_equipo_2002["values"] = lista_equipo_2002  # Se cambia la lista de elementos
            entrada_v2002.configure(bg="SpringGreen3")
        elif Voc > 5 and Voc <= 15:
            lista_equipo_2002 = ["Switchgear", "Cable", "Other_'OA'"]  # Elementos de la lista nueva
            check_equipo_2002["values"] = lista_equipo_2002  # Se cambia la lista de elementos
            entrada_v2002.configure(bg="SpringGreen3")
        else: #Si el voltaje ingresado está fuera del rango
            check_equipo_2002["values"] = []  # Limpia la lista de "tipos de equipo" | valores del combobox
            entrada_v2002.configure(bg="OrangeRed2") # La casilla de voltaje se torna color Rojo
    except ValueError:
        check_equipo_2002["values"] = []  # Limpiar los valores del combobox
        entrada_v2002.configure(bg="OrangeRed2") #La casilla de voltaje se torna color Rojo

# Se activa cuando cambia el tipo de equipo seleccionado "var_equipo_2002" o "check_equipo_2002"
#Funcion para establecer los datos tipicos de acuerdo al tipo de equipo y nivel de voltaje seleccionado
def rellena_typicaldata_2002 (*args):
    try:
        Voc = float(var_entrada_v2002.get()) #Obtiene el voltaje ingresado
        equipo = var_equipo_2002.get() #Obtiene el equipo seleccionado
        if Voc >= 0.208 and Voc <= 1:
            var_dis_2002.set(typical_data_2002["1"][equipo]["workd"]) #Distancia de trabajo
            var_gap_2002.set(typical_data_2002["1"][equipo]["gap"])   #Distancia entre conductores
            var_xfactor_2002.set(typical_data_2002["1"][equipo]["xfactor"]) #Distancia x factor

        elif Voc > 1 and Voc <= 5:
            var_dis_2002.set(typical_data_2002["5"][equipo]["workd"]) #Distancia de trabajo
            var_gap_2002.set(typical_data_2002["5"][equipo]["gap"])   #Distancia entre conductores
            var_xfactor_2002.set(typical_data_2002["5"][equipo]["xfactor"]) #Distancia x factor

        elif Voc > 5 and Voc <= 15:
            var_dis_2002.set(typical_data_2002["15"][equipo]["workd"]) #Distancia de trabajo
            var_gap_2002.set(typical_data_2002["15"][equipo]["gap"])   #Distancia entre conductores
            var_xfactor_2002.set(typical_data_2002["15"][equipo]["xfactor"]) #Distancia x factor
        else:
            pass
    except (KeyError, ValueError):
        # KeyError: Se lanza cuando intentas acceder a una clave que no existe en un diccionario.
        # ValueError: Se lanza cuando intentas realizar una operación con un valor inapropiado, como convertir una cadena no numérica en número.
        pass

def calcula_proteccion_epp(E):
    E = float(E)
    if E <= 4:
        EPP = 1

    elif E > 4 and E <= 8:
        EPP = 2

    elif E > 8 and E <= 25:
        EPP = 3 

    elif E > 25 and E <= 40:
        EPP = 4

    elif E > 40:
        EPP = ">4"

    return EPP 

# ******************** PORTADA ********************
# >>>>> Contenedores
frame1 = tk.Frame(ventana, width=300, height=200, bd=5, padx=20) #IMAGEN 1
frame1.grid(row=0, column=0)

frame2 = tk.Frame(ventana, width=300, height=200, bd=5) #TITULO
frame2.grid(row=0, column=1)

frame3 = tk.Frame(ventana, width=300, height=200, bd=5) #IMAGEN 2
frame3.grid(row=0, column=2)

frame4 = tk.Frame(ventana, width=300, height=200, bd=5) #RADIOBUTTON TIPO DE CALCULO
frame4.grid(row=1, column=1) 

frame5 = tk.Frame(ventana, width=300, height=200, bd=5) #IEEE 1584-2002
frame5.grid(row=2, column=1)
frame5.grid_remove()  # Oculta inicialmente el frame5

frame6 = tk.Frame(ventana, width=300, height=200, bd=5) #IEEE 1584-2018
frame6.grid(row=2, column=1)
frame6.grid_remove()  # Oculta inicialmente el frame6
# <<<<< Contenedores

# >>>>> Imagenes
imagen1 = tk.PhotoImage(file="50UAM_corto_m.png")
imagen2 = tk.PhotoImage(file="CBI_m.png")
etiqueta1 = tk.Label(frame1, image=imagen1)
etiqueta2 = tk.Label(frame3, image=imagen2)
etiqueta1.pack()
etiqueta2.pack()
# <<<<< Imagenes

# >>>>> Texto portada
titulo1 = tk.Label(frame2, text="UNIVERSIDAD AUTÓNOMA METROPOLITANA")
titulo2 = tk.Label(frame2,text="UNIDAD AZCAPOTZALCO")
titulo3 = tk.Label(frame2,text="INGENIERÍA ELÉCTRICA")
titulo4 = tk.Label(frame2,text="")
titulo5 = tk.Label(frame2,text="CÁLCULO DE ARCO ELÉCTRICO")
titulo6 = tk.Label(frame2,text="IEEE 1584-2002 & IEEE 1584-2018")
titulo7 = tk.Label(frame2, text= "Desarrollado por José de Jesús T.M. - Nov 2024")
titulo1.pack()
titulo2.pack()
titulo5.pack()
titulo7.pack()
# <<<<< Texto portada

# ******************** METODO DE CALCULO ********************
# >>>>> LabelFrame Método de cálculo
cont_met = tk.LabelFrame(frame4 , width=300, height=200,text="Método de cálculo", padx=5, pady=5)
cont_met.pack()

# >>>>> RadioButton Método de cálculo
var_radiobutton = tk.IntVar() #Variable de control
var_radiobutton.set(2)  # Selecciona por defecto la opción 2 "IEEE 1584-2018"
show_frame() #Llama a la funcion para que muestre inicialmente la opción 2 "IEEE 1584-2018"
opcion1 = tk.Radiobutton(cont_met, text="IEEE 1584-2002", variable=var_radiobutton, value=1, command=show_frame)
opcion2 = tk.Radiobutton(cont_met, text="IEEE 1584-2018", variable=var_radiobutton, value=2, command=show_frame)
opcion1.pack(side="left")
opcion2.pack(side="right")

################################## DATOS DEL SISTEMA | IEEE 1584 2018 ##################################
# ******************** DATOS DEL SISTEMA | IEEE 1584 2018 ********************
# >>>>> LabelFrame Datos del sistema | IEEE 1584 2018
cont_2018 = tk.LabelFrame(frame6, width=250, height=200, text="Datos del sistema", padx=5, pady=5)
cont_2018.pack(fill='both', expand=True) # Ocupará todo el espacio del contenedor

# >>>>> Variable de control Voltaje del sistema | IEEE 1584 2018
var_entrada_v2018 = tk.StringVar(value=4.160) #value es un valor de origen
# >>>>> Label Voltaje del sistema | IEEE 1584 2018
lb_volt_2018 = tk.Label(cont_2018, text="Voltaje del sistema")
lb_volt_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
# >>>>> Entry Voltaje del sistema | IEEE 1584 2018
entrada_v2018 = tk.Entry(cont_2018, bg="SpringGreen3", font=("Arial", 12), textvariable=var_entrada_v2018, width=25)
entrada_v2018.grid(row=0, column=1, sticky="w", padx=5, pady=5)
# >>>>> Label Voltaje del sistema | IEEE 1584 2018
lb_volt_u_2018 = tk.Label(cont_2018, text="kV")
lb_volt_u_2018.grid(row=0, column=2, sticky="w", padx=5, pady=5)
# >>>>> Trace Voltaje del sistema | IEEE 1584 2018
var_entrada_v2018.trace("w", rellena_typicalequipment_2018) #trace y "w" detectan cuando hay un cambio en la variable texto1

# >>>>> Variable de control Corriente de corto circuito | IEEE 1584 2018
var_icc_2018 = tk.StringVar(value=15)
# >>>>> Label Corriente de corto circuito | IEEE 1584 2018
lb_icc_2018 = tk.Label(cont_2018, text="Corriente de corto circuito")
lb_icc_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
# >>>>> Entry Corriente de corto circuito | IEEE 1584 2018
entrada_icc_2018 = tk.Entry(cont_2018, bg="SpringGreen3", font=("Arial", 12), textvariable=var_icc_2018, width=25)
entrada_icc_2018.grid(row=1, column=1, sticky="w", padx=5, pady=5)
# >>>>> Label Corriente de corto circuito | IEEE 1584 2018
lb_icc_u2018 = tk.Label(cont_2018, text="kA")
lb_icc_u2018.grid(row=1, column=2, sticky="w", padx=5, pady=5)
var_icc_2018.trace("w", verifica_rango_icc_2018)

# >>>>> Variable de control Tipo de equipo | IEEE 1584 2018
var_equipo_2018 = tk.StringVar(value="Switchgear_small") #Valor inicial
# >>>>> Label Tipo de equipo | IEEE 1584 2018
lb_equipo_2018 = tk.Label(cont_2018, text="Tipo de equipo")
lb_equipo_2018.grid(row=2, column=0, sticky="w", padx=5, pady=5) #sticky="w" alinea los Label a la izquierda del espacio asignado (west).
# >>>>> Combobox Tipo de equipo | IEEE 1584 2018
check_equipo_2018 = ttk.Combobox(cont_2018, width=20, font=("Arial", 12), foreground="blue", background="white", textvariable=var_equipo_2018)
check_equipo_2018.grid(row=2, column=1, columnspan=2, sticky="nsew",padx=5, pady=5)
lista_equipo_2018 = ["Switchgear_large", "Switchgear_small", "MCC", "Cable_junction_box_shallow", "Cable_junction_box_deep"]  # Elementos de la lista
check_equipo_2018["values"] = lista_equipo_2018  # Se agrega la lista de elementos usando combobox["values"]
var_equipo_2018.trace("w", rellena_typicaldata_2018) #Sigue los cambios de la variable de control

# ******************** PARAMETROS DE ARCO ELECTRICO | IEEE 1584 2018 ********************
# >>>>> LabelFrame Parámetros de arco eléctrico | IEEE 1584 2018
cont_AF_2018 = tk.LabelFrame(frame6, width=300, height=200, text="Parámetros de arco eléctrico", padx=5, pady=5)
cont_AF_2018.pack(fill='both', expand=True) # Ocupará todo el espacio del contenedor

# >>>>> Variable de control Distancia de trabajo | IEEE 1584 2018
var_dis_2018 = tk.StringVar(value=914.4)
# >>>>> Label Distancia de trabajo | IEEE 1584 2018
lb_dis_2018 = tk.Label(cont_AF_2018, text="Distancia de trabajo")
lb_dis_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
# >>>>> Entry Distancia de trabajo | IEEE 1584 2018
entrada_dis_2018 = tk.Entry(cont_AF_2018, bg="sky blue", font=("Arial", 12), textvariable=var_dis_2018)
entrada_dis_2018.grid(row=0, column=1, sticky="w", padx=5, pady=5)
# >>>>> Label Distancia de trabajo | IEEE 1584 2018
lb_dis_u2018 = tk.Label(cont_AF_2018, text="mm")
lb_dis_u2018.grid(row=0, column=2, sticky="w", padx=5, pady=5)
var_dis_2018.trace("w", verifica_rango_dis_2018)

# >>>>> Variable de control Distancia entre los conductores GAP | IEEE 1584 2018
var_gap_2018 = tk.StringVar(value=104)
# >>>>> Label Distancia entre los conductores GAP | IEEE 1584 2018
lb_gap_2018 = tk.Label(cont_AF_2018, text="Distancia entre los conductores")
lb_gap_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
# >>>>> Entry Distancia entre los conductores GAP | IEEE 1584 2018
entrada_gap_2018 = tk.Entry(cont_AF_2018, bg="sky blue", font=("Arial", 12), textvariable=var_gap_2018)
entrada_gap_2018.grid(row=1, column=1, sticky="w", padx=5, pady=5)
# >>>>> Label Distancia entre los conductores GAP | IEEE 1584 2018
lb_gap_u2018 = tk.Label(cont_AF_2018, text="mm")
lb_gap_u2018.grid(row=1, column=2, sticky="w", padx=5, pady=5)
var_gap_2018.trace("w", verifica_rango_gap_2018) #Sigue los cambios de la variable de control

# ******************** CONFIGURACION DE LOS ELECTRODOS EC | IEEE 1584 2018 ********************
# >>>>> LabelFrame Configuración de los electrodos EC | IEEE 1584 2018
cont_EC_2018 = tk.LabelFrame(cont_AF_2018, width=100, height=50, text="Enclosure type", padx=5, pady=5)
cont_EC_2018.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

# >>>>> RadioButton Configuración de los electrodos EC | IEEE 1584 2018
var_EC = tk.IntVar() #Variable de control
var_EC.set(2)  # Selecciona por defecto la opción 2 "'BOX'"
opcion_EC1 = tk.Radiobutton(cont_EC_2018, text="'OA'", variable=var_EC, value=1, command=show_frame_EC)
opcion_EC2 = tk.Radiobutton(cont_EC_2018, text="'BOX'", variable=var_EC, value=2, command=show_frame_EC)
opcion_EC1.grid(row=0, column=0, sticky="w", padx=5)
opcion_EC2.grid(row=0, column=1, sticky="w", padx=5)

# ******************** CONFIGURACIONES A EVALUAR 'BOX' | IEEE 1584 2018 ********************
# >>>>> LabelFrame Configuraciones a evaluar 'BOX' | IEEE 1584 2018
cont_BOX_2018 = tk.LabelFrame(cont_AF_2018, width=250, height=50, text="Configuración de los electrodos", padx=10, pady=10)
cont_BOX_2018.grid(row=3, column=0, columnspan=3, sticky="nsew",padx=5)
cont_BOX_2018.grid_remove()  # Oculta inicialmente el contenedor "BOX"
#variables de control
variable_VCB = tk.BooleanVar(value=True) #Entregara un booleano True o False dependiendo si esta seleccionado o no
variable_VCBB = tk.BooleanVar(value=False)
variable_HCB = tk.BooleanVar(value=False)
# >>>>> CheckButton Configuraciones a evaluar 'BOX' | IEEE 1584 2018
#con 'variable' asociamos la variable de control
check1 = tk.Checkbutton(cont_BOX_2018, text="VCB",variable=variable_VCB, font=("Arial", 12), fg="blue", bg="lightgray")
check2 = tk.Checkbutton(cont_BOX_2018, text="VCBB",variable=variable_VCBB,font=("Arial", 12), fg="blue", bg="lightgray")
check3 = tk.Checkbutton(cont_BOX_2018, text="HCB",variable=variable_HCB, font=("Arial", 12), fg="blue", bg="lightgray")
check1.grid(row=0, column=0, sticky="w", padx=5)
check2.grid(row=0, column=1, sticky="w", padx=5)
check3.grid(row=0, column=2, sticky="w", padx=5)

# ******************** CONFIGURACIONES A EVALUAR 'OA' | IEEE 1584 2018 ********************
# >>>>> LabelFrame Configuraciones a evaluar 'OA' | IEEE 1584 2018
cont_OA_2018 = tk.LabelFrame(cont_AF_2018, width=250, height=50, text="Configuración de los electrodos", padx=10, pady=10)
cont_OA_2018.grid(row=3, column=0, columnspan=3, sticky="nsew",padx=5)
cont_OA_2018.grid_remove()  # Oculta inicialmente el contenedir "OA"
#variables de control
variable_VOA = tk.BooleanVar()
variable_HOA = tk.BooleanVar()
# >>>>> CheckButton Configuraciones a evaluar 'OA' | IEEE 1584 2018
#con 'variable' asociamos la variable de control
check1 = tk.Checkbutton(cont_OA_2018, text="VOA", variable=variable_VOA, font=("Arial", 12), fg="blue", bg="lightgray")
check2 = tk.Checkbutton(cont_OA_2018, text="HOA", variable=variable_HOA,font=("Arial", 12), fg="blue", bg="lightgray")
check1.grid(row=0, column=0, sticky="w", padx=5)
check2.grid(row=0, column=1, sticky="w", padx=5)

show_frame_EC() #Llama a la funcion para que muestre inicialmente la opción 2 "BOX"

# ******************** ENCLOSURE PARAMETERS | IEEE 1584 2018 ********************
# >>>>> LabelFrame Enclosure parameters | IEEE 1584 2018
cont_enc_2018 = tk.LabelFrame(cont_AF_2018, width=250, height=50, text="Enclosure parameters", padx=5, pady=5)
cont_enc_2018.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5)

# >>>>> Variable de control Height | IEEE 1584 2018
var_h_2018 = tk.StringVar(value=1143)
# >>>>> Label height | IEEE 1584 2018
lb_h_2018 = tk.Label(cont_enc_2018, text="Height")
lb_h_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
# >>>>> Entry height | IEEE 1584 2018
entrada_h = tk.Entry(cont_enc_2018, bg="sky blue", font=("Arial", 12), width=5, textvariable=var_h_2018)
entrada_h.grid(row=0, column=1, sticky="w", pady=5)
# >>>>> Label height | IEEE 1584 2018
lb_h_2018 = tk.Label(cont_enc_2018, text="mm")
lb_h_2018.grid(row=0, column=2, sticky="w", padx=5, pady=5)
var_h_2018.trace("w", verifica_rango_height_2018)

# >>>>> Variable de control Width | IEEE 1584 2018
var_w_2018 = tk.StringVar(value=762)
# >>>>> Label Width | IEEE 1584 2018
lb_w_2018 = tk.Label(cont_enc_2018, text="Width")
lb_w_2018.grid(row=0, column=3, sticky="w", padx=5, pady=5)
# >>>>> Entry Width | IEEE 1584 2018
entrada_w = tk.Entry(cont_enc_2018, bg="sky blue", font=("Arial", 12), width=5, textvariable=var_w_2018)
entrada_w.grid(row=0, column=4, sticky="w", pady=5)
# >>>>> Label Width | IEEE 1584 2018
lb_w_2018 = tk.Label(cont_enc_2018, text="mm")
lb_w_2018.grid(row=0, column=5, sticky="w", padx=5, pady=5)
var_w_2018.trace("w", verifica_rango_width_2018)

# >>>>> Variable de control Depth | IEEE 1584 2018
var_d_2018 = tk.StringVar(value=762)
# >>>>> Label depth | IEEE 1584 2018
lb_d_2018 = tk.Label(cont_enc_2018, text="Depth")
lb_d_2018.grid(row=0, column=6, sticky="w", padx=5, pady=5)
# >>>>> Entry height | IEEE 1584 2018
entrada_d = tk.Entry(cont_enc_2018, bg="sky blue", font=("Arial", 12), width=5, textvariable=var_d_2018)
entrada_d.grid(row=0, column=7, sticky="w", pady=5)
# >>>>> depth height | IEEE 1584 2018
lb_d_2018 = tk.Label(cont_enc_2018, text="mm")
lb_d_2018.grid(row=0, column=8, sticky="w", padx=5, pady=5)


################################## DATOS DEL SISTEMA | IEEE 1584 2002 ##################################
# ******************** DATOS DEL SISTEMA | IEEE 1584 2002 ********************
# >>>>> LabelFrame Datos del sistema | IEEE 1584 2002
cont_2002 = tk.LabelFrame(frame5, width=250, height=200, text="Datos del sistema", padx=5, pady=5)
cont_2002.pack(fill='both', expand=True) # Ocupará todo el espacio del contenedor

# >>>>> Variable de control Voltaje del sistema | IEEE 1584 2002
var_entrada_v2002 = tk.StringVar(value=4.160) #value es un valor de origen
# >>>>> Label Voltaje del sistema | IEEE 1584 2002
lb_volt_2002 = tk.Label(cont_2002, text="Voltaje del sistema")
lb_volt_2002.grid(row=0, column=0, sticky="w", padx=5, pady=5)
# >>>>> Entry Voltaje del sistema | IEEE 1584 2002
entrada_v2002 = tk.Entry(cont_2002, bg="SpringGreen3", font=("Arial", 12), textvariable=var_entrada_v2002)
entrada_v2002.grid(row=0, column=1, sticky="w", padx=5, pady=5)
# >>>>> Label Voltaje del sistema | IEEE 1584 2002
lb_volt_u_2002 = tk.Label(cont_2002, text="kV")
lb_volt_u_2002.grid(row=0, column=2, sticky="w", padx=5, pady=5)
var_entrada_v2002.trace("w", rellena_typicalequipment_2002) #trace y "w" detectan cuando hay un cambio en la variable de control del voltaje

# >>>>> Variable de control Corriente de corto circuito | IEEE 1584 2002
var_icc_2002 = tk.StringVar(value=15)
# >>>>> Label Corriente de corto circuito | IEEE 1584 2002
lb_icc_2002 = tk.Label(cont_2002, text="Corriente de corto circuito")
lb_icc_2002.grid(row=1, column=0, sticky="w", padx=5, pady=5)
# >>>>> Entry Corriente de corto circuito | IEEE 1584 2002
entrada_icc_2002 = tk.Entry(cont_2002, bg="SpringGreen3", font=("Arial", 12), textvariable=var_icc_2002)
entrada_icc_2002.grid(row=1, column=1, sticky="w", padx=5, pady=5)
# >>>>> Label Corriente de corto circuito | IEEE 1584 2002
lb_icc_u2002 = tk.Label(cont_2002, text="kA")
lb_icc_u2002.grid(row=1, column=2, sticky="w", padx=5, pady=5)
var_icc_2002.trace("w", verifica_rango_icc_2002) #Sigue los cambios de la variable de control

# >>>>> Variable de control Tipo de equipo | IEEE 1584 2018
var_equipo_2002 = tk.StringVar(value="Switchgear") #Valor inicial
# >>>>> Label Tipo de equipo | IEEE 1584 2002
lb_equipo_2002 = tk.Label(cont_2002, text="Tipo de equipo")
lb_equipo_2002.grid(row=2, column=0, sticky="w", padx=5, pady=5) #sticky="w" alinea los Label a la izquierda del espacio asignado (west).
# >>>>> Combobox Tipo de equipo | IEEE 1584 2002
check_equipo_2002 = ttk.Combobox(cont_2002, width=20, font=("Arial", 12), foreground="blue", background="white", textvariable=var_equipo_2002)
check_equipo_2002.grid(row=2, column=1, padx=5, pady=5)
lista_equipo_2002 = ["Switchgear", "Cable", "Other_'OA'"]  # Elementos de la lista
check_equipo_2002["values"] = lista_equipo_2002  # Se agrega la lista de elementos usando combobox["values"]
var_equipo_2002.trace("w", rellena_typicaldata_2002) #Sigue los cambios de la variable de control

# >>>>> Variable de control Tipo de equipo | IEEE 1584 2018
var_ground_2002 = tk.StringVar(value="Grounded") #Valor inicial
# >>>>> Label GROUNDING | IEEE 1584 2002
lb_ground_2002 = tk.Label(cont_2002, text="Ground")
lb_ground_2002.grid(row=3, column=0, sticky="w", padx=5, pady=5) #sticky="w" alinea los Label a la izquierda del espacio asignado (west).
# >>>>> Combobox Tipo de Grounding | IEEE 1584 2002
check_ground_2002 = ttk.Combobox(cont_2002, width=20, font=("Arial", 12), foreground="blue", background="white", textvariable=var_ground_2002)
check_ground_2002.grid(row=3, column=1, padx=5, pady=5)
lista_ground_2002 = ["Grounded", "Ungrounded", "High Resistance"]  # Elementos de la lista
check_ground_2002["values"] = lista_ground_2002  # Se agrega la lista de elementos usando combobox["values"]

# ******************** PARAMETROS DE ARCO ELECTRICO | IEEE 1584 2002 ********************
# >>>>> LabelFrame Parámetros de arco eléctrico | IEEE 1584 2002
cont_AF_2002 = tk.LabelFrame(frame5, width=300, height=200, text="Parámetros de arco eléctrico", padx=5, pady=5)
cont_AF_2002.pack(fill='both', expand=True) # Ocupará todo el espacio del contenedor

# >>>>> Variable de control Distancia de trabajo | IEEE 1584 2002
var_dis_2002 = tk.StringVar(value=914.4)
# >>>>> Label Distancia de trabajo | IEEE 1584 2002
lb_dis_2002 = tk.Label(cont_AF_2002, text="Distancia de trabajo")
lb_dis_2002.grid(row=0, column=0, sticky="w", padx=5, pady=5)
# >>>>> Entry Distancia de trabajo | IEEE 1584 2002
entrada_dis_2002 = tk.Entry(cont_AF_2002, bg="sky blue", font=("Arial", 12), textvariable=var_dis_2002)
entrada_dis_2002.grid(row=0, column=1, sticky="w", padx=5, pady=5)
# >>>>> Label Distancia de trabajo | IEEE 1584 2002
lb_dis_u2002 = tk.Label(cont_AF_2002, text="mm")
lb_dis_u2002.grid(row=0, column=2, sticky="w", padx=5, pady=5)

# >>>>> Variable de control Distancia entre los conductores GAP | IEEE 1584 2018
var_gap_2002 = tk.StringVar(value=104)
# >>>>> Label Distancia entre los conductores GAP | IEEE 1584 2002
lb_gap_2002 = tk.Label(cont_AF_2002, text="Distancia entre los conductores")
lb_gap_2002.grid(row=1, column=0, sticky="w", padx=5, pady=5)
# >>>>> Entry Distancia entre los conductores GAP | IEEE 1584 2002
entrada_gap_2002 = tk.Entry(cont_AF_2002, bg="sky blue", font=("Arial", 12), textvariable=var_gap_2002)
entrada_gap_2002.grid(row=1, column=1, sticky="w", padx=5, pady=5)
# >>>>> Label Distancia entre los conductores GAP | IEEE 1584 2002
lb_gap_u2002 = tk.Label(cont_AF_2002, text="mm")
lb_gap_u2002.grid(row=1, column=2, sticky="w", padx=5, pady=5)
var_gap_2002.trace("w", verifica_rango_gap_2002) #Sigue los cambios de la variable de control

# >>>>> Variable de control Factor de distancia X | IEEE 1584 2002   NOTE: LO SIGUIENTE NO SE MUESTRA EN LA PANTALLA, SOLO ES PARA TENER LA VARIABLE DE CONTROL
var_xfactor_2002 = tk.StringVar(value=0.973)
# >>>>> Label Factor de distancia X | IEEE 1584 2002
lb_xfactor_2002 = tk.Label(cont_AF_2002, text="Distancia entre los conductores", textvariable=var_xfactor_2002)
lb_xfactor_2002.grid(row=2, column=0, sticky="w", padx=5, pady=5)
lb_xfactor_2002.grid_remove()  # Oculta "#IEEE 1584-2018"

def ventana_toplevel_2002():
    global ventana_calculo_2002
    # Verifica si la ventana ya está abierta
    if ventana_calculo_2002 is None or not ventana_calculo_2002.winfo_exists():
        ventana_calculo_2002 = Toplevel(ventana)
        ventana_calculo_2002.title("Cálculo arco eléctrico IEEE 1584-2002")
        ventana_calculo_2002.geometry("750x250+60+60")
        ventana_calculo_2002.attributes("-alpha", 0.95)
        # >>>>> Contenedores
        cont_res_2002 = tk.LabelFrame(ventana_calculo_2002,width=300, height=200, padx=20, text="Resultados") #RESULTADOS "2002"
        cont_res_2002.grid(row=0, column=0)

        # ******************** CONTENEDOR RESULTADO | IEEE 1584 2002 ********************
        # >>>>> LabelFrame 2002
        cont_res_ET_2002 = tk.LabelFrame(cont_res_2002, width=150, height=100, text="") #RESULTADOS
        cont_res_ET_2002.grid(row=0, column=0)
        cont_res_ET_2002.config(text=var_equipo_2002.get())
        # >>>>> Contenedor corriente de arco 2002
        res_2002_iarc = tk.Frame(cont_res_ET_2002, width=100, height=100, bd=5, padx=5, background="SkyBlue1") #Calculo con corriente normal
        res_2002_iarc.grid(row=1, column=0)
        # >>>>> Contenedor ARCH FLASH PROTECTION corriente de arco 2002
        res_afp_2002 = tk.Frame(cont_res_ET_2002, width=100, height=100, bd=5, padx=5, background="salmon") #Resultado arc flash protection
        res_afp_2002.grid(row=1, column=1, sticky="ns")
        # >>>>> Contenedor corriente de arco reducida 2002
        res_2002_iarcmin = tk.Frame(cont_res_ET_2002, width=100, height=100, bd=5, padx=5, background="SkyBlue1") #Calculo con corriente reducida
        res_2002_iarcmin.grid(row=1, column=2)
        # >>>>> Contenedor ARCH FLASH PROTECTION corriente de arco minima 2002
        res_afpmin_2002 = tk.Frame(cont_res_ET_2002, width=100, height=100, bd=5, padx=5, background="salmon") #Resultado arc flash protection reducida
        res_afpmin_2002.grid(row=1, column=3, sticky="ns")
        # >>>>> Contenedor % Variacion de corriente de arco
        cont_iarc_varation = tk.LabelFrame(cont_res_ET_2002, width=150, height=50, text="Variación de la corriente de arco Iarc (%)")
        cont_iarc_varation.grid(row=0, column=1, columnspan=2, sticky="nsew")
        #cont_res_ET_2002.grid_columnconfigure(0, weight=1)  # Expande el contenedor en toda la ventana
        cont_iarc_varation.grid_columnconfigure(0, weight=1) # Permite que el control deslizante ocupe todo el ancho dentro del contenedor


        def inicia_primer_calculo_2002():
            #CALCULAR IARC NORMAL | enviar diccionario system_data_HCB
            main_2002(system_data_2002) #Llama a la función que realiza el promer calculo "I_arc"
            # print (system_data_2002)
            var_iarc_2002.set("{:.3f}".format(system_data_2002["I_arc"])) # Usar formato para limitar a 3 decimales
            #Actualiza el valor de Iarc_min
            porcentaje_iarc = float(system_data_2002["I_arc"]) - (float(system_data_2002["I_arc"])*(iarc_variation.get()/100))
            var_iarcmin_2002.set("{:.3f}".format(porcentaje_iarc)) #Muestra el valor de la corriente de arco reducida en la pantalla

        def imprime_datos_sistema_2002():
            print("")
            print("#################### INICIO DATOS DEL SISTEMA ####################")
            print(f"Metodo seleccionado: {AC_metod_valor}")
            print("Tipo de equipo: ", tipo_equipo)
            print("Aterrizado a tierra: ", tipo_ground)
            print("Enclosure Type: ", ET_2002)
            print("Voltaje del sistema: ", Voc)
            print("Corriente de corto circuito: ", I_bf)
            print("Distancia de trabajo: ", dis)
            print("Distancia entre los conductores: ", gap)
            print("Distancia x factor: ", xfactor)
            print("#################### FIN DATOS DEL SISTEMA ####################", "\n")

        def actualiza_tfalla_2002():
            system_data_2002["Tfalla"] = float(var_tfalla_2002.get())/1000 #Obtiene el valor de Tfalla ingresado por el usuario y lo convierte en segundos
            main_afp_2002 (system_data_2002) #Llama a la función que calcula E y AFB
            boton_afpmin_2002.configure(state="active") #Activa el boton 1_2 para calcular la corriente de arco reducida
            var_e_2002.set("{:.3f}".format(system_data_2002["E"])) #Muestra el valor de la energia incidente en la pantalla
            var_afb_2002.set("{:.3f}".format(system_data_2002["AFB"])) #Muestra el valor del limite de arco eléctrico en la pantalla
            EPP = calcula_proteccion_epp(system_data_2002["E"]) #Llama a ala función que calcula la categoría de EPP
            var_epp_2002.set(value=EPP) #Muestra el valor de la categoría de EPP en la pantalla
            # print (system_data_2002)

        def actualiza_tfallamin_2002():
            system_data_2002["I_arc_min"] = var_iarcmin_2002.get() #Se añade el valor de I_arc reducida al diccionario
            system_data_2002["Tfalla_min"] = float(var_tfallamin_2002.get())/1000 #Obtiene el valor de Tfalla ingresado por el usuario y lo convierte en segundos
            main_afpmin_2002 (system_data_2002) #Llama a la función que calcula E y AFB
            var_emin_2002.set("{:.3f}".format(system_data_2002["E_min"])) #Muestra el valor de la energia incidente en la pantalla
            var_afbmin_2002.set("{:.3f}".format(system_data_2002["AFB_min"])) #Muestra el valor del limite de arco eléctrico en la pantalla
            # print (system_data_2002)
            EPP = calcula_proteccion_epp(system_data_2002["E_min"]) #Llama a ala función que calcula la categoría de EPP
            var_eppmin_2002.set(value=EPP) #Muestra el valor de la categoría de EPP en la pantalla

        def actualiza_variacion_Iarc(*args):
            porcentaje_iarc = float(system_data_2002["I_arc"]) - (float(system_data_2002["I_arc"])*(iarc_variation.get()/100))
            var_iarcmin_2002.set("{:.3f}".format(porcentaje_iarc)) #Muestra el valor de la corriente de arco reducida en la pantalla

        # ******************** OBTIENE LOS DATOS DEL SISTEMA INGRESADOS | IEEE 1584 2018 ********************
        # >>>>> Obtiene el metodo de calculo seleccionado IEEE 1584-2002 O IEEE 1584-2018 
        selected_value_metod = var_radiobutton.get() #Obtenemos el valor seleccionado 1 o 2
        AC_metod_valor = dic_metodo.get(selected_value_metod, "Opcion no encontrada") # Se busca en el diccionario el texto 
        tipo_equipo = var_equipo_2002.get() # >>>>> Obtiene el tipo de equipo 
        tipo_ground = var_ground_2002.get() # >>>>> Obtiene el tipo de ground
        Voc = var_entrada_v2002.get() # >>>>> Obtiene el voltaje del sistema
        I_bf = var_icc_2002.get() # >>>>> Obtiene la corriente de corto circuito
        dis = var_dis_2002.get() # >>>>> Obtiene la distancia de trabajo
        gap = var_gap_2002.get() # >>>>> Obtiene la distancia entre los conductores GAP
        xfactor = var_xfactor_2002.get()

        if tipo_equipo == "Other_'OA'":
            ET_2002 = "OA"
        else: ET_2002 = "BOX"

        #Diccionarios base para cada configuración de electrodos
        system_data_2002 = { #BOTON 1
            "ACmetod":AC_metod_valor, # Metodo de calculo elegido
            "tipo_equipo": tipo_equipo, #Tipo de equipo seleccionado
            "ET": ET_2002, #Enclosure type
            "ground": tipo_ground, #Tipo de grounding
            "Voc": Voc, #kV rms | voltaje del sistema trifasico
            "I_bf": I_bf,  #kA symm rms | Three-phase bolted fault current
            "dis": dis, #mm | distancia de trabajo
            "gap": gap, #mm | espacio entre los conductores (electrodos)
            "xfactor": xfactor # Distancia x factor
            }
        
        ################################## RESULTADOS | IEEE 1584 2002 ##################################
        # ******************** CONTENEDOR RESULTADO corriente de arco | IEEE 1584 2002 ********************
        # >>>>> Variable de control Corriente de arco | IEEE 1584 2002
        var_iarc_2002 = tk.StringVar() #value es un valor de origen
        # >>>>> Label Corriente de arco | IEEE 1584 2002
        lb_iarc_2002 = tk.Label(res_2002_iarc, text="Iarc: ")
        lb_iarc_2002.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # >>>>> Label Corriente de arco | IEEE 1584 2002
        lb_iarc_2002_res = tk.Label(res_2002_iarc, textvariable=var_iarc_2002)
        lb_iarc_2002_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        # >>>>> Label Corriente de arco | IEEE 1584 2002
        lb_iarc_2002_u = tk.Label(res_2002_iarc, text="kA")
        lb_iarc_2002_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

        # >>>>> Variable de control Liberacion de la falla | IEEE 1584 2002
        var_tfalla_2002 = tk.StringVar(value=100) #value es un valor de origen
        # >>>>> Label Liberacion de la falla | IEEE 1584 2002
        lb_tfalla_2002 = tk.Label(res_2002_iarc, text="T: ")
        lb_tfalla_2002.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        # >>>>> Entry Liberacion de la falla | IEEE 1584 2002
        entrada_tfalla_2002 = tk.Entry(res_2002_iarc, bg="SpringGreen3", font=("Arial", 12), width=6, textvariable=var_tfalla_2002)
        entrada_tfalla_2002.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # >>>>> Label Liberacion de la falla | IEEE 1584 2002
        lb_tfalla_2002_u = tk.Label(res_2002_iarc, text="ms")
        lb_tfalla_2002_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)
        # >>>>> BOTON Liberacion de la falla | IEEE 1584 2002
        boton_afp_2002 = tk.Button(res_2002_iarc, text="Calcular", background="green", command= actualiza_tfalla_2002)
        boton_afp_2002.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5)

        # ******************** CONTENEDOR RESULTADO arc flash protection | IEEE 1584 2002 ********************
        # >>>>> Variable de control de Energía incidente | IEEE 1584 2002
        var_e_2002 = tk.StringVar() #value es un valor de origen
        # >>>>> Label Energía incidente | IEEE 1584 2002
        lb_e_2002 = tk.Label(res_afp_2002, text="E: ")
        lb_e_2002.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # >>>>> Label Energía incidente | IEEE 1584 2002
        lb_e_2002_res = tk.Label(res_afp_2002, textvariable=var_e_2002, width=7)
        lb_e_2002_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        # >>>>> Label Energía incidente | IEEE 1584 2002
        lb_e_2002_u = tk.Label(res_afp_2002, text="cal/cm2")
        lb_e_2002_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

        # >>>>> Variable de control de Limite de arco electrico | AFB | IEEE 1584 2002
        var_afb_2002 = tk.StringVar() #value es un valor de origen
        # >>>>> Label Limite de arco electrico | IEEE 1584 2002
        lb_afb_2002 = tk.Label(res_afp_2002, text="AFB: ")
        lb_afb_2002.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        # >>>>> Label Limite de arco electrico | IEEE 1584 2002
        lb_afb_2002_res = tk.Label(res_afp_2002, textvariable=var_afb_2002, width=7)
        lb_afb_2002_res.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        # >>>>> Label Limite de arco electrico | IEEE 1584 2002
        lb_afb_2002_u = tk.Label(res_afp_2002, text="mm")
        lb_afb_2002_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)

        # >>>>> Variable de control de Equipo de protección personal | EPP | IEEE 1584 2002
        var_epp_2002 = tk.StringVar()
        # >>>>> Label EPP | IEEE 1584 2002
        lb_epp_2002 = tk.Label(res_afp_2002, text="Categoría EPP: ")
        lb_epp_2002.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        # >>>>> Label EPP | IEEE 1584 2002
        lb_epp_2002_res = tk.Label(res_afp_2002, textvariable=var_epp_2002, width=5)
        lb_epp_2002_res.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        iarc_variation = tk.DoubleVar(value=15.0)
        #tk.Scale es la funciona para activar el modo deslizante
        #variable es el valor inicial a tomar
        #resolution es de cuanto en cuanto se mueve la barra
        control_deslizante = tk.Scale(cont_iarc_varation, variable=iarc_variation, from_=0, to=15, resolution=0.10, orient=tk.HORIZONTAL)
        control_deslizante.grid(row=0, column=0, sticky="ew", padx=5)
        iarc_variation.trace("w", actualiza_variacion_Iarc)
        
        # ******************** CONTENEDOR RESULTADO corriente de arco reducida | IEEE 1584 2002 ********************
        # >>>>> Variable de control Corriente de arco reducida | IEEE 1584 2002
        var_iarcmin_2002 = tk.StringVar() #value es un valor de origen
        # >>>>> Label Corriente de arco reducida | IEEE 1584 2002
        lb_iarcmin_2002 = tk.Label(res_2002_iarcmin, text="Iarcmin: ")
        lb_iarcmin_2002.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # >>>>> Label Corriente de arco reducida | IEEE 1584 2002
        lb_iarcmin_2002_res = tk.Label(res_2002_iarcmin, textvariable=var_iarcmin_2002, width=5)
        lb_iarcmin_2002_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        # >>>>> Label Corriente de arco reducida | IEEE 1584 2002
        lb_iarcmin_2002_u = tk.Label(res_2002_iarcmin, text="kA")
        lb_iarcmin_2002_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

        # >>>>> Variable de control Liberacion de la falla reducida | IEEE 1584 2002
        var_tfallamin_2002 = tk.StringVar(value=100) #value es un valor de origen
        # >>>>> Label Liberacion de la falla reducida | IEEE 1584 2002
        lb_tfallamin_2002 = tk.Label(res_2002_iarcmin, text="T: ")
        lb_tfallamin_2002.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        # >>>>> Entry Liberacion de la falla reducida | IEEE 1584 2002
        entrada_tfallamin_2002 = tk.Entry(res_2002_iarcmin, bg="SpringGreen3", font=("Arial", 12), width=6, textvariable=var_tfallamin_2002)
        entrada_tfallamin_2002.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        # >>>>> Label Liberacion de la falla reducida | IEEE 1584 2002
        lb_tfallamin_2002_u = tk.Label(res_2002_iarcmin, text="ms")
        lb_tfallamin_2002_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)
        # >>>>> BOTON Liberacion de la falla reducida | IEEE 1584 2002
        boton_afpmin_2002 = tk.Button(res_2002_iarcmin, text="Calcular", background="green", command=actualiza_tfallamin_2002, state="disabled")
        boton_afpmin_2002.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5)

        # ******************** CONTENEDOR RESULTADO arc flash protection reducida | IEEE 1584 2002 ********************
        # >>>>> Variable de control de Energía incidente | IEEE 1584 2002
        var_emin_2002 = tk.StringVar() #value es un valor de origen
        # >>>>> Label Energía incidente reducida | IEEE 1584 2002
        lb_emin_2002 = tk.Label(res_afpmin_2002, text="E: ")
        lb_emin_2002.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # >>>>> Label Energía incidente reducida | IEEE 1584 2002
        lb_emin_2002_res = tk.Label(res_afpmin_2002, textvariable=var_emin_2002, width=7)
        lb_emin_2002_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        # >>>>> Label Energía incidente reducida | IEEE 1584 2002
        lb_emin_2002_u = tk.Label(res_afpmin_2002, text="cal/cm2")
        lb_emin_2002_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

        # >>>>> Variable de control de Limite de arco electrico | AFB | IEEE 1584 2002
        var_afbmin_2002 = tk.StringVar() #value es un valor de origen
        # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2002
        lb_afbmin_2002 = tk.Label(res_afpmin_2002, text="AFB: ")
        lb_afbmin_2002.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2002
        lb_afbmin_2002_res = tk.Label(res_afpmin_2002, textvariable=var_afbmin_2002, width=7)
        lb_afbmin_2002_res.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2002
        lb_afbmin_2002_u = tk.Label(res_afpmin_2002, text="mm")
        lb_afbmin_2002_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)

        # >>>>> Variable de control de Equipo de protección personal | EPP | IEEE 1584 2002
        var_eppmin_2002 = tk.StringVar()
        # >>>>> Label EPP | IEEE 1584 2002
        lb_eppmin_2002 = tk.Label(res_afpmin_2002, text="Categoría EPP: ")
        lb_eppmin_2002.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        # >>>>> Label EPP | IEEE 1584 2002
        lb_eppmin_2002_res = tk.Label(res_afpmin_2002, textvariable=var_eppmin_2002, width=5)
        lb_eppmin_2002_res.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        imprime_datos_sistema_2002() #Llama a la funcion que imprime los datos del sistema ingresados
        inicia_primer_calculo_2002()

def ventana_toplevel_2018():
    global ventana_calculo_2018
    # Verifica si la ventana ya está abierta
    if ventana_calculo_2018 is None or not ventana_calculo_2018.winfo_exists():
        ventana_calculo_2018 = Toplevel(ventana)
        ventana_calculo_2018.title("Cálculo arco eléctrico IEEE 1584-2018")
        ventana_calculo_2018.geometry("750x420+60+60")
        ventana_calculo_2018.attributes("-alpha", 0.95)
        # >>>>> Contenedores
        cont_res_oa = tk.LabelFrame(ventana_calculo_2018, width=300, height=200, padx=20, text="Resultados") #RESULTADOS "OA"
        cont_res_oa.grid(row=0, column=0)

        cont_res_box = tk.LabelFrame(ventana_calculo_2018, width=300, height=200, padx=20, text="Resultados") #RESULTADOS "BOX"
        cont_res_box.grid(row=0, column=0)
        
        # ******************** CONTENEDOR RESULTADO VOA | IEEE 1584 2018 ********************
        # >>>>> LabelFrame VCB
        cont_res_voa = tk.LabelFrame(cont_res_oa, width=150, height=100, text="Enclosure type: VOA") #RESULTADOS "BOX"
        cont_res_voa.grid(row=0, column=0)
        # >>>>> Contenedor corriente de arco VOA
        res_voa_iarc = tk.Frame(cont_res_voa, width=100, height=100, bd=5, padx=5, background="SkyBlue1") #Calculo con corriente normal
        res_voa_iarc.grid(row=0, column=0)
        # >>>>> Contenedor ARCH FLASH PROTECTION corriente de arco VOA
        res_afp_voa = tk.Frame(cont_res_voa, width=100, height=100, bd=5, padx=5, background="salmon") #Resultado arc flash protection
        res_afp_voa.grid(row=0, column=1, sticky="ns")
        # >>>>> Contenedor corriente de arco reducida VCB
        res_voa_iarcmin = tk.Frame(cont_res_voa, width=100, height=100, bd=5, padx=5, background="SkyBlue1") #Calculo con corriente reducida
        res_voa_iarcmin.grid(row=0, column=2)
        # >>>>> Contenedor ARCH FLASH PROTECTION corriente de arco minima VOA
        res_afpmin_voa = tk.Frame(cont_res_voa, width=100, height=100, bd=5, padx=5, background="salmon") #Resultado arc flash protection reducida
        res_afpmin_voa.grid(row=0, column=3, sticky="ns")

        # ******************** CONTENEDOR RESULTADO HOA | IEEE 1584 2018 ********************
        # >>>>> LabelFrame HOA
        cont_res_hoa = tk.LabelFrame(cont_res_oa, width=150, height=100, text="Enclosure type: HOA") #RESULTADOS "BOX"
        cont_res_hoa.grid(row=1, column=0)
        # >>>>> Contenedor corriente de arco VCB
        res_hoa_iarc = tk.Frame(cont_res_hoa, width=100, height=100, bd=5, padx=5, background="SkyBlue1") #Calculo con corriente normal
        res_hoa_iarc.grid(row=0, column=0)
        # >>>>> Contenedor ARCH FLASH PROTECTION corriente de arco VCB
        res_afp_hoa = tk.Frame(cont_res_hoa, width=100, height=100, bd=5, padx=5, background="salmon") #Resultado arc flash protection
        res_afp_hoa.grid(row=0, column=1, sticky="ns")
        # >>>>> Contenedor corriente de arco reducida VCB
        res_hoa_iarcmin = tk.Frame(cont_res_hoa, width=100, height=100, bd=5, padx=5, background="SkyBlue1") #Calculo con corriente reducida
        res_hoa_iarcmin.grid(row=0, column=2)
        # >>>>> Contenedor ARCH FLASH PROTECTION corriente de arco minima VCB
        res_afpmin_hoa = tk.Frame(cont_res_hoa, width=100, height=100, bd=5, padx=5, background="salmon") #Resultado arc flash protection reducida
        res_afpmin_hoa.grid(row=0, column=3, sticky="ns") #sticky="ns" Ocupara todo el espacio Norte-Sur "verticalmente" 

        # ******************** CONTENEDOR RESULTADO VCB | IEEE 1584 2018 ********************
        # >>>>> LabelFrame VCB
        cont_res_vcb = tk.LabelFrame(cont_res_box, width=150, height=100, text="Enclosure type: VCB") #RESULTADOS "BOX"
        cont_res_vcb.grid(row=0, column=0)
        # >>>>> Contenedor corriente de arco VCB
        res_vcb_iarc = tk.Frame(cont_res_vcb, width=100, height=100, bd=5, padx=5, background="SkyBlue1") #Calculo con corriente normal
        res_vcb_iarc.grid(row=0, column=0)
        # >>>>> Contenedor ARCH FLASH PROTECTION corriente de arco VCB
        res_afp_vcb = tk.Frame(cont_res_vcb, width=100, height=100, bd=5, padx=5, background="salmon") #Resultado arc flash protection
        res_afp_vcb.grid(row=0, column=1, sticky="ns")
        # >>>>> Contenedor corriente de arco reducida VCB
        res_vcb_iarcmin = tk.Frame(cont_res_vcb, width=100, height=100, bd=5, padx=5, background="SkyBlue1") #Calculo con corriente reducida
        res_vcb_iarcmin.grid(row=0, column=2)
        # >>>>> Contenedor ARCH FLASH PROTECTION corriente de arco minima VCB
        res_afpmin_vcb = tk.Frame(cont_res_vcb, width=100, height=100, bd=5, padx=5, background="salmon") #Resultado arc flash protection reducida
        res_afpmin_vcb.grid(row=0, column=3, sticky="ns")

        # ******************** CONTENEDOR RESULTADO VCBB | IEEE 1584 2018 ********************
        # >>>>> LabelFrame VCBB
        cont_res_vcbb = tk.LabelFrame(cont_res_box, width=150, height=100, text="Enclosure type: VCBB") #RESULTADOS "BOX"
        cont_res_vcbb.grid(row=1, column=0)
        # >>>>> Contenedor corriente de arco VCBB
        res_vcbb_iarc = tk.Frame(cont_res_vcbb, width=100, height=100, bd=5, padx=5, background="SkyBlue1") #Calculo con corriente normal
        res_vcbb_iarc.grid(row=0, column=0)
        # >>>>> Contenedor ARCH FLASH PROTECTION corriente de arco VCB
        res_afp_vcbb = tk.Frame(cont_res_vcbb, width=100, height=100, bd=5, padx=5, background="salmon") #Resultado arc flash protection
        res_afp_vcbb.grid(row=0, column=1, sticky="ns")
        # >>>>> Contenedor corriente de arco reducida VCBB
        res_vcbb_iarcmin = tk.Frame(cont_res_vcbb, width=100, height=100, bd=5, padx=5, background="SkyBlue1") #Calculo con corriente reducida
        res_vcbb_iarcmin.grid(row=0, column=2)
        # >>>>> Contenedor ARCH FLASH PROTECTION corriente de arco minima VCBB
        res_afpmin_vcbb = tk.Frame(cont_res_vcbb, width=100, height=100, bd=5, padx=5, background="salmon") #Resultado arc flash protection reducida
        res_afpmin_vcbb.grid(row=0, column=3, sticky="ns")

        # ******************** CONTENEDOR RESULTADO HCB | IEEE 1584 2018 ********************
        # >>>>> LabelFrame HCB
        cont_res_hcb = tk.LabelFrame(cont_res_box, width=150, height=100, text="Enclosure type: HCB") #RESULTADOS "BOX"
        cont_res_hcb.grid(row=2, column=0)
        # >>>>> Contenedor corriente de arco HCB
        res_hcb_iarc = tk.Frame(cont_res_hcb, width=100, height=100, bd=5, padx=5, background="SkyBlue1") #Calculo con corriente normal
        res_hcb_iarc.grid(row=0, column=0)
        # >>>>> Contenedor ARCH FLASH PROTECTION corriente de arco VCB
        res_afp_hcb = tk.Frame(cont_res_hcb, width=100, height=100, bd=5, padx=5, background="salmon") #Resultado arc flash protection
        res_afp_hcb.grid(row=0, column=1, sticky="ns")
        # >>>>> Contenedor corriente de arco reducida HCB
        res_hcb_iarcmin = tk.Frame(cont_res_hcb, width=100, height=100, bd=5, padx=5, background="SkyBlue1") #Calculo con corriente reducida
        res_hcb_iarcmin.grid(row=0, column=2)
        # >>>>> Contenedor ARCH FLASH PROTECTION corriente de arco minima HCB
        res_afpmin_hcb = tk.Frame(cont_res_hcb, width=100, height=100, bd=5, padx=5, background="salmon") #Resultado arc flash protection reducida
        res_afpmin_hcb.grid(row=0, column=3, sticky="ns")

        #Funciones llamadas por BOTONES
        def actualiza_tfalla_voa_2018(*args): #BOTON 1_1
            system_data_VOA["Tfalla"] = var_tfalla_voa_2018.get() #Obtiene l valor de Tfalla ingresado por el usuario
            main_afp (system_data_VOA) #Llama a la función que calcula E y AFB
            boton_1_2.configure(state="active") #Activa el boton 1_2 para calcular la corriente de arco reducida
            var_iarcmin_voa_2018.set("{:.3f}".format(system_data_VOA["I_arc_min"])) #Muestra el valor de la corriente de arco reducida en la pantalla
            var_e_voa_2018.set("{:.3f}".format(system_data_VOA["E"])) #Muestra el valor de la energia incidente en la pantalla
            var_afb_voa_2018.set("{:.3f}".format(system_data_VOA["AFB"])) #Muestra el valor del limite de arco eléctrico en la pantalla
            EPP = calcula_proteccion_epp(system_data_VOA["E"]) #Llama a la función que calcula la categoría de EPP
            var_epp_voa_2018.set(value=EPP) #Muestra el valor de la categoría de EPP en la pantalla

        def actualiza_tfallamin_voa_2018(*args): #BOTON 1_2
            system_data_VOA["Tfalla_min"] = var_tfallamin_voa_2018.get() #Obtiene l valor de Tfalla_min ingresado por el usuario
            main_afp_min (system_data_VOA)
            var_emin_voa_2018.set("{:.3f}".format(system_data_VOA["E_min"])) #Muestra el valor de la energia incidente en la pantalla
            var_afbmin_voa_2018.set("{:.3f}".format(system_data_VOA["AFB_min"])) #Muestra el valor del limite de arco eléctrico en la pantalla
            EPP = calcula_proteccion_epp(system_data_VOA["E_min"]) #Llama a ala función que calcula la categoría de EPP
            var_eppmin_voa_2018.set(value=EPP) #Muestra el valor de la categoría de EPP en la pantalla

        def actualiza_tfalla_hoa_2018(*args): #BOTON 2_1
            system_data_HOA["Tfalla"] = var_tfalla_hoa_2018.get() #Obtiene l valor de Tfalla ingresado por el usuario
            main_afp (system_data_HOA) #Llama a la función que calcula E y AFB
            boton_2_2.configure(state="active") #Activa el boton 2_2 para calcular la corriente de arco reducida
            var_iarcmin_hoa_2018.set("{:.3f}".format(system_data_HOA["I_arc_min"])) #Muestra el valor de la corriente de arco reducida en la pantalla
            var_e_hoa_2018.set("{:.3f}".format(system_data_HOA["E"])) #Muestra el valor de la energia incidente en la pantalla
            var_afb_hoa_2018.set("{:.3f}".format(system_data_HOA["AFB"])) #Muestra el valor del limite de arco eléctrico en la pantalla
            EPP = calcula_proteccion_epp(system_data_HOA["E"]) #Llama a ala función que calcula la categoría de EPP
            var_epp_hoa_2018.set(value=EPP) #Muestra el valor de la categoría de EPP en la pantalla

        def actualiza_tfallamin_hoa_2018(*args): #BOTON 2_2
            system_data_HOA["Tfalla_min"] = var_tfallamin_hoa_2018.get() #Obtiene l valor de Tfalla_min ingresado por el usuario
            main_afp_min (system_data_HOA)
            var_emin_hoa_2018.set("{:.3f}".format(system_data_HOA["E_min"])) #Muestra el valor de la energia incidente en la pantalla
            var_afbmin_hoa_2018.set("{:.3f}".format(system_data_HOA["AFB_min"])) #Muestra el valor del limite de arco eléctrico en la pantalla
            EPP = calcula_proteccion_epp(system_data_HOA["E_min"]) #Llama a ala función que calcula la categoría de EPP
            var_eppmin_hoa_2018.set(value=EPP) #Muestra el valor de la categoría de EPP en la pantalla
        
        #Funciones llamadas por BOTONES
        def actualiza_tfalla_vcb_2018(*args): #BOTON 3
            system_data_VCB["Tfalla"] = var_tfalla_vcb_2018.get() #Obtiene el valor de Tfalla ingresado por el usuario
            main_afp (system_data_VCB) #Llama a la función que calcula E y AFB
            boton_4.configure(state="active") #Activa el botn 4 para calcular la corriente de arco reducida
            var_iarcmin_vcb_2018.set("{:.3f}".format(system_data_VCB["I_arc_min"])) #Muestra el valor de la corriente de arco reducida en la pantalla
            var_e_vcb_2018.set("{:.3f}".format(system_data_VCB["E"])) #Muestra el valor de la energia incidente en la pantalla
            var_afb_vcb_2018.set("{:.3f}".format(system_data_VCB["AFB"])) #Muestra el valor del limite de arco eléctrico en la pantalla
            EPP = calcula_proteccion_epp(system_data_VCB["E"]) #Llama a ala función que calcula la categoría de EPP
            var_epp_vcb_2018.set(value=EPP) #Muestra el valor de la categoría de EPP en la pantalla


        def actualiza_tfallamin_vcb_2018(*args): #BOTON 4
            system_data_VCB["Tfalla_min"] = var_tfallamin_vcb_2018.get() #Obtiene l valor de Tfalla_min ingresado por el usuario
            main_afp_min (system_data_VCB)
            var_emin_vcb_2018.set("{:.3f}".format(system_data_VCB["E_min"])) #Muestra el valor de la energia incidente en la pantalla
            var_afbmin_vcb_2018.set("{:.3f}".format(system_data_VCB["AFB_min"])) #Muestra el valor del limite de arco eléctrico en la pantalla
            EPP = calcula_proteccion_epp(system_data_VCB["E_min"]) #Llama a ala función que calcula la categoría de EPP
            var_eppmin_vcb_2018.set(value=EPP) #Muestra el valor de la categoría de EPP en la pantalla
        
        def actualiza_tfalla_vcbb_2018(*args): #BOTON 5
            system_data_VCBB["Tfalla"] = var_tfalla_vcbb_2018.get() #Obtiene l valor de Tfalla ingresado por el usuario
            main_afp (system_data_VCBB) #Llama a la función que calcula E y AFB
            boton_6.configure(state="active") #Activa el boton 6 para calcular la corriente de arco reducida
            var_iarcmin_vcbb_2018.set("{:.3f}".format(system_data_VCBB["I_arc_min"])) #Muestra el valor de la corriente de arco reducida en la pantalla
            var_e_vcbb_2018.set("{:.3f}".format(system_data_VCBB["E"])) #Muestra el valor de la energia incidente en la pantalla
            var_afb_vcbb_2018.set("{:.3f}".format(system_data_VCBB["AFB"])) #Muestra el valor del limite de arco eléctrico en la pantalla
            EPP = calcula_proteccion_epp(system_data_VCBB["E"]) #Llama a ala función que calcula la categoría de EPP
            var_epp_vcbb_2018.set(value=EPP) #Muestra el valor de la categoría de EPP en la pantalla

        def actualiza_tfallamin_vcbb_2018(*args): #BOTON 6
            system_data_VCBB["Tfalla_min"] = var_tfallamin_vcbb_2018.get() #Obtiene l valor de Tfalla_min ingresado por el usuario
            main_afp_min (system_data_VCBB)
            var_emin_vcbb_2018.set("{:.3f}".format(system_data_VCBB["E_min"])) #Muestra el valor de la energia incidente en la pantalla
            var_afbmin_vcbb_2018.set("{:.3f}".format(system_data_VCBB["AFB_min"])) #Muestra el valor del limite de arco eléctrico en la pantalla
            EPP = calcula_proteccion_epp(system_data_VCBB["E_min"]) #Llama a ala función que calcula la categoría de EPP
            var_eppmin_vcbb_2018.set(value=EPP) #Muestra el valor de la categoría de EPP en la pantalla
        
        def actualiza_tfalla_hcb_2018(*args): #BOTON 7
            system_data_HCB["Tfalla"] = var_tfalla_hcb_2018.get() #Obtiene l valor de Tfalla ingresado por el usuario
            main_afp (system_data_HCB) #Llama a la función que calcula E y AFB
            boton_8.configure(state="active") #Activa el botn 4 para calcular la corriente de arco reducida
            var_iarcmin_hcb_2018.set("{:.3f}".format(system_data_HCB["I_arc_min"])) #Muestra el valor de la corriente de arco reducida en la pantalla
            var_e_hcb_2018.set("{:.3f}".format(system_data_HCB["E"])) #Muestra el valor de la energia incidente en la pantalla
            var_afb_hcb_2018.set("{:.3f}".format(system_data_HCB["AFB"])) #Muestra el valor del limite de arco eléctrico en la pantalla
            EPP = calcula_proteccion_epp(system_data_HCB["E"]) #Llama a ala función que calcula la categoría de EPP
            var_epp_hcb_2018.set(value=EPP) #Muestra el valor de la categoría de EPP en la pantalla

        def actualiza_tfallamin_hcb_2018(*args): #BOTON 8
            system_data_HCB["Tfalla_min"] = var_tfallamin_hcb_2018.get() #Obtiene l valor de Tfalla_min ingresado por el usuario
            main_afp_min (system_data_HCB)
            var_emin_hcb_2018.set("{:.3f}".format(system_data_HCB["E_min"])) #Muestra el valor de la energia incidente en la pantalla
            var_afbmin_hcb_2018.set("{:.3f}".format(system_data_HCB["AFB_min"])) #Muestra el valor del limite de arco eléctrico en la pantalla
            EPP = calcula_proteccion_epp(system_data_HCB["E_min"]) #Llama a ala función que calcula la categoría de EPP
            var_eppmin_hcb_2018.set(value=EPP) #Muestra el valor de la categoría de EPP en la pantalla
        
        def imprime_datos_sistema():
            print("")
            print("#################### INICIO DATOS DEL SISTEMA ####################")
            print(f"Metodo seleccionado: {AC_metod_valor}")
            print("Tipo de equipo: ", tipo_equipo)
            print("Voltaje del sistema: ", Voc)
            print("Corriente de corto circuito: ", I_bf)
            print("Distancia de trabajo: ", dis)
            print("Distancia entre los conductores: ", gap)
            print(f"Enclosure type: {ET}")
            print ("VOA: ", variable_VOA.get())
            print ("HOA: ",variable_HOA.get())
            print ("VCB: ",variable_VCB.get())
            print ("VCBB: ",variable_VCBB.get())
            print ("HCB: ",variable_HCB.get())
            print("Width: ", width)
            print("Height: ", height)
            print("Depth: ", depth)
            print ("#################### FIN DATOS DEL SISTEMA ####################", "\n")
        
        def inicia_primer_calculo_OA():
            if variable_VOA.get() == False:
                cont_res_voa.grid_remove() #Remueve el contenedor resultado de "VOA"
            if variable_VOA.get() == True:
                #CALCULAR IARC NORMAL | enviar diccionario system_data_VOA
                main(system_data_VOA)
                # print (system_data_VOA)
                var_iarc_voa_2018.set("{:.3f}".format(system_data_VOA["I_arc"])) # Usar formato para limitar a 3 decimales

            if variable_HOA.get() == False:
                cont_res_hoa.grid_remove() #Remueve el contenedor resultado de "HOA"
            if variable_HOA.get() == True:
                #CALCULAR IARC NORMAL | enviar diccionario system_data_HOA
                main(system_data_HOA)
                # print (system_data_HOA)
                var_iarc_hoa_2018.set("{:.3f}".format(system_data_HOA["I_arc"])) # Usar formato para limitar a 3 decimales
        
        def inicia_primer_calculo_BOX():
            #DETERMINA QUE CONFIGURACIONES MOSTRAR EN BASE A LAS SELECCIONADA EN LA VENTANA PRINCIPAL
            if variable_VCB.get() == False:
                cont_res_vcb.grid_remove()
            if variable_VCB.get() == True:
                #CALCULAR IARC NORMAL | enviar diccionario system_data_VCB
                main(system_data_VCB)
                # print (system_data_VCB)
                var_iarc_vcb_2018.set("{:.3f}".format(system_data_VCB["I_arc"])) # Usar formato para limitar a 3 decimales

            if variable_VCBB.get() == False:
                cont_res_vcbb.grid_remove()
            if variable_VCBB.get() == True:
                #CALCULAR IARC NORMAL | enviar diccionario system_data_VCBB
                main(system_data_VCBB)
                # print (system_data_VCBB)
                var_iarc_vcbb_2018.set("{:.3f}".format(system_data_VCBB["I_arc"])) # Usar formato para limitar a 3 decimales

            if variable_HCB.get() == False:
                cont_res_hcb.grid_remove()
            if variable_HCB.get() == True:
                #CALCULAR IARC NORMAL | enviar diccionario system_data_HCB
                main(system_data_HCB)
                # print (system_data_HCB)
                var_iarc_hcb_2018.set("{:.3f}".format(system_data_HCB["I_arc"])) # Usar formato para limitar a 3 decimales

        # ******************** OBTIENE LOS DATOS DEL SISTEMA INGRESADOS | IEEE 1584 2018 ********************
        # >>>>> Obtiene el metodo de calculo seleccionado IEEE 1584-2002 O IEEE 1584-2018 
        selected_value_metod = var_radiobutton.get() #Obtenemos el valor seleccionado 1 o 2
        AC_metod_valor = dic_metodo.get(selected_value_metod, "Opcion no encontrada") # Se busca en el diccionario el texto 
        tipo_equipo = var_equipo_2018.get() # >>>>> Obtiene el tipo de equipo 
        Voc = var_entrada_v2018.get() # >>>>> Obtiene el voltaje del sistema
        I_bf = var_icc_2018.get() # >>>>> Obtiene la corriente de corto circuito
        dis = var_dis_2018.get() # >>>>> Obtiene la distancia de trabajo
        gap = var_gap_2018.get() # >>>>> Obtiene la distancia entre los conductores GAP
        selectec_value_ET = var_EC.get() # >>>>> Obtiene el Enclosure type | 1="OA" o 2="BOX"
        ET = dic_ET.get(selectec_value_ET, "Opcion no encontrada") 
        width = var_w_2018.get() # >>>>> Obtiene el width
        height = var_h_2018.get() # >>>>> Obtiene el height        
        depth = var_d_2018.get() # >>>>> Obtiene el depth

        imprime_datos_sistema() #Llama a la funcion que imprime los datos del sistema ingresados

        #Diccionarios base para cada configuración de electrodos
        system_data_VOA = { #BOTON 1
            "ACmetod":AC_metod_valor, # Metodo de calculo elegido
            "tipo_equipo": tipo_equipo, #Tipo de equipo seleccionado
            "Voc": Voc, #kV rms | voltaje del sistema trifasico
            "I_bf": I_bf,  #kA symm rms | Three-phase bolted fault current
            "dis": dis, #mm | distancia de trabajo
            "gap": gap, #mm | espacio entre los conductores (electrodos)
            "ET": "OA", #Enclosure type
            "EC": "VOA", #Configuracion de los electrodos (VCB, VCBB, HCB, VOA, HOA)
            "width": width, #mm | ancho del gabinete
            "height":height, #mm | altura del gabinete
            "depth": depth #mm | profundidad del gabinete
            }
        system_data_HOA = { #BOTON 2
            "ACmetod":AC_metod_valor, # Metodo de calculo elegido
            "tipo_equipo": tipo_equipo, #Tipo de equipo seleccionado
            "Voc": Voc, #kV rms | voltaje del sistema trifasico
            "I_bf": I_bf,  #kA symm rms | Three-phase bolted fault current
            "dis": dis, #mm | distancia de trabajo
            "gap": gap, #mm | espacio entre los conductores (electrodos)
            "ET": "OA", #Enclosure type
            "EC": "HOA", #Configuracion de los electrodos (VCB, VCBB, HCB, VOA, HOA)
            "width": width, #mm | ancho del gabinete
            "height":height, #mm | altura del gabinete
            "depth": depth #mm | profundidad del gabinete
            }
        system_data_VCB = { #BOTON 3,4
            "ACmetod":AC_metod_valor, # Metodo de calculo elegido
            "tipo_equipo": tipo_equipo, #Tipo de equipo seleccionado
            "Voc": Voc, #kV rms | voltaje del sistema trifasico
            "I_bf": I_bf,  #kA symm rms | Three-phase bolted fault current
            "dis": dis, #mm | distancia de trabajo
            "gap": gap, #mm | espacio entre los conductores (electrodos)
            "ET": "BOX", #Enclosure type
            "EC": "VCB", #Configuracion de los electrodos (VCB, VCBB, HCB, VOA, HOA)
            "width": width, #mm | ancho del gabinete
            "height":height, #mm | altura del gabinete
            "depth": depth, #mm | profundidad del gabinete
            }
        system_data_VCBB = { #BOTON 5,6
            "ACmetod":AC_metod_valor, # Metodo de calculo elegido
            "tipo_equipo": tipo_equipo, #Tipo de equipo seleccionado
            "Voc": Voc, #kV rms | voltaje del sistema trifasico
            "I_bf": I_bf,  #kA symm rms | Three-phase bolted fault current
            "dis": dis, #mm | distancia de trabajo
            "gap": gap, #mm | espacio entre los conductores (electrodos)
            "ET": "BOX", #Enclosure type
            "EC": "VCBB", #Configuracion de los electrodos (VCB, VCBB, HCB, VOA, HOA)
            "width": width, #mm | ancho del gabinete
            "height":height, #mm | altura del gabinete
            "depth": depth #mm | profundidad del gabinete
            }
        system_data_HCB = { #BOTON 7,8
            "ACmetod":AC_metod_valor, # Metodo de calculo elegido
            "tipo_equipo": tipo_equipo, #Tipo de equipo seleccionado
            "Voc": Voc, #kV rms | voltaje del sistema trifasico
            "I_bf": I_bf,  #kA symm rms | Three-phase bolted fault current
            "dis": dis, #mm | distancia de trabajo
            "gap": gap, #mm | espacio entre los conductores (electrodos)
            "ET": "BOX", #Enclosure type
            "EC": "HCB", #Configuracion de los electrodos (VCB, VCBB, HCB, VOA, HOA)
            "width": width, #mm | ancho del gabinete
            "height":height, #mm | altura del gabinete
            "depth": depth #mm | profundidad del gabinete
            }

        if selectec_value_ET == 1: #OA
            cont_res_box.grid_remove() #Remueve contenedor de resultados "BOX"
            cont_res_oa.grid() #Muestra contenedor de resultados "OA"
            
            ################################## RESULTADOS | ENCLOSURE TYPE "VOA" | IEEE 1584 2018 ##################################
            # ******************** CONTENEDOR RESULTADO corriente de arco | IEEE 1584 2018 ********************
            # >>>>> Variable de control Corriente de arco | VOA | IEEE 1584 2018
            var_iarc_voa_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_voa_2018 = tk.Label(res_voa_iarc, text="Iarc: ")
            lb_iarc_voa_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_voa_2018_res = tk.Label(res_voa_iarc, textvariable=var_iarc_voa_2018)
            lb_iarc_voa_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_voa_2018_u = tk.Label(res_voa_iarc, text="kA")
            lb_iarc_voa_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control Liberacion de la falla | VOA | IEEE 1584 2018
            var_tfalla_voa_2018 = tk.StringVar(value=100) #value es un valor de origen
            # >>>>> Label Liberacion de la falla | IEEE 1584 2018
            lb_tfalla_voa_2018 = tk.Label(res_voa_iarc, text="T: ")
            lb_tfalla_voa_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Entry Liberacion de la falla | IEEE 1584 2018
            entrada_tfalla_voa_2018 = tk.Entry(res_voa_iarc, bg="SpringGreen3", font=("Arial", 12), width=6, textvariable=var_tfalla_voa_2018)
            entrada_tfalla_voa_2018.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            
            # >>>>> Label Liberacion de la falla | IEEE 1584 2018
            lb_tfalla_voa_2018_u = tk.Label(res_voa_iarc, text="ms")
            lb_tfalla_voa_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)
            # >>>>> BOTON Liberacion de la falla | IEEE 1584 2018
            boton_voa = tk.Button(res_voa_iarc, text="Calcular", background="green", command= actualiza_tfalla_voa_2018)
            boton_voa.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO arc flash protection | IEEE 1584 2018 ********************
            # >>>>> Variable de control de Energía incidente | VOA | IEEE 1584 2018
            var_e_voa_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_voa_2018 = tk.Label(res_afp_voa, text="E: ")
            lb_e_voa_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_voa_2018_res = tk.Label(res_afp_voa, textvariable=var_e_voa_2018, width=7)
            lb_e_voa_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_voa_2018_u = tk.Label(res_afp_voa, text="cal/cm2")
            lb_e_voa_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Limite de arco electrico | AFB | VOA | IEEE 1584 2018
            var_afb_voa_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_voa_2018 = tk.Label(res_afp_voa, text="AFB: ")
            lb_afb_voa_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_voa_2018_res = tk.Label(res_afp_voa, textvariable=var_afb_voa_2018, width=7)
            lb_afb_voa_2018_res.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_voa_2018_u = tk.Label(res_afp_voa, text="mm")
            lb_afb_voa_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Equipo de protección personal | EPP | VOA | IEEE 1584 2018
            var_epp_voa_2018 = tk.StringVar()
            # >>>>> Label EPP | IEEE 1584 2018
            lb_epp_voa_2018 = tk.Label(res_afp_voa, text="Categoría EPP: ")
            lb_epp_voa_2018.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            # >>>>> Label EPP | IEEE 1584 2018
            lb_epp_voa_2018_res = tk.Label(res_afp_voa, textvariable=var_epp_voa_2018, width=5)
            lb_epp_voa_2018_res.grid(row=2, column=2, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO corriente de arco reducida | IEEE 1584 2018 ********************
            # >>>>> Variable de control Corriente de arco reducida | VOA | IEEE 1584 2018
            var_iarcmin_voa_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_voa_2018 = tk.Label(res_voa_iarcmin, text="Iarcmin: ")
            lb_iarcmin_voa_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_voa_2018_res = tk.Label(res_voa_iarcmin, textvariable=var_iarcmin_voa_2018, width=5)
            lb_iarcmin_voa_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_voa_2018_u = tk.Label(res_voa_iarcmin, text="kA")
            lb_iarcmin_voa_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control Liberacion de la falla reducida | VOA | IEEE 1584 2018
            var_tfallamin_voa_2018 = tk.StringVar(value=100) #value es un valor de origen
            # >>>>> Label Liberacion de la falla reducida | IEEE 1584 2018
            lb_tfallamin_voa_2018 = tk.Label(res_voa_iarcmin, text="T: ")
            lb_tfallamin_voa_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Entry Liberacion de la falla reducida | IEEE 1584 2018
            entrada_tfallamin_voa_2018 = tk.Entry(res_voa_iarcmin, bg="SpringGreen3", font=("Arial", 12), width=6, textvariable=var_tfallamin_voa_2018)
            entrada_tfallamin_voa_2018.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Liberacion de la falla reducida | IEEE 1584 2018
            lb_tfallamin_voa_2018_u = tk.Label(res_voa_iarcmin, text="ms")
            lb_tfallamin_voa_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)
            # >>>>> BOTON Liberacion de la falla reducida | IEEE 1584 2018
            boton_1_2 = tk.Button(res_voa_iarcmin, text="Calcular", background="green", command=actualiza_tfallamin_voa_2018, state="disabled")
            boton_1_2.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO arc flash protection reducida | IEEE 1584 2018 ********************
            # >>>>> Variable de control de Energía incidente | VOA | IEEE 1584 2018
            var_emin_voa_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Energía incidente reducida | IEEE 1584 2018
            lb_emin_voa_2018 = tk.Label(res_afpmin_voa, text="E: ")
            lb_emin_voa_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente reducida | IEEE 1584 2018
            lb_emin_voa_2018_res = tk.Label(res_afpmin_voa, textvariable=var_emin_voa_2018, width=7)
            lb_emin_voa_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente reducida | IEEE 1584 2018
            lb_emin_voa_2018_u = tk.Label(res_afpmin_voa, text="cal/cm2")
            lb_emin_voa_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Limite de arco electrico | AFB | VOA | IEEE 1584 2018
            var_afbmin_voa_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_voa_2018 = tk.Label(res_afpmin_voa, text="AFB: ")
            lb_afbmin_voa_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_voa_2018_res = tk.Label(res_afpmin_voa, textvariable=var_afbmin_voa_2018, width=7)
            lb_afbmin_voa_2018_res.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_voa_2018_u = tk.Label(res_afpmin_voa, text="mm")
            lb_afbmin_voa_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Equipo de protección personal reducida | EPP | VOA | IEEE 1584 2018
            var_eppmin_voa_2018 = tk.StringVar()
            # >>>>> Label EPP reducida | IEEE 1584 2018
            lb_eppmin_voa_2018 = tk.Label(res_afpmin_voa, text="Categoría EPP: ")
            lb_eppmin_voa_2018.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            # >>>>> Label EPP reducida | IEEE 1584 2018
            lb_eppmin_voa_2018_res = tk.Label(res_afpmin_voa, textvariable=var_eppmin_voa_2018, width=5)
            lb_eppmin_voa_2018_res.grid(row=2, column=2, sticky="w", padx=5, pady=5)

            ################################## RESULTADOS | ENCLOSURE TYPE "HOA" | IEEE 1584 2018 ##################################
            # ******************** CONTENEDOR RESULTADO corriente de arco | IEEE 1584 2018 ********************
            # >>>>> Variable de control Corriente de arco | HOA | IEEE 1584 2018
            var_iarc_hoa_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_hoa_2018 = tk.Label(res_hoa_iarc, text="Iarc: ")
            lb_iarc_hoa_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_hoa_2018_res = tk.Label(res_hoa_iarc, textvariable=var_iarc_hoa_2018)
            lb_iarc_hoa_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_hoa_2018_u = tk.Label(res_hoa_iarc, text="kA")
            lb_iarc_hoa_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control Liberacion de la falla | HOA | IEEE 1584 2018
            var_tfalla_hoa_2018 = tk.StringVar(value=100) #value es un valor de origen
            # >>>>> Label Liberacion de la falla | IEEE 1584 2018
            lb_tfalla_hoa_2018 = tk.Label(res_hoa_iarc, text="T: ")
            lb_tfalla_hoa_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Entry Liberacion de la falla | IEEE 1584 2018
            entrada_tfalla_hoa_2018 = tk.Entry(res_hoa_iarc, bg="SpringGreen3", font=("Arial", 12), width=6, textvariable=var_tfalla_hoa_2018)
            entrada_tfalla_hoa_2018.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            
            # >>>>> Label Liberacion de la falla | IEEE 1584 2018
            lb_tfalla_hoa_2018_u = tk.Label(res_hoa_iarc, text="ms")
            lb_tfalla_hoa_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)
            # >>>>> BOTON Liberacion de la falla | IEEE 1584 2018
            boton_hoa = tk.Button(res_hoa_iarc, text="Calcular", background="green", command= actualiza_tfalla_hoa_2018)
            boton_hoa.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO arc flash protection | IEEE 1584 2018 ********************
            # >>>>> Variable de control de Energía incidente | HOA | IEEE 1584 2018
            var_e_hoa_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_hoa_2018 = tk.Label(res_afp_hoa, text="E: ")
            lb_e_hoa_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_hoa_2018_res = tk.Label(res_afp_hoa, textvariable=var_e_hoa_2018, width=7)
            lb_e_hoa_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_hoa_2018_u = tk.Label(res_afp_hoa, text="cal/cm2")
            lb_e_hoa_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Limite de arco electrico | AFB | HOA | IEEE 1584 2018
            var_afb_hoa_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_hoa_2018 = tk.Label(res_afp_hoa, text="AFB: ")
            lb_afb_hoa_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_hoa_2018_res = tk.Label(res_afp_hoa, textvariable=var_afb_hoa_2018, width=7)
            lb_afb_hoa_2018_res.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_hoa_2018_u = tk.Label(res_afp_hoa, text="mm")
            lb_afb_hoa_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Equipo de protección personal | EPP | HOA | IEEE 1584 2018
            var_epp_hoa_2018 = tk.StringVar()
            # >>>>> Label EPP | IEEE 1584 2018
            lb_epp_hoa_2018 = tk.Label(res_afp_hoa, text="Categoría EPP: ")
            lb_epp_hoa_2018.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            # >>>>> Label EPP | IEEE 1584 2018
            lb_epp_hoa_2018_res = tk.Label(res_afp_hoa, textvariable=var_epp_hoa_2018, width=5)
            lb_epp_hoa_2018_res.grid(row=2, column=2, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO corriente de arco reducida | IEEE 1584 2018 ********************
            # >>>>> Variable de control Corriente de arco reducida | HOA | IEEE 1584 2018
            var_iarcmin_hoa_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_hoa_2018 = tk.Label(res_hoa_iarcmin, text="Iarcmin: ")
            lb_iarcmin_hoa_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_hoa_2018_res = tk.Label(res_hoa_iarcmin, textvariable=var_iarcmin_hoa_2018, width=5)
            lb_iarcmin_hoa_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_hoa_2018_u = tk.Label(res_hoa_iarcmin, text="kA")
            lb_iarcmin_hoa_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control Liberacion de la falla reducida | HOA | IEEE 1584 2018
            var_tfallamin_hoa_2018 = tk.StringVar(value=100) #value es un valor de origen
            # >>>>> Label Liberacion de la falla reducida | IEEE 1584 2018
            lb_tfallamin_hoa_2018 = tk.Label(res_hoa_iarcmin, text="T: ")
            lb_tfallamin_hoa_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Entry Liberacion de la falla reducida | IEEE 1584 2018
            entrada_tfallamin_hoa_2018 = tk.Entry(res_hoa_iarcmin, bg="SpringGreen3", font=("Arial", 12), width=6, textvariable=var_tfallamin_hoa_2018)
            entrada_tfallamin_hoa_2018.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Liberacion de la falla reducida | IEEE 1584 2018
            lb_tfallamin_hoa_2018_u = tk.Label(res_hoa_iarcmin, text="ms")
            lb_tfallamin_hoa_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)
            # >>>>> BOTON Liberacion de la falla reducida | IEEE 1584 2018
            boton_2_2 = tk.Button(res_hoa_iarcmin, text="Calcular", background="green", command=actualiza_tfallamin_hoa_2018, state="disabled")
            boton_2_2.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO arc flash protection reducida | IEEE 1584 2018 ********************
            # >>>>> Variable de control de Energía incidente | HOA | IEEE 1584 2018
            var_emin_hoa_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Energía incidente reducida | IEEE 1584 2018
            lb_emin_hoa_2018 = tk.Label(res_afpmin_hoa, text="E: ")
            lb_emin_hoa_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente reducida | IEEE 1584 2018
            lb_emin_hoa_2018_res = tk.Label(res_afpmin_hoa, textvariable=var_emin_hoa_2018, width=7)
            lb_emin_hoa_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente reducida | IEEE 1584 2018
            lb_emin_hoa_2018_u = tk.Label(res_afpmin_hoa, text="cal/cm2")
            lb_emin_hoa_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Limite de arco electrico | AFB | HOA | IEEE 1584 2018
            var_afbmin_hoa_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_hoa_2018 = tk.Label(res_afpmin_hoa, text="AFB: ")
            lb_afbmin_hoa_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_hoa_2018_res = tk.Label(res_afpmin_hoa, textvariable=var_afbmin_hoa_2018, width=7)
            lb_afbmin_hoa_2018_res.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_hoa_2018_u = tk.Label(res_afpmin_hoa, text="mm")
            lb_afbmin_hoa_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Equipo de protección personal reducida | EPP | HOA | IEEE 1584 2018
            var_eppmin_hoa_2018 = tk.StringVar()
            # >>>>> Label EPP reducida | IEEE 1584 2018
            lb_eppmin_hoa_2018 = tk.Label(res_afpmin_hoa, text="Categoría EPP: ")
            lb_eppmin_hoa_2018.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            # >>>>> Label EPP reducida | IEEE 1584 2018
            lb_eppmin_hoa_2018_res = tk.Label(res_afpmin_hoa, textvariable=var_eppmin_hoa_2018, width=5)
            lb_eppmin_hoa_2018_res.grid(row=2, column=2, sticky="w", padx=5, pady=5)

            inicia_primer_calculo_OA()#Llama a la función que realiza el promer calculo "I_arc"

        elif selectec_value_ET == 2: #BOX
            cont_res_oa.grid_remove() #Remueve contenedor de resultados "OA"
            cont_res_box.grid() #Muestra contenedor de resultados "BOX"
 
            ################################## RESULTADOS | ENCLOSURE TYPE "VCB" | IEEE 1584 2018 ##################################
            # ******************** CONTENEDOR RESULTADO corriente de arco | IEEE 1584 2018 ********************
            # >>>>> Variable de control Corriente de arco | VCB | IEEE 1584 2018
            var_iarc_vcb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_vcb_2018 = tk.Label(res_vcb_iarc, text="Iarc: ")
            lb_iarc_vcb_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_vcb_2018_res = tk.Label(res_vcb_iarc, textvariable=var_iarc_vcb_2018)
            lb_iarc_vcb_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_vcb_2018_u = tk.Label(res_vcb_iarc, text="kA")
            lb_iarc_vcb_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control Liberacion de la falla | VCB | IEEE 1584 2018
            var_tfalla_vcb_2018 = tk.StringVar(value=100) #value es un valor de origen
            # >>>>> Label Liberacion de la falla | IEEE 1584 2018
            lb_tfalla_vcb_2018 = tk.Label(res_vcb_iarc, text="T: ")
            lb_tfalla_vcb_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Entry Liberacion de la falla | IEEE 1584 2018
            entrada_tfalla_vcb_2018 = tk.Entry(res_vcb_iarc, bg="SpringGreen3", font=("Arial", 12), width=6, textvariable=var_tfalla_vcb_2018)
            entrada_tfalla_vcb_2018.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            
            # >>>>> Label Liberacion de la falla | IEEE 1584 2018
            lb_tfalla_vcb_2018_u = tk.Label(res_vcb_iarc, text="ms")
            lb_tfalla_vcb_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)
            # >>>>> BOTON Liberacion de la falla | IEEE 1584 2018
            boton_vcb = tk.Button(res_vcb_iarc, text="Calcular", background="green", command= actualiza_tfalla_vcb_2018)
            boton_vcb.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO arc flash protection | IEEE 1584 2018 ********************
            # >>>>> Variable de control de Energía incidente | VCB | IEEE 1584 2018
            var_e_vcb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_vcb_2018 = tk.Label(res_afp_vcb, text="E: ")
            lb_e_vcb_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_vcb_2018_res = tk.Label(res_afp_vcb, textvariable=var_e_vcb_2018, width=7)
            lb_e_vcb_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_vcb_2018_u = tk.Label(res_afp_vcb, text="cal/cm2")
            lb_e_vcb_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Limite de arco electrico | AFB | VCB | IEEE 1584 2018
            var_afb_vcb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_vcb_2018 = tk.Label(res_afp_vcb, text="AFB: ")
            lb_afb_vcb_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_vcb_2018_res = tk.Label(res_afp_vcb, textvariable=var_afb_vcb_2018, width=7)
            lb_afb_vcb_2018_res.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_vcb_2018_u = tk.Label(res_afp_vcb, text="mm")
            lb_afb_vcb_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Equipo de protección personal | EPP | VCB | IEEE 1584 2018
            var_epp_vcb_2018 = tk.StringVar()
            # >>>>> Label EPP | IEEE 1584 2018
            lb_epp_vcb_2018 = tk.Label(res_afp_vcb, text="Categoría EPP: ")
            lb_epp_vcb_2018.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            # >>>>> Label EPP | IEEE 1584 2018
            lb_epp_vcb_2018_res = tk.Label(res_afp_vcb, textvariable=var_epp_vcb_2018, width=5)
            lb_epp_vcb_2018_res.grid(row=2, column=2, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO corriente de arco reducida | IEEE 1584 2018 ********************
            # >>>>> Variable de control Corriente de arco reducida | VCB | IEEE 1584 2018
            var_iarcmin_vcb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_vcb_2018 = tk.Label(res_vcb_iarcmin, text="Iarcmin: ")
            lb_iarcmin_vcb_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_vcb_2018_res = tk.Label(res_vcb_iarcmin, textvariable=var_iarcmin_vcb_2018, width=5)
            lb_iarcmin_vcb_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_vcb_2018_u = tk.Label(res_vcb_iarcmin, text="kA")
            lb_iarcmin_vcb_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control Liberacion de la falla reducida | VCB | IEEE 1584 2018
            var_tfallamin_vcb_2018 = tk.StringVar(value=100) #value es un valor de origen
            # >>>>> Label Liberacion de la falla reducida | IEEE 1584 2018
            lb_tfallamin_vcb_2018 = tk.Label(res_vcb_iarcmin, text="T: ")
            lb_tfallamin_vcb_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Entry Liberacion de la falla reducida | IEEE 1584 2018
            entrada_tfallamin_vcb_2018 = tk.Entry(res_vcb_iarcmin, bg="SpringGreen3", font=("Arial", 12), width=6, textvariable=var_tfallamin_vcb_2018)
            entrada_tfallamin_vcb_2018.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Liberacion de la falla reducida | IEEE 1584 2018
            lb_tfallamin_vcb_2018_u = tk.Label(res_vcb_iarcmin, text="ms")
            lb_tfallamin_vcb_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)
            # >>>>> BOTON Liberacion de la falla reducida | IEEE 1584 2018
            boton_4 = tk.Button(res_vcb_iarcmin, text="Calcular", background="green", command=actualiza_tfallamin_vcb_2018, state="disabled")
            boton_4.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO arc flash protection reducida | IEEE 1584 2018 ********************
            # >>>>> Variable de control de Energía incidente | VCB | IEEE 1584 2018
            var_emin_vcb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Energía incidente reducida | IEEE 1584 2018
            lb_emin_vcb_2018 = tk.Label(res_afpmin_vcb, text="E: ")
            lb_emin_vcb_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente reducida | IEEE 1584 2018
            lb_emin_vcb_2018_res = tk.Label(res_afpmin_vcb, textvariable=var_emin_vcb_2018, width=7)
            lb_emin_vcb_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente reducida | IEEE 1584 2018
            lb_emin_vcb_2018_u = tk.Label(res_afpmin_vcb, text="cal/cm2")
            lb_emin_vcb_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Limite de arco electrico | AFB | VCB | IEEE 1584 2018
            var_afbmin_vcb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_vcb_2018 = tk.Label(res_afpmin_vcb, text="AFB: ")
            lb_afbmin_vcb_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_vcb_2018_res = tk.Label(res_afpmin_vcb, textvariable=var_afbmin_vcb_2018, width=7)
            lb_afbmin_vcb_2018_res.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_vcb_2018_u = tk.Label(res_afpmin_vcb, text="mm")
            lb_afbmin_vcb_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Equipo de protección personal reducida | EPP | VCB | IEEE 1584 2018
            var_eppmin_vcb_2018 = tk.StringVar()
            # >>>>> Label EPP reducida | IEEE 1584 2018
            lb_eppmin_vcb_2018 = tk.Label(res_afpmin_vcb, text="Categoría EPP: ")
            lb_eppmin_vcb_2018.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            # >>>>> Label EPP reducida | IEEE 1584 2018
            lb_eppmin_vcb_2018_res = tk.Label(res_afpmin_vcb, textvariable=var_eppmin_vcb_2018, width=5)
            lb_eppmin_vcb_2018_res.grid(row=2, column=2, sticky="w", padx=5, pady=5)

            ################################## RESULTADOS | ENCLOSURE TYPE "VCBB" | IEEE 1584 2018 ##################################
            # ******************** CONTENEDOR RESULTADO corriente de arco | IEEE 1584 2018 ********************
            # >>>>> Variable de control Corriente de arco | VCBB | IEEE 1584 2018
            var_iarc_vcbb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_vcbb_2018 = tk.Label(res_vcbb_iarc, text="Iarc: ")
            lb_iarc_vcbb_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_vcbb_2018_res = tk.Label(res_vcbb_iarc, textvariable=var_iarc_vcbb_2018)
            lb_iarc_vcbb_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_vcbb_2018_u = tk.Label(res_vcbb_iarc, text="kA")
            lb_iarc_vcbb_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control Liberacion de la falla | VCBB | IEEE 1584 2018
            var_tfalla_vcbb_2018 = tk.StringVar(value=100) #value es un valor de origen
            # >>>>> Label Liberacion de la falla | IEEE 1584 2018
            lb_tfalla_vcbb_2018 = tk.Label(res_vcbb_iarc, text="T: ")
            lb_tfalla_vcbb_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Entry Liberacion de la falla | IEEE 1584 2018
            entrada_tfalla_vcbb_2018 = tk.Entry(res_vcbb_iarc, bg="SpringGreen3", font=("Arial", 12), width=6, textvariable=var_tfalla_vcbb_2018)
            entrada_tfalla_vcbb_2018.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Liberacion de la falla | IEEE 1584 2018
            lb_tfalla_vcbb_2018_u = tk.Label(res_vcbb_iarc, text="ms")
            lb_tfalla_vcbb_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)
            # >>>>> BOTON Liberacion de la falla | IEEE 1584 2018
            boton_5 = tk.Button(res_vcbb_iarc, text="Calcular", background="green", command=actualiza_tfalla_vcbb_2018)
            boton_5.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO arc flash protection | IEEE 1584 2018 ********************
            # >>>>> Variable de control de Energía incidente | VCBB | IEEE 1584 2018
            var_e_vcbb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_vcbb_2018 = tk.Label(res_afp_vcbb, text="E: ")
            lb_e_vcbb_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_vcbb_2018_res = tk.Label(res_afp_vcbb, textvariable=var_e_vcbb_2018, width=7)
            lb_e_vcbb_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_vcbb_2018_u = tk.Label(res_afp_vcbb, text="cal/cm2")
            lb_e_vcbb_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Limite de arco electrico | AFB | VCBB | IEEE 1584 2018
            var_afb_vcbb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_vcbb_2018 = tk.Label(res_afp_vcbb, text="AFB: ")
            lb_afb_vcbb_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_vcbb_2018_res = tk.Label(res_afp_vcbb, textvariable=var_afb_vcbb_2018, width=7)
            lb_afb_vcbb_2018_res.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_vcbb_2018_u = tk.Label(res_afp_vcbb, text="mm")
            lb_afb_vcbb_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Equipo de protección personal | EPP | VCBB | IEEE 1584 2018
            var_epp_vcbb_2018 = tk.StringVar()
            # >>>>> Label EPP | IEEE 1584 2018
            lb_epp_vcbb_2018 = tk.Label(res_afp_vcbb, text="Categoría EPP: ")
            lb_epp_vcbb_2018.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            # >>>>> Label EPP | IEEE 1584 2018
            lb_epp_vcbb_2018_res = tk.Label(res_afp_vcbb, textvariable=var_epp_vcbb_2018, width=5)
            lb_epp_vcbb_2018_res.grid(row=2, column=2, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO corriente de arco reducida | IEEE 1584 2018 ********************
            # >>>>> Variable de control Corriente de arco reducida | VCBB | IEEE 1584 2018
            var_iarcmin_vcbb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_vcbb_2018 = tk.Label(res_vcbb_iarcmin, text="Iarcmin: ")
            lb_iarcmin_vcbb_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_vcbb_2018_res = tk.Label(res_vcbb_iarcmin, textvariable=var_iarcmin_vcbb_2018, width=5)
            lb_iarcmin_vcbb_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_vcbb_2018_u = tk.Label(res_vcbb_iarcmin, text="kA")
            lb_iarcmin_vcbb_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control Liberacion de la falla reducida | VCBB | IEEE 1584 2018
            var_tfallamin_vcbb_2018 = tk.StringVar(value=100) #value es un valor de origen
            # >>>>> Label Liberacion de la falla reducida | IEEE 1584 2018
            lb_tfallamin_vcbb_2018 = tk.Label(res_vcbb_iarcmin, text="T: ")
            lb_tfallamin_vcbb_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Entry Liberacion de la falla reducida | IEEE 1584 2018
            entrada_tfallamin_vcbb_2018 = tk.Entry(res_vcbb_iarcmin, bg="SpringGreen3", font=("Arial", 12), width=6, textvariable=var_tfallamin_vcbb_2018)
            entrada_tfallamin_vcbb_2018.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Liberacion de la falla reducida | IEEE 1584 2018
            lb_tfallamin_vcbb_2018_u = tk.Label(res_vcbb_iarcmin, text="ms")
            lb_tfallamin_vcbb_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)
            # >>>>> BOTON Liberacion de la falla reducida | IEEE 1584 2018
            boton_6 = tk.Button(res_vcbb_iarcmin, text="Calcular", background="green", command=actualiza_tfallamin_vcbb_2018, state="disabled")
            boton_6.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO arc flash protection reducida | IEEE 1584 2018 ********************
            # >>>>> Variable de control de Energía incidente reducida | VCBB | IEEE 1584 2018
            var_emin_vcbb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Energía incidente reducida | IEEE 1584 2018
            lb_emin_vcbb_2018 = tk.Label(res_afpmin_vcbb, text="E: ")
            lb_emin_vcbb_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente reducida| IEEE 1584 2018
            lb_emin_vcbb_2018_res = tk.Label(res_afpmin_vcbb, textvariable=var_emin_vcbb_2018, width=7)
            lb_emin_vcbb_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente reducida| IEEE 1584 2018
            lb_emin_vcbb_2018_u = tk.Label(res_afpmin_vcbb, text="cal/cm2")
            lb_emin_vcbb_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Limite de arco electrico reducida | AFB | VCBB | IEEE 1584 2018
            var_afbmin_vcbb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_vcbb_2018 = tk.Label(res_afpmin_vcbb, text="AFB: ")
            lb_afbmin_vcbb_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_vcbb_2018_res = tk.Label(res_afpmin_vcbb, textvariable=var_afbmin_vcbb_2018, width=7)
            lb_afbmin_vcbb_2018_res.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_vcbb_2018_u = tk.Label(res_afpmin_vcbb, text="mm")
            lb_afbmin_vcbb_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Equipo de protección personal reducida | EPP | VCBB | IEEE 1584 2018
            var_eppmin_vcbb_2018 = tk.StringVar()
            # >>>>> Label EPP reducida | IEEE 1584 2018
            lb_eppmin_vcbb_2018 = tk.Label(res_afpmin_vcbb, text="Categoría EPP: ")
            lb_eppmin_vcbb_2018.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            # >>>>> Label EPP reducida | IEEE 1584 2018
            lb_eppmin_vcbb_2018_res = tk.Label(res_afpmin_vcbb, textvariable=var_eppmin_vcbb_2018, width=5)
            lb_eppmin_vcbb_2018_res.grid(row=2, column=2, sticky="w", padx=5, pady=5)

            ################################## RESULTADOS | ENCLOSURE TYPE "HCB" | IEEE 1584 2018 ##################################
            # ******************** CONTENEDOR RESULTADO corriente de arco | IEEE 1584 2018 ********************
            # >>>>> Variable de control Corriente de arco | HCB | IEEE 1584 2018
            var_iarc_hcb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_hcb_2018 = tk.Label(res_hcb_iarc, text="Iarc: ")
            lb_iarc_hcb_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_hcb_2018_res = tk.Label(res_hcb_iarc, textvariable=var_iarc_hcb_2018)
            lb_iarc_hcb_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco | IEEE 1584 2018
            lb_iarc_hcb_2018_u = tk.Label(res_hcb_iarc, text="kA")
            lb_iarc_hcb_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control Liberacion de la falla | HCB | IEEE 1584 2018
            var_tfalla_hcb_2018 = tk.StringVar(value=100) #value es un valor de origen
            # >>>>> Label Liberacion de la falla | IEEE 1584 2018
            lb_tfalla_hcb_2018 = tk.Label(res_hcb_iarc, text="T: ")
            lb_tfalla_hcb_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Entry Liberacion de la falla | IEEE 1584 2018
            entrada_tfalla_hcb_2018 = tk.Entry(res_hcb_iarc, bg="SpringGreen3", font=("Arial", 12), width=6, textvariable=var_tfalla_hcb_2018)
            entrada_tfalla_hcb_2018.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Liberacion de la falla | IEEE 1584 2018
            lb_tfalla_hcb_2018_u = tk.Label(res_hcb_iarc, text="ms")
            lb_tfalla_hcb_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)
            # >>>>> BOTON Liberacion de la falla | IEEE 1584 2018
            boton_7 = tk.Button(res_hcb_iarc, text="Calcular", background="green", command=actualiza_tfalla_hcb_2018)
            boton_7.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO arc flash protection | IEEE 1584 2018 ********************
            # >>>>> Variable de control de Energía incidente | HCB | IEEE 1584 2018
            var_e_hcb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_hcb_2018 = tk.Label(res_afp_hcb, text="E: ")
            lb_e_hcb_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_hcb_2018_res = tk.Label(res_afp_hcb, textvariable=var_e_hcb_2018, width=7)
            lb_e_hcb_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente | IEEE 1584 2018
            lb_e_hcb_2018_u = tk.Label(res_afp_hcb, text="cal/cm2")
            lb_e_hcb_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Limite de arco electrico | AFB | HCB | IEEE 1584 2018
            var_afb_hcb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_hcb_2018 = tk.Label(res_afp_hcb, text="AFB: ")
            lb_afb_hcb_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_hcb_2018_res = tk.Label(res_afp_hcb, textvariable=var_afb_hcb_2018, width=7)
            lb_afb_hcb_2018_res.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico | IEEE 1584 2018
            lb_afb_hcb_2018_u = tk.Label(res_afp_hcb, text="mm")
            lb_afb_hcb_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Equipo de protección personal | EPP | HCB | IEEE 1584 2018
            var_epp_hcb_2018 = tk.StringVar()
            # >>>>> Label EPP | IEEE 1584 2018
            lb_epp_hcb_2018 = tk.Label(res_afp_hcb, text="Categoría EPP: ")
            lb_epp_hcb_2018.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            # >>>>> Label EPP | IEEE 1584 2018
            lb_epp_hcb_2018_res = tk.Label(res_afp_hcb, textvariable=var_epp_hcb_2018, width=5)
            lb_epp_hcb_2018_res.grid(row=2, column=2, sticky="w", padx=5, pady=5)
            
            # ******************** CONTENEDOR RESULTADO corriente de arco reducida| IEEE 1584 2018 ********************
            # >>>>> Variable de control Corriente de arco reducida | HCB | IEEE 1584 2018
            var_iarcmin_hcb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_hcb_2018 = tk.Label(res_hcb_iarcmin, text="Iarcmin: ")
            lb_iarcmin_hcb_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_hcb_2018_res = tk.Label(res_hcb_iarcmin, textvariable=var_iarcmin_hcb_2018, width=5)
            lb_iarcmin_hcb_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Corriente de arco reducida | IEEE 1584 2018
            lb_iarcmin_hcb_2018_u = tk.Label(res_hcb_iarcmin, text="kA")
            lb_iarcmin_hcb_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control Liberacion de la falla reducida | HCB | IEEE 1584 2018
            var_tfallamin_hcb_2018 = tk.StringVar(value=100) #value es un valor de origen
            # >>>>> Label Liberacion de la falla reducida | IEEE 1584 2018
            lb_tfallamin_hcb_2018 = tk.Label(res_hcb_iarcmin, text="T: ")
            lb_tfallamin_hcb_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Entry Liberacion de la falla reducida | IEEE 1584 2018
            entrada_tfallamin_hcb_2018 = tk.Entry(res_hcb_iarcmin, bg="SpringGreen3", font=("Arial", 12), width=6, textvariable=var_tfallamin_hcb_2018)
            entrada_tfallamin_hcb_2018.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Liberacion de la falla reducida | IEEE 1584 2018
            lb_tfallamin_hcb_2018_u = tk.Label(res_hcb_iarcmin, text="ms")
            lb_tfallamin_hcb_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)
            # >>>>> BOTON Liberacion de la falla reducida | IEEE 1584 2018
            boton_8 = tk.Button(res_hcb_iarcmin, text="Calcular", background="green", command=actualiza_tfallamin_hcb_2018, state="disabled")
            boton_8.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=5)

            # ******************** CONTENEDOR RESULTADO arc flash protection reducida | IEEE 1584 2018 ********************
            # >>>>> Variable de control de Energía incidente | HCB | IEEE 1584 2018
            var_emin_hcb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Energía incidente reducida | IEEE 1584 2018
            lb_emin_hcb_2018 = tk.Label(res_afpmin_hcb, text="E: ")
            lb_emin_hcb_2018.grid(row=0, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente reducida | IEEE 1584 2018
            lb_emin_hcb_2018_res = tk.Label(res_afpmin_hcb, textvariable=var_emin_hcb_2018, width=7)
            lb_emin_hcb_2018_res.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Energía incidente reducida | IEEE 1584 2018
            lb_emin_hcb_2018_u = tk.Label(res_afpmin_hcb, text="cal/cm2")
            lb_emin_hcb_2018_u.grid(row=0, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Limite de arco electrico | AFB | HCB | IEEE 1584 2018
            var_afbmin_hcb_2018 = tk.StringVar() #value es un valor de origen
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_hcb_2018 = tk.Label(res_afpmin_hcb, text="AFB: ")
            lb_afbmin_hcb_2018.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_hcb_2018_res = tk.Label(res_afpmin_hcb, textvariable=var_afbmin_hcb_2018, width=7)
            lb_afbmin_hcb_2018_res.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            # >>>>> Label Limite de arco electrico reducida | IEEE 1584 2018
            lb_afbmin_hcb_2018_u = tk.Label(res_afpmin_hcb, text="mm")
            lb_afbmin_hcb_2018_u.grid(row=1, column=2, sticky="w", padx=5, pady=5)

            # >>>>> Variable de control de Equipo de protección personal reducida | EPP | HCB | IEEE 1584 2018
            var_eppmin_hcb_2018 = tk.StringVar()
            # >>>>> Label EPP reducida | IEEE 1584 2018
            lb_eppmin_hcb_2018 = tk.Label(res_afpmin_hcb, text="Categoría EPP: ")
            lb_eppmin_hcb_2018.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
            # >>>>> Label EPP reducida | IEEE 1584 2018
            lb_eppmin_hcb_2018_res = tk.Label(res_afpmin_hcb, textvariable=var_eppmin_hcb_2018, width=5)
            lb_eppmin_hcb_2018_res.grid(row=2, column=2, sticky="w", padx=5, pady=5)

            inicia_primer_calculo_BOX() #Llama a la función que realiza el promer calculo "I_arc"

    else:
        # Si la ventana ya está abierta, la trae al frente
        ventana_calculo_2018.lift()

# Inicializa la variable que controlará la ventana toplevel
ventana_calculo_2018 = None
ventana_calculo_2002 = None

# ******************** BUTTON CALCULAR | IEEE 1584 2018 ********************
# >>>>> LabelFrame Enclosure parameters | IEEE 1584 2018
cont_bot_2018 = tk.LabelFrame(cont_AF_2018, width=250, height=50, text="Iniciar cálculo", padx=5, pady=5 )
cont_bot_2018.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=5)
# Este botón abre una ventana Top Level
boton_2018 = tk.Button(cont_bot_2018, text="CALCULAR", background="green", command = ventana_toplevel_2018 )
boton_2018.pack(padx=5, pady=(0, 10))

# ******************** BUTTON CALCULAR | IEEE 1584 2002 ********************
cont_bot_2002 = tk.LabelFrame(cont_AF_2002, width=250, height=50, text="Iniciar cálculo", padx=5, pady=5 )
cont_bot_2002.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=5,)

boton_2002 = tk.Button(cont_bot_2002, text="CALCULAR", background="green", command = ventana_toplevel_2002)
boton_2002.pack(padx=5, pady=(0, 10))

ventana.mainloop()