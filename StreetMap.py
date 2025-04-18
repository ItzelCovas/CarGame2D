from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import math
import random

# MAPA GRAFOS

class Nodo:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y 
        self.id = id
        self.destinos = []
        
    def posicion(self):
        return np.array([self.x , self.y])
    
    def nodo_id(self):
        return self.id
    
WHITE = (0.5, 0.5, 0.5)

class Grafo:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nodos = {}
        self.aristas = {}
    
    def new_nodo(self, x, y):
        id = len(self.nodos)
        self.nodos[id] = Nodo(x, y, id)
        
    def new_arista(self, nodo_origen, nodo_destino, dir):
        if nodo_origen in self.nodos and nodo_destino in self.nodos:
            self.aristas[(nodo_origen, nodo_destino)] = dir
            self.nodos[nodo_origen].destinos.append(nodo_destino)
    
    def posicion(self, id):
        return self.nodos[id].posicion()
    
    def render(self):
        offset = 28
        glPointSize(30.0)
        glColor3f(0.25, 0.25, 0.25)  #GRAY nodos
        glBegin(GL_POINTS)
        for node_id, node in self.nodos.items():
            glVertex2f(node.x, node.y)
        glEnd()
        
        # Render edges
        glColor3f(1.0, 1.0, 1.0)  # WHITE edges
        glLineWidth(2.0)
        glBegin(GL_LINES)
        for nodo_origen, nodo_destino in self.aristas:
            origen = self.nodos[nodo_origen]
            destino = self.nodos[nodo_destino]
            glVertex2f(origen.x, origen.y)
            glVertex2f(destino.x, destino.y)
        glEnd()


