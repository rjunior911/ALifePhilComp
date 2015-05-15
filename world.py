import pdb
import functools
import random
#from numpy import *
from agents import *
from genetics import *
class World(object):
        #done
        def __init__(self,physics,life_conditions):
                self.time=0
                self.life_conditions=life_conditions

                #physical constants
                self.size = physics["world size"]
                self.state = [0 for i in range(self.size)]
                self.duration = physics["end of time"] #This may be unnecessary
                self.sunshine=physics["sunshine"]
                self.energy_packet =physics["energy packet"]
                self.friction=physics["friction"]
                #life condition constants
                #self.population=life_conditions["initial population"] number of living agents
                #self.biodiversity=life_conditions["initial biodiversity"] biodiversity is the number of genomes in action
                #self.max_population = life_conditions["max agents"]
                #self.max_diversity = life_conditions["max diversity"]
                #self.temperature=life_conditions["initial temp"]
                #self.max_memory=life_conditions["max memory"]
                #self.max_vision=life_conditions["max vision"]
                #self.max_separators=life_conditions["max separators"]
                #self.existence_cost=life_conditions["existence cost"]
                #self.complexity_cost=life_conditions["complexity cost"]
                self.absorption_cost=life_conditions["absorption cost"]
                self.defense_cost=life_conditions["defense cost"]
                self.attack_cost=life_conditions["attack cost"]
                self.bio_packet_size = life_conditions["packet size"]
                self.reproduction_age=life_conditions["reproduction age"]
                #self.reproduction_likelihood=life_conditions["reproduction likelihood"]
                #self.mutation_rate=life_conditions["mutation rate"]
                #self.response_permutation_rate = life_conditions["response permutation rate"]
                #self.response_insertion_rate = life_conditions["response insertion rate"]
                #self.response_deletion_rate = life_conditions["response deletion rate"]
                #self.heuristics_deletion_rate = life_conditions["heuristics deletion rate"]
                #self.heuristics_insertion_rate =life_conditions["heuristics insertion rate"]
                #self.vision_mutation_rate = life_conditions["vision mutation rate"]
                #self.memory_mutation_rate =life_conditions["memory mutation rate"]
                #self.grace_period=life_conditions["grace period"] time allotted to remain below required energy level before death

                self.genome_names=[]
                self.genomes =self.seed_genomes()
                self.agent_names=[]
                self.agents=self.seed_agents() # a list of agent objects
                self.fittest =[]
        #done
        def show(self):
                return str(self.state)+ '\t'+" ".join([str(self.fittest[i].complexity) for i in range(min(10,len(self.genomes)))]) +'\n'
        #DONE
        def sort_fitness(self):
                self.genomes=sorted(self.genomes,key=lambda genome:genome.fitness)
                self.fittest = self.genomes[:10]
        def sort_complexity(self):
                self.genomes=sorted(self.genomes,key=lambda genome:genome.complexity)
                self.most_complex = self.genomes[:10]
        def extinction(self):
              for genome in self.genomes:
                      if genome.living_instantiations == 0:
                              self.genomes.remove(genome)
        #done
        def update(self):
                self.time += 1
                self.shine()
                state_changes = [0 for i in range(self.size)]
                #retrieve responses
                responses = []
                for agent in self.agents:
                        #first update each agent's knowledge
                        local_info = self.relevant_data(agent)
                        agent.observe(local_info)
                        #then have each act accordingly
                        responses.append((agent.name,agent.position,agent.energy,agent.act()))
                #process responses (name, pos, energy, action)
                fates = self.calculate_fates(responses)
                #update agents according to the results of all responses
                for agent in self.agents:
                        living = self.death(agent,fates[agent.name]) 
                        if living:
                                agent.react(fates[agent.name])
                        else:
                                self.kill(agent) 
                self.repopulate()
                self.sort_fitness()
                self.sort_complexity()
                self.extinction()
                

        #DONE 
        def seed_agents(self):
                agents = []
                for i in range(self.life_conditions["initial population"]):
                        pos = random.randrange(self.size)
                        name = self.create_agent_name()
                        #agents[i] = Agent(name,pos)
                        a = Agent(name,pos)
                        agents.append(a)
                        self.genomes.append(a.behavior.genome)
                        a.behavior.genome.instantiations = 1
                        a.behavior.genome.living_instantiations = 1
                return agents
        #DONE 
        def seed_genomes(self):
                #create 10 default genomes and mutate each once
                genomes = []
                for i in range(self.life_conditions["initial biodiversity"]):
                        g = Genome()
                        genomes.append(g)
                return genomes

        #done
        def repopulate(self):
                for agent in self.agents:
                        if agent.age%self.reproduction_age == 0: 
                                r =random.random()
                                while r < reproduction_likelihood & agent.energy >= self.reproduction_energy:
                                        agent.energy-=self.reproduction_energy
                                        self.birth(agent.behavior.genome)
                                        r = random.random()
                lives = len(self.agents)
                genomes = len(self.genomes)
                if genomes< self.life_conditions["initial biodiversity"]:
                        self.genomes += self.seed_genomes()
                if lives< self.life_conditions["initial population"]:
                        self.agents += self.seed_agents()

        #this is where all of the dynamics is coded (described in physics.txt)
        def calculate_fates(self,responses):
            #active_positions is a dictionary of positions referring to lists of actor-response pairs
            
            fates = {}
            active_positions = {}
            #responses: (name, pos, energy, action)
            for response in responses:
                    if response[1] not in active_positions:
                            active_positions[response[1]]= [(response[0],response[2],response[3])]
                    else:
                            #old = active_postions[response[1]]
                            active_positions[response[1]]= active_positions[response[1]]+[(response[0],response[2],response[3])]
                            #new = active_postions[response[1]]
            #active_positions: keys are positions values are (name,energy,action)
            for pos, pairs in active_positions.items():
                    background_energy = self.state[pos]
                    life_energy = 0
                    absorptions = []
                    defenses = []
                    attacks = []
                    movements = []
                    energies = {}
                    new_energies = {}
                    for pair in pairs:
                            background_energy-=pair[1]
                            life_energy+=pair[1]
                            energies[pair[0]]=pair[1]
                            new_energies[pair[0]]=0
                            absorptions.append((pair[0],pair[2][0]))
                            defenses.append((pair[0],pair[2][1]))
                            attacks.append((pair[0],pair[2][2]))
                            movements.append((pair[0],pair[2][3]))

                    self.energy_allocate(energies,background_energy,absorptions)
                    new_life_energy = self.defenses(energies,new_energies,life_energy,defenses)
                    en_list =[]
                    for name in energies:
                            en_list.append((name,energies[name]))
                    en_list.sort(key=lambda pair:pair[1])
                    attacks.sort(key=lambda pair:pair[1])
                    self.attacks(en_list,new_energies,new_life_energy,attacks)
                    position_changes = self.movements(new_energies,movements)
                    
                    for pair in pairs:
                            name = pair[0]
                            payout = new_energies[name]
                            #living = death(self.agents,payout)
                            motion = position_changes[name]
                            fates[name]=(payout,motion)
            return fates



        #Done
        def relevant_data(self, agent):
                pos= agent.position
                vis = agent.behavior.vision
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
                name = "".join(random.choice(string.ascii_letters + string.digits) for i in range(6))
                while name in self.agent_names:
                        name = "".join(random.choice(string.ascii_letters + string.digits) for i in range(6))
                self.agent_names.append(name)
                return name
        def create_genome_name(self):
                #use a random string
                name = "".join(random.choice(string.ascii_letters + string.digits) for i in range(6))
                while name in self.genome_names:
                        name = "".join(random.choice(string.ascii_letters + string.digits) for i in range(6))
                self.genome_names.append(name)
                return name

        #energies is a dictionary with name-energy pairs encoded
        #absorptions is a list of 
        def energy_allocate(self,energies,background_energy,absorptions):
                absorptions_paid=[]
                for request in absorptions:
                        name = request[0]
                        amount = request[1]
                        cost = amount*self.absorption_cost
                        if cost +amount*self.bio_packet_size < energies[name]:
                                absorptions_paid.append((name,amount))
                                energies[name]-=cost
                absorptions_paid = sorted(absorptions_paid,key=lambda request:request[1])
                remaining = background_energy
                for absorption in absorptions_paid:
                        if remaining > 0:
                                name = absorption[0]
                                energies[name]+=absorption[1]*self.bio_packet_size
                                background_energy-=absorption[1]*self.bio_packet_size
        def defenses(self,energies,new_energies,life_energy,defenses):
                defenses_paid=[]
                new_life_energy = life_energy
                for request in defenses:
                        name = request[0]
                        amount = request[1]
                        cost = amount*self.defense_cost
                        if cost +amount*self.bio_packet_size < energies[name]:
                                defenses_paid.append((name,defense))
                                energies[name]-=cost
                                new_life_energy -=cost
                for defense in defenses_paid:
                        name = defense[0]
                        new_energies[name]+=defense[1]*self.bio_packet_size
                        energies[name]-=defense[1]*self.bio_packet_size
                        new_life_energy-=defense[1]*self.bio_packet_size
                return new_life_energy
        #energies sorted in increasing order
        #attacks sorted in increasing order
        # attacks paid for are carried out on the first agent with enough energy to sustain it
        def attacks(self,energies,new_energies,life_energy,attacks):
                for request in attacks:
                        name = request[0]
                        amount = request[1]
                        cost = amount*self.attack_cost
                        index = find(name,energies)
                        if cost +amount*self.bio_packet_size < energies[index]:
                                energies[index]=(energies[index][0],energies[index][1]-cost)
                                amount_to_steal = amount*self.bio_packet_size
                                has_not_stolen =True
                                for i in range(len(energies)):
                                        if amount_to_steal < energies[i][1] & (energies[i][0]!=name) &  has_not_stolen:
                                               new_energies[name]+=amount_to_steal
                                               energies[i]=(energies[i][0],energies[i][1]-amount_to_steal)
                                               has_not_stolen=False


        def movements(self,new_energies,movements):
                movements_paid=[]
                positions={}
                for request in movements:
                        name = request[0]
                        positions[name]=0
                        amount = request[1]
                        cost = abs(amount)*self.friction
                        if cost +amount*self.bio_packet_size < new_energies[name]:
                                movements_paid.append((name,amount))
                                new_energies[name]-=cost
                for movement in movements_paid:
                        name = movement[0]
                        positions[name]+=movement[1]
                return positions

        #done
        def birth(self, parent):
                name = self.create_agent_name()
                pos = random.choice(range(self.size))
                parent.behavior.genome.reproductions+=1
                child = Agent(name,pos,parent.behavior.genome.mutate(self.life_conditions,self.temperature),reproduction_energy)
                child.behavior.genome.living_instantiations+=1
                child.behavior.genome.instantiations+=1
                if child.behavior.genome == parent.behavior.genome:
                        parent.behavior.genome.living_instantiations+=1
                        parent.behavior.genome.instantiations+=1
                else:
                        self.genomes.append(child.behavior.genome)

        def kill(self, agent):
                self.agent_names.remove(agent.name)
                self.agents.remove(agent)
                agent.behavior.genome.living_instantiations-=1
                #agent.genome
                #TODO
                #somehow take into account the death in the fitness of its genome
                #maybe record
        #done
        def death(self,agent,new_energy):
                if new_energy < 0:
                        agent.danger+=1
                else:
                        agent.danger = 0
                if agent.danger == self.life_conditions["grace period"]:
                        return True
                else:
                        return False
        #done
        def shine(self):
                dispersed = 0
                while dispersed <= self.sunshine:
                        pos = random.choice(range(self.size))
                        self.state[pos]+= self.energy_packet
                        dispersed += self.energy_packet


def find(name,list_of_pairs):
        for pair in list_of_pairs:
                if pair[0]==name:
                        return list_of_pairs.index(pair)
                #else:
                        #return None
