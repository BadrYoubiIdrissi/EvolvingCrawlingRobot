# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 11:26:04 2016

@author: Badr Youbi Idrissi
"""

import constants
import utilitaires as ut
from copy import deepcopy

class Espece():
    def __init__(self, archetype, espId, genCount):
        self.id = espId
        self.leader = archetype
        self.archetype = deepcopy(archetype)
        self.contenu = [archetype]
        self.best = [archetype]
        self.evolPrcnt = [0 for _ in range(genCount)]
        self._bestLastFitness = None
        self.age = 0
        self.stagnationAge = 0    
    def __repr__(self):
        s = "Espece"+ str(self.id) + " :"
        for i in self.contenu:
            s += (" " + str(i.id))
        s += "\nBest: "+ str(self.leader.id)
        s += "\nArchetype: "+ str(self.archetype.id)
        return s
        
    def __contains__(self, ind):
        return ind in self.contenu

    def add(self, ind):
        self.contenu.append(ind)
        if ind.rawFitness() > self.leader.rawFitness():
            self.leader = ind
    
    def size(self):
        return len(self.contenu)
    
    def flush(self):
        self.archetype = deepcopy(self.leader)
        self._bestLastFitness = self.leader.sharedFitness
        self.contenu = []
        self.age += 1
        
    def bestLastFitness(self):
        assert self._bestLastFitness != None, "Best last fitness not set"
        return self._bestLastFitness
        
    def stagnated(self):
        return self.leader.sharedFitness == self.bestLastFitness()
        
    def averageFitness(self):
        total = 0
        for ind in self.contenu:
            total += ind.sharedFitness
        return total/self.size()
        
    def averageRawFitness(self):
        total = 0
        for ind in self.contenu:
            total += ind.fitness
        return total/self.size()

        
    def ajusterFitness(self):
        if self.age > constants.speciation.ageThreshold:
            fitnessModify = constants.speciation.oldFitMod
        else:
            fitnessModify = constants.speciation.youngFitMod
        for ind in self.contenu:
            ind.sharedFitness = ind.rawFitness()*fitnessModify/self.size()
    
    def calculateBest(self):
        self.contenu.sort(key = lambda i : i.fitness, reverse = True)
        self.best = self.contenu[:int(constants.speciation.percentageBest*len(self.contenu))]
        
    def individu(self):
        return ut.randomPick(self.best)
        
    def parents(self):
        return ut.randomCoupleIf(self.best,self.best, lambda a, b: a == b)
          