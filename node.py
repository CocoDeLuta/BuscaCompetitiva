
class Node:
    name = None
    direita = None
    esquerda = None
    cima = None
    baixo = None

    def __init__(self, name=None, direita=None, esquerda=None, cima=None, baixo=None):
        self.name = name
        self.direita = direita
        self.esquerda = esquerda
        self.cima = cima
        self.baixo = baixo
        

    def __str__(self):
        return f'{self.direita.name} {self.esquerda.name} {self.cima.name} {self.baixo.name}'

    

    