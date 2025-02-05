import node
import pygame
import numpy

class functions:
      
    nodesA = [None] * 9
    nodesB = [None] * 9
    nodesC =  [None] * 9 
    
    def __init__(self):
        pass
        
        
    
    def create_conections(self):  
      
        for i in range(0, 9):
            self.nodesA[i] = node.Node(name='A' + str(i))
            self.nodesB[i] = node.Node(name='B' + str(i))
            self.nodesC[i] = node.Node(name='C' + str(i))
            
        # ligando os nos aos vizinhos
        # camada de fora A
        self.nodesA[1].direita = self.nodesA[2]
        self.nodesA[1].baixo = self.nodesA[8]

        self.nodesA[2].direita = self.nodesA[3]
        self.nodesA[2].esquerda = self.nodesA[1]
        self.nodesA[2].baixo = self.nodesB[2]

        self.nodesA[3].esquerda = self.nodesA[2]
        self.nodesA[3].baixo = self.nodesA[4]

        self.nodesA[4].cima = self.nodesA[3]
        self.nodesA[4].esquerda = self.nodesB[4]
        self.nodesA[4].baixo = self.nodesA[5]

        self.nodesA[5].cima = self.nodesA[4]
        self.nodesA[5].esquerda = self.nodesA[6]
        
        self.nodesA[6].direita = self.nodesA[5]
        self.nodesA[6].cima = self.nodesB[6]
        self.nodesA[6].esquerda = self.nodesA[7]
        
        self.nodesA[7].direita = self.nodesA[6]
        self.nodesA[7].cima = self.nodesA[8]
        
        self.nodesA[8].cima = self.nodesA[1]
        self.nodesA[8].baixo = self.nodesA[7]
        self.nodesA[8].direita = self.nodesB[8]
        
        # camada do meio B
        self.nodesB[1].direita = self.nodesB[2]
        self.nodesB[1].baixo = self.nodesB[8]
        
        self.nodesB[2].direita = self.nodesB[3]
        self.nodesB[2].esquerda = self.nodesB[1]
        self.nodesB[2].baixo = self.nodesC[2]
        self.nodesB[2].cima = self.nodesA[2]
        
        self.nodesB[3].esquerda = self.nodesB[2]
        self.nodesB[3].baixo = self.nodesB[4]
        
        self.nodesB[4].cima = self.nodesB[3]
        self.nodesB[4].esquerda = self.nodesC[4]
        self.nodesB[4].baixo = self.nodesB[5]
        self.nodesB[4].direita = self.nodesA[4]
        
        self.nodesB[5].cima = self.nodesB[4]
        self.nodesB[5].esquerda = self.nodesB[6]
        
        self.nodesB[6].direita = self.nodesB[5]
        self.nodesB[6].cima = self.nodesC[6]
        self.nodesB[6].esquerda = self.nodesB[7]
        self.nodesB[6].baixo = self.nodesA[6]
        
        self.nodesB[7].direita = self.nodesB[6]
        self.nodesB[7].cima = self.nodesB[8]
        
        self.nodesB[8].cima = self.nodesB[1]
        self.nodesB[8].baixo = self.nodesB[7]
        self.nodesB[8].direita = self.nodesC[8]
        self.nodesB[8].esquerda = self.nodesA[8]
        
        # camada de dentro C
        self.nodesC[1].direita = self.nodesC[2]
        self.nodesC[1].baixo = self.nodesC[8]
        
        self.nodesC[2].direita = self.nodesC[3]
        self.nodesC[2].esquerda = self.nodesC[1]
        self.nodesC[2].cima = self.nodesB[2]
        
        self.nodesC[3].esquerda = self.nodesC[2]
        self.nodesC[3].baixo = self.nodesC[4]
        
        self.nodesC[4].cima = self.nodesC[3]
        self.nodesC[4].direita = self.nodesB[4]
        self.nodesC[4].baixo = self.nodesC[5]
        
        self.nodesC[5].cima = self.nodesC[4]
        self.nodesC[5].esquerda = self.nodesC[6]
        
        self.nodesC[6].direita = self.nodesC[5]
        self.nodesC[6].baixo = self.nodesB[6]
        self.nodesC[6].esquerda = self.nodesC[7]
        
        self.nodesC[7].direita = self.nodesC[6]
        self.nodesC[7].cima = self.nodesC[8]
        
        self.nodesC[8].cima = self.nodesC[1]
        self.nodesC[8].baixo = self.nodesC[7]
        self.nodesC[8].esquerda = self.nodesB[8]