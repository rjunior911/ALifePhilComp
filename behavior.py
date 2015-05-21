import pdb
from genetics import *

class Behavior(object):
        def __init__(self,genome):
                self.separators = genome.separators
                self.vision = genome.vision
                self.memory = genome.memory
                self.responses = genome.responses
                self.heuristics = genome.heuristics
                #place keeps track of the last heuristic action performed
                self.place = 0
                self.h_length = len(self.heuristics)
                self.genome = genome

        #take some knowledge and return an response tuple based on behavior table
        #  knowledge is a (vision x memory)-matrix filled in with all avaliable information about energy levels
        def respond(self,knowledge):
                #Approach 1: keep lookup table ordered (decreasing) by complexity of response
                #Approach 2: randomly permute as part of mutations (going with this for now)
                #go with the first match to the knowledge
                #if there is no match resort to heuristics
                for resp in self.responses:
                        scenario = resp[0]
                        if matches(scenario,knowledge):
                                return resp[1]
                #print(self.heuristics)
                #print(self.place)
                response = self.heuristics[self.place]
                self.place += 1 
                self.place %= self.h_length
                return response


        #boolean function taking a scenario and determining whether or not it matches reality determined by knowledge
        #  where scenario is some list of coordinates and energy levels and knowledge is the matrix containing the real info
        def matches(scenario,knowledge):
                match = True
                #coordinates is a list (relative position, time in past, energy level) where a 0 time in the past is the current
                for coordinates in scenario:
                        anticipated_level= level(coordinates[2])
                        actual_level = level(knowledge[coordinates[0],coordinates[1]])
                        if anticipated_level != actual_level:
                                match = False
                return match

        #finds the energy level of a given cell based on the separators of the agent
        #done
        def level(self,energy):
                seps = self.separators
                #lev = -1 #default for unknown
                lev=0
                for sep in seps:
                        if sep <= energy:
                                lev += 1
                return lev
