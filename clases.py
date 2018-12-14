import pygame, random
import funciones

# Variables
imgs_basura = ["lata.gif","organico.gif","organico1.gif","organico2.gif","organico3.gif","otros.gif","papel.gif","toxico.gif","vidrio.gif"]
imgs_basura_organica = ["organico.gif","organico1.gif","organico2.gif","organico3.gif"]
cont_txt_residuos = 0

area_permitida = 285 # Luego de esta posicion en pantalla, la zona es permitida
puntos = 0 # Aca se acumulan los puntos del jugador
puntos_sumados = 0 # Se guarda cuantos puntos se suman al recolectar una basura

# Esta clase crea las collisiones que el jugador no podra traspasar (Autos y centro del escenatio en modo por tiempo)
class Walls:
    def __init__(self, walls, cantidad, posiciones, tamanos):
        for i in range(cantidad):
            self.rect = pygame.Rect((posiciones[i]), (tamanos[i]))
            walls.append(self.rect)

class Baureros_mExtra:
    def __init__(self, basureros, cantidad, posiciones, tamanos):
        for i in range(cantidad):
            self.rect = pygame.Rect((posiciones[i]), (tamanos[i]))
            basureros.append(self.rect)

# Clases
class Player:
    
    def __init__(self,pos_inicial, tamano, path):
        self.path = path
        self.pos_inicial = pos_inicial
        self.player_img = funciones.Imagen(str(self.path)+str("/images/player_right.png"), True) # La imagen inicial va a ser "player_right" (mirando a la derecha)
        self.tamano = tamano
        self.player_img = pygame.transform.scale(self.player_img, tamano) # Se asigna el tamano inicial del jugador
        self.rect = self.player_img.get_rect()
        self.rect.topleft = pos_inicial # Se lo coloca en la posicion inicial
        self.basureros_encontrados = 0
        
        # En las siguientes dos lineas se definen las variables que definiran para donde se mueve el jugador
        self.p_right = self.p_down = self.p_left = self.p_up = False

    # Collisiones del jugador con la basura
    def Collisiones(self, bas, estado, organico, sonido_w, sonido_l, basureros):
        global puntos, cont_txt_residuos, puntos_sumados

        # Se comprueba si se esta jugando y si la basura fue recolectada en un area "permitida"        
        if(self.rect.colliderect(bas.rect) and (estado == "jugando_portiempo" or estado == "jugando_porpuntos")):
            if(bas.rect.left > area_permitida or organico):
                sonido_w.stop()
                sonido_w.play()
                if(bas.tipo_bas == "papel.gif"):
                    puntos += 30
                    puntos_sumados = 30
                    cont_txt_residuos = 3
                    bas.colocada = False
                    bas.movimiento_asignado = False
                elif(bas.tipo_bas == "lata.gif"):
                    puntos += 50
                    puntos_sumados = 50
                    cont_txt_residuos = 3
                    bas.colocada = False
                    bas.movimiento_asignado = False
                elif(bas.tipo_bas == "vidrio.gif"):
                    puntos += 75
                    puntos_sumados = 75
                    cont_txt_residuos = 3
                    bas.colocada = False
                    bas.movimiento_asignado = False
                elif(bas.tipo_bas == "toxico.gif"):
                    puntos += 150
                    puntos_sumados = 150
                    cont_txt_residuos = 3
                    bas.colocada = False
                    bas.movimiento_asignado = False
                elif(bas.tipo_bas == "organico.gif" or bas.tipo_bas == "organico1.gif" or bas.tipo_bas == "organico2.gif" or
                     bas.tipo_bas == "organico3.gif"):
                    puntos += 200
                    puntos_sumados = 200
                    cont_txt_residuos = 3
                    bas.colocada = False
                    bas.movimiento_asignado = False
                elif(bas.tipo_bas == "otros.gif"):
                    puntos += 10
                    puntos_sumados = 10
                    cont_txt_residuos = 3
                    bas.colocada = False
                    bas.movimiento_asignado = False

            # Si la basura se recolectada en una zona "prohibida" se restan puntos
            elif(bas.rect.left <= 285):
                bas.colocada = False
                bas.movimiento_asignado = False
                sonido_l.stop()
                sonido_l.play()
                puntos -= 50
                cont_txt_residuos = 3
                if(puntos < 0):
                    puntos_sumados = -1
                    puntos = 0
                else:
                    puntos_sumados = -50
        if((estado == "jugando_modo_extra")):
            for b in basureros:
                if(self.rect.colliderect(b)):
                    basureros.remove(b)
                    self.basureros_encontrados += 1
                    sonido_w.stop()
                    sonido_w.play()

    # Movimiento del jugador
    def Mover_en_eje(self, x, y, w, estado):
        self.rect.left += x
        self.rect.top += y

        if(estado == "jugando_portiempo" or estado == "jugando_modo_extra" or estado == "jugando_porpuntos"):
            for wall in w:
                if(self.rect.colliderect(wall)):
                    if(x > 0):
                        self.rect.right = wall.left
                    if(x < 0):
                        self.rect.left = wall.right
                    if(y > 0):
                        self.rect.bottom = wall.top
                    if(y < 0):
                        self.rect.top = wall.bottom
        
    def Mover(self, x, y, walls, estado_juego):
        if(x != 0):
            self.Mover_en_eje(x, 0, walls, estado_juego)
        if(y != 0):
            self.Mover_en_eje(0, y, walls, estado_juego)

    def Set_image(self, img):
        self.player_img = funciones.Imagen(str(self.path)+str("/images/")+str(img), True)
        self.player_img = pygame.transform.scale(self.player_img, self.tamano) # Se asigna el tamano del jugador

    # En esta funcion se le asigna la imagen correcta al jugador segun su movimiento
    def Sprite_Control(self):

        if(self.p_right and (self.p_left == False and self.p_up == False and self.p_down == False)):
            self.Set_image("player_right.png")
        elif(self.p_right and self.p_down and (self.p_left == False and self.p_up == False)):
            self.Set_image("player_right_down.png")
        elif(self.p_right and self.p_up and (self.p_left == False and self.p_down == False)):
            self.Set_image("player_right_up.png")
        elif(self.p_left and (self.p_right == False and self.p_up == False and self.p_down == False)):
            self.Set_image("player_left.png")
        elif(self.p_left and self.p_down and (self.p_right == False and self.p_up == False)):
            self.Set_image("player_left_down.png")
        elif(self.p_left and self.p_up and (self.p_right == False and self.p_down == False)):
            self.Set_image("player_left_up.png")
        elif(self.p_up and (self.p_right == False and self.p_left == False and self.p_down == False)):
            self.Set_image("player_up.png")
        elif(self.p_down and (self.p_right == False and self.p_left == False and self.p_up == False)):
            self.Set_image("player_down.png")


class Basura:

    def __init__(self, min_pos, max_pos, path):
        self.path = path
        self.min_pos = min_pos
        self.max_pos = max_pos
        self.tipo_bas = random.choice(imgs_basura_organica)
        self.basura_img = funciones.Imagen(str(self.path)+str("/images/")+str(self.tipo_bas), True)
        self.rect = self.basura_img.get_rect()
        self.rect.topleft = (random.randint(self.min_pos[0], self.max_pos[0]), random.randint(self.min_pos[1], self.max_pos[1]))

        self.min_pos = min_pos
        self.max_pos = max_pos
        self.colocada = True
        self.movimiento_asignado = True
        self.movimientos = ["lineal","aleatorio"]
        self.tipo_movimiento = "aleatorio"
        self.pos_objetivo = (0, 0)

    def Reasignar_basura(self, organico):
        if(organico):
            self.tipo_bas = random.choice(imgs_basura_organica)
        else:
            self.tipo_bas = random.choice(imgs_basura)
        self.basura_img = funciones.Imagen(str(self.path)+str("/images/")+str(self.tipo_bas), True)
        self.rect.topleft = (random.randint(self.min_pos[0], self.max_pos[0]), random.randint(self.min_pos[1], self.max_pos[1]))

    def Reasignar_limites(self,minim, maxim):
        self.max_pos = maxim
        self.min_pos = minim
    
    def Mover_colocar(self, org):
        if(not self.colocada):
            self.Reasignar_basura(org)
            self.colocada = True
        if(self.colocada and (not self.movimiento_asignado or self.pos_objetivo == (0,0))):
            self.tipo_movimiento = random.choice(self.movimientos)
            self.movimiento_asignado = True
            if(self.tipo_movimiento == "lineal"):
                self.pos_objetivo = (random.randint(-1,1), random.randint(-1,1))
            else:
                self.pos_objetivo = (random.randint(self.min_pos[0],self.max_pos[0]), random.randint(self.min_pos[1],self.max_pos[1]))
        if(self.tipo_movimiento == "lineal"):
            self.rect.left += self.pos_objetivo[0]
            self.rect.top += self.pos_objetivo[1]
            if(self.rect.right >= self.max_pos[0]):
                self.rect.right = self.max_pos[0] - 10
                self.movimiento_asignado = False
            elif(self.rect.left <= self.min_pos[0]):
                self.rect.left = self.min_pos[0] + 10
                self.pos_objetivo = (2, self.pos_objetivo[1])
            if(self.rect.top <= self.min_pos[1]):
                self.rect.top = self.min_pos[1] + 10
                self.pos_objetivo = (self.pos_objetivo[0], 2)
            elif(self.rect.bottom >= self.max_pos[1]):
                self.rect.bottom = self.max_pos[1] - 10
                self.movimiento_asignado = False
        elif(self.tipo_movimiento == "aleatorio"):

            if(self.rect.topleft != self.pos_objetivo):
                if(self.rect.left > self.pos_objetivo[0]):
                    self.rect.left -= 1
                elif(self.rect.left < self.pos_objetivo[0]):
                    self.rect.left += 1
                if(self.rect.top > self.pos_objetivo[1]):
                    self.rect.top -= 1
                elif(self.rect.top < self.pos_objetivo[1]):
                    if(self.rect < self.max_pos[1]):
                        self.rect.top += 1
                    else:
                        self.movimiento_asignado = False
            else:
                self.movimiento_asignado = False

            








                
