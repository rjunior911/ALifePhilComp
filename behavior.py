#done for now
from genetics import *

class Behavior(object):
        #TODO Allow for more advanced handling of multiple responses to the same scenario:
            #1) cycle through them in order
            #2) prune them out
        def __init__(self,genome):
                self.separators = genome.separators
                self.vision = genome.vision
                self.memory = genome.memory
                self.responses = genome.responses
                self.heuristics = genome.heuristics
                #place keeps track of the last heuristic action performed
                self.place = 0
                #self.h_length = len(self.heuristics)
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
                        if matches(scenario,knowledge,self.separators):
                                return resp[1]
                #TODO Check if responses conflict with amount of memory/vision i.e. is pruning working properly?
                self.place %= len(self.heuristics)
                response = self.heuristics[self.place]
                self.place += 1
                return response

        #finds the energy level of a given cell based on the separators of the agent
        #done
def level(separators,energy):
                #lev = -1 #default for unknown
                #Problem D HERE
                lev=0
                for sep in separators:
                        if sep <= energy:
                                lev += 1
                return lev

        #boolean function taking a scenario and determining whether or not it matches reality determined by knowledge
        #  where scenario is some list of coordinates and energy levels and knowledge is the matrix containing the real info
def matches(scenario,knowledge,separators):
        #TODO This is all messed up:
            #when the vision of an agent exceeds the size of the world, the position of the agent's state is no longer centered
        match = True
        #coordinates is a list (relative position, time in past, energy level) where a 0 time in the past is the current
        #scenario is a list of (pos,mem,level) triples
        for coordinates in scenario:
                if coordinates[1]>=len(knowledge):
                    #In the case where the memory is 0 the configuration always has a negative level as a flag
                    return False
                local_state = knowledge[coordinates[1]]
                index = coordinates[0]+((len(local_state)-1)/2)
                if index >= len(local_state) or index < 0:
                    return False
                energy = local_state[index]
                actual_level = level(separators,energy)
                anticipated_level= level(separators,coordinates[2])
                if anticipated_level != actual_level:
                        match = False
        return match
