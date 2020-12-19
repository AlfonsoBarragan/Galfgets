import copy 
import time
import pygame
import numpy as np


# Juego de la vida

pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 25, 25

dimCW = width / nxC
dimCH = height / nyC

gameState = np.zeros((nxC, nyC))
newGameState = copy.deepcopy(gameState)


pauseExect = False

while True:
    
    ev = pygame.event.get()
    
    for event in ev:
        
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
            
        mouseClick = pygame.mouse.get_pressed()
        
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW), np.floor(posY / dimCH))
            
            newGameState[celX, celY] = not mouseClick[2]
                
    
    for y in range(0, nxC):
        for x in range(0, nyC):
            
            if not pauseExect:
                screen.fill(bg)
                time.sleep(0.1)
                
                newGameState = copy.deepcopy(gameState)
                
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC]   + \
                          gameState[(x) % nxC,   (y-1) % nyC]   + \
                          gameState[(x+1) % nxC, (y-1) % nyC]   + \
                          gameState[(x-1) % nxC, (y) % nyC]     + \
                          gameState[(x+1) % nxC, (y) % nyC]     + \
                          gameState[(x-1) % nxC, (y+1) % nyC]   + \
                          gameState[(x) % nxC,   (y+1) % nyC]   + \
                          gameState[(x+1) % nxC, (y+1) % nyC]
               
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x,y] = 1
                
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x,y] = 0
                    
                    
                poly = [((x) * dimCW, y * dimCH),
                        ((x+1) * dimCW, y * dimCH),
                        ((x+1) * dimCW, (y+1) * dimCH),
                        ((x) * dimCW, (y+1) * dimCH)]
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
    
                if newGameState[x, y] == 0:
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
                else:
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0)
                    
                gameState = copy.deepcopy(newGameState)
                
    pygame.display.flip()