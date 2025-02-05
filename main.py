import pygame
import numpy
import node
import functions

fun = functions.functions()
fun.create_conections()

nodesA = fun.nodesA
nodesB = fun.nodesB
nodesC = fun.nodesC

for i in range(1, 9):
    print(nodesA[i].name)
    if nodesA[i].direita != None:
        print( 'direita: ' + nodesA[i].direita.name)
    if nodesA[i].esquerda != None:
        print( 'esquerda: ' + nodesA[i].esquerda.name)
    if nodesA[i].cima != None:
        print( 'cima: ' + nodesA[i].cima.name)
    if nodesA[i].baixo != None:
        print( 'baixo: ' + nodesA[i].baixo.name)
    print('')
    

for i in range(1, 9):
    print(nodesB[i].name)
    if nodesB[i].direita != None:
        print( 'direita: ' + nodesB[i].direita.name)
    if nodesB[i].esquerda != None:
        print( 'esquerda: ' + nodesB[i].esquerda.name)
    if nodesB[i].cima != None:
        print( 'cima: ' + nodesB[i].cima.name)
    if nodesB[i].baixo != None:
        print( 'baixo: ' + nodesB[i].baixo.name)
    print('')
    
for i in range(1, 9):
    print(nodesC[i].name)
    if nodesC[i].direita != None:
        print( 'direita: ' + nodesC[i].direita.name)
    if nodesC[i].esquerda != None:
        print( 'esquerda: ' + nodesC[i].esquerda.name)
    if nodesC[i].cima != None:
        print( 'cima: ' + nodesC[i].cima.name)
    if nodesC[i].baixo != None:
        print( 'baixo: ' + nodesC[i].baixo.name)
            



