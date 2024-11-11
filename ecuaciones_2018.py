import math #para calcular el logaritmo base 10 de I_bf
import numpy as np
from tablas_2018 import EC_Voc, tabla_2, tabla_3, tabla_4, tabla_5, enclosure_AB, Box_type

#OBTIENE LOS DATOS DEL SISTEMA
def obtener_parametros_main(system_data):
    #Obtiene los parametros del diccionario recibido
    EC     = system_data["EC"]
    Voc    = float( system_data["Voc"] )
    I_bf   = float( system_data["I_bf"] )
    gap    = float( system_data["gap"] )
    lg_Ibf = math.log10(I_bf) #logaritmo base 10 de "I_bf"
    lg_gap = math.log10(gap)  #logaritmo base 10 de "gap"
    
    return EC, Voc, I_bf, lg_Ibf, lg_gap

def obtener_parametros_afp1 (system_data):
    #Obtiene los parametros del diccionario recibido
    EC     = system_data["EC"]
    Voc    = float( system_data["Voc"] )
    I_bf   = float( system_data["I_bf"] )
    gap    = float( system_data["gap"] )
    dis    = float( system_data["dis"] )
    width  = float( system_data["width"] )
    height = float( system_data["height"] )
    depth  = float( system_data["depth"] )
    I_arc = float( system_data["I_arc"] )
    I_arc_600 = float( system_data["I_arc_600"] )
    Tfalla = float( system_data["Tfalla"] )
    lg_Ibf = math.log10(I_bf) #logaritmo base 10 de "I_bf"
    lg_gap = math.log10(gap)  #logaritmo base 10 de "gap"
    
    return dis, EC, I_bf, I_arc_600, Tfalla, Voc, lg_Ibf, lg_gap, width, height, depth, I_arc

#OBTIENE LOS DATOS DEL SISTEMA
def obtener_parametros_afp2(system_data):
    #Obtiene los parametros del diccionario recibido
    EC     = system_data["EC"]
    Voc    = float( system_data["Voc"] )
    I_bf   = float( system_data["I_bf"] )
    gap    = float( system_data["gap"] )
    dis    = float( system_data["dis"] )
    width  = float( system_data["width"] )
    height = float( system_data["height"] )
    depth  = float( system_data["depth"] )
    I_arc_600 = float( system_data["I_arc_600"] )
    I_arc_2700 = float( system_data["I_arc_2700"] )
    I_arc_14300 = float( system_data["I_arc_14300"] )
    Tfalla = float( system_data["Tfalla"] )
    

    lg_Ibf = math.log10(I_bf) #logaritmo base 10 de "I_bf"
    lg_gap = math.log10(gap)  #logaritmo base 10 de "gap"
    
    return dis, EC, I_bf, I_arc_600, I_arc_2700, I_arc_14300, Tfalla, Voc, lg_Ibf, lg_gap, width, height, depth

def obtener_parametros_afp_min1(system_data):
    #Obtiene los parametros del diccionario recibido
    EC     = system_data["EC"]
    I_bf   = float( system_data["I_bf"] )
    gap    = float( system_data["gap"] )
    dis    = float( system_data["dis"] )
    I_arc_600 = float( system_data["I_arc_600"] )
    I_arc_min = float( system_data["I_arc_min"] )
    Tmin = float( system_data["Tfalla_min"] )
    CF = float( system_data["CF"] )

    lg_Ibf = math.log10(I_bf) #logaritmo base 10 de "I_bf"
    lg_gap = math.log10(gap)  #logaritmo base 10 de "gap"
    
    return dis, EC, I_bf, I_arc_600, I_arc_min, Tmin, CF, lg_Ibf, lg_gap

def obtener_parametros_afp_min2(system_data):
    #Obtiene los parametros del diccionario recibido
    EC     = system_data["EC"]
    Voc    = float( system_data["Voc"] )
    I_bf   = float( system_data["I_bf"] )
    gap    = float( system_data["gap"] )
    dis    = float( system_data["dis"] )
    I_arc_600_min = float( system_data["I_arc_600_min"] )
    I_arc_2700_min = float( system_data["I_arc_2700_min"] )
    I_arc_14300_min = float( system_data["I_arc_14300_min"] )
    Tfalla_min = float( system_data["Tfalla_min"] )
    CF = float( system_data["CF"] )

    lg_Ibf = math.log10(I_bf) #logaritmo base 10 de "I_bf"
    lg_gap = math.log10(gap)  #logaritmo base 10 de "gap"
    
    return dis, EC, I_bf, I_arc_600_min, I_arc_2700_min, I_arc_14300_min, Tfalla_min, Voc, lg_Ibf, lg_gap, CF

#Definicion de funciones
#ECUACION 1
def ecuacion_1 (EC,Voc,I_bf,lg_Ibf,lg_gap):
    #Primero define los coeficientes k en base a la configuracion de electrodos EC
    k1 = EC_Voc[EC][Voc]["k1"]
    k2 = EC_Voc[EC][Voc]["k2"]
    k3 = EC_Voc[EC][Voc]["k3"]
    k4 = EC_Voc[EC][Voc]["k4"]
    k5 = EC_Voc[EC][Voc]["k5"]
    k6 = EC_Voc[EC][Voc]["k6"]
    k7 = EC_Voc[EC][Voc]["k7"]
    k8 = EC_Voc[EC][Voc]["k8"]
    k9 = EC_Voc[EC][Voc]["k9"]
    k10 = EC_Voc[EC][Voc]["k10"]

    I_arc_Voc = 10**(k1+k2*lg_Ibf+k3*lg_gap)*(
        k4*I_bf**6 +
        k5*I_bf**5 +
        k6*I_bf**4 +
        k7*I_bf**3 +
        k8*I_bf**2 +
        k9*I_bf    +
        k10 )
    return I_arc_Voc

def ecuacion_2 (I_arc, CF_VarCF):
    I_arc_min = I_arc*CF_VarCF
    return I_arc_min

#*******************************
def ecuacion_3456 (tabla, EC, T, I_bf,lg_Ibf,lg_gap, lg_dis, lg_Iarc, lg_CF, I_arc):
    #Primero define los coeficientes k en base a la configuracion de electrodos EC y la tabla (3, 4, 5)
    k1 = tabla[EC]["k1"]
    k2 = tabla[EC]["k2"]
    k3 = tabla[EC]["k3"]
    k4 = tabla[EC]["k4"]
    k5 = tabla[EC]["k5"]
    k6 = tabla[EC]["k6"]
    k7 = tabla[EC]["k7"]
    k8 = tabla[EC]["k8"]
    k9 = tabla[EC]["k9"]
    k10 = tabla[EC]["k10"]
    k11 = tabla[EC]["k11"]
    k12 = tabla[EC]["k12"]
    k13 = tabla[EC]["k13"]

    ecuacion_general = (12.552/50)*T*10**(k1+k2*lg_gap+(k3*I_arc/(        
        k4*I_bf**7 +
        k5*I_bf**6 +
        k6*I_bf**5 +
        k7*I_bf**4 +
        k8*I_bf**3 +
        k9*I_bf**2 +
        k10*I_bf)) +  k11*lg_Ibf+k12*lg_dis+k13*lg_Iarc+lg_CF)
    return ecuacion_general
#*******************************
def ecuacion_7 (EC, I_bf, lg_T, lg_Ibf, lg_gap,I_arc_600, lg_Iarc_600, lg_CF):    
    k1 = tabla_3[EC]["k1"]
    k2 = tabla_3[EC]["k2"]
    k3 = tabla_3[EC]["k3"]
    k4 = tabla_3[EC]["k4"]
    k5 = tabla_3[EC]["k5"]
    k6 = tabla_3[EC]["k6"]
    k7 = tabla_3[EC]["k7"]
    k8 = tabla_3[EC]["k8"]
    k9 = tabla_3[EC]["k9"]
    k10 = tabla_3[EC]["k10"]
    k11 = tabla_3[EC]["k11"]
    k12 = tabla_3[EC]["k12"]
    k13 = tabla_3[EC]["k13"]
   
    AFB_600 = 10**((k1+k2*lg_gap + (k3*I_arc_600/(
        k4*I_bf**7 +
        k5*I_bf**6 +
        k6*I_bf**5 +
        k7*I_bf**4 +
        k8*I_bf**3 +
        k9*I_bf**2 +
        k10*I_bf)) + (k11*lg_Ibf+k13*lg_Iarc_600+lg_CF-lg_T))/-k12)
    return AFB_600

def ecuacion_8 (EC, I_bf, lg_T, lg_Ibf, lg_gap,I_arc_2700, lg_Iarc_2700, lg_CF):      
    k1 = tabla_4[EC]["k1"]
    k2 = tabla_4[EC]["k2"]
    k3 = tabla_4[EC]["k3"]
    k4 = tabla_4[EC]["k4"]
    k5 = tabla_4[EC]["k5"]
    k6 = tabla_4[EC]["k6"]
    k7 = tabla_4[EC]["k7"]
    k8 = tabla_4[EC]["k8"]
    k9 = tabla_4[EC]["k9"]
    k10 = tabla_4[EC]["k10"]
    k11 = tabla_4[EC]["k11"]
    k12 = tabla_4[EC]["k12"]
    k13 = tabla_4[EC]["k13"]

    AFB_2700 = 10**((k1+k2*lg_gap + (k3*I_arc_2700/(
        k4*I_bf**7 +
        k5*I_bf**6 +
        k6*I_bf**5 +
        k7*I_bf**4 +
        k8*I_bf**3 +
        k9*I_bf**2 +
        k10*I_bf)) + (k11*lg_Ibf+k13*lg_Iarc_2700+lg_CF-lg_T))/-k12)   
    return AFB_2700

def ecuacion_9 (EC, I_bf, lg_T, lg_Ibf, lg_gap,I_arc_14300, lg_Iarc_14300, lg_CF):
    k1 = tabla_5[EC]["k1"]
    k2 = tabla_5[EC]["k2"]
    k3 = tabla_5[EC]["k3"]
    k4 = tabla_5[EC]["k4"]
    k5 = tabla_5[EC]["k5"]
    k6 = tabla_5[EC]["k6"]
    k7 = tabla_5[EC]["k7"]
    k8 = tabla_5[EC]["k8"]
    k9 = tabla_5[EC]["k9"]
    k10 = tabla_5[EC]["k10"]
    k11 = tabla_5[EC]["k11"]
    k12 = tabla_5[EC]["k12"]
    k13 = tabla_5[EC]["k13"]

    AFB_14300 = 10**((k1+k2*lg_gap + (k3*I_arc_14300/(
        k4*I_bf**7 +
        k5*I_bf**6 +
        k6*I_bf**5 +
        k7*I_bf**4 +
        k8*I_bf**3 +
        k9*I_bf**2 +
        k10*I_bf)) + (k11*lg_Ibf+k13*lg_Iarc_14300+lg_CF-lg_T))/-k12)
    return AFB_14300

def ecuacion_10 (EC, I_bf, lg_T, lg_Ibf, lg_gap, I_arc_600, lg_Iarc, lg_CF):
    k1 = tabla_3[EC]["k1"]
    k2 = tabla_3[EC]["k2"]
    k3 = tabla_3[EC]["k3"]
    k4 = tabla_3[EC]["k4"]
    k5 = tabla_3[EC]["k5"]
    k6 = tabla_3[EC]["k6"]
    k7 = tabla_3[EC]["k7"]
    k8 = tabla_3[EC]["k8"]
    k9 = tabla_3[EC]["k9"]
    k10 = tabla_3[EC]["k10"]
    k11 = tabla_3[EC]["k11"]
    k12 = tabla_3[EC]["k12"]
    k13 = tabla_3[EC]["k13"]

    AFB_600 = 10**((k1+k2*lg_gap + (k3*I_arc_600/(
        k4*I_bf**7 +
        k5*I_bf**6 +
        k6*I_bf**5 +
        k7*I_bf**4 +
        k8*I_bf**3 +
        k9*I_bf**2 +
        k10*I_bf)) + (k11*lg_Ibf+k13*lg_Iarc+lg_CF-lg_T))/-k12)
    return AFB_600
#*******************************
def ecuacion_11 (width, Voc, A, B):
    width_1 = (660.4 + (width - 660.4)*( (Voc + A)/B ))/25.4
    return width_1

def ecuacion_12 (height, Voc, A, B):
    # print("height: ", height)
    # print("Voc: ", Voc)
    # print("A: ", A)
    # print("B: ", B)
    height_1 =( 660.4 + (height - 660.4)*((Voc + A)/B) )/25.4
    return height_1 
#*******************************
def ecuacion_13 (height_1, width_1):
    EES = (height_1+width_1)/2
    return EES
#*******************************
def ecuacion_14 (b1, b2, b3, EES):
    CF = b1*EES**2 + b2*EES + b3
    return CF

def ecuacion_15 (b1, b2, b3, EES):
    CF = 1/(b1*EES**2 + b2*EES + b3)
    return CF
#*******************************
def ecuacion_16(I_arc_600, I_arc_2700, Voc):
    I_arc_1 = (I_arc_2700 - I_arc_600)/2.1 * (Voc - 2.7) + I_arc_2700
    return I_arc_1

def ecuacion_17(I_arc_2700, I_arc_14300, Voc):
    I_arc_2 = (I_arc_14300 - I_arc_2700)/11.6 * (Voc - 14.3) + I_arc_14300
    return I_arc_2

def ecuacion_18(I_arc_1, I_arc_2, Voc):
    I_arc_3 = I_arc_1*(2.7 - Voc) / 2.1 + I_arc_2*(Voc - 0.6) / 2.1
    return I_arc_3
#*******************************
def ecuacion_19 (E_600, E_2700, Voc):
    E_1 = (E_2700-E_600)/2.1*(Voc-2.7)+E_2700
    return E_1

def ecuacion_20 (E_2700, E_14300, Voc):
    E_2 = (E_14300-E_2700)/11.6*(Voc-14.3)+E_14300
    return E_2

def ecuacion_21 (E_1, E_2, Voc):
    E_3 = E_1*(2.7-Voc)/2.1 + E_2*(Voc-0.6)/2.1
    return E_3

#*******************************
def ecuacion_22 (AFB_600, AFB_2700, Voc):
    AFB_1 = ((AFB_2700-AFB_600)/2.1)*(Voc-2.7)+AFB_2700
    return AFB_1

def ecuacion_23 (AFB_2700, AFB_14300, Voc):
    AFB_2 = ((AFB_14300-AFB_2700)/11.6)*(Voc-14.3)+AFB_14300
    return AFB_2

def ecuacion_24 (AFB_1, AFB_2, Voc):
    AFB_3 = AFB_1*(2.7-Voc)/2.1 + AFB_2*(Voc-0.6)/2.1
    return AFB_3
#*******************************
def ecuacion_25 (Voc, I_arc_600, I_bf):
    I_arc = (1 / np.sqrt((0.6 / Voc)**2 * ((1 / I_arc_600**2) - ((0.6**2 - Voc**2) / (0.6**2 * I_bf**2)))))
    return I_arc
#*******************************
#OBTENIDO DE LA TABLA 6
def calcula_width (EC, width, Voc):
    if EC == "VCB" or EC == "VCBB" or EC == "HCB":
        if width < 508:
            width_1 = 20
        elif width >= 508 and width <= 660.4:
            width_1 = 0.03937*width
        elif width > 660.4 and width <= 1244.6:
            width_1 = ecuacion_11 (width, Voc, enclosure_AB[EC]["A"], enclosure_AB[EC]["B"])
        elif width > 1244.6:
            width_1 = ecuacion_11 (1244.6, Voc, enclosure_AB[EC]["A"], enclosure_AB[EC]["B"])
    return width_1

#OBTENIDO DE LA TABLA 6
def calcula_height (EC, height, Voc):
    if EC == "VCB":
        if height < 508:
            height_1 = 20
        elif height >= 508 and height <= 660.4:
            height_1 = 0.03937*height
        elif height > 660.4 and height <= 1244.6:
            height_1 = 0.03937*height
        elif height > 1244.6:
            height_1 = 49
    elif EC == "VCBB" or EC == "HCB":
        if height < 508:
            height_1 = 20
        elif height >= 508 and height <= 660.4:
            height_1 = 0.03937*height
        elif height > 660.4 and height <= 1244.6:
            height_1 = ecuacion_12(height, Voc, enclosure_AB[EC]["A"], enclosure_AB[EC]["B"])
        elif height > 1244.6:
            height_1 = ecuacion_12(1244.6, Voc, enclosure_AB[EC]["A"], enclosure_AB[EC]["B"])
    return height_1
#*******************************
def calcula_VarCF(Voc, EC):
    k1 = tabla_2[EC]["k1"]
    k2 = tabla_2[EC]["k2"]
    k3 = tabla_2[EC]["k3"]
    k4 = tabla_2[EC]["k4"]
    k5 = tabla_2[EC]["k5"]
    k6 = tabla_2[EC]["k6"]
    k7 = tabla_2[EC]["k7"]

    VarCF = k1*Voc**6 + k2*Voc**5 + k3*Voc**4 + k4*Voc**3 + k5*Voc**2 + k6*Voc + k7 
    return VarCF
#*******************************
def I_arco_inter1 (EC, I_bf, lg_Ibf, lg_gap):
    I_arc_600 = ecuacion_1 (EC, "600V", I_bf, lg_Ibf,lg_gap)
    print (">>> Corriente de arco intermedia a 600V <<< \n", "I_arc_600 (kA): ", I_arc_600, "\n") #Corriente rms promedio
    return I_arc_600

def I_arco_fin1 (Voc, I_bf, I_arc_600):
    I_arc = ecuacion_25 (Voc, I_arc_600, I_bf)
    print (">>> Corriente de arco final <<< \n", "I_arc (kA): ", I_arc, "\n") #Corriente rms promedio
    return I_arc

def I_arco_inter2 (EC, I_bf, lg_Ibf, lg_gap):
    I_arc_600 = (ecuacion_1 (EC, "600V", I_bf, lg_Ibf,lg_gap))
    I_arc_2700 = (ecuacion_1 (EC, "2700V", I_bf, lg_Ibf,lg_gap))
    I_arc_14300 = (ecuacion_1 (EC, "14300V", I_bf, lg_Ibf,lg_gap))
    print (">>> Corrientes de arco intermedias (Interpolando) <<<\n", "I_arc_600 (kA): ", I_arc_600) #Corriente rms promedio
    print ("I_arc_2700 (kA): ", I_arc_2700) #Corriente rms promedio
    print ("I_arc_14300 (kA): ", I_arc_14300, "\n") #Corriente rms promedio
    return I_arc_600, I_arc_2700, I_arc_14300

def I_arco_fin2 (I_arc_600, I_arc_2700, I_arc_14300, Voc):
    # >>>>>>> NOTE: PASO 2 <<<<<<< DETERMINAR LA CORRIENTE DE ARCO FINAL | ARCING CURRENT (Iarc)
    I_arc_1 = ecuacion_16 (I_arc_600, I_arc_2700, Voc) #primera interpolación entre 600V y 2700V
    I_arc_2 = ecuacion_17 (I_arc_2700, I_arc_14300, Voc)
    I_arc_3 = ecuacion_18 (I_arc_1, I_arc_2, Voc)
    print ("I_arc_1 (kA): ", I_arc_1)
    print ("I_arc_2 (kA): ", I_arc_2)
    print ("I_arc_3 (kA): ", I_arc_3, "\n")

    global I_arc #NOTE: HACEMOS I_arc UNA VARIABLE GLOBAL
    if Voc > 600 and Voc <= 2.7:  
        I_arc = I_arc_3   
        print (">>> Corriente de arco final (kA) <<< \n", "I_arc (kA): ", I_arc, "\n") 
    elif Voc > 2.7:
        I_arc = I_arc_2
        print (">>> Corriente de arco final (kA) <<< \n", "I_arc (kA): ", I_arc, "\n")

    return I_arc

def lee_duracion_t ():
    #Para encontrar la duración del arco "T" se usa la Curva Tiempo-Corriente característica del fusible de potencia 
    #T: Tiempo de liberacion de la falla 
    T = int(input("Ingresa la duración del arco (T) en ms: "))
    print("\n") #Salto de linea
    return T

def enclosure (EC, Voc, height, width, depth):    ################################# REVISAR QUE DEPTH SEA ENVIADO COMO DATO 
    if EC == "VCB" or EC == "VCBB" or EC == "HCB":
        if Voc < 0.600 and height < 508 and width < 508:
            if depth <= 203.2:
                enclosure_type = "shallow"
            else:
                enclosure_type = "typical"
        else:
            enclosure_type = "typical"
    else:
        enclosure_type = "open"
    print ("enclosure: ", enclosure_type, "\n")
    return enclosure_type

def calcula_CF (enclosure_type, EC, width, height, Box_type, Voc):
    if enclosure_type == "typical":
        width_1 = calcula_width (EC, width, Voc)
        height_1 = calcula_height (EC, height, Voc)
        EES = ecuacion_13 (height_1, width_1)
        if EES < 20:
            EES = 20
        CF = abs( ecuacion_14 ( Box_type["Typical"][EC]["b1"] , Box_type["Typical"][EC]["b2"], Box_type["Typical"][EC]["b3"], EES) ) #####################################REVISAR VALOR ABSOLUTO
        print (">>> Ajuste de ancho y altura <<<\n", "width_1: ", width_1)
        print ("height_1: ", height_1, "\n")
        print (">>> Equivalent Enclosure Size <<<\n", "EES: ", EES, "\n")
        print (">>> Factor de Correccion <<<\n", "CF: ",CF, "\n")

    elif enclosure_type == "shallow":
        width_1 = 0.03937*width
        height_1 = 0.03937*height
        EES = ecuacion_13 (height_1, width_1)
        CF = abs( ecuacion_15 ( Box_type["Shallow"][EC]["b1"] , Box_type["Shallow"][EC]["b2"], Box_type["Shallow"][EC]["b3"], EES) ) #####################################REVISAR VALOR ABSOLUTO
        print ("width_1: ", width_1)
        print ("height_1: ", height_1)
        print ("EES: ", EES)
        print (">>> Factor de Correccion <<<\n", "CF: ",CF, "\n")
    elif enclosure_type == "open": #"open" <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        CF = 1
    else: print("ERROR: ENCLOSURE TYPE")
    return CF

def calc_E_AFB2 (dis, EC, I_bf, I_arc_600, I_arc_2700, I_arc_14300, T, CF, Voc, lg_Ibf, lg_gap):
    #>>>>>>> NOTE: PASO 4 <<<<<<<
    lg_dis = math.log10(dis)  #logaritmo base 10 de "dis"
    lg_Iarc_600 = math.log10(I_arc_600)
    lg_Iarc_2700 = math.log10(I_arc_2700)
    lg_Iarc_14300 = math.log10(I_arc_14300)
    lg_CF = math.log10(1/CF)

    E_600 = ecuacion_3456(tabla_3, EC, T, I_bf, lg_Ibf, lg_gap, lg_dis, lg_Iarc_600, lg_CF, I_arc_600)
    E_2700 = ecuacion_3456(tabla_4, EC, T, I_bf, lg_Ibf, lg_gap, lg_dis, lg_Iarc_2700, lg_CF, I_arc_2700)
    E_14300 = ecuacion_3456(tabla_5, EC, T, I_bf, lg_Ibf, lg_gap, lg_dis, lg_Iarc_14300, lg_CF, I_arc_14300)
    print(">>> Valores intermedios de la Energia Incidente <<<\n", "E_600 (J/mc2):", E_600)
    print("E_2700 (J/mc2): ", E_2700)
    print("E_14300 (J/mc2): ", E_14300, "\n")

    #>>>>>>> NOTE: PASO 5 <<<<<<<
    E_1 = ecuacion_19 (E_600, E_2700, Voc)
    E_2 = ecuacion_20 (E_2700, E_14300, Voc)
    E_3 = ecuacion_21 (E_1, E_2, Voc)
    print ("E_1 (J/mc2): ", E_1)
    print ("E_2 (J/mc2): ", E_2)
    print ("E_3 (J/mc2): ", E_3, "\n")

    if Voc > 600 and Voc <= 2.7:  
        E = E_3   
        print (">>> Energia Incidente final <<<\n", "E (J/mc2): ", E) 
        E = E/4.184 #Convierte la energia incidente a cal/cm2
        print ("E (cal/cm2): ", E, "\n")

    elif Voc > 2.7:
        E = E_2
        print (">>> Energia Incidente final <<<\n", "E (J/mc2): ", E)
        E = E/4.184 #Convierte la energia incidente a cal/cm2
        print ("E (cal/cm2): ", E, "\n")

    #>>>>>>> NOTE: PASO 6 <<<<<<<
    lg_T = math.log10(20/T)
    AFB_600 = ecuacion_7 (EC, I_bf, lg_T, lg_Ibf, lg_gap, I_arc_600 , lg_Iarc_600, lg_CF)
    AFB_2700 = ecuacion_8 (EC, I_bf, lg_T, lg_Ibf, lg_gap, I_arc_2700 , lg_Iarc_2700, lg_CF)
    AFB_14300 = ecuacion_9 (EC, I_bf, lg_T, lg_Ibf, lg_gap, I_arc_14300, lg_Iarc_14300, lg_CF)
    print (">>> Valores intermedios del limite de arco eléctrico <<<\n", "AFB_600 (mm): ", AFB_600)
    print ("AFB_2700 (mm): ", AFB_2700)
    print ("AFB_14300 (mm): ", AFB_14300, "\n")

    #>>>>>>> NOTE: PASO 7 <<<<<<<
    AFB_1 = ecuacion_22 (AFB_600, AFB_2700, Voc)
    AFB_2 = ecuacion_23 (AFB_2700, AFB_14300, Voc)
    AFB_3 = ecuacion_24 (AFB_1, AFB_2, Voc)
    print("AFB_1: ", AFB_1)
    print("AFB_2: ", AFB_2)
    print("AFB_3: ", AFB_3, "\n")

    if Voc > 600 and Voc <= 2.7:  
        AFB = AFB_3   
        print (">>> Limite de arco final <<<\n", "AFB (mm): ", AFB, "\n") 
    elif Voc > 2.7:
        AFB = AFB_2
        print (">>> Limite de arco final <<<\n", "AFB (mm): ", AFB, "\n")

    return E, AFB
                #dis, EC, I_bf, I_arc_600_min, I_arc_min, Tmin, CF, lg_Ibf, lg_gap Datos recibidos de la fucnion main_afp_min
def calc_E_AFB1 (dis, EC, I_bf, I_arc_600, I_arc, T, CF, lg_Ibf, lg_gap): #>>>>> NOTE: SISTEMAS MAYORES A 208V Y MENORES A 600V <<<<<
    #>>>>>>> NOTE: PASO 4 <<<<<<<
    lg_dis = math.log10(dis)  #logaritmo base 10 de "dis"
    lg_Iarc = math.log10(I_arc) #main_afp: I_arc | main_afp_min: I_arc_min
    lg_CF = math.log10(1/CF)
    E_600_menor = ecuacion_3456 (tabla_3, EC, T, I_bf, lg_Ibf, lg_gap, lg_dis, lg_Iarc, lg_CF, I_arc_600)
    print("E_600_menor: ", E_600_menor, "\n")

    #>>>>>>> NOTE: PASO 5 <<<<<<<
    E = E_600_menor  
    print (">>> Energia Incidente final <<<\n", "E (J/mc2): ", E) 
    E = E/4.184 #Convierte la energia incidente a cal/cm2
    print ("E (cal/cm2): ", E, "\n")

    #>>>>>>> NOTE: PASO 6 <<<<<<<
    lg_T = math.log10(20/T)
    AFB_600_menor = ecuacion_10 (EC, I_bf, lg_T, lg_Ibf, lg_gap, I_arc_600, lg_Iarc, lg_CF)
    print (">>> Valor intermedio del limite de arco eléctrico <<<\n", "AFB_600_menor (mm): ", AFB_600_menor, "\n")

    #>>>>>>> NOTE: PASO 7 <<<<<<<
    AFB = AFB_600_menor
    print (">>> Limite de arco final <<<\n", "AFB (mm): ", AFB) 

    return E, AFB

def I_arco_inter_min1 (Voc, EC, I_arc):
    #>>>>>>> NOTE: PASO 8 <<<<<<<
    VarCF = calcula_VarCF(Voc, EC)
    CF_VarCF = 1-(0.5*VarCF)
    print ("\n>>> Factor de correccion <<<\n", "CF_VarCF: ", CF_VarCF, "\n")

    #>>>>>>> NOTE: PASO 9 <<<<<<< 
    I_arc_600_min = ecuacion_2 (I_arc, CF_VarCF) #NOTE: Esta ecuacion solo multiplica I_arc * CF_VarCF
    print ("I_arc_600_min: ", I_arc_600_min)

    return I_arc_600_min

def I_arco_fin_min1 (I_arc_600_min):
    I_arc_min = I_arc_600_min
    return I_arc_min

def I_arco_inter_min2 (Voc, EC, I_arc_600, I_arc_2700, I_arc_14300):
    #>>>>>>> NOTE: PASO 8 <<<<<<<
    VarCF = calcula_VarCF(Voc, EC)
    CF_VarCF = 1-0.5*VarCF
    print(">>>>> VARIACION DE LA CORRIENTE DE ARCO <<<<<\n")
    print (">>> Factor de correccion <<<\n", "CF_VarCF", CF_VarCF, "\n")

    #>>>>>>> NOTE: PASO 9 <<<<<<< POSIBLEMENTE HACER EL CALCULO DIRECTO DE LA ECUACION 2
    I_arc_600_min = ecuacion_2 (I_arc_600, CF_VarCF)
    I_arc_2700_min = ecuacion_2 (I_arc_2700, CF_VarCF)
    I_arc_14300_min = ecuacion_2 (I_arc_14300, CF_VarCF)
    print (">>> Ajuste - Corrientes de arco intermedias <<<\n", "I_arc_600_min (kA): ", I_arc_600_min)
    print ("I_arc_2700_min (kA): ", I_arc_2700_min)
    print ("I_arc_14300_min (kA): ", I_arc_14300_min, "\n")
    return I_arc_600_min, I_arc_2700_min, I_arc_14300_min

def I_arco_fin_min2 (I_arc_600_min, I_arc_2700_min, I_arc_14300_min, Voc):
    I_arc_1 = ecuacion_16 (I_arc_600_min, I_arc_2700_min, Voc)
    I_arc_2 = ecuacion_17 (I_arc_2700_min, I_arc_14300_min, Voc)
    I_arc_3 = ecuacion_18 (I_arc_1, I_arc_2, Voc)
    print ("I_arc_1: ", I_arc_1)
    print ("I_arc_2: ", I_arc_2)
    print ("I_arc_3: ", I_arc_3, "\n")

    if Voc > 600 and Voc <= 2.7:  
        I_arc_min = I_arc_3   
        print (">>> Corriente de arco final reducida <<<\n", "I_arc_min (kA): ", I_arc_min, "\n") 
    elif Voc > 2.7:
        I_arc_min = I_arc_2
        print (">>> Corriente de arco final reducida <<<\n", "I_arc_min (kA): ", I_arc_min, "\n")

    return I_arc_min