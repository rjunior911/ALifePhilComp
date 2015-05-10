import behavior.py
class Agent(object):

    #Each agent will have:
    #a set of genes
    #a position
    #some knowledge
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
            #every action is a number corresponding to a piece of knowledge and an action to perform
                #possible actions are:
                    #move left or right n steps; cost of movement proportional to energy stored
                    #defend with n (later versions)
                    #spend n to absorb:
                        
                    #attack with n (later versions)
        #a sequence of heuristic actions to take in the event that action is not determined by knowledge

    def __init__(self,genome=None,generation=0,position=None,energy=None,knowledge=None):
        #At the moment the behavior class is a needless composition but perhaps later it will leave room for gene expression
        self.behavior = Behavior(genome)
        self.position = position
        self.energy = energy
        self.knowledge = knowledge
        self.living =1
        self.age = 0
        self.name = genome.name

    #def create_name(genome):
        ##TODO
        ##figure out a hash scheme


    def act(self):
        if self.living != 0:
            action = self.behavior.respond(self.knowledge)
            self.age += 1
            return action
        else:
            return None

    #the world determines the allocation of energy, the resulting positions and the life or death of each agent.
    #a fate tuple consists of
        #alive or dead bit
        #energy payout
        #new position

    def react(self,fate):
        if fate[0]!=0:
            energy_gained = fate[1]
            movement = fate[2]
            self.position += movement
            self.energy += energy_gained
        else:
            self.living = 0
        

    #def __del__(self):
        #record a summary of the life of this agent
            #identifier
            #age at death
            #energy at death
            #complexity estimate
        #summary = [self.name,self.age,complexity_estimate()]



