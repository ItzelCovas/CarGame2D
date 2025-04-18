import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

#import random
import math
import numpy as np

class OpMat:
    def __init__(self):
        #Se inicializa las coordenadas de los vertices del cubo
        #matrices de transformación
        self.T = np.identity(3)
        self.R = np.identity(3)
        self.E = np.identity(3)
        self.A = np.identity(3)  
        
        self.stack = [] #pila para almacenar estados de transformación

    def translate(self, tx, ty):
        #aplicar TRASLACIÓN a la matriz A
        self.T = np.identity(3)
        self.T[0][2] = tx #coord de la matriz de trasLacioón T
        self.T[1][2] = ty
        self.A = self.A @ self.T #MULT DE MATRIZ para aplicar la traslación

        
    def scale(self, sx, sy):
        #aplicar ESCALADO a matriz A
        self.E = np.identity(3)
        self.E[0][0] = sx #coortdenadas de la matriz de escalado S
        self.E[1][1] = sy
        self.A = self.A @ self.E

        
    def rotate(self, deg):
        #aplicar ROTACIÓN en grados a matriz A
        self.R = np.identity(3)
        rad = np.radians(deg) #convierte grados a radianes
        self.R[0][0] = np.cos(rad)
        self.R[0][1] = -np.sin(rad) 
        self.R[1][0] = np.sin(rad)
        self.R[1][1] = np.cos(rad)
        self.A = self.A @ self.R

                
    # funcion que realiza la operacion A * p -> p'
    # se asume que points en un array de puntos, donde cada renglon
    # es una coordenada homogenea 2D de puntos [x, y, 1]
    def mult_Points(self, points): #PARAMETRO POR REFERENCIA = VALOR ORIG DESDE EL LLAMDO DE LA FUNCION
        for i in range(len(points)):  #recorre cada punto del array
            p = np.array([points[i][0], points[i][1], 1])  # Convierte el punto a coordenadas homogéneas
            p_transformed = self.A @ p  # Multiplica el punto por la matriz de transformación A
            points[i][0] = p_transformed[0]  # Actualiza X
            points[i][1] = p_transformed[1]  # Actualiza Y
    
    def loadId(self):
        #reestablece la matriz de transformación a la identidad
        self.A = np.identity(3)
        

    def push(self):
        self.stack.append(self.A.copy()) 

    
    def pop(self):
        if (self.stack): #Si la pila está vacía, no hace nada (evita errores)
            self.A = self.stack.pop()  #recupera la última matriz guardada

        
