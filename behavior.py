
class Behavior(object):
        def __init__(self,genome):
                self.separators = genome.separators
                self.vision = genome.vision
                self.memory = genome.memory
                self.actions = genome.actions
                self.heuristics = genome.heuristics

        #take some knowledge and return an action tuple based on behavior table
        def respond(self,knowledge):
