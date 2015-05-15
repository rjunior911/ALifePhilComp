import functools
import random
from numpy import *
class World(object):
        def __init__(self,physics,life_conditions):
                self.time=0
                self.genome_names=[]
                self.genomes =self.seed_genomes()
                self.agent_names=[]
                self.agents=self.seed_agents() # a list of agent objects
                self.fittest =[]
                #physical constants
                self.size = physics["world size"]
                self.state = zeros(self.size) #initialized to zero energy using numpy array
                self.duration = physics["end of time"] #This may be unnecessary
                self.sunshine=physics["sunshine"]
                self.packet_size =physics["energy packet"]
                self.friction=physics["friction"]
                #life condition constants
                self.population=life_conditions["initial population"] #number of living agents
                self.biodiversity=life_conditions["initial biodiversity"] #biodiversity is the number of genomes in action
                self.max_population = life_conditions["max agents"]
                self.max_diversity = life_conditions["max diversity"]
                self.temperature=life_conditions["initial temp"]
                self.max_memory=life_conditions["max memory"]
                self.max_vision=life_conditions["max vision"]
                self.max_separators=life_conditions["max separators"]
                self.existence_cost=life_conditions["existence cost"]
                self.complexity_cost=life_conditions["complexity cost"]
                self.complexity_cost=life_conditions["absorption cost"]
                self.complexity_cost=life_conditions["defense cost"]
                self.complexity_cost=life_conditions["attack cost"]
                #perhaps cost of attack/defense/absorption
                self.reproduction_age=life_conditions["reproduction age"]
                self.reproduction_likelihood=life_conditions["reproduction likelihood"]
                self.mutation_rate=life_conditions["mutation rate"]
                self.response_permutation_rate = life_conditions["response permutation rate"]
                self.response_insertion_rate = life_conditions["response insertion rate"]
                self.response_deletion_rate = life_conditions["response deletion rate"]
                self.heuristics_deletion_rate = life_conditions["heuristics deletion rate"]
                self.heuristics_insertion_rate =life_conditions["heuristics insertion rate"]
                self.vision_mutation_rate = life_conditions["vision mutation rate"]
                self.memory_mutation_rate =life_conditions["memory mutation rate"]
                self.grace_period=life_conditions["grace period"] #time allotted to remain below required energy level before death

        #done
        def show(self):
                return self.state

        #DONE
        def sort_genomes(self):
                self.genomes=sorted(self.genomes,key=lambda genome:genome.fitness)

        def update(self):
                self.time += 1
                self.shine()
                state_changes = zeros(self.size)
                #retrieve actions
                actions = []
                for agent in self.agents:
                        #first update each agent's knowledge
                        local_info = relevant_data(agent)
                        agent.observe(local_info)
                        #then have each act accordingly
                        actions.append((agent.name,agent.position,agent.energy,agent.act()))
                #process actions
                fates = self.calculate_fates(actions)
                #update agents according to the results of all actions
                for agent in self.agents:
                        living = fates[agent.name]
                        if living:
                                agent.react(fates[agent.name])
                        else:
                               kill(agent) 
                self.repopulate()
                


        #DONE 
        def seed_agents(self):
                #take each seed genome, a random position, and the initial life energy
                agents = []
                for i in range(self.physics["initial population"]):
                        pos = random.randrange(self.physics["world size"])
                        #TODO (You are here)
                        name = create_agent_name()
                        a = Agent(name)
                        agents.append(a)
                return agents
        #DONE 
        def seed_genomes(self):
                #create 10 default genomes and mutate each once
                genomes = []
                for i in range(self.physics["initial_biodiversity"]):
                        #TODO
                        g = Genome()
                        genomes.append()
                return genomes


        def repopulate(self):
                for agent in self.agents:
                        if agent.age%self.reproduction_age == 0: 
                                r =random.random()
                                while r < reproduction_likelihood & agent.energy >= self.reproduction_energy:
                                        agent.energy-=self.reproduction_energy
                                        self.birth(agent.behavior.genome)
                                        r = random.random()


        #this is where all of the dynamics is coded (described in physics.txt)
        def calculate_fates(self,actions):
            #sort by position
            #active_positions is a dictionary of positions referring to lists of actor-action pairs
            fates = {}
            active_positions = {}
            for action in actions:
                    if action[1] not in active_positions:
                            active_positions[action[1]]= [(action[0],action[2])]
                    else:
                            active_positions[action[1]]= active_positions[action[1]].append((action[0],action[2]))
            for pos, acts in active_positions.items():
                    #TODO
                    #each needs to know about the results of the previous somehow
                    payouts = energy_allocate(acts)
                    movements = movement_calculate(acts)
                    living = death(acts)


        #Done
        def relevant_data(self, agent):
                pos= agent.position
                vis = agent.vision
                right = pos + vis
                left = pos - vis
                width = 2*vis
                size = self.size
                if width >=size:
                        return self.state
                else:
                        if left < 0:
                                return self.state[left:]+self.state[:right]
                        elif right > size:
                                r = right-size
                                return self.state[left:]+self.state[:r]
                        else:
                                return self.state[left:right]


        #DONE
        def create_agent_name(self):
                #use a random string
                name = "".join(random.choice(string.ascii_letters + string.digits) for i in range(self.name_size))
                while name in self.agent_names:
                        name = "".join(random.choice(string.ascii_letters + string.digits) for i in range(self.name_size))
                self.agent_names.append(name)
                return name
        def create_genome_name(self):
                #use a random string
                name = "".join(random.choice(string.ascii_letters + string.digits) for i in range(self.name_size))
                while name in self.genome_names:
                        name = "".join(random.choice(string.ascii_letters + string.digits) for i in range(self.name_size))
                self.genome_names.append(name)
                return name

        def energy_allocate(self,actions):
                #TODO

        def movement_calculate(self,actions):
                #TODO

        def birth(self, parent):
                name = self.create_agent_name()
                pos = random.choice(range(self.size))
                child = Agent(name,pos,parent.behavior.genome,reproduction_energy)
        def kill(self, agent):
                self.agent_names.remove(agent.name)
                agent.genome
                #TODO
                #somehow take into account the death in the fitness of its genome
                #maybe record

        #done
        def shine(self):
                dispersed = 0
                while dispersed <= self.sunshine:
                        pos = random.choice(range(self.size))
                        self.state[pos]+= self.energy_packet
                        dispersed += self.energy_packet


