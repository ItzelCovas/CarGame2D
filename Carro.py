import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math
import numpy as np

class Carro:
    def __init__(self, op, color, esc, pos, dir, grafo, n_dir, control):
        #Se inicializa las coordenadas de los vertices del coche
        self.points = np.array([
                        [-4.0,-2.0,1.0], [4.0,-2.0,1.0], [4.0,2.0,1.0], [-4.0,2.0,1.0], 
                        [-4.0,-4.0,1.0], [-2.0,-4.0,1.0], [-2.0,-3.0,1.0], [-4.0,-3.0,1.0],
                        [2.0, -4.0, 1.0], [4.0, -4.0, 1.0], [4.0, -3.0, 1.0], [2.0, -3.0, 1.0],
                        [2.0, 3.0, 1.0], [4.0,3.0,1.0], [4.0,4.0,1.0], [2.0,4.0,1.0], 
                        [-4.0, 3.0, 1.0], [-2.0, 3.0, 1.0], [-2.0, 4.0, 1.0], [-4.0, 4.0, 1.0]
                    ])
        
        self.opera = op
        self.n_dir = n_dir
        self.controlado = control
        self.yaGiro = False 
        self.speed = 1.0
        self.deg = 0.0
        self.deltadeg = 1.0
        self.color = color
        self.esc = esc * 0.8 #escala del carro
        self.pos = pos
        self.dir = dir
        self.count_deg = 0 #90: left, -90: right
        self.radio = math.sqrt((4.0 * esc)**2 + (2.0 * esc)**2) 
        self.colision = 0
        self.grafo = grafo

        self.dir_map = {
            1: [0, 1],   #arriba
            2: [1, 0],   #derecha
            3: [0, -1],  #abajo
            4: [-1, 0]   #izquierda
        }

        self.direction_angles = {
            1: 90,   
            2: 0,  
            3: 270,  
            4: 180   
        }
            
    def up(self):
        tx = self.pos[0] + self.dir[0] * self.speed
        ty = self.pos[1] + self.dir[1] * self.speed
        self.pos = (tx, ty)
        
    def down(self):
        tx = self.pos[0] - self.dir[0]
        ty = self.pos[1] - self.dir[1]
        self.pos = (tx, ty)
        
    def vueltaIzquierda(self, possible_directions):
        if ((self.n_dir == 2) and (1 in possible_directions)) or ((self.n_dir == 1) and (4 in possible_directions)) or ((self.n_dir == 4) and (3 in possible_directions)) or ((self.n_dir == 3) and (2 in possible_directions)):
            return True
        return False
    
    def vueltaDerecha(self, possible_directions):
        if ((self.n_dir == 2) and (3 in possible_directions)) or ((self.n_dir == 3) and (4 in possible_directions)) or ((self.n_dir == 4) and (1 in possible_directions)) or ((self.n_dir == 1) and (2 in possible_directions)):
            return True
        return False
        
    def setTurnLR(self, turn):
        if (turn == 1):  #izq
            self.count_deg = 90
            self.yaGiro = True
        if (turn == 0): #derecha
            self.count_deg = -90
            self.yaGiro = True
    
    def setColor(self, r, g, b):
        self.color[0] = r
        self.color[1] = g
        self.color[2] = b
    
    def salirNodo(self):
        self.up()
        self.up()
        self.up()
        self.up()
        self.up()

    def enNodo(self):
        for nodo in self.grafo.nodos.values():
            if np.array_equal(self.pos, nodo.posicion()):
                return nodo.nodo_id()
        return -1
    
    
    def update(self):
        if (self.count_deg > 0):
            self.deg += 1
            self.count_deg -= 1
        elif (self.count_deg < 0):
            self.deg -= 1
            self.count_deg += 1
        else:
            self.dir[0] = round(self.dir[0])
            self.dir[1] = round(self.dir[1])
            if (self.colision == 0 and self.count_deg == 0):
                if not self.controlado:
                    id_origen = self.enNodo()
                    if id_origen != -1 and not self.yaGiro:
                        self.yaGiro = True
                        num_destinos = len(self.grafo.nodos[id_origen].destinos)
                        ind_destino = random.randint(0, num_destinos - 1)
                        id_destino = self.grafo.nodos[id_origen].destinos[ind_destino]
                        dir_arista = self.grafo.aristas[(id_origen, id_destino)]
                        
                        
                        #turn logic
                        if self.n_dir == dir_arista:
                            self.up()  #seguir derecho
                        else:
                            # determinar si vulta der o izq 
                            if (dir_arista - self.n_dir) % 4 == 1:  #vuelta derecha
                                self.setTurnLR(0)
                            else:  # vuelta izq
                                self.setTurnLR(1)
                        
                            # actu. dirección usando dir_map
                            self.dir = self.dir_map[dir_arista]
                            self.n_dir = dir_arista
                            
                            self.deg = self.direction_angles[self.n_dir]
                            
                    else:
                        self.yaGiro = False
                        self.up()
    
                
    # def update(self):
    #     if (self.colision == 0):
    #         move = random.randint(1, 100)
    #         if move > 2 and move < 100:
    #             self.up()
    #         if move == 1:
    #             if (self.count_deg == 0):
    #                 self.setTurnLR(0)
    #         if move == 2:
    #             if (self.count_deg == 0):
    #                 self.setTurnLR(1)
    #         if (self.count_deg > 0):
    #             self.deg += 1
    #             self.count_deg -= 1
    #             self.dir[0] = (math.cos(math.radians(self.deg)))
    #             self.dir[1] = (math.sin(math.radians(self.deg)))
    #         if (self.count_deg < 0):
    #             self.deg -= 1
    #             self.count_deg += 1
    #             self.dir[0] = (math.cos(math.radians(self.deg)))
    #             self.dir[1] = (math.sin(math.radians(self.deg)))
        
        
        
    def render(self): 
        self.opera.push() #guardar estado de transformación
        pointsR = self.points.copy()
        self.update()
        self.opera.translate(self.pos[0], self.pos[1])
        
        if self.count_deg == 0:
            self.deg = self.direction_angles[self.n_dir]
        self.opera.rotate(self.deg) #e1
        
        self.opera.scale(self.esc, self.esc) #e3
        self.opera.mult_Points(pointsR)
        glColor3fv(self.color)
        
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        #Redibujan los rectangulos
        glBegin(GL_QUADS)
        
        glVertex2f(pointsR[0][0], pointsR[0][1])
        glVertex2f(pointsR[1][0], pointsR[1][1])
        glVertex2f(pointsR[2][0], pointsR[2][1])
        glVertex2f(pointsR[3][0], pointsR[3][1])
        glVertex2f(pointsR[4][0], pointsR[4][1])
        glVertex2f(pointsR[5][0], pointsR[5][1])
        glVertex2f(pointsR[6][0], pointsR[6][1])
        glVertex2f(pointsR[7][0], pointsR[7][1])
        glVertex2f(pointsR[8][0], pointsR[8][1])
        glVertex2f(pointsR[9][0], pointsR[9][1])
        glVertex2f(pointsR[10][0], pointsR[10][1])
        glVertex2f(pointsR[11][0], pointsR[11][1])
        glVertex2f(pointsR[12][0], pointsR[12][1])
        glVertex2f(pointsR[13][0], pointsR[13][1])
        glVertex2f(pointsR[14][0], pointsR[14][1])
        glVertex2f(pointsR[15][0], pointsR[15][1])
        glVertex2f(pointsR[16][0], pointsR[16][1])
        glVertex2f(pointsR[17][0], pointsR[17][1])
        glVertex2f(pointsR[18][0], pointsR[18][1])
        glVertex2f(pointsR[19][0], pointsR[19][1])
        glEnd()
        
        self.opera.pop()  #restaurar transformación
        
    def distEuc(self, pos_1, pos_2):
        return math.sqrt((pos_2[0] - pos_1[0])**2 + (pos_2[1] - pos_1[1])**2)
    
    def Colision(self, carro):
        new_pos = list(self.pos) 
        new_pos[0] += self.dir[0]
        new_pos[1] += self.dir[1]
        new_pos = tuple(new_pos)
        dist_centros = self.distEuc(new_pos, carro.pos) #distancia euclidiana
        #(umbral de colision)
        if (self.radio + carro.radio >= dist_centros) :
            self.colision = 1
        else:
            self.colision = 0
        
        