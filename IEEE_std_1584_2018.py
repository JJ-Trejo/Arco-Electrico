import math #para calcular el logaritmo base 10 de I_bf
import numpy as np
#import openpyxl #Importa la biblioteca Openpyxl
#import pandas as pd
from tablas_2018 import Box_type #Se importan las tablas (diccionarios) de la IEEE Std. 1584-2018
#Se importan las ecuaciones (funciones) de la IEEE Std. 1584-2018
from ecuaciones_2018 import obtener_parametros_main, obtener_parametros_afp1, obtener_parametros_afp2, obtener_parametros_afp_min1, obtener_parametros_afp_min2, I_arco_inter1, I_arco_fin1, I_arco_inter2, I_arco_fin2, lee_duracion_t, enclosure, calcula_CF, calc_E_AFB2, calc_E_AFB1, I_arco_inter_min1, I_arco_fin_min1, I_arco_inter_min2, I_arco_fin_min2
from imprimir import imprime

def main (dic_system_data):
    print ("#################### INICIO main | I_arc | ", dic_system_data["EC"] ,  " ####################", "\n")
    EC, Voc, I_bf, lg_Ibf, lg_gap = obtener_parametros_main (dic_system_data) #Se obtienen los parametros del sistema ingresado
    dic_system_data["lg_Ibf"] = lg_Ibf
    dic_system_data["lg_gap"] = lg_gap
    #>>>>> NOTE: SISTEMAS MAYORES A 208V Y MENORES A 600V <<<<<
    if Voc >= 0.208 and Voc <= 0.600:
        I_arc_600 = I_arco_inter1 (EC, I_bf, lg_Ibf,lg_gap) #NOTE: PASO 1
        I_arc = I_arco_fin1 (Voc, I_bf, I_arc_600)          #NOTE: PASO 2
        dic_system_data["I_arc_600"] = I_arc_600
        dic_system_data["I_arc"] = float(I_arc) #Se convierte el dato de tipo numpy a dato de tipo flotante
        print("Datos recopilados:")
        print (dic_system_data, "\n")
        print ("#################### FIN main | I_arc | ", dic_system_data["EC"] , "####################", "\n")

    #>>>>> NOTE: SISTEMAS MAYORES A 600V Y MENORES A 15 kV <<<<<
    elif Voc > 0.600 and Voc <= 15.0:
        I_arc_600, I_arc_2700, I_arc_14300 = I_arco_inter2 (EC, I_bf, lg_Ibf, lg_gap) #NOTE: PASO 1
        I_arc = I_arco_fin2 (I_arc_600, I_arc_2700, I_arc_14300, Voc)    #NOTE: PASO 2
        dic_system_data["I_arc_600"] = I_arc_600
        dic_system_data["I_arc_2700"] = I_arc_2700
        dic_system_data["I_arc_14300"] = I_arc_14300
        dic_system_data["I_arc"] = I_arc
        print("Datos recopilados:")
        print (dic_system_data, "\n")
        print ("#################### FIN main | I_arc | ", dic_system_data["EC"] , "####################", "\n")
    else:
        print ("ALERTA: Voltaje fuera del rango \n")

#>>>>> NOTE: SISTEMAS MAYORES A 600V Y MENORES A 15 kV <<<<<
def main_afp(dic_system_data):
    print ("#################### INICIO main afp | calculo de E, AFB, I_arc_min | ", dic_system_data["EC"] ,  "####################", "\n")
    Voc = float( dic_system_data["Voc"] )
    #>>>>> NOTE: SISTEMAS MAYORES A 208V Y MENORES A 600V <<<<<
    if Voc >= 0.208 and Voc <= 0.600:
        dis, EC, I_bf, I_arc_600, T, Voc, lg_Ibf, lg_gap, width, height, depth, I_arc = obtener_parametros_afp1 (dic_system_data) #Se obtienen los parametros del sistema ingresado
        enclosure_type = enclosure (EC, Voc, height, width, depth) #Determina el tipo de gabinete Shallow, Typical, Open #NOTE: PASO 3
        CF = calcula_CF (enclosure_type, EC, width, height, Box_type, Voc) #NOTE: PASO 3 
        # energia_incidente & limite_arco_electrico
        E, AFB = calc_E_AFB1 ( dis, EC, I_bf, I_arc_600, I_arc, T, CF, lg_Ibf, lg_gap) #NOTE: PASO 4,5,6,7
        I_arc_600_min = I_arco_inter_min1 (Voc, EC, I_arc_600) #NOTE: PASO 8,9 ##################################################### pasar I_arc en lugar de I_arc_600
        I_arc_min = I_arco_fin_min1 (I_arc_600_min) #NOTE: PASO 10
        dic_system_data["CF"] = CF
        dic_system_data["E"] = E
        dic_system_data["AFB"] = AFB  
        dic_system_data["I_arc_600_min"] = I_arc_600_min
        dic_system_data["I_arc_min"] = I_arc_min
        print("Datos recopilados:")
        print (dic_system_data, "\n")
        print ("#################### FIN main afp | calculo de E, AFB, I_arc_min | ", dic_system_data["EC"] ,  "####################", "\n")
        
    #>>>>> NOTE: SISTEMAS MAYORES A 600V Y MENORES A 15 kV <<<<<
    elif Voc > 0.600 and Voc <= 15.0:
        dis, EC, I_bf, I_arc_600, I_arc_2700, I_arc_14300, T, Voc, lg_Ibf, lg_gap, width, height, depth  = obtener_parametros_afp2 (dic_system_data) #Se obtienen los parametros del sistema ingresado
        enclosure_type = enclosure (EC, Voc, height, width, depth) #Determina el tipo de gabinete Shallow, Typical, Open #NOTE: PASO 3
        CF = calcula_CF (enclosure_type, EC, width, height, Box_type, Voc) #NOTE: PASO 3 
        # energia_incidente_limite_arco_electrico
        E, AFB = calc_E_AFB2 ( dis, EC, I_bf, I_arc_600, I_arc_2700, I_arc_14300, T, CF, Voc, lg_Ibf, lg_gap) #NOTE: PASO 4,5,6,7
        I_arc_600_min, I_arc_2700_min, I_arc_14300_min = I_arco_inter_min2 (Voc, EC,  I_arc_600, I_arc_2700, I_arc_14300) #NOTE: PASO 8,9
        I_arc_min = I_arco_fin_min2 (I_arc_600_min, I_arc_2700_min, I_arc_14300_min, Voc) #NOTE: PASO 10
        dic_system_data["CF"] = CF
        dic_system_data["E"] = E
        dic_system_data["AFB"] = AFB  
        dic_system_data["I_arc_600_min"] = I_arc_600_min
        dic_system_data["I_arc_2700_min"] = I_arc_2700_min
        dic_system_data["I_arc_14300_min"] = I_arc_14300_min
        dic_system_data["I_arc_min"] = I_arc_min
        print("Datos recopilados:")
        print (dic_system_data, "\n")
        print ("#################### FIN main afp | calculo de E, AFB, I_arc_min | ", dic_system_data["EC"] ,  "####################", "\n")
    else:
            print ("ALERTA: Voltaje fuera del rango \n")

def main_afp_min(dic_system_data):
    print ("#################### INICIO main afp_min | calculo de E_min, AFB_min | ", dic_system_data["EC"] ,  "####################", "\n")
    Voc = float( dic_system_data["Voc"] )
    #>>>>> NOTE: SISTEMAS MAYORES A 208V Y MENORES A 600V <<<<<
    if Voc >= 0.208 and Voc <= 0.600:
        dis, EC, I_bf, I_arc_600_min, I_arc_min, Tmin, CF, lg_Ibf, lg_gap = obtener_parametros_afp_min1(dic_system_data)
        # energia_incidente_limite_arco_electrico
        E, AFB = calc_E_AFB1 ( dis, EC, I_bf, I_arc_600_min, I_arc_min, Tmin, CF, lg_Ibf, lg_gap) #NOTE: PASO 4,5,6,7   #NOTE: REVISAR IARCMIN ##################################################
        dic_system_data["E_min"] = E
        dic_system_data["AFB_min"] = AFB
        print("Datos recopilados:")
        print (dic_system_data, "\n")
        print ("#################### FIN main afp_min | calculo de E_min, AFB_min | ", dic_system_data["EC"] ,  "####################", "\n")
    #>>>>> NOTE: SISTEMAS MAYORES A 600V Y MENORES A 15 kV <<<<<
    elif Voc > 0.600 and Voc <= 15.0:
        dis, EC, I_bf, I_arc_600_min, I_arc_2700_min, I_arc_14300_min, Tmin, Voc, lg_Ibf, lg_gap, CF = obtener_parametros_afp_min2(dic_system_data)
        print (">>>>> CALCULO USANDO LA CORRIENTE DE ARCO REDUCIDA <<<<<", "\n")
        # energia_incidente_limite_arco_electrico
        E, AFB = calc_E_AFB2 ( dis, EC, I_bf, I_arc_600_min, I_arc_2700_min, I_arc_14300_min, Tmin, CF, Voc, lg_Ibf, lg_gap) #NOTE: PASO 4,5,6,7
        dic_system_data["E_min"] = E
        dic_system_data["AFB_min"] = AFB
        print("Datos recopilados:")
        print (dic_system_data, "\n")
        print ("#################### FIN main afp_min | calculo de E_min, AFB_min | ", dic_system_data["EC"] ,  "####################", "\n")
    else:
        print ("ALERTA: Voltaje fuera del rango \n")