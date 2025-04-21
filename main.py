import pygame
from pygame.locals import *
import numpy as np
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import sys
sys.path.append('..')

from OpMat import OpMat
from Carro import Carro
from StreetMap import *

opera = OpMat() #REGRESA UN APUNTADOR -> DIR DE MEMORIA DEL OBJETO

carros = []
#ncarros = 6

pygame.init()

screen_width = 900
screen_height = 600

#Variables para dibujar los ejes del sistema
X_MIN=-450
X_MAX=450
Y_MIN=-300
Y_MAX=300

#variable global control
deg = 0.0
deg1 = 0.0

degrot = 0.0
delta_degrot = 10.0

PINK = (1.0, 0.6, 0.8)
WHITE = (1.0, 1.0, 1.0)

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(5.0)
    #X axis in black
    glColor3f(0.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in black
    glColor3f(0.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    glLineWidth(1.0)
    
screen = pygame.display.set_mode(
    (screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("OpenGL: MapaCarros 2D")

def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-450,450,-300,300)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0,0,0,0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
def InitGrafo():
    graph = Grafo(screen_width, screen_height)
    
    graph.new_nodo(-400, 250)  # 0 - esquina sup izq
    graph.new_nodo(-200, 250)  # 1 - derecha del 0
    graph.new_nodo(0, 250)     # 2 - derecha del 1
    graph.new_nodo(200, 250)   # 3
    graph.new_nodo(400, 250)   # 4

    graph.new_nodo(-400, 0)    # 5 izq medio
    graph.new_nodo(-200, 0)    # 6 derecha de 5
    graph.new_nodo(0, 0)       # 7
    graph.new_nodo(200, 0)     # 8
    graph.new_nodo(400, 0)     # 9

    graph.new_nodo(-400, -250) # 10 esquina inf izq
    graph.new_nodo(-200, -250) # 11
    graph.new_nodo(0, -250)    # 12
    graph.new_nodo(200, -250)  # 13
    graph.new_nodo(400, -250)  # 14
    
    
    #ARISTAS    
    #arriba
    graph.new_arista(0, 1, 2)  #derecha
    graph.new_arista(1, 0, 4)  #izq
    graph.new_arista(1, 2, 2)
    graph.new_arista(2, 1, 4)
    graph.new_arista(2, 3, 2)
    graph.new_arista(3, 2, 4)
    graph.new_arista(3, 4, 2)
    graph.new_arista(4, 3, 4)

    #en medio 
    graph.new_arista(5, 6, 2)
    graph.new_arista(6, 5, 4)
    graph.new_arista(6, 7, 2)
    graph.new_arista(7, 6, 4)
    graph.new_arista(7, 8, 2) 
    graph.new_arista(8, 7, 4)
    graph.new_arista(8, 9, 2)
    graph.new_arista(9, 8, 4)

    #abajo 
    graph.new_arista(10, 11, 2)
    graph.new_arista(11, 10, 4)
    graph.new_arista(11, 12, 2)
    graph.new_arista(12, 11, 4)
    graph.new_arista(12, 13, 2)
    graph.new_arista(13, 12, 4)
    graph.new_arista(13, 14, 2)
    graph.new_arista(14, 13, 4)
    
    for i in range(5):
        graph.new_arista(i, i+5, 3)   #arriba to middle
        graph.new_arista(i+5, i, 1)   #middle to arriba (reversa
        graph.new_arista(i+5, i+10, 3) #middle to abajo
        graph.new_arista(i+10, i+5, 1) #abajo to middle
    
    
    return graph

def InitRobots(grafo):      
    carros.append(Carro(opera,[0.6, 0.2, 0.8],7,[-350,250],[1,0], grafo, 2, False)) #0
    carros.append(Carro(opera,[0.6, 0.2, 0.8],7,[-50,250],[1,0], grafo, 4, False)) #1
    
    carros.append(Carro(opera,[0.6, 0.2, 0.8],7,[350,0],[-1,0], grafo, 2, False)) #2
    
    carros.append(Carro(opera,[0.6, 0.2, 0.8],7,[-250,-250],[1,0], grafo, 2, False)) #3
    
    carros.append(Carro(opera,[0.6, 0.2, 0.8],7,[-400,50],[0,-1], grafo, 4, False)) #4
    
    carros.append(Carro(opera,[0.6, 0.2, 0.8],7,[250,-250],[1,0], grafo, 3, False)) #5
    
    carros.append(Carro(opera,[0.6, 0.2, 0.8],7,[350,250],[-1,0], grafo, 4, False)) #6
    
    carros.append(Carro(opera,[0.6, 0.2, 0.8],7,[400,-200],[0,1], grafo, 2, False)) #7
    
    carros.append(Carro(opera,[0.6, 0.2, 0.8],7,[150,0],[-1,0], grafo, 4, False)) #8
    
    carros.append(Carro(opera,[0.6, 0.2, 0.8],7,[200,200],[0,-1], grafo, 1, False)) #9


def display():
    for c1 in carros:
        for c2 in carros:
            if (c1 != c2):
                c1.Colision(c2)
                if c1.colision == True:
                    break
        
    for carrito in carros:
        carrito.render()
    c1.render()

#main PROGRAM
init()
graph = InitGrafo()
InitRobots(graph)
opera.loadId()
c1 = Carro(opera, [1.0,0.0,0.5], 7, [0, -250], [-1.0, 0.0], graph, 4, True)
carros.append(c1)

done = False
while not done:
    nodo_presente = c1.enNodo()
    keys = pygame.key.get_pressed()
    
    if c1.colision == 0 and c1.count_deg == 0:
        if nodo_presente != -1:
            destinos = graph.nodos[nodo_presente].destinos
            direcciones = []
            for dest in destinos:
                posible_dir = graph.aristas[(nodo_presente, dest)]
                direcciones.append(posible_dir)
                print(c1.vueltaDerecha(direcciones))
                
            if keys[pygame.K_LEFT] and c1.vueltaIzquierda(direcciones):
                c1.setTurnLR(1)
                if (c1.dir[0] == 1):
                    c1.dir = [0, 1]
                    c1.n_dir = 1
                elif (c1.dir[1] == 1) :
                    c1.dir = [-1, 0]
                    c1.n_dir = 4
                elif (c1.dir[0] == -1) :
                    c1.dir = [0, -1]
                    c1.n_dir = 3
                else:
                    c1.dir = [1, 0]
                    c1.n_dir = 2
                c1.up()
                
            if keys[pygame.K_RIGHT] and c1.vueltaDerecha(direcciones):
                c1.setTurnLR(0)
                if (c1.dir[0] == 1):
                    c1.dir = [0, -1]
                    c1.n_dir = 3
                elif (c1.dir[1] == -1) :
                    c1.dir = [-1, 0]
                    c1.n_dir = 4
                elif (c1.dir[0] == -1) :
                    c1.dir = [0, 1]
                    c1.n_dir = 1
                else:
                    c1.dir = [1, 0]
                    c1.n_dir = 2
                c1.up()
                
            if keys[pygame.K_UP] and (c1.n_dir in direcciones):
                c1.up()
        else:
            c1.up()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    glClear(GL_COLOR_BUFFER_BIT)
    Axis()
    graph.render()
    display()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()