import math

# Arcing current Ia
def ecuacion_1 (K, lg_Ibf, Voc, gap):
    lg_Ia = K + 0.662*lg_Ibf + 0.0966*Voc + 0.000526*gap + 0.5588*Voc*lg_Ibf - 0.00304*gap*lg_Ibf
    I_arc = 10**lg_Ia 
    print (">>> Corriente de arco final <<< \n", "I_arc (kA): ", I_arc, "\n") #Corriente rms promedio
    return lg_Ia, I_arc

def ecuacion_2 (lg_Ibf):
    lg_Ia = 0.00402 + 0.983*lg_Ibf
    I_arc = 10**lg_Ia
    print (">>> Corriente de arco final <<< \n", "I_arc (kA): ", I_arc, "\n") #Corriente rms promedio
    return lg_Ia, I_arc

# Incident Energy
def ecuacion_4 (K1, K2, lg_Ia, gap, Cf, tfalla, dis, xfactor):
    lg_En = K1 + K2 + 1.081*lg_Ia + 0.0011*gap

    #NOTE: Ecuacion (5)
    En = 10**lg_En #Energía incidente normalizada

    #NOTE: Ecuacion (6)
    E = 4.184*Cf*En*(tfalla/0.2)*((610**xfactor)/(dis**xfactor))
    print (">>> Parametros de calculo <<<")
    print ("K1: ", K1)
    print ("K2: ", K2)
    print ("lg_Ia: ", lg_Ia)
    print ("gap: ", gap)
    print ("Cf: ", Cf)
    print ("tfalla: ", tfalla)
    print ("dis: ", dis)
    print ("xfactor: ", xfactor, "\n")
    print (">>> Energia Incidente normalizada <<<\n", "En (J/mc2): ", En, "\n")
    print (">>> Energia Incidente final <<<\n", "E (J/mc2): ", E)
    E = E/4.184 #Convierte la energia incidente a cal/cm2
    print ("E (cal/cm2): ", E, "\n") 

    return lg_En, En, E

# Flas Protection Boundary

def ecuacion_8 (Cf, En, tfalla, EB, xfactor):
    AFB = (4.184*Cf*En*(tfalla/0.2)*((610**xfactor)/EB))**(1/xfactor)
    print (">>> Limite de arco final <<<\n", "AFB (mm): ", AFB, "\n") 
    return AFB

# Current limiting fuses

# 5.6.1 Equations for Class L fuses 1601 A–2000 A 
def ecuacion_10 (Ibf):
    E = 4.184*(-0.1284*Ibf+32.262)
    return E

def ecuacion_11 (Ibf):
    E = 4.184*(-0.5177*Ibf+57.917)
    return E

# 5.6.2 Equations for Class L fuses 1201 A–1600 A
def ecuacion_12 (Ibf):
    E = 4.184*(-0.1863*Ibf+27.926)
    return E

def ecuacion_13 (Ibf):
    E = 4.184*(-1.5504*Ibf+71.303)
    return E

def ecuacion_14 (Ibf):
    E = 4.184*(-0.0631*Ibf+7.0878)
    return E

#5.6.3 Equations for Class L fuses 801 A–1200 A 
def ecuacion_15 (Ibf):
    E = 4.184*(-0.1928*Ibf+14.226)
    return E

def ecuacion_16 (Ibf):
    E = 4.184*(0.0143*Ibf**2-1.3919*Ibf+34.045)
    return E

# 5.6.4 Equations for Class L fuses 601 A–800 A 
def ecuacion_17 (Ibf):
    E = 4.184*(-0.0601*Ibf+2.8992)
    return E

# 5.6.5 Equations for Class RK1 fuses 401 A–600 A 
def ecuacion_18 (Ibf):
    E = 4.184*(-3.0545*Ibf+43.364)
    return E

def ecuacion_19 (Ibf):
    E = 4.184*(-0.0507*Ibf+1.3964)
    return E

# 5.6.6 Equations for Class RK1 fuses 201 A–400 A
def ecuacion_20 (Ibf):
    E = 4.184*(-19.053*Ibf+96.808)
    return E

def ecuacion_21 (Ibf):
    E = 4.184*(-0.0302*Ibf+0.9321)
    return E

# 5.6.7 Equations for Class RK1 fuses 101A–200 A 
def ecuacion_22 (Ibf):
    E = 4.184*(-18.409*Ibf+36.355)
    return E

def ecuacion_23 (Ibf):
    E = 4.184*(-4.2628*Ibf+13.721)
    return E

# 5.6.8 Equations for Class RK1 fuses up to 100 A
def ecuacion_24 (Ibf):
    E = 4.184*(-11.176*Ibf+13.565)
    return E

def ecuacion_25 (Ibf):
    E = 4.184*(-1.4583*Ibf+2.2917)
    return E

def obtener_parametros_main_2002(dic_system_data):
    Voc = float(dic_system_data["Voc"])
    I_bf = float(dic_system_data["I_bf"])
    gap = float(dic_system_data["gap"])
    lg_Ibf = math.log10(I_bf) #logaritmo base 10 de "I_bf"
    ET = dic_system_data["ET"] 
    ground = dic_system_data["ground"]
    #Define los parámetros K y K1
    if ET == "BOX": 
        K = -0.097
        K1 = -0.555
    if ET == "OA":
        K = -0.153
        K1 = -0.792
    if ground == "Grounded":
        K2 = -0.113
    if ground == "Ungrounded" or ground == "High Resistance":
        K2 = 0
    if Voc > 1:
        Cf = 1.0
    if Voc <= 1:
        Cf = 1.5

    return Voc, lg_Ibf, I_bf, gap, K, K1, K2, Cf

def obtener_parametros_mainafp_2002(dic_system_data):
    K1 = float(dic_system_data["K1"])
    K2 = float(dic_system_data["K2"])
    Cf = float(dic_system_data["Cf"])
    lg_Ia = float(dic_system_data["lg_Ia"])
    gap = float(dic_system_data["gap"])
    tfalla = float(dic_system_data["Tfalla"])
    dis = float(dic_system_data["dis"])
    xfactor = float(dic_system_data["xfactor"])
    return K1, K2, Cf, lg_Ia, gap, tfalla, dis, xfactor

def obtener_parametros_mainafpmin_2002(dic_system_data):
    K1 = float(dic_system_data["K1"])
    K2 = float(dic_system_data["K2"])
    Cf = float(dic_system_data["Cf"])
    I_arc_min = float(dic_system_data["I_arc_min"])
    gap = float(dic_system_data["gap"])
    tfalla_min = float(dic_system_data["Tfalla_min"])
    dis = float(dic_system_data["dis"])
    xfactor = float(dic_system_data["xfactor"])
    lg_Ia_min = math.log10(I_arc_min)
    return K1, K2, Cf, lg_Ia_min, gap, tfalla_min, dis, xfactor

def main_2002 (dic_system_data):
    print ("#################### INICIO main_2002 | I_arc | ", dic_system_data["tipo_equipo"], " ####################", "\n")
    Voc, lg_Ibf, I_bf, gap, K, K1, K2, Cf = obtener_parametros_main_2002(dic_system_data)
    dic_system_data["K"] = K
    dic_system_data["K1"] = K1
    dic_system_data["K2"] = K2
    dic_system_data["Cf"] = Cf

    if Voc >= 0.208 and Voc <= 1:
        #ARCING CURRENT
        lg_Ia, I_arc = ecuacion_1(K, lg_Ibf, Voc, gap)
        dic_system_data["lg_Ia"] = lg_Ia
        dic_system_data["I_arc"] = I_arc
        print("Datos recopilados:")
        print (dic_system_data, "\n")
        print ("#################### FIN main_2002 | I_arc | ", dic_system_data["tipo_equipo"], " ####################", "\n")
        
    elif Voc > 1 and Voc <= 15.0:
        #ARCING CURRENT
        lg_Ia, I_arc = ecuacion_2(lg_Ibf)
        dic_system_data["lg_Ia"] = lg_Ia
        dic_system_data["I_arc"] = I_arc
        print("Datos recopilados:")
        print (dic_system_data, "\n")
        print ("#################### FIN main_2002 | I_arc | ", dic_system_data["tipo_equipo"], " ####################", "\n")

    else:
        print ("ALERTA: Voltaje fuera del rango \n")

def main_afp_2002(dic_system_data):
    print ("#################### INICIO main_afp_2002 | calculo de E, AFB, I_arc_min | ", dic_system_data["tipo_equipo"] ,  "####################", "\n")
    K1, K2, Cf, lg_Ia, gap, tfalla, dis, xfactor = obtener_parametros_mainafp_2002(dic_system_data)
    lg_En, En, E = ecuacion_4 (K1, K2, lg_Ia, gap, Cf, tfalla, dis, xfactor) #Calculo energia incidente
    # E = E/4.184 #Convierte la energia incidente a cal/cm2 NOTE: Este paso se hace en lac ecuacion (4)
    dic_system_data["lg_En"] = lg_En
    dic_system_data["En"] = En
    dic_system_data["E"] = E
    EB = 5.0208 # J/cm2 
    # EB = 1.2 cal/cm2
    dic_system_data["EB"] = EB
    AFB = ecuacion_8(Cf, En, tfalla, EB, xfactor) #Calculo flash protection boundary
    dic_system_data["AFB"] = AFB
    print("Datos recopilados:")
    print (dic_system_data, "\n")
    print ("#################### FIN main_afp_2002 | calculo de E, AFB, I_arc_min | ", dic_system_data["tipo_equipo"] ,  "####################", "\n")

def main_afpmin_2002(dic_system_data):
    print ("#################### INICIO main_afpmin_2002 | calculo de E_min, AFB_min | ", dic_system_data["tipo_equipo"] ,  "####################", "\n")
    K1, K2, Cf, lg_Ia_min, gap, tfalla_min, dis, xfactor = obtener_parametros_mainafpmin_2002(dic_system_data)
    lg_En_min, En_min, E_min = ecuacion_4 (K1, K2, lg_Ia_min, gap, Cf, tfalla_min, dis, xfactor) #Calculo energia incidente
    # E_min = E_min/4.184 #Convierte la energia incidente a cal/cm2 NOTE: Este paso se hace en lac ecuacion (4)
    dic_system_data["lg_En_min"] = lg_En_min
    dic_system_data["En_min"] = En_min
    dic_system_data["E_min"] = E_min
    EB_min = 5.0
    dic_system_data["EB_min"] = EB_min
    AFB_min = ecuacion_8(Cf, En_min, tfalla_min, EB_min, xfactor) #Calculo flash protection boundary
    dic_system_data["AFB_min"] = AFB_min
    print("Datos recopilados:")
    print (dic_system_data, "\n")
    print ("#################### FIN main_afpmin_2002 | calculo de E_min, AFB_min | ", dic_system_data["tipo_equipo"] ,  "####################", "\n")