from behavior import *
import random
import string
class Agent(object):

    #Each agent will have:
    #a name
    #a set of genes
    #a position
    #some knowledge about the environment
    #a quota for survival
    #an energy store
    #an identifier based on genome for visualization purposes
    #its generation

    #A genome (set of genes) will contain the following information:
        #number of energy separators
        #positions of separators on energy continuum (in sorted order)
        #vision range
        #memory range
        #determined actions table
            #knowledge are lists of data with coordinates given by (relative position, depth into past, energy coordinate)
            #every action is a sequence of coordinates each corresponding to a piece of knowledge and an action to perform
                #possible actions are:
                    #move left or right n steps; cost of movement proportional to energy stored
                    #defend with n (later versions)
                    #spend n to absorb:

                    #attack with n (later versions)
        #a sequence of heuristic actions to take in the event that action is not determined by knowledge
    def __init__(self,name,position,genome=Genome(),energy=50,knowledge=[]):
        #At the moment the behavior class is a needless composition but perhaps later it will leave room for gene expression
        self.behavior = Behavior(genome)
        genome.instantiations +=1
        genome.living_instantiations +=1
        self.position = position
        self.energy = energy
        self.knowledge = knowledge
        self.age = 0
        self.name = name
        self.danger = 0
        self.generation = genome.generation



    #returns a tuple of coordinate-energies and an agent-action 4-tuple
    def act(self):
        action = self.behavior.respond(self.knowledge)
        self.age += 1
        return action

        #else:
            #return None

    def react(self,fate):
            new_energy = fate[0]
            movement = fate[1]
            self.position += movement
            self.energy = new_energy
    #done
    def observe(self,data):
        self.knowledge=[data.insert(self.behavior.vision,self.energy)]+ self.knowledge
        if len(self.knowledge) > self.behavior.memory:
            self.knowledge.pop()

    def show(self):
        #TODO This may have to return instead of print
        print "Name:\t"+self.name
        print "Age at death:\t"+str(self.age)
        print "Generation:"+str(self.generation)
        print "Vis, Mem:\t"+str(self.behavior.vision)+"\t"+str(self.behavior.memory)
        print "Separators:\t"+"\t".join(map(str,self.behavior.separators))
        print "Heuristics:"
        for heuristic in self.behavior.heuristics:
            print str(heuristic)
        print "Responses:"
        for response in self.behavior.responses:
            print str(response)

    #the world determines the allocation of energy, the resulting positions and the life or death of each agent.
    #a fate tuple consists of
        #alive or dead bit
        #energy payout
        #new position
