# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 00:33:13 2017

@author: byoub
"""

import vrep
from pygame.locals import *
from individu import Individu
from population import Population
import utilitaires as ut
from math import pi

print ('Program started')
pop = Population(10, 3, 2)
pop.generer()
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP

if clientID != -1:
    vrep.simxSynchronous(clientID, True)
    mot1 = []
    mot2 = []
    cores = []
    for i in range(10):
        error, tempmot1 = vrep.simxGetObjectHandle(clientID, 'Motor1#'+str(i), vrep.simx_opmode_blocking)
        error, tempmot2 = vrep.simxGetObjectHandle(clientID, 'Motor2#'+str(i), vrep.simx_opmode_blocking)
        error, tempcore = vrep.simxGetObjectHandle(clientID, 'Core#'+str(i), vrep.simx_opmode_blocking)
        mot1.append(tempmot1)
        mot2.append(tempmot2)
        cores.append(tempcore)
    for i in range(5):
        print("Generation ",i)
        pop.evoluer(clientID,mot1,mot2,cores)
    
else:
    print ('Failed connecting to remote API server')