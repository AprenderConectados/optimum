"""
Programming Minds
.Escuela secundaria Obispo Zapata
-Integrantes: _Francisco Ramos _Leandro Olmos _Adrian Aciar
-Profe: Gabriel Ramis

---Descripcion: El juego consiste en recolectar basura en diferentes escenarios y de esa manera ir sumando puntos.
Hay un sistema de puntuaciones integrado en el juego, de esa manera se puede competir con otros jugadores, aparte hay
algunos obstaculos en cada escenario que dificultan un poco la recoleccion de residuos. Aviso! "Para entrar al top se debe
ingresar (600 puntos) en modo por puntos o (30 segundos) en modo por tiempo. De esa manera es mas justo el sistema de puntuaciones,
ya que si otro jugador ingresara un valor menor o superior a los dichos, pueden tener algun tipo de beneficio y eso no seria algo justo"
"""

# Librerias
import pygame, os, random
from pygame.locals import *
import funciones, clases

pygame.init()

# Reloj que controlara los FPS del juego
Reloj = pygame.time.Clock()

# Direccion del codigo .py
path = os.getcwd()

# Se crea y configura el tamano de la ventana
sizeScreen = (1020,700)
screen = pygame.display.set_mode(sizeScreen)
pygame.display.set_caption("OPTIMUM -Programming Minds-")

# Fuentes de textos
my_font = pygame.font.Font(None,55)
my_font2 = pygame.font.Font(None,35)
my_font3 = pygame.font.Font(None,20)

# Variables utiles en un futuro
done = False
numero_ingresado = 0
name_player = "PLAYER"
texto_por_residuo = "Excelente!"
tmp_name_player = len(name_player)
tecla = pygame.key.get_pressed()
estado_juego = "inicio"
current_time = 0
solo_organico = False
puntos_obtenidos = 0
tiempo_transcurrido = 0
walls = [] # Rectangulos para collisiones del escenario
basureros = []

# Cargamos imagenes
fondo_menu = funciones.Imagen(path+str("/images/fondo_menu.jpg"))
fondo_tabla_puntuaciones = funciones.Imagen(path+str("/images/puntuaciones.jpg"))
fondo_info_robot = funciones.Imagen(path+str("/images/info_robot.jpg"))
config_tiempo_fondo = funciones.Imagen(path+str("/images/config_tiempo.jpg"))
config_puntos_fondo = funciones.Imagen(path+str("/images/config_puntos.jpg"))
por_tiempo_fondo = funciones.Imagen(path+str("/images/por_tiempo_fondo.jpg"))
por_puntos_fondo = funciones.Imagen(path+str("/images/por_puntos_fondo.jpg"))
solo_organico_fondo = funciones.Imagen(path+str("/images/solo_organico_fondo.jpg"))
finalizado_por_tiempo = funciones.Imagen(path+str("/images/finalizado_por_tiempo.jpg"))
finalizado_por_puntos = funciones.Imagen(path+str("/images/finalizado_por_puntos.jpg"))
sin_tiempo_puntos = funciones.Imagen(path+str("/images/sin_tiempo_puntos.jpg"))
info_modo_extra = funciones.Imagen(path+str("/images/info_modo_Extra.jpg"))
fondo_modo_extra = funciones.Imagen(path+str("/images/fondo_modo_extra.jpg"))
barra_modo_extra = funciones.Imagen(path+str("/images/barra_jugando_mExtra.jpg"))
finalizado_modo_extra = funciones.Imagen(path+str("/images/finalizado_modo_extra.jpg"))
sombra = funciones.Imagen(path+str("/images/sombra.png"), False, True)

# Cargamos sonidos
s_por_basura_w = pygame.mixer.Sound(path+str("/sonidos/p_basura_w.ogg"))
s_por_basura_l = pygame.mixer.Sound(path+str("/sonidos/p_basura_l.ogg"))
botones = pygame.mixer.Sound(path+str("/sonidos/botones.ogg"))
boton_play = pygame.mixer.Sound(path+str("/sonidos/boton_play.ogg"))
boton_play.set_volume(0.2)

# Se crea el jugador y la basura
player = clases.Player((500,130), (60,60), path)
basura = clases.Basura((106,100), (916, 560), path)
clases.Baureros_mExtra(basureros, 3, [(41,145), (124,520), (738,594)],
                [(41,94), (41,94), (41,94)])


# Renders de textos
txt_por_residuo = pygame.font.Font.render(my_font3, str(texto_por_residuo), 1, (245,245,245))
txt_number_button = pygame.font.Font.render(my_font2, str(numero_ingresado), 1, (245,245,245))
txt_name_player = pygame.font.Font.render(my_font, str(name_player), 1, (245,245,245))
if(estado_juego == "jugando_porpuntos"):
    txt_puntos = pygame.font.Font.render(my_font2, str(clases.puntos)+" - "+str(clases.puntos_objetivo), 1, (144,12,255))
elif(estado_juego == "jugando_portiempo"):
    txt_puntos = pygame.font.Font.render(my_font2, str(clases.puntos), 1, (144,12,255))
elif(estado_juego == "jugando_modo_extra"):
    txt_puntos = pygame.font.Font.render(my_font2, str(player.basureros_encontrados), 1, (144,12,255))
txt_time = pygame.font.Font.render(my_font2, str(current_time), 1, (255,12,255))
txt_puntos_obtenidos = pygame.font.Font.render(my_font2, str(puntos_obtenidos), 1, (244, 229, 237))
txt_tiempo_transcurrido = pygame.font.Font.render(my_font2, str(tiempo_transcurrido), 1, (244, 229, 237))
txt_top1_ptiempo = pygame.font.Font.render(my_font2, "", 1, (43, 50, 59))
txt_top2_ptiempo = pygame.font.Font.render(my_font2, "", 1, (244, 229, 237))
txt_top3_ptiempo = pygame.font.Font.render(my_font2, "", 1, (244, 229, 237))
txt_top4_ptiempo = pygame.font.Font.render(my_font2, "", 1, (244, 229, 237))
txt_top5_ptiempo = pygame.font.Font.render(my_font2, "", 1, (244, 229, 237))
txt_nombre_top1_ptiempo = txt_nombre_top2_ptiempo = txt_nombre_top3_ptiempo = txt_nombre_top4_ptiempo = txt_nombre_top5_ptiempo = pygame.font.Font.render(my_font2, "", 1, (43, 50, 59))
txt_puntos_top1_ptiempo = txt_puntos_top2_ptiempo = txt_puntos_top3_ptiempo = txt_puntos_top4_ptiempo = txt_puntos_top5_ptiempo = pygame.font.Font.render(my_font2, "", 1, (43, 50, 59))

txt_nombre_top1_ppuntos = txt_nombre_top2_ppuntos = txt_nombre_top3_ppuntos = txt_nombre_top4_ppuntos = txt_nombre_top5_ppuntos = pygame.font.Font.render(my_font2, "", 1, (43, 50, 59))
txt_tiempo_top1_ppuntos = txt_tiempo_top2_ppuntos = txt_tiempo_top3_ppuntos = txt_tiempo_top4_ppuntos = txt_tiempo_top5_ppuntos = pygame.font.Font.render(my_font2, "", 1, (43, 50, 59))


# Todo lo necesario para cargar y guardar puntuacion (archivos ".txt")
puntuacion_anterior = [] #0 = nombre  |1 = puntos  |2 = tiempo
puntuaciones_modo_puntos = [] # 0= nombre |1 = tiempo
puntuaciones_modo_tiempo = [] # 0= nombre |1 = puntos


# Esta funcion carga todas las puntuaciones pertenecientes al TOP por tiempo.
def Cargar_puntuaciones_tabla_Ptiempo():
    global txt_nombre_top1_ptiempo, txt_nombre_top2_ptiempo, txt_nombre_top3_ptiempo, txt_nombre_top4_ptiempo, txt_nombre_top5_ptiempo
    global txt_puntos_top1_ptiempo, txt_puntos_top2_ptiempo, txt_puntos_top3_ptiempo, txt_puntos_top4_ptiempo, txt_puntos_top5_ptiempo, puntuaciones_modo_tiempo

    del puntuaciones_modo_tiempo[:]
    archivo_txt = open("por tiempo.txt","a")
    archivo_txt.close()
    archivo_txt = open("por tiempo.txt","r")
    cont = 0
    for line in archivo_txt.readlines():
        line = line.strip()
        if(line != ""):
            puntuaciones_modo_tiempo.append(line)
    for punt in puntuaciones_modo_tiempo:
        if(punt != ("-","-") and str(type(punt)) != "<type 'list'>"):
            puntuaciones_modo_tiempo[cont] = punt.split(';')
        cont += 1
    archivo_txt.close()
    if(len(puntuaciones_modo_tiempo) < 5):
        for i in range( 5 - len(puntuaciones_modo_tiempo)):
            puntuaciones_modo_tiempo.append(["-","-"])
    txt_nombre_top1_ptiempo = pygame.font.Font.render(my_font2, str(puntuaciones_modo_tiempo[0][0]), 1, (43, 50, 59))
    txt_nombre_top2_ptiempo = pygame.font.Font.render(my_font2, str(puntuaciones_modo_tiempo[1][0]), 1, (43, 50, 59))
    txt_nombre_top3_ptiempo = pygame.font.Font.render(my_font2, str(puntuaciones_modo_tiempo[2][0]), 1, (43, 50, 59))
    txt_nombre_top4_ptiempo = pygame.font.Font.render(my_font2, str(puntuaciones_modo_tiempo[3][0]), 1, (43, 50, 59))
    txt_nombre_top5_ptiempo = pygame.font.Font.render(my_font2, str(puntuaciones_modo_tiempo[4][0]), 1, (43, 50, 59))

    txt_puntos_top1_ptiempo = pygame.font.Font.render(my_font2, str(puntuaciones_modo_tiempo[0][1]), 1, (43, 50, 59))
    txt_puntos_top2_ptiempo = pygame.font.Font.render(my_font2, str(puntuaciones_modo_tiempo[1][1]), 1, (43, 50, 59))
    txt_puntos_top3_ptiempo = pygame.font.Font.render(my_font2, str(puntuaciones_modo_tiempo[2][1]), 1, (43, 50, 59))
    txt_puntos_top4_ptiempo = pygame.font.Font.render(my_font2, str(puntuaciones_modo_tiempo[3][1]), 1, (43, 50, 59))
    txt_puntos_top5_ptiempo = pygame.font.Font.render(my_font2, str(puntuaciones_modo_tiempo[4][1]), 1, (43, 50, 59))

# Esta funcion carga todas las puntuaciones pertenecientes al TOP por puntos.
def Cargar_tiempos_tabla_Ppuntos():

    global txt_nombre_top1_ppuntos, txt_nombre_top2_ppuntos, txt_nombre_top3_ppuntos, txt_nombre_top4_ppuntos, txt_nombre_top5_ppuntos
    global txt_tiempo_top1_ppuntos, txt_tiempo_top2_ppuntos, txt_tiempo_top3_ppuntos, txt_tiempo_top4_ppuntos, txt_tiempo_top5_ppuntos, puntuaciones_modo_puntos

    del puntuaciones_modo_puntos[:]
    archivo_txt = open("por puntos.txt","a")
    archivo_txt.close()
    archivo_txt = open("por puntos.txt","r")
    cont = 0
    for line in archivo_txt.readlines():
        line = line.strip()
        if(line != ""):
            puntuaciones_modo_puntos.append(line)
    for punt in puntuaciones_modo_puntos:
        if(punt != ("-","-") and str(type(punt)) != "<type 'list'>"):
            puntuaciones_modo_puntos[cont] = punt.split(';')
        cont += 1
    archivo_txt.close()
    if(len(puntuaciones_modo_puntos) < 5):
        for i in range( 5 - len(puntuaciones_modo_puntos)):
            puntuaciones_modo_puntos.append(["-","-"])
    txt_nombre_top1_ppuntos = pygame.font.Font.render(my_font2, str(puntuaciones_modo_puntos[0][0]), 1, (43, 50, 59))
    txt_nombre_top2_ppuntos = pygame.font.Font.render(my_font2, str(puntuaciones_modo_puntos[1][0]), 1, (43, 50, 59))
    txt_nombre_top3_ppuntos = pygame.font.Font.render(my_font2, str(puntuaciones_modo_puntos[2][0]), 1, (43, 50, 59))
    txt_nombre_top4_ppuntos = pygame.font.Font.render(my_font2, str(puntuaciones_modo_puntos[3][0]), 1, (43, 50, 59))
    txt_nombre_top5_ppuntos = pygame.font.Font.render(my_font2, str(puntuaciones_modo_puntos[4][0]), 1, (43, 50, 59))

    txt_tiempo_top1_ppuntos = pygame.font.Font.render(my_font2, str(puntuaciones_modo_puntos[0][1]), 1, (43, 50, 59))
    txt_tiempo_top2_ppuntos = pygame.font.Font.render(my_font2, str(puntuaciones_modo_puntos[1][1]), 1, (43, 50, 59))
    txt_tiempo_top3_ppuntos = pygame.font.Font.render(my_font2, str(puntuaciones_modo_puntos[2][1]), 1, (43, 50, 59))
    txt_tiempo_top4_ppuntos = pygame.font.Font.render(my_font2, str(puntuaciones_modo_puntos[3][1]), 1, (43, 50, 59))
    txt_tiempo_top5_ppuntos = pygame.font.Font.render(my_font2, str(puntuaciones_modo_puntos[4][1]), 1, (43, 50, 59))


# Esta funcion carga la puntuacion que obtubo el usuario que jugo anteriormente    
def Cargar_puntuacion():
    global txt_nombre_anterior, txt_puntos_anteriores, txt_tiempo_anterior, puntuacion_anterior
    # Se intenta abrir el archivo .txt, si esto es posible, se lee y almacena por linea en una lista. De lo contrario se crea un nuevo archivo .txt
    puntuacion_anterior = []
    archivo = open("puntuaciones.txt","a")
    archivo.close()
    archivo = open("puntuaciones.txt","r")
    for line in archivo.readlines():
        puntuacion_anterior.append(line)
    archivo.close()
    if(len(puntuacion_anterior) == 0):
        puntuacion_anterior = ["-", "-", "-"]

    if(len(puntuacion_anterior) > 0):
        txt_nombre_anterior = pygame.font.Font.render(my_font2, str(puntuacion_anterior[0]), 1, (244, 229, 237))
        txt_puntos_anteriores = pygame.font.Font.render(my_font2, str(puntuacion_anterior[1]), 1, (244, 229, 237))
        txt_tiempo_anterior = pygame.font.Font.render(my_font2, str(puntuacion_anterior[2]), 1, (244, 229, 237))
    else:
        txt_nombre_anterior = pygame.font.Font.render(my_font2, "-", 1, (244, 229, 237))
        txt_puntos_anteriores = pygame.font.Font.render(my_font2, "-", 1, (244, 229, 237))
        txt_tiempo_anterior = pygame.font.Font.render(my_font2, "-", 1, (244, 229, 237))

# Cargamos puntuaciones guardadas
Cargar_puntuacion()
Cargar_puntuaciones_tabla_Ptiempo()
Cargar_tiempos_tabla_Ppuntos()

# Constantes
BLACK = (0,0,0)
LETRAS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
           "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

# Funcion que dibuja todo lo necesario en pantalla
def Draw():
    global texto_por_residuo, txt_por_residuo
    
    screen.fill(BLACK)

    if(estado_juego == "inicio"):
        screen.blit(fondo_menu, (0,0))
    elif(estado_juego == "tabla_puntuaciones"):
        screen.blit(fondo_tabla_puntuaciones, (0,0))
        screen.blit(txt_nombre_top1_ptiempo, (140,351))
        screen.blit(txt_puntos_top1_ptiempo, (393,351))
        screen.blit(txt_nombre_top2_ptiempo, (140,394))
        screen.blit(txt_puntos_top2_ptiempo, (393,394))
        screen.blit(txt_nombre_top3_ptiempo, (140,442))
        screen.blit(txt_puntos_top3_ptiempo, (393,442))
        screen.blit(txt_nombre_top4_ptiempo, (140,486))
        screen.blit(txt_puntos_top4_ptiempo, (393,486))
        screen.blit(txt_nombre_top5_ptiempo, (140,531))
        screen.blit(txt_puntos_top5_ptiempo, (393,531))

        screen.blit(txt_nombre_top1_ppuntos, (620,351))
        screen.blit(txt_tiempo_top1_ppuntos, (890,351))
        screen.blit(txt_nombre_top2_ppuntos, (620,394))
        screen.blit(txt_tiempo_top2_ppuntos, (890,394))
        screen.blit(txt_nombre_top3_ppuntos, (620,442))
        screen.blit(txt_tiempo_top3_ppuntos, (890,442))
        screen.blit(txt_nombre_top4_ppuntos, (620,486))
        screen.blit(txt_tiempo_top4_ppuntos, (890,486))
        screen.blit(txt_nombre_top5_ppuntos, (620,531))
        screen.blit(txt_tiempo_top5_ppuntos, (890,531))
    elif(estado_juego == "info_robot"):
        screen.blit(fondo_info_robot, (0,0))
    elif(estado_juego == "config_por_tiempo"):
        screen.blit(config_tiempo_fondo, (0,0))
        screen.blit(txt_number_button,(423,293))
        screen.blit(txt_name_player,(370,444))
    elif(estado_juego == "config_por_puntos" or estado_juego == "config_solo_organico"):
        screen.blit(config_puntos_fondo, (0,0))
        screen.blit(txt_number_button,(423,293))
        screen.blit(txt_name_player,(370,444))
    elif(estado_juego == "info_modo_extra"):
        screen.blit(info_modo_extra, (0,0))
    elif(estado_juego == "jugando_portiempo"):
        screen.blit(por_tiempo_fondo, (0,0))

        #__Si esto se activa, se mostraran los rectangulos de las collisiones del escenario
        #for wall in walls:
            #pygame.draw.rect(screen, (BLACK), wall)
        screen.blit(player.player_img, player.rect.topleft)
        screen.blit(basura.basura_img, basura.rect.topleft)
        screen.blit(txt_time, (113,10))
        screen.blit(txt_puntos, (904,10))
        if(clases.cont_txt_residuos > 0):
            if(int(clases.puntos_sumados) > 0):
                texto_por_residuo = "Excelente! +"+str(clases.puntos_sumados)
                txt_por_residuo = pygame.font.Font.render(my_font3, str(texto_por_residuo), 1, (40, 180, 99))
            else:
                if(int(clases.puntos_sumados) == -1):
                    texto_por_residuo = "Cuidado! "
                else:
                    texto_por_residuo = "Cuidado! "+str(clases.puntos_sumados)
                txt_por_residuo = pygame.font.Font.render(my_font3, str(texto_por_residuo), 1, (231, 76, 60))
            screen.blit(txt_por_residuo, (680,20))

    elif(estado_juego == "jugando_modo_extra"):
        screen.blit(fondo_modo_extra, (0,0))
        screen.blit(player.player_img, player.rect.topleft)
        screen.blit(sombra, (player.rect.center[0] - (sombra.get_size()[0] / 2),player.rect.center[1] - (sombra.get_size()[1] / 2)))
        screen.blit(barra_modo_extra, (0,0))
        screen.blit(txt_puntos, (904,10))
        #__Si esto se activa, se mostraran los rectangulos de las collisiones del escenario
        #for wall in walls:
            #pygame.draw.rect(screen, (BLACK), wall)
        #for b in basureros:
            #pygame.draw.rect(screen, (BLACK), b)
    elif(estado_juego == "jugando_porpuntos"):
        if(not solo_organico):
            screen.blit(por_puntos_fondo, (0,0))
        else:
            screen.blit(solo_organico_fondo, (0,0))

        #for wall in walls:
            #pygame.draw.rect(screen, (BLACK), wall)
        screen.blit(basura.basura_img, basura.rect.topleft)
        screen.blit(player.player_img, player.rect.topleft)
        screen.blit(txt_time, (113,10))
        screen.blit(txt_puntos, (904,10))
        if(clases.cont_txt_residuos > 0):
            if(int(clases.puntos_sumados) > 0):
                texto_por_residuo = "Exelente! +"+str(clases.puntos_sumados)
                txt_por_residuo = pygame.font.Font.render(my_font3, str(texto_por_residuo), 1, (40, 180, 99))
            else:
                if(int(clases.puntos_sumados) == -1):
                    texto_por_residuo = "Cuidado! "
                else:
                    texto_por_residuo = "Cuidado! "+str(clases.puntos_sumados)
                txt_por_residuo = pygame.font.Font.render(my_font3, str(texto_por_residuo), 1, (231, 76, 60))
            screen.blit(txt_por_residuo, (700,20))
    elif(estado_juego == "finalizado_por_tiempo"):
        screen.blit(finalizado_por_tiempo, (0,0))
        screen.blit(txt_puntos_obtenidos, (473,307))
        screen.blit(txt_tiempo_transcurrido, (692,307))
        screen.blit(txt_name_player,(546,242))
        screen.blit(txt_nombre_anterior, (578, 462))
        screen.blit(txt_puntos_anteriores, (560, 517))
        screen.blit(txt_tiempo_anterior, (605, 560))
    elif(estado_juego == "finalizado_modo_extra"):
        screen.blit(finalizado_modo_extra, (0,0))
    elif(estado_juego == "finalizado_por_puntos"):
        screen.blit(finalizado_por_puntos, (0,0))
        screen.blit(txt_puntos_obtenidos, (530,307))
        screen.blit(txt_tiempo_transcurrido, (374,348))
        screen.blit(txt_name_player,(546,242))
        screen.blit(txt_nombre_anterior, (578, 462))
        screen.blit(txt_puntos_anteriores, (560, 517))
        screen.blit(txt_tiempo_anterior, (605, 560))
    elif(estado_juego == "sin_tiempo_por_puntos"):
        screen.blit(sin_tiempo_puntos, (0,0))
    
    pygame.display.flip()

# Evento que se actualiza cada "1 segundo"
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Se guarda la puntuacion y tiempo obtenido
def Guardar_puntuacion():
    archivo = open("puntuaciones.txt","w")
    archivo.write(""+str(name_player)+" \n")
    archivo.write(""+str(puntos_obtenidos)+" \n")
    archivo.write(""+str(tiempo_transcurrido))
    archivo.close()

# Esta funcion se encarga de actualizar el top del modo por tiempo, depende de el resultado obtenido
def Actualizar_lista_tabla_ptiempo():
    global puntuaciones_modo_tiempo, puntos_obtenidos, name_player
    for i in range(5):
        if(str(puntuaciones_modo_tiempo[i][1]) == "-"):
            puntuaciones_modo_tiempo[i][0] = name_player
            puntuaciones_modo_tiempo[i][1] = puntos_obtenidos
            break
        elif(puntos_obtenidos > int(puntuaciones_modo_tiempo[i][1])):
            puntuaciones_modo_tiempo.insert(i, [str(name_player), puntos_obtenidos])
            if(len(puntuaciones_modo_tiempo) > 5):
                puntuaciones_modo_tiempo.pop()
            break

# Se guarda la puntuacion general para luego poder cargarla y mostrarla en el top
def Guardar_puntuacion_tabla_ptiempo():
        archivo_txt = open("por tiempo.txt","w")
        for punt in puntuaciones_modo_tiempo:
            if(punt[1] != "-"):
                archivo_txt.write(str("\n")+ str(punt[0])+str(";")+str(punt[1]))
        archivo_txt.close()

# Esta funcion se encarga de actualizar el top del modo por puntos, depende de el resultado obtenido
def Actualizar_lista_tabla_ppuntos():
    global puntuaciones_modo_puntos, current_time, name_player
    for i in range(5):
        if(str(puntuaciones_modo_puntos[i][1]) == "-"):
            puntuaciones_modo_puntos[i][0] = name_player
            puntuaciones_modo_puntos[i][1] = current_time
            break
        elif(current_time < int(puntuaciones_modo_puntos[i][1])):
            puntuaciones_modo_puntos.insert(i, [str(name_player), current_time])
            if(len(puntuaciones_modo_puntos) > 5):
                puntuaciones_modo_puntos.pop()
            break

# Se guarda la puntuacion general para luego poder cargarla y mostrarla en el top
def Guardar_puntuacion_tabla_ppuntos():
        archivo_txt = open("por puntos.txt","w")
        for punt in puntuaciones_modo_puntos:
            if(punt[1] != "-"):
                archivo_txt.write(str("\n")+ str(punt[0])+str(";")+str(punt[1]))
        archivo_txt.close()
            

# Se deja al juego en un estado inicial para poder empezar a jugar en otro modo desde cero
def Resetear_valores():
    global current_time, txt_time, numero_ingresado, puntuaciones_modo_tiempo, txt_number_button, name_player, tmp_name_player, txt_name_player, puntos_obtenidos, tiempo_transcurrido, cont_txt_reciduo 

    Cargar_puntuacion()
    del puntuaciones_modo_tiempo[:]
    del puntuaciones_modo_puntos[:]
    del walls[:]
    del basureros[:]
    clases.Baureros_mExtra(basureros, 3, [(41,145), (124,520), (738,594)],
                [(41,94), (41,94), (41,94)])
    player.basureros_encontrados = 0
    Cargar_puntuaciones_tabla_Ptiempo()
    Cargar_tiempos_tabla_Ppuntos()
    cont_txt_reciduo = 0
    current_time = 0
    txt_time = pygame.font.Font.render(my_font2, str(current_time), 1, (255,12,255))
    clases.puntos = 0
    clases.puntos_objetivo = 0
    numero_ingresado = 0
    txt_number_button = pygame.font.Font.render(my_font2, str(numero_ingresado), 1, (245,245,245))
    name_player = "PLAYER"
    player.rect.topleft = player.pos_inicial
    tmp_name_player = len(name_player)
    txt_name_player = pygame.font.Font.render(my_font, str(name_player), 1, (245,245,245))
    puntos_obtenidos = 0
    tiempo_transcurrido = 0
    basura.colocada = False
    basura.movimiento_asignado = False
    player.p_up = False
    player.p_down = False
    player.p_left = False
    player.p_right = False


# Esta funcion se ejecuta en el bucle del juego y sirve para ejecutar las acciones necesarias cuando deban ser ejecutadas
# _Ejemplo: Si se esta jugando entonces se "mueve la basura", mientras que si estas en "inicio" no
def Check_state():
    global txt_puntos, estado_juego, puntos_obtenidos, txt_puntos_obtenidos, tiempo_transcurrido, txt_tiempo_transcurrido, txt_puntos, numero_ingresado
    
    if(estado_juego == "jugando_portiempo" or estado_juego == "jugando_porpuntos"):
        
        basura.Mover_colocar(solo_organico)
        player.Collisiones(basura, estado_juego, solo_organico, s_por_basura_w, s_por_basura_l, basureros)
        if(estado_juego == "jugando_porpuntos"):
            txt_puntos = pygame.font.Font.render(my_font2, str(clases.puntos)+" - "+str(clases.puntos_objetivo), 1, (144,12,255))
            if(clases.puntos >= clases.puntos_objetivo):
                estado_juego = "finalizado_por_puntos"
                if(not solo_organico):
                    if(numero_ingresado == 600):
                        Actualizar_lista_tabla_ppuntos()
                    Guardar_puntuacion_tabla_ppuntos()
                puntos_obtenidos = clases.puntos_objetivo
                txt_puntos_obtenidos = pygame.font.Font.render(my_font2, str(puntos_obtenidos), 1, (244, 229, 237))
                tiempo_transcurrido = current_time
                txt_tiempo_transcurrido = pygame.font.Font.render(my_font2, str(tiempo_transcurrido), 1, (244, 229, 237))
                Guardar_puntuacion()
        elif(estado_juego == "jugando_portiempo"):
            txt_puntos = pygame.font.Font.render(my_font2, str(clases.puntos), 1, (144,12,255))
    elif(estado_juego == "jugando_modo_extra"):
        player.Collisiones(basura, estado_juego, solo_organico, s_por_basura_w, s_por_basura_l, basureros)
        txt_puntos = pygame.font.Font.render(my_font2, str(player.basureros_encontrados), 1, (144,12,255))
        if(player.basureros_encontrados >= 3):
            estado_juego = "finalizado_modo_extra"
        

# Bucle del juego
while(not done):
    # Si se pulsa el boton salir de la ventana entonces salir
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            done = True
            break;

        # Evento que se ejecuta cada 1 segundo
        if(event.type == pygame.USEREVENT):
            if(estado_juego == "jugando_portiempo" or estado_juego == "jugando_porpuntos"):
                if(clases.cont_txt_residuos > 0):
                    clases.cont_txt_residuos -= 1
            if(estado_juego == "jugando_portiempo"):
                if(current_time > 0):
                    current_time -= 1
                else:
                    estado_juego = "finalizado_por_tiempo"
                    puntos_obtenidos = clases.puntos
                    txt_puntos_obtenidos = pygame.font.Font.render(my_font2, str(puntos_obtenidos), 1, (244, 229, 237))
                    tiempo_transcurrido = numero_ingresado
                    txt_tiempo_transcurrido = pygame.font.Font.render(my_font2, str(tiempo_transcurrido), 1, (244, 229, 237))
                    Guardar_puntuacion()
                    if(numero_ingresado == 30):
                        Actualizar_lista_tabla_ptiempo()
                    Guardar_puntuacion_tabla_ptiempo()
                txt_time = pygame.font.Font.render(my_font2, str(current_time), 1, (144,12,255))
            elif(estado_juego == "jugando_porpuntos"):
                if(current_time < 400):
                    current_time += 1
                else:
                    estado_juego = "sin_tiempo_por_puntos"
                txt_time = pygame.font.Font.render(my_font2, str(current_time), 1, (144,12,255))
        
        if(event.type == pygame.MOUSEBUTTONDOWN):
            
            # Se guarda la posicion del mouse en el momento en que el usuario lo pulse
            mx,my = pygame.mouse.get_pos()

            # Si se pulso en el boton "salir" entonces detener el juego y salir
            if((my >= 0 and my <= 69) and (mx >= 951 and mx <= 1020) and (estado_juego == "finalizado_por_tiempo" or
                                                                          estado_juego == "finalizado_por_puntos" or
                                                                          estado_juego == "inicio" or
                                                                          estado_juego == "tabla_puntuaciones" or
                                                                          estado_juego == "info_modo_extra" or
                                                                          estado_juego == "finalizado_modo_extra" or
                                                                          estado_juego == "info_robot")):
                estado_juego == "salir"
                done = True
            if(estado_juego == "inicio"):
                
                # Si se pulso en el boton "Por Tiempo" entonces configurar
                if((my >= 484 and my <= 604) and (mx >= 545 and mx <= 729)):
                    botones.stop()
                    botones.play()
                    estado_juego = "config_por_tiempo"
                    numero_ingresado = 30
                    txt_number_button = pygame.font.Font.render(my_font2, str(numero_ingresado), 1, (245,245,245))
                    basura.Reasignar_limites((106,100), (916, 632))

                # Si se pulso en el boton "modo extra"
                elif((my >= 251 and my <= 401) and (mx >= 730 and mx <= 964)):
                    estado_juego = "info_modo_extra"
                    txt_puntos = pygame.font.Font.render(my_font2, str(player.basureros_encontrados), 1, (144,12,255))

                # Si se pulsa en el boton "Tabla de puntos" entonces ir a la tabla
                elif((my >= 248 and my <= 303) and (mx >= 63 and mx <= 269)):
                    botones.stop()
                    botones.play()
                    del puntuaciones_modo_tiempo[:]
                    Cargar_puntuaciones_tabla_Ptiempo()
                    estado_juego = "tabla_puntuaciones"

                # Si se pulsa en el boton "info robot" entonces ir a la info
                elif((my >= 546 and my <= 601) and (mx >= 63 and mx <= 269)):
                    botones.stop()
                    botones.play()
                    estado_juego = "info_robot"
                    
                # Si se pulso en el boton "Por Puntos" entonces configurar
                elif((my >= 488 and my <= 600) and (mx >= 365 and mx <= 540)):
                    botones.stop()
                    botones.play()
                    estado_juego = "config_por_puntos"
                    numero_ingresado = 600
                    txt_number_button = pygame.font.Font.render(my_font2, str(numero_ingresado), 1, (245,245,245))
                    basura.Reasignar_limites((13, 55), (1013,655))

                # Si se pulso en el boton "Solo Organico" entonces configurar
                elif((my >= 252 and my <= 475) and (mx >= 365 and mx <= 722)):
                    botones.stop()
                    botones.play()
                    estado_juego = "config_solo_organico"
                    solo_organico = True
                    numero_ingresado = 600
                    txt_number_button = pygame.font.Font.render(my_font2, str(numero_ingresado), 1, (245,245,245))
                    basura.Reasignar_limites((13, 55), (1013,655))
            elif(estado_juego == "jugando_porpuntos" or estado_juego == "jugando_portiempo" or estado_juego == "jugando_modo_extra"):

                # Si se pulso en el boton "menu" durante el juego entonces salir al menu
                if((my >= 0 and my <= 46) and (mx >= 488 and mx <= 531)):
                    botones.stop()
                    botones.play()
                    estado_juego = "inicio"
                    solo_organico = False
                    Resetear_valores()
            elif(estado_juego == "tabla_puntuaciones" or estado_juego == "info_robot"):

                # Si se pulso en el boton "volver" entonces salir al menu
                if((my >= 37 and my <= 116) and (mx >= 35 and mx <= 88)):
                    botones.stop()
                    botones.play()
                    estado_juego = "inicio"
                    solo_organico = False
                    Resetear_valores()
            elif(estado_juego == "finalizado_por_tiempo" or estado_juego == "finalizado_por_puntos" or estado_juego == "sin_tiempo_por_puntos" or
                 estado_juego == "finalizado_modo_extra"):
                # Si se pulsa en el boton "menu" entonces salir
                if((my >= 295 and my <= 378) and (mx >= 77 and mx <= 162)):
                    botones.stop()
                    botones.play()
                    estado_juego = "inicio"
                    solo_organico = False
                    if(estado_juego == "finalizado_por_tiempo"):
                        Guardar_puntuacion_tabla_ptiempo()
                    Resetear_valores()
            elif(estado_juego == "config_por_tiempo" or estado_juego == "config_por_puntos" or estado_juego == "config_solo_organico" or
                 estado_juego == "info_modo_extra"):
                
                # El siguiente codigo se encarga de controlar el boton que permite la seleccion de un valor numerico
                if((my >= 269 and my <= 316) and (mx >= 513 and mx <= 587)):
                    if(numero_ingresado < 100 and estado_juego == "config_por_tiempo"):
                        numero_ingresado += 2
                        txt_number_button = pygame.font.Font.render(my_font2, str(numero_ingresado), 1, (245,245,245))
                    elif(numero_ingresado < 9999 and estado_juego == "config_por_puntos" or estado_juego == "config_solo_organico"):
                        numero_ingresado += 20
                        txt_number_button = pygame.font.Font.render(my_font2, str(numero_ingresado), 1, (245,245,245))
                if((my >= 326 and my <= 363) and (mx >= 513 and mx <= 587)):
                    if(numero_ingresado > 0):
                        if(estado_juego == "config_por_puntos" or estado_juego == "config_solo_organico"):
                            numero_ingresado -= 20
                        elif(estado_juego == "config_por_tiempo"):
                            numero_ingresado -= 2
                        txt_number_button = pygame.font.Font.render(my_font2, str(numero_ingresado), 1, (245,245,245))

                # Codigo que hace que cuando se elije nombre y tiempo o puntos (segun el modo de juego), se establezcan los mismos (Boton jugar)
                if((my >= 269 and my <= 363) and (mx >= 885 and mx <= 979)):
                    boton_play.stop()
                    boton_play.play()
                    if(estado_juego == "config_por_tiempo"):
                        if(numero_ingresado < 4):
                            current_time = 4
                            numero_ingresado = current_time
                        else:
                            current_time = numero_ingresado
                    elif(estado_juego == "config_por_puntos" or estado_juego == "config_solo_organico"):
                        
                        if(numero_ingresado < 40):
                            clases.puntos_objetivo = 40
                            numero_ingresado = clases.puntos_objetivo
                        else:
                            clases.puntos_objetivo = numero_ingresado
                            
                    if(name_player == ""):
                        name_player = "PLAYER"
                    if(estado_juego == "config_por_puntos" or estado_juego == "config_solo_organico"):
                        estado_juego = "jugando_porpuntos"
                        player.rect.topleft = (238,350)
                        Cargar_puntuacion()
                        # Se definen las collisiones
                        if(not solo_organico):
                            clases.Walls(walls, 2, [(700,232), (258,109)], # Posiciones
                                         [(135, 135), (300,145)]) # Tamanos
                        else:
                            clases.Walls(walls, 5, [(650,170), (475,451), (82,358), (45, 338), (0, 597)], # Posiciones
                                         [(120, 120), (27, 27), (27, 27), (27, 27), (1020,40)]) # Tamanos
                        
                    elif(estado_juego == "config_por_tiempo"):
                        Cargar_puntuaciones_tabla_Ptiempo()
                        estado_juego = "jugando_portiempo"
                        # Se definen las collisiones
                        clases.Walls(walls, 7, [(103,80), (918,80), (20, 88), (20, 635), (784,103), (516, 220), (103,367)], # Posiciones
                                     [(16, 590), (16,590), (960,16), (960, 16), (150,78), (18, 260), (152,54)]) # Tamanos
                        Cargar_puntuacion()
                    elif(estado_juego == "info_modo_extra"):
                        estado_juego = "jugando_modo_extra"
                        player.rect.topleft = (477,95)
                        clases.Walls(walls, 13, [(547,46), (811,116), (932, 161), (804, 261), (804,493), (546, 495), (103,595), (160,366), (31,219), (31,47),
                                                 (280, 47), (547, 264), (0, 390)], # Posiciones
                                     [(170, 125), (209, 58), (100, 200), (214, 139), (214, 206), (166, 206), (444, 106), (292, 138), (157, 210), (210, 89),(175, 228) ,
                                      (165, 137), (111,313)]) # Tamanos
                    txt_time = pygame.font.Font.render(my_font2, str(current_time), 1, (144,12,255))
                # Si se pulso el boton "volver" regresar a inicio
                if((my >= 269 and my <= 363) and (mx >= 72 and mx <= 133)):
                    botones.stop()
                    botones.play()
                    estado_juego = "inicio"
                    solo_organico = False
                    Resetear_valores()
        if(event.type == pygame.KEYDOWN):
            # Este codigo crea un especie de teclado, el cual usando el numero entero que representa cada letra, detecta cual pulsaste
            # -y de esa manera se va almacenando en una variable "string" formando una cadena de texto (se utiliza para ingresar el nombre
            # --del jugador)
            if(estado_juego == "config_por_tiempo" or estado_juego == "config_por_puntos" or estado_juego == "config_solo_organico"):
                tecl = int(event.key) - 97
                if((tecl <= 25 and tecl >= 0) and (len(name_player) < 10)):
                    tmp_name_player = len(name_player)
                    name_player = name_player + str(LETRAS[tecl])
                    txt_name_player = pygame.font.Font.render(my_font, str(name_player), 1, (245,245,245))
                if(tecl == -89):
                    name_player = name_player[:tmp_name_player]
                    txt_name_player = pygame.font.Font.render(my_font, str(name_player), 1, (245,245,245))
                    tmp_name_player = tmp_name_player - 1

            # Se detecta la pulsacion de las flechas del teclado para luego establecer el sprite adecuado para el jugador
            if(estado_juego == "jugando_portiempo" or estado_juego == "jugando_porpuntos" or estado_juego == "jugando_modo_extra"):
                if(event.key == K_UP):
                    player.p_up = True
                if(event.key == K_DOWN):
                    player.p_down = True
                if(event.key == K_LEFT):
                    player.p_left = True
                if(event.key == K_RIGHT):
                    player.p_right = True
                if(event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT):
                    player.Sprite_Control()
                    
        if(event.type == pygame.KEYUP):
            
            # Se detecta la pulsacion de las flechas del teclado para luego establecer el sprite adecuado para el jugador
            if(estado_juego == "jugando_portiempo" or estado_juego == "jugando_porpuntos" or estado_juego == "jugando_modo_extra"):
                if(event.key == K_UP):
                    player.p_up = False
                if(event.key == K_DOWN):
                    player.p_down = False
                if(event.key == K_LEFT):
                    player.p_left = False
                if(event.key == K_RIGHT):
                    player.p_right = False
                if(event.key == K_UP or event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT):
                    player.Sprite_Control()

    # Tecla que se esta pulsando
    tecla = pygame.key.get_pressed()

    Check_state()
    Draw()

    # Movimiento del jugador
    if(tecla[K_RIGHT] and not(tecla[K_LEFT])):
        if((estado_juego == "jugando_portiempo" or estado_juego == "jugando_porpuntos" or estado_juego == "jugando_modo_extra") and player.rect.right < 1015):
            player.Mover(3,0, walls, estado_juego)
        player.p_right = True
        player.p_left = False
    elif(tecla[K_LEFT] and not(tecla[K_RIGHT])):
        if((estado_juego == "jugando_portiempo" or estado_juego == "jugando_porpuntos" or estado_juego == "jugando_modo_extra") and player.rect.left > 10):
            player.Mover(-3,0, walls, estado_juego)
        player.p_left = True
        player.p_right = False
    if(tecla[K_UP] and not(tecla[K_DOWN])):
        if((estado_juego == "jugando_portiempo" or estado_juego == "jugando_porpuntos" or estado_juego == "jugando_modo_extra") and player.rect.top > 50):
            player.Mover(0,-3, walls, estado_juego)
        player.p_up = True
        player.p_down = False
    elif(tecla[K_DOWN] and not(tecla[K_UP])):
        if((estado_juego == "jugando_portiempo" or estado_juego == "jugando_porpuntos" or estado_juego == "jugando_modo_extra") and player.rect.bottom < 659):            
            player.Mover(0,3, walls, estado_juego)
        player.p_down = True
        player.p_up = False

    #Actualizamos el reloj para que el juego se ejecute a "60" FPS
    Reloj.tick(60)

pygame.quit()
