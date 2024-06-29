import tkinter as tk
from tkinter import font
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import random
import os


#main

#simula 1 mano
#mano, True(usuario mano), False(bot mano)
#mazo, lista que contiene 40 objetos cartas mezcladas
#puntos_jugador son los puntos de cada jugador
def jugar_mano(mano, mazo, puntos_jugador, puntos_jugador2, elementos, cartas_p1, cartas_p2):
    global info
    
    try:
        info["elementos"]["comentario"].config(text=" ")
    except:
        pass
    
    #se limpia el tablero
    try:
        limpiar_mesa(info["elementos"]["cartas mesa"], info["elementos"]["fondo mesa"])
    except:
        pass
    
    #se les dan 3 cartas diferentes a cada jugador
    cartas_p1, cartas_p2 = repartir(crear_mazo())
    
    
    #se le asignan valores a variables necesarias
    puntos_mano_p1 = 0
    puntos_mano_p2 = 0
    parda1 = False
    parda2 = False
    parda3 = False
    carta_vacia = Carta(" ", " ", 0, 0, " ", " ")
    clasificacion = calificar_mano(cartas_p2)
    cartas_p1 = ordenar_cartas(cartas_p1)
    cartas_p2 = ordenar_cartas(cartas_p2)
    ronda = 0
    info = {
        "eleccion" : None,
        "primero" : True,
        "segundo" : 1,
        "puntos_primero" : [None, None],
        "quiero" : 0,
        "cartas_jugadas" : [carta_vacia] * 6,
        "puntos_jugador" : puntos_jugador,
        "puntos_jugador2" : puntos_jugador2,
        "cartas_j1" : cartas_p1,
        "cartas_j2" : cartas_p2,
        "mano" : mano,
        "parda1" : parda1,
        "parda2" : parda2,
        "parda3" : parda3,
        "clasificacion" : clasificacion,
        "ronda" : ronda,
        "puntos_mano_j1" : puntos_mano_p1,
        "puntos_mano_j2" : puntos_mano_p2,
        "elementos" : elementos
    }
    
    actualizar_frame()
    
    #ronda 1
    
    info["ronda"] = 1
    
    if mano:
        mostrar_mesa(info, mano, info["elementos"]["mesa"])
        info = elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_jugador, puntos_jugador2)
        #ejecutar despues de elegir accion para revisar si se fue al mazo o dijo no quiero y que el rival no juegue
        retornar, jugador = fin_mano(info["eleccion"])
        if retornar == True:
            if info["eleccion"] == 10 and info["primero"] == True:
                info["segundo"] = 2
            return jugador, info["segundo"], info["puntos_primero"], info
        info["cartas_jugadas"][0] = cartas_p1[info["eleccion"]]
        eleccion_bot, info = turno_bot(info, mano, cartas_p1, cartas_p2, puntos_jugador, puntos_jugador2)
        #revisa si alguno no quizo el truco
        retornar, jugador = fin_mano(eleccion_bot)
        if retornar == True:
            return jugador, info["segundo"], info["puntos_primero"], info
        info["cartas_jugadas"][1] = cartas_p2[eleccion_bot]
    else: 
        mostrar_mesa(info, mano, info["elementos"]["mesa"])
        eleccion_bot, info = turno_bot(info, mano, cartas_p1, cartas_p2, puntos_jugador, puntos_jugador2)
        retornar, jugador = fin_mano(eleccion_bot)
        if retornar == True:
            return jugador, info["segundo"], info["puntos_primero"], info
        info["cartas_jugadas"][1] = cartas_p2[eleccion_bot]
        mostrar_mesa(info, mano, info["elementos"]["mesa"])
        info = elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_jugador, puntos_jugador2)
        #--
        retornar, jugador = fin_mano(info["eleccion"])
        if retornar == True:
            return jugador, info["segundo"], info["puntos_primero"], info
        info["cartas_jugadas"][0] = cartas_p1[info["eleccion"]]
    
    
    resultado1 = revisar_ronda(cartas_p1[info["eleccion"]], cartas_p2[eleccion_bot])
    #cartas_p1.pop(info["eleccion"])
    cartas_p2.pop(eleccion_bot)
    
    #revisa quien gano la ronda
    if resultado1 == 1:
        info["puntos_mano_j1"] += 1
    elif resultado1 == 2:
        info["puntos_mano_j2"] += 1
    else:
        parda1 = True
        info["parda1"] = True
    
    #marca que no se puede cantar envido
    info["primero"]  = False
        
    #ronda 2
    info["ronda"] = 2
    
    if resultado1 == 2:
        mostrar_mesa(info, mano, info["elementos"]["mesa"])
        eleccion_bot, info = turno_bot(info, mano, cartas_p1, cartas_p2, puntos_jugador, puntos_jugador2)
        retornar, jugador = fin_mano(eleccion_bot)
        if retornar == True:
            return jugador, info["segundo"], info["puntos_primero"], info
        info["cartas_jugadas"][3] = cartas_p2[eleccion_bot]
        mostrar_mesa(info, mano, info["elementos"]["mesa"])
        info = elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_jugador, puntos_jugador2)
        #--
        retornar, jugador = fin_mano(info["eleccion"])
        if retornar == True:
            return jugador, info["segundo"], info["puntos_primero"], info
        info["cartas_jugadas"][2] = cartas_p1[info["eleccion"]]
    elif resultado1 == 1:   
        mostrar_mesa(info, mano, info["elementos"]["mesa"])     
        info = elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_jugador, puntos_jugador2)
        #--
        retornar, jugador = fin_mano(info["eleccion"])
        if retornar == True:
            return jugador, info["segundo"], info["puntos_primero"], info
        info["cartas_jugadas"][2] = cartas_p1[info["eleccion"]]
        mostrar_mesa(info, mano, info["elementos"]["mesa"])
        eleccion_bot, info = turno_bot(info, mano, cartas_p1, cartas_p2, puntos_jugador, puntos_jugador2)
        retornar, jugador = fin_mano(eleccion_bot)
        if retornar == True:
            return jugador, info["segundo"], info["puntos_primero"], info
        info["cartas_jugadas"][3] = cartas_p2[eleccion_bot]
    else:
        if mano:
            mostrar_mesa(info, mano, info["elementos"]["mesa"])
            info  = elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_jugador, puntos_jugador2)
            #--
            retornar, jugador = fin_mano(info["eleccion"])
            if retornar == True:
                return jugador, info["segundo"], info["puntos_primero"], info
            info["cartas_jugadas"][2] = cartas_p1[info["eleccion"]]
            mostrar_mesa(info, mano, info["elementos"]["mesa"])
            eleccion_bot, info = turno_bot(info, mano, cartas_p1, cartas_p2, puntos_jugador, puntos_jugador2)
            retornar, jugador = fin_mano(eleccion_bot)
            if retornar == True:
                return jugador, info["segundo"], info["puntos_primero"], info
            info["cartas_jugadas"][3] = cartas_p2[eleccion_bot]
        else:
            mostrar_mesa(info, mano, info["elementos"]["mesa"])
            eleccion_bot, info = turno_bot(info, mano, cartas_p1, cartas_p2, puntos_jugador, puntos_jugador2)
            retornar, jugador = fin_mano(eleccion_bot)
            if retornar == True:
                return jugador, info["segundo"], info["puntos_primero"], info
            info["cartas_jugadas"][3] = cartas_p2[eleccion_bot]
            mostrar_mesa(info, mano, info["elementos"]["mesa"])
            info  = elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_jugador, puntos_jugador2) 
            #--
            retornar, jugador = fin_mano(info["eleccion"])
            if retornar == True:
                return jugador, info["segundo"], info["puntos_primero"], info
            info["cartas_jugadas"][2] = cartas_p1[info["eleccion"]]
            
    resultado2 = revisar_ronda(cartas_p1[info["eleccion"]], cartas_p2[eleccion_bot])
    #cartas_p1.pop(info["eleccion"])
    cartas_p2.pop(eleccion_bot)
    
    mostrar_mesa(info, mano, info["elementos"]["mesa"])

    if resultado2 == 1:
        info["puntos_mano_j1"] += 1
    elif resultado2 == 2:
        info["puntos_mano_j2"] += 1
    else:
        parda2 = True
        
    #revisa si algun jugador gano    
    if info["puntos_mano_j1"] == 2:
        return 1, info["segundo"], info["puntos_primero"], info
    elif info["puntos_mano_j2"] == 2:
        return 2, info["segundo"], info["puntos_primero"], info
    elif parda1 == True:
        if resultado2 == 1:
            return 1, info["segundo"], info["puntos_primero"], info
        elif resultado2 == 2:
            return 2, info["segundo"], info["puntos_primero"], info
    elif parda2 == True:
        if resultado1 == 1:
            return 1, info["segundo"], info["puntos_primero"], info
        elif resultado1 == 2:
            return 2, info["segundo"], info["puntos_primero"], info
    
    #ronda 3
    info["ronda"] = 3
    
    if resultado2 == 2:
        mostrar_mesa(info, mano, info["elementos"]["mesa"])
        eleccion_bot, info = turno_bot(info, mano, cartas_p1, cartas_p2, puntos_jugador, puntos_jugador2)
        retornar, jugador = fin_mano(eleccion_bot)
        if retornar == True:
            return jugador, info["segundo"], info["puntos_primero"], info
        info["cartas_jugadas"][5] = cartas_p2[eleccion_bot]
        mostrar_mesa(info, mano, info["elementos"]["mesa"])
        info = elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_jugador, puntos_jugador2)
        #--
        retornar, jugador = fin_mano(info["eleccion"])
        if retornar == True:
            return jugador, info["segundo"], info["puntos_primero"], info
        info["cartas_jugadas"][4] = cartas_p1[info["eleccion"]]
    elif resultado2 == 1:   
        mostrar_mesa(info, mano, info["elementos"]["mesa"])     
        info  = elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_jugador, puntos_jugador2)
        #--
        retornar, jugador = fin_mano(info["eleccion"])
        if retornar == True:
            return jugador, info["segundo"], info["puntos_primero"], info
        info["cartas_jugadas"][4] = cartas_p1[info["eleccion"]]
        mostrar_mesa(info, mano, info["elementos"]["mesa"])
        eleccion_bot, info = turno_bot(info, mano, cartas_p1, cartas_p2, puntos_jugador, puntos_jugador2)
        retornar, jugador = fin_mano(eleccion_bot)
        if retornar == True:
            return jugador, info["segundo"], info["puntos_primero"], info
        info["cartas_jugadas"][5] = cartas_p2[eleccion_bot]
    else:
        if mano:
            mostrar_mesa(info, mano, info["elementos"]["mesa"])
            info  = elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_jugador, puntos_jugador2)
            #--
            retornar, jugador = fin_mano(info["eleccion"])
            if retornar == True:
                return jugador, info["segundo"], info["puntos_primero"], info
            info["cartas_jugadas"][4] = cartas_p1[info["eleccion"]]
            mostrar_mesa(info, mano, info["elementos"]["mesa"])
            eleccion_bot, info = turno_bot(info, mano, cartas_p1, cartas_p2, puntos_jugador, puntos_jugador2)
            retornar, jugador = fin_mano(eleccion_bot)
            if retornar == True:
                return jugador, info["segundo"], info["puntos_primero"], info
            info["cartas_jugadas"][5] = cartas_p2[eleccion_bot]
        else:
            mostrar_mesa(info, mano, info["elementos"]["mesa"])
            eleccion_bot, info = turno_bot(info, mano, cartas_p1, cartas_p2, puntos_jugador, puntos_jugador2)
            retornar, jugador = fin_mano(eleccion_bot)
            if retornar == True:
                return jugador, info["segundo"], info["puntos_primero"], info
            info["cartas_jugadas"][5] = cartas_p2[eleccion_bot]
            mostrar_mesa(info, mano, info["elementos"]["mesa"])
            info  = elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_jugador, puntos_jugador2) 
            #--
            retornar, jugador = fin_mano(info["eleccion"])
            if retornar == True:
                return jugador, info["segundo"], info["puntos_primero"], info
            info["cartas_jugadas"][4] = cartas_p1[info["eleccion"]]
        
    resultado3 = revisar_ronda(cartas_p1[info["eleccion"]], cartas_p2[eleccion_bot])
    if resultado3 == 1:
        info["puntos_mano_j1"] += 1
    elif resultado3 == 2:
        info["puntos_mano_j2"] += 1
    else:
        parda3 = True   
       
    #muestra mesa terminada
    mostrar_mesa(info, mano, info["elementos"]["mesa"])   
        
    if info["puntos_mano_j1"] == 2:
        return 1, info["segundo"], info["puntos_primero"], info
    elif info["puntos_mano_j2"] == 2:
        return 2, info["segundo"], info["puntos_primero"], info
    elif parda2 == True:
        if resultado3 == 1:
            return 1, info["segundo"], info["puntos_primero"], info
        elif resultado3 == 2:
            return 2, info["segundo"], info["puntos_primero"], info
    elif parda3 == True:
        if resultado1 == 1:
            return 1, info["segundo"], info["puntos_primero"], info
        elif resultado1 == 2:
            return 2, info["segundo"], info["puntos_primero"], info
        else:
            return 1, info["segundo"], info["puntos_primero"], info
        
    #deveria ser imposible que pase pero si pasa va a tirar error porque espera que devuelva 2 valores int no 1 str
    return "no gano nadie"


#simula una partida completa
def partido(elementos, cartas_p1, cartas_p2):
    
    global puntos_para_ganar_elegidos

    global PUNTOS_PARA_GANAR
    
    PUNTOS_PARA_GANAR = 15
    
    #se le asignan valores a variables necesarias
    if puntos_para_ganar_elegidos == "A 30 puntos" or puntos_para_ganar_elegidos == "To 30 points":
        PUNTOS_PARA_GANAR = 30
    elif puntos_para_ganar_elegidos == "A 15 puntos" or puntos_para_ganar_elegidos == "To 15 points":
        PUNTOS_PARA_GANAR = 15
    puntos_p1 = 0
    puntos_p2 = 0
    mano = True
    mazo = crear_mazo()
    
    while True:
        
        #simula una mano y anota cuantos puntos gano cada uno
        ganador, puntos, nada, info = jugar_mano(mano, mazo, puntos_p1, puntos_p2, elementos, cartas_p1, cartas_p2)
            
        puntos_p1 = info["puntos_jugador"]
        puntos_p2 = info["puntos_jugador2"]
        
                
        #se dan los puntos por el truco
        if ganador == 1:
            puntos_p1 += puntos
            try:
                if puntos == 1:
                    cartel = {"Ingles" : f"{comentarios[-1]}\n The player 1 gained {puntos} point for the hand",
                              "Español" : f"{comentarios[-1]}\n El jugador 1 gano {puntos} punto por la mano"}
                else:
                    cartel = {"Ingles" : f"{comentarios[-1]}\n The player 1 gained {puntos} points for the hand",
                              "Español" : f"{comentarios[-1]}\n El jugador 1 gano {puntos} puntos por la mano"}
                mostrar_cartel(cartel[idioma])
            except:
                if puntos == 1:
                    cartel = {"Ingles" : f"The player 1 gained {puntos} point for the hand",
                              "Español" : f"El jugador 1 gano {puntos} punto por la mano"}
                else:
                    cartel = {"Ingles" : f"The player 1 gained {puntos} points for the hand",
                              "Español" : f"El jugador 1 gano {puntos} puntos por la mano"}
                mostrar_cartel(cartel[idioma])

            confirmar_var.set("no")
            
        elif ganador == 2:
            puntos_p2 += puntos
            try:   
                if puntos == 1:
                    cartel = {"Ingles" : f"{comentarios[-1]}\n The player 2 gained {puntos} point for the hand",
                              "Español" : f"{comentarios[-1]}\n El jugador 2 gano {puntos} punto por la mano"}
                else:
                    cartel = {"Ingles" : f"{comentarios[-1]}\n The player 2 gained {puntos} points for the hand",
                              "Español" : f"{comentarios[-1]}\n El jugador 2 gano {puntos} puntos por la mano"}
                mostrar_cartel(cartel[idioma])
            except:
                if puntos == 1:
                    cartel = {"Ingles" : f"The player 2 gained {puntos} point for the hand",
                              "Español" : f"El jugador 2 gano {puntos} punto por la mano"}
                else:
                    cartel = {"Ingles" : f"The player 2 gained {puntos} points for the hand",
                              "Español" : f"El jugador 2 gano {puntos} puntos por la mano"}
                mostrar_cartel(cartel[idioma])
                 
            
            confirmar_var.set("no")    

        

        #se revisa si alguien gano
        if puntos_p1 >= PUNTOS_PARA_GANAR:
            ganador_text = {"Ingles" : "Player 1 won the game",
                            "Español" : "El jugador 1 gano la partida"}
            mostrar_cartel(ganador_text[idioma])
            return mostrar_escena(crear_escena_inicio, ventana)
        elif puntos_p2 >= PUNTOS_PARA_GANAR:
            ganador_text = {"Ingles" : "Player 2 won the game",
                            "Español" : "El jugador 2 gano la partida"}
            mostrar_cartel(ganador_text[idioma])
            return mostrar_escena(crear_escena_inicio, ventana)

        #se cambia la mano
        if mano == True:
            mano = False
        else:
            mano = True

#revisa si se termino la mano
def fin_mano(eleccion):
    if eleccion == 4:
        return True, 1
    elif eleccion == 10:
        return True, 2
    elif eleccion == 50:
        return True, 3
    else:
        return False, 0

        
        
        
#cartaa

class Carta:
    def __init__(self, nombre, palo, fuerza, tanto, categoria, foto):
        self.nombre = nombre
        self.palo = palo
        self.fuerza = fuerza
        self.tanto = tanto
        self.cat = categoria
        self.foto = foto
    
    #suma las cartas para determinar su envido
    def __add__(self, otro):
        if self.palo == otro.palo:
            return self.tanto + otro.tanto + 20
        else:
            if self.tanto > otro.tanto:
                return self.tanto
            else:
                return otro.tanto
            
    
#crea el mazo de cartas
def crear_mazo(): 
    
    global directorio_programa
    
    mazo = [None] * 40

    #cartas de espada
    mazo[0] = Carta("1 de espada", "espada", 14, 1, "T", os.path.join(directorio_programa, "imagenes/espada/1.jpg"))
    mazo[1] = Carta("2 de espada", "espada", 9, 2, "A", os.path.join(directorio_programa, "imagenes/espada/2.jpg"))
    mazo[2] = Carta("3 de espada", "espada", 10, 3, "A", os.path.join(directorio_programa, "imagenes/espada/3.jpg"))
    mazo[3] = Carta("4 de espada", "espada", 1, 4, "B", os.path.join(directorio_programa, "imagenes/espada/4.jpg"))
    mazo[4] = Carta("5 de espada", "espada", 2, 5, "B", os.path.join(directorio_programa, "imagenes/espada/5.jpg"))
    mazo[5] = Carta("6 de espada", "espada", 3, 6, "B", os.path.join(directorio_programa, "imagenes/espada/6.jpg"))
    mazo[6] = Carta("7 de espada", "espada", 12, 7, "T", os.path.join(directorio_programa, "imagenes/espada/7.jpg"))
    mazo[7] = Carta("10 de espada", "espada", 5, 0, "M", os.path.join(directorio_programa, "imagenes/espada/10.jpg"))
    mazo[8] = Carta("11 de espada", "espada", 6, 0, "M", os.path.join(directorio_programa, "imagenes/espada/11.jpg"))
    mazo[9] = Carta("12 de espada", "espada", 7, 0, "M", os.path.join(directorio_programa, "imagenes/espada/12.jpg"))

    #cartas de basto
    mazo[10] = Carta("1 de basto", "basto", 13, 1, "T", os.path.join(directorio_programa, "imagenes/basto/1.jpg"))
    mazo[11] = Carta("2 de basto", "basto", 9, 2, "A", os.path.join(directorio_programa, "imagenes/basto/2.jpg"))
    mazo[12] = Carta("3 de basto", "basto", 10, 3, "A", os.path.join(directorio_programa, "imagenes/basto/3.jpg"))
    mazo[13] = Carta("4 de basto", "basto", 1, 4, "B", os.path.join(directorio_programa, "imagenes/basto/4.jpg"))
    mazo[14] = Carta("5 de basto", "basto", 2, 5, "B", os.path.join(directorio_programa, "imagenes/basto/5.jpg"))
    mazo[15] = Carta("6 de basto", "basto", 3, 6, "B", os.path.join(directorio_programa, "imagenes/basto/6.jpg"))
    mazo[16] = Carta("7 de basto", "basto", 4, 7, "B", os.path.join(directorio_programa, "imagenes/basto/7.jpg"))
    mazo[17] = Carta("10 de basto", "basto", 5, 0, "M", os.path.join(directorio_programa, "imagenes/basto/10.jpg"))
    mazo[18] = Carta("11 de basto", "basto", 6, 0, "M", os.path.join(directorio_programa, "imagenes/basto/11.jpg"))
    mazo[19] = Carta("12 de basto", "basto", 7, 0, "M", os.path.join(directorio_programa, "imagenes/basto/12.jpg"))

    #cartas de oro
    mazo[20] = Carta("1 de oro", "oro", 8, 1, "M", os.path.join(directorio_programa, "imagenes/oro/1.jpg"))
    mazo[21] = Carta("2 de oro", "oro", 9, 2, "A", os.path.join(directorio_programa, "imagenes/oro/2.jpg"))
    mazo[22] = Carta("3 de oro", "oro", 10, 3, "A", os.path.join(directorio_programa, "imagenes/oro/3.jpg"))
    mazo[23] = Carta("4 de oro", "oro", 1, 4, "B", os.path.join(directorio_programa, "imagenes/oro/4.jpg"))
    mazo[24] = Carta("5 de oro", "oro", 2, 5, "B", os.path.join(directorio_programa, "imagenes/oro/5.jpg"))
    mazo[25] = Carta("6 de oro", "oro", 3, 6, "B", os.path.join(directorio_programa, "imagenes/oro/6.jpg"))
    mazo[26] = Carta("7 de oro", "oro", 11, 7, "T", os.path.join(directorio_programa, "imagenes/oro/7.jpg"))
    mazo[27] = Carta("10 de oro", "oro", 5, 0, "M", os.path.join(directorio_programa, "imagenes/oro/10.jpg"))
    mazo[28] = Carta("11 de oro", "oro", 6, 0, "M", os.path.join(directorio_programa, "imagenes/oro/11.jpg"))
    mazo[29] = Carta("12 de oro", "oro", 7, 0, "M", os.path.join(directorio_programa, "imagenes/oro/12.jpg"))

    #cartas de copa
    mazo[30] = Carta("1 de copa", "copa", 8, 1, "M", os.path.join(directorio_programa, "imagenes/copa/1.jpg"))
    mazo[31] = Carta("2 de copa", "copa", 9, 2, "A", os.path.join(directorio_programa, "imagenes/copa/2.jpg"))
    mazo[32] = Carta("3 de copa", "copa", 10, 3, "A", os.path.join(directorio_programa, "imagenes/copa/3.jpg"))
    mazo[33] = Carta("4 de copa", "copa", 1, 4, "B", os.path.join(directorio_programa, "imagenes/copa/4.jpg"))
    mazo[34] = Carta("5 de copa", "copa", 2, 5, "B", os.path.join(directorio_programa, "imagenes/copa/5.jpg"))
    mazo[35] = Carta("6 de copa", "copa", 3, 6, "B", os.path.join(directorio_programa, "imagenes/copa/6.jpg"))
    mazo[36] = Carta("7 de copa", "copa", 4, 7, "B", os.path.join(directorio_programa, "imagenes/copa/7.jpg"))
    mazo[37] = Carta("10 de copa", "copa", 5, 0, "M", os.path.join(directorio_programa, "imagenes/copa/10.jpg"))
    mazo[38] = Carta("11 de copa", "copa", 6, 0, "M", os.path.join(directorio_programa, "imagenes/copa/11.jpg"))
    mazo[39] = Carta("12 de copa", "copa", 7, 0, "M", os.path.join(directorio_programa, "imagenes/copa/12.jpg"))

    return mazo

#mezcla las cartas
def mezclar(mazo):
    random.shuffle(mazo)
    return mazo

#reparte 3 cartas a cada jugador
def repartir(mazo):
    mazo = mezclar(mazo)
    p1 = [mazo[0], mazo[2], mazo[4]]
    p2 = [mazo[1], mazo[3], mazo[5]]
    return p1, p2
    
#revisa quien gano la ronda, devolviendo 1 si gano el jugador 1, 2 si gano el jugador 2 y 0 si fue empate
def revisar_ronda(carta1, carta2):
    if carta1.fuerza > carta2.fuerza:
        return 1
    elif carta1.fuerza < carta2.fuerza:
        return 2
    else:
        return 0

            
#jugador elige que accion realizar   
#cartas_jugador contiene las cartas del usuario
#info contiene informacion general de la mano
#cartas_p2 contiene las cartas del bot
#mano contiene True si el usuario es mano False si no
def elegir_accion(cartas_jugador, info, cartas_p2, mano, puntos_p1, puntos_p2):
    
    global opcion_elegida
    global opciones_validas
    global validos
    
    validos = []
    i = 1
    
    #muestra las cartas disponibles
    for carta in cartas_jugador:
        validos.append({"nombre" : carta.nombre,
                        "index" : i})
        i += 1
        
    #muestra si se puede aumentar
    if info["quiero"] == 1 or info["quiero"] == 0:
        if info["segundo"] == 1:
            validos.append({"nombre" : "truco",
                        "index" : 4})
        elif info["segundo"] == 2:
            validos.append({"nombre" : "retruco",
                        "index" : 4})
        elif info["segundo"] == 3:
            validos.append({"nombre" : "vale cuatro",
                        "index" : 4})
        
    #Muestra si se puede cantar tanto
    if info["primero"]:
        validos.append({"nombre" : "envido",
                        "index" : 7})
        validos.append({"nombre" : "real envido",
                        "index" : 8})
        validos.append({"nombre" : "falta envido",
                        "index" : 9})
       
    #muestra la opcion de irse al mazo 
    validos.append({"nombre" : "irse al mazo",
                        "index" : 0})    
       
    opcion_elegida = None

      
    info["elementos"]["ventana"].wait_variable(confirmar_var)
    confirmar_var.set("no")
    
    # if opcion_elegida == None:
    #     for opcion in validos:
    #         if opcion["nombre"] == seleccion.get():
    #             info["eleccion"] = opcion["index"]
    # else:
    #     for opcion in validos:
    #         if opcion["nombre"] == opcion_elegida:
    #             info["eleccion"] = opcion["index"]
                
    info["eleccion"] = opcion_elegida

    
    return revisar_accion(info, cartas_jugador, cartas_p2, mano, puntos_p1, puntos_p2)
      
#revisa la accion del usuario y la ejecuta 
def revisar_accion(info, cartas_p1, cartas_p2, mano, puntos_p1, puntos_p2):
    jugador = 1
    estado = ("Normal", "Normal", "Truco", "Retruco", "Vale cuatro")    

    #revisa si se eligio una carta
    if 0 < info["eleccion"] < 4:
        info["eleccion"] = info["eleccion"] - 1
        return info 
    if info["eleccion"] == 0:
        info["eleccion"] = 10
        return info
        
    #si se canto Truco 
    if info["eleccion"] == 4:
        respuesta = canto_truco(jugador, info)
        info["primero"] = False
        #no acepta, se termina la mano
        if respuesta == 2:
            no_quiero_text = {"Ingles" : "I don't want",
                              "Español" : "No quiero"}
            comentarios.append(no_quiero_text[idioma])
            return info
        #acepta se le pide al usuario que vuelva a elegir que hacer
        elif respuesta == 1:
            info["segundo"] = 2
            info["quiero"] = 2
            mostrar_mesa(info, mano, info["elementos"]["mesa"])
            quiero_text = {"Ingles" : "I want",
                           "Español" : "Quiero"}
            info["elementos"]["comentario"].config(text=quiero_text[idioma])
            return elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_p1, puntos_p2)
        #aumenta
        elif respuesta == 3:
            jugador = 2
            info["segundo"] = info["segundo"] + 1
            mostrar_mesa(info, mano, info["elementos"]["mesa"])

            quiero_text = {"Ingles" : f"I want {estado[info['segundo'] + 1]}!",
                           "Español" : f"Quiero {estado[info['segundo'] + 1]}!"}
            info["elementos"]["comentario"].config(text=quiero_text[idioma])
            respuesta = canto_truco(jugador, info)
            #usuario quizo
            if respuesta == 1:
                info["segundo"] = info["segundo"] + 1
                info["quiero"] = 1
                mostrar_mesa(info, mano, info["elementos"]["mesa"])
                return elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_p1, puntos_p2)
            #usuario no quizo
            elif respuesta == 2:
                info["eleccion"] = 10
                return info
            #usuario aumento
            elif respuesta == 3:
                jugador = 1
                info["segundo"] = info["segundo"] + 1
                respuesta = canto_truco(jugador, info)
                #bot acepto
                if respuesta == 1:
                    mostrar_mesa(info, mano, info["elementos"]["mesa"])
                    info["segundo"] = info["segundo"] + 1
                    info["quiero"] = 2
                    
                    quiero_text = {"Ingles" : "I want",
                                   "Español" : "Quiero"}
                    info["elementos"]["comentario"].config(text=quiero_text[idioma])
                    return elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_p1, puntos_p2)
                #bot no acepto
                elif respuesta == 2:
                    no_quier_text = {"Ingles" : "I don't want",
                                     "Español" : "No quiero"}
                    comentarios.append(no_quier_text[idioma])
                    return info
                    
            
    #Si se canto retruco, si se canto valecutro
    if info["eleccion"] == 5:
        jugador = 1
        respuesta = canto_truco(jugador, info)
        if respuesta == 1:
            info["segundo"] = 3
            info["quiero"] = 2
            mostrar_mesa(info, mano, info["elementos"]["mesa"])
            quiero_text = {"Ingles" : "I want",
                                   "Español" : "Quiero"}
            info["elementos"]["comentario"].config(text=quiero_text[idioma])
            return elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_p1, puntos_p2)
        #el bot no acepto
        elif respuesta == 2:
            info["eleccion"] = 4
            no_quiero_text = {"Ingles" : "I don't want",
                                   "Español" : "No quiero"}
            comentarios.append(no_quiero_text[idioma])
            return info
        elif respuesta == 3:
            info["segundo"] = 3
            jugador = 2
            respuesta = canto_truco(jugador, info)
            if respuesta == 1:
                info["segundo"] = 4
                mostrar_mesa(info, mano, info["elementos"]["mesa"])
                return elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_p1, puntos_p2)
            else:
                info["eleccion"] = 10
                return info
    if info["eleccion"] == 6:
        #se marca que lo canto el usuario
        jugador = 1
        respuesta = canto_truco(jugador,info)
        #el bot acepto
        if respuesta == 1:
            info["segundo"] = 4
            mostrar_mesa(info, mano, info["elementos"]["mesa"])
            quiero_text = {"Ingles" : "I want",
                                   "Español" : "Quiero"}
            info["elementos"]["comentario"].config(text=quiero_text[idioma])
            return elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_p1, puntos_p2)
        #el bot no acepto
        elif respuesta == 2:
            info["eleccion"] = 4
            no_quiero_text = {"Ingles" : "I don'twant",
                                   "Español" : "No quiero"}
            comentarios.append(no_quiero_text[idioma])
            return info
    
    #usuario canto envido
    if info["eleccion"] == 7 :
        jugador = 1
        cantado = [1]
        #no se puede cantar mas envido
        info["primero"] = False
        #se crea el loop del envido y se devuelve el resultado
        info  = loop_envido(cantado, jugador, info, mano, cartas_p1, cartas_p2, puntos_p1, puntos_p2)
        
        #revisa si alguien gano por envido
        alguien_gano_por_envido = alguien_gano(info)
        if alguien_gano_por_envido:
            info["eleccion"] = 50
            return info
            
        return elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_p1, puntos_p2)
    elif info["eleccion"] == 8 :
        jugador = 1
        cantado = [2]
        #no se puede cantar mas envido
        info["primero"] = False
        #se crea el loop del envido y se devuelve el resultado
        info  = loop_envido(cantado, jugador, info, mano, cartas_p1, cartas_p2, puntos_p1, puntos_p2)
        
        #revisa si alguien gano por envido
        alguien_gano_por_envido = alguien_gano(info)
        if alguien_gano_por_envido:
            info["eleccion"] = 50
            return info
            
        return elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_p1, puntos_p2)
    elif info["eleccion"] == 9 :
        jugador = 1
        cantado = [3]
        #no se puede cantar mas envido
        info["primero"] = False
        #se crea el loop del envido y se devuelve el resultado
        info  = loop_envido(cantado, jugador, info, mano, cartas_p1, cartas_p2, puntos_p1, puntos_p2)
        
        #revisa si alguien gano por envido
        alguien_gano_por_envido = alguien_gano(info)
        if alguien_gano_por_envido:
            info["eleccion"] = 50
            return info
            
        return elegir_accion(cartas_p1, info, cartas_p2, mano, puntos_p1, puntos_p2)
        
        
        
       

#calcula cuanto tanto tiene un jugador  
def calcular_tanto(cartas):
    valor_max = 0
    tantos = []
    tantos.append(cartas[0] + cartas[1])
    tantos.append(cartas[0] + cartas[2])
    tantos.append(cartas[1] + cartas[2])
    
    for tanto in tantos:
        if tanto > valor_max:
            valor_max = tanto
                
    return valor_max
 
   
#True si gana el jugador, False si gana el bot
def revisar_tanto(cartas_p1, cartas_p2, mano):
    tanto_p1 = calcular_tanto(cartas_p1)
    tanto_p2 = calcular_tanto(cartas_p2)
    
    if tanto_p1 > tanto_p2:
        ganador = True
    elif tanto_p2 > tanto_p1:
        ganador = False
    #si es empate gana la mano, mano es True si el jugador es mano
    else:
        ganador = mano
        
    if ganador == mano == True:
        resultado_tanto = {"Ingles" : f'Player 1 has "{tanto_p1}"\nThey are good',
                           "Español" : f'Jugador 1 tiene "{tanto_p1}"\nSon buenas'}
        comentarios.append(resultado_tanto[idioma])
    elif ganador == mano == False:
        resultado_tanto = {"Ingles" : f'Player 2 has "{tanto_p1}"\nThey are good',
                           "Español" : f'Jugador 2 tiene "{tanto_p1}"\nSon buenas'}
        comentarios.append(resultado_tanto[idioma])
    else:
        resultado_tanto = {"Ingles" : f'Player 1 has "{tanto_p1}"\nPlayer 2 has "{tanto_p2}"',
                           "Español" : f'Jugador 1 tiene "{tanto_p1}"\nJugador 2 tiene "{tanto_p2}"'}
        comentarios.append(resultado_tanto[idioma])
        
    return ganador
   
   
#pide al usuario o al bot que acepte, rechaze o aumente
#jugador es el usuario que canto 1=usuario, 2=bot
#aumentar True si se puede aumentar, False si no
def canto_truco(jugador, info):
    
    global opcion_elegida
    global validos
    
    if info["segundo"] == 3:
        aumentar = False
    else:
        aumentar = True
    
    estado = ("Normal", "Normal", "Truco", "Retruco", "Vale cuatro", "--")    
    validos = [{"nombre" : "quiero", "index_viejo" : 1, "index" : 10},
              {"nombre" : "no quiero", "index_viejo" : 2, "index" : 20}]
    
    #si el usuario lo canta el bot responde
    if jugador == 1:
        x = responder_truco(info, aumentar)
        if x > 10:
            cantado = [x - 10]
            info = loop_envido(cantado, 2, info, info["mano"], info["cartas_j1"], info["cartas_j2"], info["puntos_jugador"], info["puntos_jugador2"])
            x = responder_truco(info, aumentar)
            
        #1=quiero, 2=no quiero, 3=aumentar
        return responder_truco(info, aumentar)
    #si el bot lo canto 
    elif jugador == 2:
        
        
        
        info["quiero"] = 1
        mostrar_mesa(info, info["mano"], info["elementos"]["mesa"])
        if info["segundo"] < 3:
            m = estado[info["segundo"] + 2]
            validos.append({"nombre" : m, "index_viejo" : 3, "index" : 4})
            
        if info["primero"] and not info["mano"]:
            validos.append({"nombre" : "envido", "index_viejo" : 7, "index" : 7})
            validos.append({"nombre" : "real envido", "index_viejo" : 8, "index" : 8})
            validos.append({"nombre" : "falta envido", "index_viejo" : 9, "index" : 9})
            
        canto_dos = {"Ingles" : f"Player 2 announce: {estado[info['segundo'] + 1]}",
                     "Español" : f'El jugador 2 cantó: {estado[info["segundo"] + 1]}'}
        info["elementos"]["comentario"].config(text=canto_dos[idioma])
        info["elementos"]["truco"].config(text=estado[info["segundo"]+2])
        
           
        
        info["elementos"]["ventana"].wait_variable(confirmar_var)
        confirmar_var.set("no")
        
        for opcion in validos:
            if opcion["index"] == opcion_elegida:
                eleccion = opcion["index_viejo"]
                if eleccion == 7 or eleccion == 8 or eleccion == 9:
                    cantado = [eleccion - 6]
                    info = loop_envido(cantado, 1, info, info["mano"], info["cartas_j1"], info["cartas_j2"], info["puntos_jugador"], info["puntos_jugador2"])
                    info["primero"] = False
                    
                    
                    info["elementos"]["ventana"].wait_variable(confirmar_var)
                    confirmar_var.set("no")
                    
                    
                    eleccion = canto_truco(jugador, info)
                    
                info["elementos"]["comentario"].config(text=" ")
                return eleccion
        
            
        
        
#pide al usuario o al bot que acepte, rechaze o aumente el envido(implementado parcialmente)
#jugador es quien lo canta, 1=usuario, 2=bot
def canto_tanto(jugador, cantado, info):
    #si el usuario lo canta el bot responde
    
    global opcion_elegida
    global validos

    
    if jugador == 1:
        
        #quiero = 10
        #no quiero = 30
        #envido = 1
        #real envido = 2
        #falta envido = 3
        
        return responder_envido(info, info["cartas_j2"], cantado)
            
    #si el bot lo canto el usuario responde
    elif jugador == 2:
        
        
        
        #revisa la accion anterior y le pide al usuario su respuesta
        
        while cantado[-1] == None:
            cantado.pop()
        
        if cantado[-1] == 1:
            
            info["elementos"]["comentario"].config(text=f"Envido")
            
            i = 3
            unico = False
            
            validos = [{"nombre" : "quiero", "index_viejo" : 1, "index" : 10},
                       {"nombre" : "no quiero", "index_viejo" : 2, "index" : 20}]
            
            try:
                if cantado[-2] == 1:
                    pass
            except:
                i += 1
                unico = True
                validos.append({"nombre" : "envido", "index_viejo" : 3, "index" : 7})

            
            validos.append({"nombre" : "real envido", "index_viejo" : 4, "index" : 8})
            validos.append({"nombre" : "falta envido", "index_viejo" : 5, "index" : 9})
            

            

            
            info["elementos"]["ventana"].wait_variable(confirmar_var)
            confirmar_var.set("no")
            
            
            for opcion in validos:
                if opcion["index"] == opcion_elegida:
                    eleccion = opcion["index_viejo"]
                           
                    
            if eleccion == 1:
                return 10
            elif eleccion == 2:
                return  20
            
            n = (0,0,0,1,2,3)
            return n[eleccion]

            
        
        elif cantado[-1] == 2:

            
            info["elementos"]["comentario"].config(text=f"Real envido")
            

            
            validos = [{"nombre" : "quiero", "index_viejo" : 1, "index" : 10},
                       {"nombre" : "no quiero", "index_viejo" : 2, "index" : 20},
                       {"nombre" : "falta envido", "index_viejo" : 3, "index" : 9}]
            
             
            

            
            info["elementos"]["ventana"].wait_variable(confirmar_var)
            confirmar_var.set("no")
            
            
            for opcion in validos:
                if opcion["index"] == opcion_elegida:
                    eleccion = opcion["index_viejo"]
            
            if eleccion == 1:
                return 10
            elif eleccion == 2:
                return  20
            elif eleccion == 3:
                return 3
            
            
            

                    
        elif cantado[-1] == 3:

            
            info["elementos"]["comentario"].config(text=f"Falta envido!")
            

            
            validos = [{"nombre" : "quiero", "index_viejo" : 1, "index" : 10},
                       {"nombre" : "no quiero", "index_viejo" : 2, "index" : 20}]
            
            
            
            info["elementos"]["ventana"].wait_variable(confirmar_var)
            confirmar_var.set("no")
            
            
            for opcion in validos:
                if opcion["index"] == opcion_elegida:
                    eleccion = opcion["index_viejo"]
                    
            if eleccion == 1:
                return 10
            elif eleccion == 2:
                return  20       
            

#el bot elije al azar entre sus cartas
def elegir_carta_aleatorio(cartas_bot):
    return random.randint(0,(len(cartas_bot) - 1))


#actualiza la pantalla para mostrar informacion actualizada
def mostrar_mesa(info, mano, mesa):
    
    
    if mano:
        n_mano = 1
    else:
        n_mano = 2
        
    estado = ("Normal", "Normal", "Truco", "Retruco", "Vale cuatro", "--")
    
    
    header_text = {"Ingles" : f'Player{n_mano} is hand // {estado[info["segundo"]]} // J1:{info["puntos_jugador"]} J2:{info["puntos_jugador2"]}',
                   "Español" : f'jugador{n_mano} es mano // {estado[info["segundo"]]} // J1:{info["puntos_jugador"]} J2:{info["puntos_jugador2"]}'}
    info["elementos"]["header"].config(text=header_text[idioma])

    for i,carta in enumerate(info["cartas_jugadas"]):
        if carta.nombre != " ":
            mostrar_carta_jugada(info["elementos"]["cartas mesa"][i], carta)
    
    info["elementos"]["truco"].config(text=estado[info["segundo"] + 1])
    
    
def mostrar_carta_jugada(posicion, carta):
    foto1 = Image.open(carta.foto)
    foto = ImageTk.PhotoImage(foto1)
    posicion.config(image=foto)
    posicion.image = foto 
    posicion.lift()
    
def limpiar_mesa(cartas_mesa, fondo_mesa):
    for carta in cartas_mesa:
        carta.config(image=None)
        carta.image = None
    
    fondo_mesa.lift()
        

    
    
    
    
    
    
    
    

def turno_bot(info, mano, cartas_p1, cartas_p2, puntos_p1, puntos_p2):
    jugador = 2
    if info["primero"] == True:
        
        decision = elegir_envido(info, cartas_p2)
        
        if decision != 0:
            info["primero"] = False
            cantado = [decision]
            info  = loop_envido(cantado, jugador, info, mano, cartas_p1, cartas_p2, puntos_p1, puntos_p2)
        
        
    
        #revisar si alguien gano por envido
        alguien_gano_por_envido = alguien_gano(info)
        if alguien_gano_por_envido:
            return 50, info        
            
    if info["quiero"] == 0 or info["quiero"] == 2:
        
        if not info["segundo"] >= 3:
            #si retorna True se canta
            if elegir_truco(info):
                situacion = canto_truco(jugador, info)
                #el usuario acepta
                if situacion == 1:
                    info["segundo"] += 1
                    info["quiero"] = 1
                #el usuario no acepta
                elif situacion == 2:
                    return 10, info
                else:
                    jugador = 1
                    info["segundo"] += 1
                    situacion = canto_truco(jugador, info)
                    #lo mismo de antes
                    if situacion == 1:

                        quiero_text = {"Ingles" : "I want",
                                       "Español" : "Quiero"}
                        info["elementos"]["comentario"].config(text=quiero_text[idioma])
                        info["segundo"] += 1
                        info["quiero"] = 1
                    #el usuario no acepta
                    elif situacion == 2:
                        no_quiero_text = {"Ingles" : "I don't want",
                                          "Español" : "No quiero"}
                        comentarios.append(no_quiero_text[idioma])
                        return 4, info
                    else:
                        jugador = 2
                        info["segundo"] += 1
                        situacion = canto_truco(jugador, info)
                        if situacion == 1:
                            quiero_text = {"Ingles" : "I want",
                                       "Español" : "Quiero"}
                            info["elementos"]["comentario"].config(text=quiero_text)
                            info["segundo"] += 1
                            info["quiero"] = 1
                        #el usuario no acepta
                        elif situacion == 2:
                            return 10, info
                
                
    
    if len(cartas_p2) == 3:
        return elegir_carta_1(info, cartas_p2), info
    elif len(cartas_p2) == 2:
        return elegir_carta_2(info, cartas_p2), info
    else:
        return elegir_carta_3(info, cartas_p2), info





def loop_envido(cantado, jugador, info, mano, cartas_p1, cartas_p2, puntos_p1, puntos_p2):
    
    mostrar_mesa(info, mano, info["elementos"]["mesa"])
    
    global comentarios
    
    comentarios = []
    
    while True:
        
        
        
        i = canto_tanto(jugador, cantado, info)
        #aceptado
        if i == 10:
            situacion = 0
            break
        #rechazado por parte del usuario
        elif i == 20:
            situacion = 1
            break
        #rechazado por parte del bot
        elif i == 30:
            situacion = 2
            break
        else:
       
                
            cantado.append(i)
            if jugador == 2:
                jugador = 1
            else:
                jugador = 2
       
    if situacion == 0:

            
            if jugador == 1:
                quiero_text = {"Ingles" : "I want!",
                                       "Español" : "Quiero!"}
                comentarios.append(quiero_text[idioma])
            
            ganador = revisar_tanto(cartas_p1, cartas_p2, mano)
            #calcular puntos
            if 3 in cantado:
                #gano el usuario
                if ganador:
                    #return a info["puntos_primero"]
                    ganaste_text = {"Ingles" : "//You won//",
                                       "Español" : "//Ganaste//"}
                    comentarios.append(ganaste_text[idioma])
                    info["puntos_primero"] = [1, 0]
                else:
                    perdiste_text = {"Ingles" : "//You lost//",
                                       "Español" : "//Perdiste//"}
                    comentarios.append(perdiste_text[idioma])
                    info["puntos_primero"] = [2, 0]
            else:
                puntos = 0
                for i in cantado:
                    if i == 1:
                        puntos += 2
                    elif i == 2:
                        puntos += 3
                        
                if ganador:
                    ganaste_text = {"Ingles" : "//You won//",
                                       "Español" : "//Ganaste//"}
                    comentarios.append(ganaste_text[idioma])
                    info["puntos_primero"] = [1, puntos]
                else:
                    perdiste_text = {"Ingles" : "//You lost//",
                                       "Español" : "//Perdiste//"}
                    comentarios.append(perdiste_text[idioma])
                    info["puntos_primero"] = [2, puntos]
            
        #el usuario no acepto
    elif situacion == 1:
        puntos = 0
        cantado.pop(-1)
        for i in cantado:
            if i == 1:
                puntos += 2
            elif i == 2:
                puntos += 3
        if puntos == 0:
            puntos = 1
        info["puntos_primero"] = [2, puntos]
        
    #el bot no acepto
    elif situacion == 2:
        no_quiero_text = {"Ingles" : "I don't want",
                          "Español" : "No quiero"}
        comentarios.append(no_quiero_text[idioma])
        puntos = 0
        cantado.pop(-1)
        for i in cantado:
            if i == 1:
                puntos += 2
            elif i == 2:
                puntos += 3
        if puntos == 0:
            puntos = 1
        info["puntos_primero"] = [1, puntos]
        
        
    if info["puntos_primero"][1] == 0:
        if puntos_p1 > puntos_p2:
            info["puntos_primero"][1] = PUNTOS_PARA_GANAR - puntos_p1
        else:
            info["puntos_primero"][1] = PUNTOS_PARA_GANAR - puntos_p2
            

    
    if info["puntos_primero"][0] == 1:
        puntos_p1 += info["puntos_primero"][1]
        puntos_tanto = {"Ingles" : f"The player 1 earned {info['puntos_primero'][1]} points for the envido",
                        "Español" : f"El jugador 1 gano {info['puntos_primero'][1]} punto por el envido"}
        comentarios.append(puntos_tanto[idioma])
    elif info["puntos_primero"][0] == 2:
        puntos_p2 += info["puntos_primero"][1]
        puntos_tanto = {"Ingles" : f"The player 2 earned {info['puntos_primero'][1]} points for the envido",
                        "Español" : f"El jugador 2 gano {info['puntos_primero'][1]} punto por el envido"}
        comentarios.append(puntos_tanto[idioma])
        
        
    info["puntos_jugador"] = puntos_p1
    info["puntos_jugador2"] = puntos_p2
    

    x = "\n".join(comentarios)
    mostrar_cartel(x)
    info["elementos"]["comentario"].config(text=" ")
    confirmar_var.set("no")
    comentarios = []
    
    return info    
   
   
def alguien_gano(info):
    if info["puntos_jugador"] >= PUNTOS_PARA_GANAR:
        return True
    elif info["puntos_jugador2"] >= PUNTOS_PARA_GANAR:
        return True
    else:
        return False              
    
    
    
    
#bot


cartas = 1

def calificar_mano(cartas):
    #Basura
    if cartas[0].cat == "B" and cartas[1].cat == "B" and cartas[2].cat == "B":
        return 1
    #Rey de pobres
    elif cartas[0].cat == "M" and cartas[1].cat == "B" and cartas[2].cat == "B":
        return 2
    elif cartas[1].cat == "M" and cartas[0].cat == "B" and cartas[2].cat == "B":
        return 2
    elif cartas[2].cat == "M" and cartas[1].cat == "B" and cartas[0].cat == "B":
        return 2
    #Pareja pobre
    elif cartas[0].cat == "B" and cartas[1].cat == "M" and cartas[2].cat == "M":
        return 3
    elif cartas[1].cat == "B" and cartas[0].cat == "M" and cartas[2].cat == "M":
        return 3
    elif cartas[2].cat == "B" and cartas[1].cat == "M" and cartas[0].cat == "M":
        return 3
    #Soltero
    elif cartas[0].cat == "A" and cartas[1].cat == "B" and cartas[2].cat == "B":
        return 4
    elif cartas[1].cat == "A" and cartas[0].cat == "B" and cartas[2].cat == "B":
        return 4
    elif cartas[2].cat == "A" and cartas[1].cat == "B" and cartas[0].cat == "B":
        return 4
    #Glass cannon
    elif cartas[0].cat == "T" and cartas[1].cat == "B" and cartas[2].cat == "B":
        return 5
    elif cartas[1].cat == "T" and cartas[0].cat == "B" and cartas[2].cat == "B":
        return 5
    elif cartas[2].cat == "T" and cartas[1].cat == "B" and cartas[0].cat == "B":
        return 5
    #Figuras
    elif cartas[0].cat == "M" and cartas[1].cat == "M" and cartas[2].cat == "M":
        return 6
    #Estandar
    elif cartas[0].cat == "A" and cartas[1].cat == "M" and cartas[2].cat == "B":
        return 7
    elif cartas[0].cat == "A" and cartas[1].cat == "B" and cartas[2].cat == "M":
        return 7
    elif cartas[0].cat == "B" and cartas[1].cat == "M" and cartas[2].cat == "A":
        return 7
    elif cartas[0].cat == "B" and cartas[1].cat == "A" and cartas[2].cat == "M":
        return 7
    elif cartas[0].cat == "M" and cartas[1].cat == "A" and cartas[2].cat == "B":
        return 7
    elif cartas[0].cat == "M" and cartas[1].cat == "B" and cartas[2].cat == "A":
        return 7
    #3 ruedas
    elif cartas[0].cat == "T" and cartas[1].cat == "M" and cartas[2].cat == "B":
        return 8
    elif cartas[0].cat == "T" and cartas[1].cat == "B" and cartas[2].cat == "M":
        return 8
    elif cartas[0].cat == "B" and cartas[1].cat == "M" and cartas[2].cat == "T":
        return 8
    elif cartas[0].cat == "B" and cartas[1].cat == "T" and cartas[2].cat == "M":
        return 8
    elif cartas[0].cat == "M" and cartas[1].cat == "T" and cartas[2].cat == "B":
        return 8
    elif cartas[0].cat == "M" and cartas[1].cat == "B" and cartas[2].cat == "T":
        return 8
    #Pareja alta
    elif cartas[0].cat == "A" and cartas[1].cat == "M" and cartas[2].cat == "M":
        return 9
    elif cartas[1].cat == "A" and cartas[0].cat == "M" and cartas[2].cat == "M":
        return 9
    elif cartas[2].cat == "A" and cartas[1].cat == "M" and cartas[0].cat == "M":
        return 9
    #Duo bajo
    elif cartas[0].cat == "B" and cartas[1].cat == "A" and cartas[2].cat == "A":
        return 10
    elif cartas[1].cat == "B" and cartas[0].cat == "A" and cartas[2].cat == "A":
        return 10
    elif cartas[2].cat == "B" and cartas[1].cat == "A" and cartas[0].cat == "A":
        return 10
    #Pareja rica
    elif cartas[0].cat == "T" and cartas[1].cat == "M" and cartas[2].cat == "M":
        return 11
    elif cartas[1].cat == "T" and cartas[0].cat == "M" and cartas[2].cat == "M":
        return 11
    elif cartas[2].cat == "T" and cartas[1].cat == "M" and cartas[0].cat == "M":
        return 11
    #Duo medio
    elif cartas[0].cat == "M" and cartas[1].cat == "A" and cartas[2].cat == "A":
        return 12
    elif cartas[1].cat == "M" and cartas[0].cat == "A" and cartas[2].cat == "A":
        return 12
    elif cartas[2].cat == "M" and cartas[1].cat == "A" and cartas[0].cat == "A":
        return 12
    #surtido bajo
    elif cartas[0].cat == "T" and cartas[1].cat == "A" and cartas[2].cat == "B":
        return 13
    elif cartas[0].cat == "T" and cartas[1].cat == "B" and cartas[2].cat == "A":
        return 13
    elif cartas[0].cat == "B" and cartas[1].cat == "A" and cartas[2].cat == "T":
        return 13
    elif cartas[0].cat == "B" and cartas[1].cat == "T" and cartas[2].cat == "A":
        return 13
    elif cartas[0].cat == "A" and cartas[1].cat == "T" and cartas[2].cat == "B":
        return 13
    elif cartas[0].cat == "A" and cartas[1].cat == "B" and cartas[2].cat == "T":
        return 13
    #Surtido medio
    elif cartas[0].cat == "T" and cartas[1].cat == "A" and cartas[2].cat == "M":
        return 14
    elif cartas[0].cat == "T" and cartas[1].cat == "M" and cartas[2].cat == "A":
        return 14
    elif cartas[0].cat == "M" and cartas[1].cat == "A" and cartas[2].cat == "T":
        return 14
    elif cartas[0].cat == "M" and cartas[1].cat == "T" and cartas[2].cat == "A":
        return 14
    elif cartas[0].cat == "A" and cartas[1].cat == "T" and cartas[2].cat == "M":
        return 14
    elif cartas[0].cat == "A" and cartas[1].cat == "M" and cartas[2].cat == "T":
        return 14
    #Hat trick
    elif cartas[0].cat == "A" and cartas[1].cat == "A" and cartas[2].cat == "A":
        return 15
    #Duo alto
    elif cartas[0].cat == "T" and cartas[1].cat == "A" and cartas[2].cat == "A":
        return 16
    elif cartas[1].cat == "T" and cartas[0].cat == "A" and cartas[2].cat == "A":
        return 16
    elif cartas[2].cat == "T" and cartas[1].cat == "A" and cartas[0].cat == "A":
        return 16
    #Messi
    elif cartas[0].cat == "T" and cartas[1].cat == "T":
        return 17
    elif cartas[0].cat == "T" and cartas[2].cat == "T":
        return 17
    elif cartas[1].cat == "T" and cartas[2].cat == "T":
        return 17
 
def ordenar_cartas(cartas):
    # Utiliza la función sorted para ordenar la lista de objetos por su fuerza
    cartas_ordenadas = sorted(cartas, key=lambda objeto: objeto.fuerza)
    return cartas_ordenadas
    
    
def tirar_mano(clasificacion):
    
    if clasificacion == 1:
        return 0
    elif clasificacion == 2:
        return 0
    elif clasificacion == 3:
        return 2
    elif clasificacion == 4:
        return 0
    elif clasificacion == 5:
        return 0
    elif clasificacion == 6:
        return 2
    elif clasificacion == 7:
        return 0
    elif clasificacion == 8:
        return 0
    elif clasificacion == 9:
        return 1
    elif clasificacion == 10:
        return 1
    elif clasificacion == 11:
        return 1
    elif clasificacion == 12:
        return 0
    elif clasificacion == 13:
        return 0
    elif clasificacion == 14:
        return 0
    elif clasificacion == 15:
        return 2
    elif clasificacion == 16:
        return 0
    elif clasificacion == 17:
        return 0
    
    
def elegir_carta_1(info, cartas):
    
    #Si es mano
    if info["mano"] == False:
        return tirar_mano(info["clasificacion"])
    
    
    #Si no soy mano
    
    c = info["cartas_jugadas"][0]
    #revisar si alguna carta le gana, si es asi tirar la mas baja
    cartas_que_ganan = []
    cartas_que_pardan = []
    vuelta = 0
    for carta in cartas:
        if carta.fuerza > c.fuerza:
            cartas_que_ganan.append(vuelta)
        elif carta.fuerza == c.fuerza:
            cartas_que_pardan.append(vuelta)
        vuelta += 1
        
    if cartas[0].cat == "T" or cartas[1].cat == "T" or cartas[2].cat == "T":
        if len(cartas_que_pardan) > 0:
            return cartas_que_pardan[0]
    
    if len(cartas_que_ganan) > 0:
        return cartas_que_ganan[0]
    
    return 0
    

def elegir_carta_2(info, cartas):
    
    if info["parda1"] == True:
        #si juego primero
        if info["mano"] == False:
            return 1
        else:
            if cartas[1].fuerza >= info["cartas_jugadas"][2].fuerza:
                return 1
            #si no le gano me voy al mazo
            else:
                irse_mazo = {"Ingles" : "I fold",
                             "Español" : "Me voy al mazo"}
                comentarios.append(irse_mazo[idioma])
                return 4
    
    
    #Si no gane la primera, y el oponente ya jugo
    if info["cartas_jugadas"][2].nombre != " ":
        c = info["cartas_jugadas"][2]
        
        cartas_que_ganan = []
        vuelta = 0
        
        for carta in cartas:
            if carta.fuerza > c.fuerza:
                cartas_que_ganan.append(vuelta)
                
            vuelta += 1
            
        if len(cartas_que_ganan) > 0:
            return cartas_que_ganan[0]
        else:
            irse_mazo = {"Ingles" : "I fold",
                             "Español" : "Me voy al mazo"}
            comentarios.append(irse_mazo[idioma])
            return 4
        
        
    #Si gane la primera
    if cartas[0].cat != "T" and cartas[1].cat != "T":
        return random.randint(0,1)
    elif cartas[1].cat == "T":
        return 0
    else:
        return 1
    
def elegir_carta_3(info, cartas):
    
    if info["cartas_jugadas"][4].fuerza > cartas[0].fuerza:
        irse_mazo = {"Ingles" : "I fold",
                             "Español" : "Me voy al mazo"}
        comentarios.append(irse_mazo[idioma])
        return 4
    #si son del mismo valor
    elif info["cartas_jugadas"][4].fuerza == cartas[0].fuerza:
        #si el oponente gano primera
        if info["cartas_jugadas"][0].fuerza > info["cartas_jugadas"][1].fuerza:
            irse_mazo = {"Ingles" : "I fold",
                             "Español" : "Me voy al mazo"}
            comentarios.append(irse_mazo[idioma])
            return 4
        #si las 3 rondas son pardas y el oponente es mano
        elif info["cartas_jugadas"][0].fuerza == info["cartas_jugadas"][1].fuerza:
            if info["mano"] == True:
                irse_mazo = {"Ingles" : "I fold",
                             "Español" : "Me voy al mazo"}
                comentarios.append(irse_mazo[idioma])
                return 4
    else:
        return 0

    
def elegir_envido(info, cartas):
    
    valor_max = 0
    tantos = []
    tantos.append(cartas[0] + cartas[1])
    tantos.append(cartas[0] + cartas[2])
    tantos.append(cartas[1] + cartas[2])
    
    for tanto in tantos:
        if tanto > valor_max:
            valor_max = tanto
                  
            
    if valor_max >= 32:
        
        if info["puntos_jugador"] > 27 and info["puntos_jugador2"] < info["puntos_jugador"]:
            return 2
        
        return 3
    
    if valor_max >=  27:
        
        if info["puntos_jugador2"] >= 28:
            return 3
        
        x = random.randint(1,4)
        if x == 4:
            return 2
        
        return 1
    
    x = random.randint(1,8)
    if x == 1:
        x = random.randint(1,3)
        if x == 3:
            return 2
        else:
            return 1
    
    return 0
    
                    
    
def responder_envido(info, cartas, cantado):

    valor_max = 0
    tantos = []
    tantos.append(cartas[0] + cartas[1])
    tantos.append(cartas[0] + cartas[2])
    tantos.append(cartas[1] + cartas[2])
    
    for tanto in tantos:
        if tanto > valor_max:
            valor_max = tanto
            
    #diferencia de puntos
    diferencia = info["puntos_jugador2"] - info["puntos_jugador"]
      
    #revisar si se esta obligado a aceptar
    copia = cantado.copy()
    puntos_por_rechazar = 0
    
    copia.pop(-1)
    for i in copia:
        if i == 1:
            puntos_por_rechazar += 2
        elif i == 2:
            puntos_por_rechazar += 3
    if puntos_por_rechazar == 0:
        puntos_por_rechazar = 1
    
    if info["puntos_jugador"] + puntos_por_rechazar >= PUNTOS_PARA_GANAR:
        return 10
    
    
    #si los puntos por rechazar son menores a los que faltan para ganar, cantar falta envido
    if puntos_por_rechazar + info["puntos_jugador2"] >= PUNTOS_PARA_GANAR:
        return 3
        
        
    #calcular los puntos por aceptar
    copia2 = cantado.copy()
    puntos_por_aceptar = 0
    
    if copia2[-1] == 3:
        if info["puntos_jugador"] > info["puntos_jugador2"]:
            puntos_por_aceptar = PUNTOS_PARA_GANAR - info["puntos_jugador"]
        else:
            puntos_por_aceptar = PUNTOS_PARA_GANAR - info["puntos_jugador2"]
    else:
        for i in copia2:
            if i == 1:
                puntos_por_aceptar += 2
            elif i == 2:
                puntos_por_aceptar += 3
        if puntos_por_aceptar == 0:
            puntos_por_aceptar = 1  
        
            
    #Si se canto envido
    if cantado[-1] == 1:
        
        if valor_max < 25:
            return 30
        
        if valor_max >= 32:
            if info["puntos_jugador2"] + puntos_por_aceptar >= PUNTOS_PARA_GANAR:
                return 10
            else:
                try:
                    if cantado[-2] == 1:
                        x = random.randint(1,4)
                        if x == 1:
                            return 2
                        else:
                            return 3
                except:
                    x = random.randint(1,5)
                    if x == 1:
                        return 1
                    elif x == 2:
                        return 2
                    else:
                        return 3
          
        #si hay mucha diferencia de puntos acepta con 25 y 26  
        if diferencia < -10:
            return 10
        
        if valor_max > 26:
            return 10
        
    elif cantado[-1] == 2:
        
        if valor_max < 28:
            return 30
        
        if valor_max >= 32:
            if info["puntos_jugador2"] + puntos_por_aceptar >= PUNTOS_PARA_GANAR:
                return 10
            else:
                return 3
        
        else:
            return 10
        
    elif cantado[-1] == 3:
        
        if valor_max >= 32:
            return 10
        
        else:
            return 30
        
        
def elegir_truco(info):
    c = calcular_fuerza(info)
    
    x = random.randint(1,10)
    
    if x == 1 and c >= 0.5:
        return True
    elif x == 2 and c >= 0.25:
        return True
    elif c >= 0.75:
        return True
    else:
        return False
        
   
        
def calcular_fuerza(info):
    
    
    #primera ronda si uno juega segundo
    if info["mano"] == True and len(info["cartas_j2"]) == 3:
        x = elegir_carta_1(info, info["cartas_j2"])
        
        #le gano
        if info["cartas_j2"][x].fuerza > info["cartas_jugadas"][0].fuerza:
            #suma de fuerza de las 2 cartas restantes
            c = 0
            if info["cartas_j2"][0] != info["cartas_j2"][x]:
                c += info["cartas_j2"][0].fuerza * info["cartas_j2"][0].fuerza
            if info["cartas_j2"][1] != info["cartas_j2"][x]:
                c += info["cartas_j2"][1].fuerza * info["cartas_j2"][1].fuerza
            if info["cartas_j2"][2] != info["cartas_j2"][x]:
                c += info["cartas_j2"][2].fuerza * info["cartas_j2"][2].fuerza
                
            return c / 196 #0.75 seria bueno
        
        #es parda
        elif info["cartas_j2"][x].fuerza == info["cartas_jugadas"][0].fuerza:
            if info["cartas_j2"][x] == info["cartas_j2"][2]:
                c = info["cartas_j2"][1].fuerza
            else:
                c = info["cartas_j2"][2].fuerza
                
            return c / 13 #0.75 seria bueno
        
        #pierdo
        else:
            return 0
     
    #primera ronda si uno juega primero
    if info["mano"] == False and len(info["cartas_j2"]) == 3: 
        return 0
        
    #segunda ronda si uno juega primero
    if info["ronda"] == 2 and info["cartas_jugadas"][2].nombre == " ":
        #si jugue antes no canta
        if info["mano"] == True:
            return 0
        else:
            c = info["cartas_j2"][0].fuerza * info["cartas_j2"][0].fuerza + info["cartas_j2"][1].fuerza * info["cartas_j2"][1].fuerza
            return c / 133
        
    #segunda ronda si uno juega segundo
    if info["ronda"] == 2 and info["cartas_jugadas"][2].nombre != " ":
        x = elegir_carta_2(info, info["cartas_j2"])
        if x == 4:
            return 0
        elif info["cartas_j2"][x].fuerza >= info["cartas_jugadas"][2].fuerza:
            return 1
        elif x == 0:
            return info["cartas_j2"][1].fuerza / 13
        else:
            return info["cartas_j2"][0].fuerza / 13
        
    #tercer ronda si uno juega primero
    if info["ronda"] == 3 and info["cartas_jugadas"][4].nombre == " ":
        return info["cartas_j2"][0].fuerza / 13
        
    #tercer ronda si uno juega segundo
    if info["ronda"] == 3 and info["cartas_jugadas"][4].nombre != " ":
        c = info["cartas_jugadas"][4]
        if info["cartas_j2"][0].fuerza > c.fuerza or info["cartas_j2"][0].fuerza == c.fuerza and info["cartas_jugadas"][0].fuerza == info["cartas_jugadas"][1].fuerza:
            return 1
        elif c.fuerza <= 3:
            return 1
        elif c.fuerza <= 6:
            return 0.7
        else:
            return 0
        
def responder_truco(info, aumentar):
    #revisa si quiere y puede cantar envido
    if info["primero"] == True and info["segundo"] == 1 and info["cartas_jugadas"][1] == " ":
        x = elegir_envido(info, info["cartas_j2"])
        if x != 0:
            return x + 10 #canta envido y el +10 hace que el numero se diferencie de el truco
    
    #si es primera mano
    if info["puntos_mano_j1"] == 0 and info["puntos_mano_j2"] == 0 and info["parda1"] == False and info["parda2"] == False and info["parda3"] == False:
        #si no conosco la carta del rival
        if info["mano"] == False:
            c = calificar_mano(info["cartas_j2"])
            x = random.randint(1,3)
            if x == 1:
                if c >= 4:
                    return 1 #quiero
            elif c >= 7:
                return 1 #quiero
            else:
                return 2 #no quiero
        #conosco la carta del rival
        else:
            x = calcular_fuerza(info)
            if x > 0.85 and aumentar:
                return 3 #aumentar
            elif x > 0.75:
                return 1 #quiero
            else:
                return 2 #no quiero
            
    #si es segunda mano
    if info["puntos_mano_j1"] + info["puntos_mano_j2"] == 1 or info["parda1"] == True and info["parda2"] == False:

        x = calcular_fuerza(info)
        if x > 0.85 and aumentar:
            return 3 #aumentar
        elif x > 0.75:
            return 1 #quiero
        else:
            return 2 #no quiero
     
    #si es tercer mano   
    if info["puntos_mano_j1"] + info["puntos_mano_j2"] == 2 or info["parda2"] == True:
        x = calcular_fuerza(info)
        if x > 0.85 and aumentar:
            return 3 #aumentar
        elif x > 0.75:
            return 1 #quiero
        else:
            return 2 #no quiero
        
#declaracion de variables

directorio_programa = os.path.dirname(os.path.abspath(__file__))
directorio_imagen = os.path.join(directorio_programa, "imagenes/madera.jpg")


#se les dan 3 cartas diferentes a cada jugador
cartas_p1, cartas_p2 = repartir(crear_mazo())

#se le asignan valores a variables necesarias
puntos_mano_p1 = 0
puntos_mano_p2 = 0
parda1 = False
parda2 = False
parda3 = False
carta_vacia = Carta(" ", " ", 0, 0, " ", " ")
clasificacion = calificar_mano(cartas_p2)
cartas_p1 = ordenar_cartas(cartas_p1)
cartas_p2 = ordenar_cartas(cartas_p2)
ronda = 0
global info
info = {
    "eleccion" : None,
    "primero" : True,
    "segundo" : 1,
    "puntos_primero" : [None, None],
    "quiero" : 0,
    "cartas_jugadas" : [carta_vacia] * 6,
    "puntos_jugador" : 0,
    "puntos_jugador2" : 0,
    "cartas_j1" : cartas_p1,
    "cartas_j2" : cartas_p2,
    "mano" : 0,
    "parda1" : parda1,
    "parda2" : parda2,
    "parda3" : parda3,
    "clasificacion" : clasificacion,
    "ronda" : ronda,
    "puntos_mano_j1" : puntos_mano_p1,
    "puntos_mano_j2" : puntos_mano_p2,
    "elementos" : 0
}   
opcion = tk.StringVar
opcion = None
opcion_elegida = None
botones_cartas = []
idioma = "Ingles"        

        
#ejecutar archivo

#GUI


def actualizar_opcion(*args):
    global puntos_para_ganar_elegidos
    global opcion_seleccionada
    puntos_para_ganar_elegidos = opcion_seleccionada.get()


def mostrar_escena(crear_funcion_escena, master):
    if master.escena_actual:
        master.escena_actual.destroy()
    master.escena_actual = crear_funcion_escena(master)
    master.escena_actual.pack()

def usuario_elige_gui():
    global opcion
    opcion = info["elementos"]["seleccion"].get()
    
def carta_elegida_imagen(indice, carta):
    # Ocultar el botón correspondiente al índice dado
    global opcion_elegida
    global botones_cartas
    global validos
    
    for opcion in validos:
        if indice + 1 == opcion["index"]:
            botones_cartas[indice].pack_forget()
            opcion_elegida = indice + 1
            confirmar_var.set("confirmado")
    
def actualizar_frame():
    
    global info
    global botones_cartas
    
    botones_cartas = []
    
    # Destruir el contenido actual del frame
    for widget in info["elementos"]["frame cartas"].winfo_children():
        widget.destroy()

    for i, carta in enumerate(info["cartas_j1"]):
        imagen_carta = ImageTk.PhotoImage(Image.open(carta.foto))
        boton_carta = tk.Button(info["elementos"]["frame cartas"], text=carta.nombre, image=imagen_carta, command=lambda i=i, carta=carta: carta_elegida_imagen(i, carta))
        boton_carta.image = imagen_carta  # Mantén una referencia para evitar que la imagen sea eliminada por el recolector de basura
        boton_carta.pack(side=tk.LEFT, padx=5)
        botones_cartas.append(boton_carta)

def cambiar_color(boton, x):
    global validos
    if x == 100:
        boton.config(bg="lightblue")
        
    for opcion in validos:
        if x == opcion["index"]: 
            boton.config(bg="lightblue")
    
def restaurar_color(boton):
    boton.config(bg="#E8E8F0")

def on_cerrar_ventana():
    global ventana

    ventana.destroy()

def accion_elegida_boton(accion):
    global opcion_elegida
    global confirmar_var
    global validos
    
    for opcion in validos:
        if accion == opcion["index"]:
            opcion_elegida = accion
            confirmar_var.set("confirmar")
            return 
    
def centrar_widget(widget, master):
    widget.update_idletasks()
    ancho = widget.winfo_reqwidth()
    x = (master.winfo_width() - ancho) // 2
    widget.place(x=x, y=widget.winfo_y())
    
def cambiar_bandera(boton):
    
    global idioma
    
    if idioma == "Ingles":
        idioma = "Español"
    else:
        idioma = "Ingles"
        
    mostrar_escena(crear_escena_inicio, ventana)
    
def mostrar_cartel(texto):
    
    global info
    global confirmar_var
    global comentarios
    
    # Crear un Toplevel como contenedor del cuadro de diálogo
    informacion = {"Ingles" : "Information",
                   "Español" : "Informacion"}
    dialogo = tk.Toplevel(ventana)
    dialogo.title(informacion[idioma])
    
    # Configurar la posición del cuadro de diálogo en el centro de la pantalla
    ancho_ventana = ventana.winfo_width()
    alto_ventana = ventana.winfo_height()
    x = ventana.winfo_x() + ancho_ventana // 2 - 150
    y = ventana.winfo_y() + alto_ventana // 2 - 75
    
    dialogo.geometry(f"400x150+{x}+{y}")

    # Hacer que el cuadro de diálogo sea modal (bloquea la interacción con otras partes de la aplicación)
    dialogo.grab_set()

    # Diseñar el contenido del cuadro de diálogo
    etiqueta = tk.Label(dialogo, text=texto, font=tamaño_fuente)
    etiqueta.pack(pady=10)

    aceptar_text = {"Ingles" : "Ok",
                    "Español" : "Aceptar"}
    boton_cerrar = tk.Button(dialogo, text=aceptar_text[idioma], command=dialogo.destroy, font=tamaño_fuente, bg="#E8E8F0")
    boton_cerrar.pack(pady=10)
    boton_cerrar.bind("<Enter>", lambda event, boton=boton_cerrar, x=100:cambiar_color(boton, x))
    boton_cerrar.bind("<Leave>", lambda event, boton=boton_cerrar :restaurar_color(boton))
    
    
    dialogo.update_idletasks()
    ancho_recomendado = dialogo.winfo_reqwidth()
    alto_recomendado = dialogo.winfo_reqheight()
    dialogo.geometry(f"{ancho_recomendado}x{alto_recomendado}")
    
    confirmar_var.set("confirmado")
    comentarios = []
    dialogo.wait_window()
          
   
def crear_escena_juego(master):
    
    global elementos
    global confirmar_var
    global comentarios
    global info
    
    comentarios = []
    
    
    #frame partida  
    frame_partida = tk.Frame(master)   
    frame_partida.pack()
 
    
    #datos de la partida
    header = tk.Label(frame_partida, text="place holder", font=tamaño_fuente)
    header.pack()

    #comentario del rival
    comentario = tk.Label(frame_partida, text=comentarios, font=tamaño_fuente)
    comentario.pack()

    #mesa
    
    foto1 = Image.open(directorio_imagen)
    foto2 = foto1.resize((400, 330))
    foto = ImageTk.PhotoImage(foto2) 

    
    frame_mesa = tk.Frame(frame_partida, width=400, height=330)
    frame_mesa.pack()
    
    carta_mesa_1 = tk.Label(frame_mesa)
    carta_mesa_1.place(x=40, y=10)
    
    carta_mesa_2 = tk.Label(frame_mesa)
    carta_mesa_2.place(x=150, y=10)
    
    carta_mesa_3 = tk.Label(frame_mesa)
    carta_mesa_3.place(x=260, y=10)
    
    carta_mesa_4 = tk.Label(frame_mesa)
    carta_mesa_4.place(x=40, y=180)
    
    carta_mesa_5 = tk.Label(frame_mesa)
    carta_mesa_5.place(x=150, y=180)
    
    carta_mesa_6 = tk.Label(frame_mesa)
    carta_mesa_6.place(x=260, y=180)
    
    
    fondo_mesa = tk.Label(frame_mesa, image=foto)
    fondo_mesa.image = foto
    fondo_mesa.place(x=0, y=0)
    

    #cartas

    imagenes_cartas = [ImageTk.PhotoImage(Image.open(info["cartas_j1"][0].foto)), ImageTk.PhotoImage(Image.open(info["cartas_j1"][1].foto)), ImageTk.PhotoImage(Image.open(info["cartas_j1"][2].foto))]

    frame_cartas = tk.Frame(frame_partida)
    frame_cartas.pack()

    for i, carta in enumerate(info["cartas_j1"]):
        boton_carta = tk.Button(frame_cartas, text=carta, image=imagenes_cartas[i], command=lambda i=i, carta=carta: carta_elegida_imagen(i, carta))
        boton_carta.pack(side=tk.LEFT, padx=5)
        botones_cartas.append(boton_carta)

    #quiero no quiero

    frame_quiero = tk.Frame(frame_partida)
    frame_quiero.pack()

    quiero_text = {"Ingles" : "I want",
                   "Español" : "Quiero"}
    quiero = tk.Button(frame_quiero, text=quiero_text[idioma], command=lambda x= 10:accion_elegida_boton(x), bg="#E8E8F0")
    quiero.pack(side=tk.LEFT)
    quiero.bind("<Enter>", lambda event, boton=quiero, x=10 :cambiar_color(boton, x))
    quiero.bind("<Leave>", lambda event, boton=quiero :restaurar_color(boton))

    no_quiero_text = {"Ingles" : "I don't want",
                   "Español" : "No quiero"}
    no_quiero = tk.Button(frame_quiero, text=no_quiero_text[idioma], command=lambda x= 20:accion_elegida_boton(x), bg="#E8E8F0")
    no_quiero.pack(side=tk.LEFT)
    no_quiero.bind("<Enter>", lambda event, boton=no_quiero, x=20 :cambiar_color(boton, x))
    no_quiero.bind("<Leave>", lambda event, boton=no_quiero :restaurar_color(boton))

    #truco, envido e irse al mazo

    frame_acciones = tk.Frame(frame_partida)
    frame_acciones.pack()

    truco = tk.Button(frame_acciones, text=info["segundo"], command=lambda x= 4:accion_elegida_boton(x), bg="#E8E8F0")
    truco.pack(side=tk.LEFT)
    truco.bind("<Enter>", lambda event, boton=truco, x=4 :cambiar_color(boton, x))
    truco.bind("<Leave>", lambda event, boton=truco :restaurar_color(boton))

    envido = tk.Button(frame_acciones, text="Envido", command=lambda x= 7:accion_elegida_boton(x), bg="#E8E8F0")
    envido.pack(side=tk.LEFT)
    envido.bind("<Enter>", lambda event, boton=envido, x=7 :cambiar_color(boton, x))
    envido.bind("<Leave>", lambda event, boton=envido :restaurar_color(boton))

    real_envido = tk.Button(frame_acciones, text="Real envido", command=lambda x= 8:accion_elegida_boton(x), bg="#E8E8F0")
    real_envido.pack(side=tk.LEFT)
    real_envido.bind("<Enter>", lambda event, boton=real_envido, x=8 :cambiar_color(boton, x))
    real_envido.bind("<Leave>", lambda event, boton=real_envido :restaurar_color(boton))

    falta_envido = tk.Button(frame_acciones, text="Falta envido", command=lambda x= 9:accion_elegida_boton(x), bg="#E8E8F0")
    falta_envido.pack(side=tk.LEFT)
    falta_envido.bind("<Enter>", lambda event, boton=falta_envido, x=9 :cambiar_color(boton, x))
    falta_envido.bind("<Leave>", lambda event, boton=falta_envido :restaurar_color(boton))

    irse_mazo_text = {"Ingles" : "Fold",
                   "Español" : "Irse al mazo"}
    irse_mazo = tk.Button(frame_acciones, text=irse_mazo_text[idioma], command=lambda x= 0:accion_elegida_boton(x), bg="#E8E8F0")
    irse_mazo.pack(side=tk.LEFT)
    irse_mazo.bind("<Enter>", lambda event, boton=irse_mazo, x=0: cambiar_color(boton, x))
    irse_mazo.bind("<Leave>", lambda event, boton=irse_mazo :restaurar_color(boton))
    
    
    elementos = {
    "comentario" : comentario,
    "mesa" : None,
    "ventana" : master,
    "frame cartas": frame_cartas,
    "header" : header,
    "truco" : truco,
    "frame mesa" : frame_mesa,
    "cartas mesa" : [carta_mesa_4, carta_mesa_1, carta_mesa_5, carta_mesa_2, carta_mesa_6, carta_mesa_3],
    "fondo mesa" : fondo_mesa
    }

    confirmar_var = tk.StringVar() 
    segundo = "normal"
    comentarios = []

    
    return frame_partida
    
    
    
def crear_escena_inicio(master):
    
    global puntos_para_ganar_elegidos
    global opcion_seleccionada
    
    
    escena = tk.Frame(master, width=1000, height=650)
    label = tk.Label(escena, text="TRUCO", font=font.Font(size=30))
    label.place(x=500,y=50)
    centrar_widget(label, master)
    subtitulo = {
        "Ingles" : "The famous game of strategies and lies",
        "Español" : "El famoso juego de estrategias y mentiras"
    }
    label2 = tk.Label(escena, text=subtitulo[idioma], font=tamaño_fuente)
    label2.place(x=500,y=105)
    centrar_widget(label2, master)
    
    opciones = {"Ingles" : ["To 30 points", "To 15 points"],
                "Español" : ["A 30 puntos", "A 15 puntos"]}
    
    #boton cambiar de idioma
    directorio_programa = os.path.dirname(os.path.abspath(__file__))
    directorio_imagen_EEUU = os.path.join(directorio_programa, "imagenes/bandera_EEUU.png")
    directorio_imagen_Argentina = os.path.join(directorio_programa, "imagenes/bandera_Argentina.png")
    foto_EEUU = Image.open(directorio_imagen_EEUU)
    foto_EEUU = foto_EEUU.resize((70,40))
    foto_EEUU = ImageTk.PhotoImage(foto_EEUU)
    foto_Argentina = Image.open(directorio_imagen_Argentina)
    foto_Argentina = foto_Argentina.resize((70,40))
    foto_Argentina = ImageTk.PhotoImage(foto_Argentina)
    
    if idioma == "Ingles":
        foto = foto_EEUU
    else:
        foto = foto_Argentina
    
    cambiar_idioma = tk.Button(escena, image=foto, width=70, height=40)
    cambiar_idioma.config(command=lambda boton=cambiar_idioma : cambiar_bandera(boton))
    cambiar_idioma.image = foto
    cambiar_idioma.place(x=900,y=25)

    # Crear una variable para almacenar la opción seleccionada
    opcion_seleccionada = tk.StringVar(escena)
    opcion_seleccionada.set(opciones[idioma][0])  # Establecer la opción predeterminada

    opcion_seleccionada.trace_add("write", actualizar_opcion)

    # Crear el menú desplegable
    menu_desplegable = tk.OptionMenu(escena, opcion_seleccionada, *opciones[idioma])
    menu_desplegable.place(x=500,y=165)
    centrar_widget(menu_desplegable, master)
    
    #boton para iniciar la partida
    texto_jugar = {"Ingles" : "¡Play!",
                   "Español" : "¡Jugar!"}
    boton_ir_a_juego = tk.Button(escena, text=texto_jugar[idioma], width=10, height=2, command=lambda: (mostrar_escena(crear_escena_juego, master), partido(elementos, cartas_p1, cartas_p2)))
    boton_ir_a_juego.place(x=500,y=200)
    centrar_widget(boton_ir_a_juego, master)
    
    puntos_para_ganar_elegidos = opcion_seleccionada.get()
    
    return escena


def iniciar_ventana_principal():
    global ventana
    global tamaño_fuente
    
    ventana = tk.Tk()
    
    icono_ruta = os.path.join(directorio_programa, "imagenes/icono.ico")
    ventana.iconbitmap(icono_ruta)
    
    tamaño_fuente = font.Font(size=16)
    ventana.protocol("WM_DELETE_WINDOW", on_cerrar_ventana)
    
    ventana.geometry("1000x650+250+100")
    ventana.title("Truco B0T")
    ventana.escena_actual = None
    mostrar_escena(crear_escena_inicio, ventana)
    ventana.mainloop()





if __name__ == "__main__":
    iniciar_ventana_principal()