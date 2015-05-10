import functools
import random
Class World(object):
        def __init__(self,physics):
                self.time=0
                self.genomes =seed_genomes()
                self.genomes=sorted(self.genomes,key=lambda genome:genome.fitness)
                self.agents=seed_agents()
                self.agents=sorted(self.agents,key=lambda agent:agent.position)
                self.physics=physics
                self.fittest =[]

        def show(self):

        def update(self):
                self.time += 1
                actions = []
                for agent in self.agents:
                        actions.append(agent.act())
                        fates = calculate_fates(actions)

        def seed_agents(self):
                #take each seed genome, a random position, and the initial life energy
                agents = []
                for i in range(self.physics["initial population"]):
                        pos = random.randrange(self.physics["world size"])
                        #TODO (You are here)
                        a = Agent()
                        agents.append()
                return agents



        def seed_genomes(self):
                #create 10 default genomes and mutate each once
                genomes = []
                for i in range(self.physics["initial_biodiversity"]):
                        #TODO
                        g = Genome()
                        genomes.append()
                return genomes



        #this is where all of the dynamics is coded
        def calculate_fates(self,actions)
