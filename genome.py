import random
import numpy
try:
        import cPickle as pickle
except:
        import pickle
import hashlib

class Genome(object):
        #default genome is completely random
        #Done
        def __init__(self,parents=None,separators=None,vision=None,memory=None,responses=None,heuristics=None):
                self.parents=parents
                self.living_instantiations =0 #add one for each born with this genome subtract for each death
                self.instantiations =0 #add one for each born with this genome  DO NOT subtract for each death
                if vision==None:
                       self.vision = abs(int(random.gauss(0,2)))
                else:
                        self.vision = vision
                if memory==None:
                       self.memory = abs(int(random.gauss(0,2)))
                else:
                        self.memory = memory
                if separators==None:
                       self.separators = abs(int(random.gauss(0,1)))+1
                else:
                        self.separators = separators
                if responses==None:
                        num_responses = int(random.betavariate(2,1))-1
                        for i in range(num_responses):
                                num_coordinates = int(random.betavariate(2,1))-1
                                coords = tuple(random_configuration(vision,memory,separators) for i in range(num_coordinates))
                                agent_action = random_action()
                                self.responses.append((coords,agent_action))
                else:
                        self.responses= responses


                if heuristics==None:
                        self.heuristics=[]
                        num_heuristics = int(random.betavariate(2,1))-1
                        for i in range(num_heuristics):
                                agent_action = random_action()
                                self.heuristics.append(agent_action)
                else:
                        self.heuristics= heuristics

                self.memory= memory
                self.responses= responses
                self.heuristics= heuristics
                self.complexity = self.complexity_estimate()
                #assign the minimum fitness of parents
                self.fitness =0
                self.reproductions = 0

        #done
        def mutate(self,life_conditions,temp=1.0):
                vision, vision_has_changed = vision_mutate(temp)
                memory, memory_has_changed = memory_mutate(temp)
                separators, sep_has_changed = separator_mutate(temp)
                #pruning eliminates actions utilizing vision and memory beyond the agent's capacity
                prune(responses,heuristics,vision,memory,separators)
                responses, resp_has_changed = responses_mutate(temp)
                heuristics, heur_has_changed = heuristics_mutate(temp)
                has_changed = vision_has_changed | memory_has_changed |sep_has_changed| resp_has_changed| heur_has_changed
                if has_changed:
                        return Genome(self,separators,vision,memory,responses,heuristics)
                else:
                        return self

       
        #Done
        def vision_mutate(self,temp):
                vision = self.vision
                r = random.random()*temp
                if r < vision_mutation_rate:
                        b = random.choice(["up","down"])
                        if b == "up" & self.vision < max_vision:
                                vision+=1 
                        elif b == "down" & self.vision >0:
                                vision -= 1
                        else:
                               pass 
                        return (vision,vision==self.vision)
        def memory_mutate(self,temp):
                memory = self.memory
                r = random.random()*temp
                if r < memory_mutation_rate:
                        b = random.choice(["up","down"])
                        if b == "up" & self.memory < max_memory:
                                memory+=1
                        elif b == "down" & self.memory >0:
                                memory-=1
                        else:
                                pass
                        return (memory, memory==self.memory)
        def responses_mutate(self,temp):
                num_responses = self.responses.len()
                responses = self.responses
                if num_responses > 0:
                        delete =random.random()*temp
                        if delete < response_deletion_rate:
                                r = random.choice(responses)
                                responses.remove(r)
                change =random.random()*temp
                if change < response_insertion_rate:
                        index = random.choice(range(responses.len()))
                        index,responses[index]=random_response()
                insert =random.random()*temp
                if insert < response_insertion_rate:
                        responses.append(random_response())
                if num_responses > 1:
                        per =random.random()*temp
                        while per < response_permutation_rate:
                                per = random.random()*temp
                                a = random.choice(range(num_responses))
                                b = random.choice(range(num_responses).remove(a))
                                responses[a], responses[b] = responses[b], responses[a]  
                return (responses,responses==self.responses)
        def heuristics_mutate(self,temp):
                num_heuristics = self.heuristics.len()
                heuristics = self.heuristics
                if num_heuristics > 1:
                        delete =random.random()*temp
                        if delete < heuristics_deletion_rate:
                                r = random.choice(heuristics)
                                heuristics.remove(r)
                change =random.random()*temp
                if change < heuristics_insertion_rate:
                        index = random.choice(range(heuristics.len()))
                        heuristics[index]=random_action()
                insert =random.random()*temp
                if insert < heuristics_insertion_rate:
                        heuristics.append(random_action())
                if num_heuristics > 1:
                        per =random.random()*temp
                        while per < heuristics_permutation_rate:
                                per = random.random()*temp
                                a = random.choice(range(num_heuristics))
                                b = random.choice(range(num_heuristics).remove(a))
                                heuristics[a], heuristics[b] = heuristics[b], heuristics[a]  
                return (heuristics,heuristics==self.heuristics)
        #TODO check this
        def separators_mutate(self,temp):
                num_separators = self.separators.len()
                separators = self.separators
                if num_separators > 0:
                        delete =random.random()*temp
                        if delete < separators_deletion_rate:
                                r = random.choice(separators)
                                separators.remove(r)

                change =random.random()*temp
                if change < separators_insertion_rate:
                        index = random.choice(range(separators.len()))
                        separators[index]=random_sep()
                add =random.random()*temp
                if add < separators_insertion_rate:
                        separators.append(random_sep())
                if num_separators > 1:
                        per =random.random()*temp
                        while per < separators_permutation_rate:
                                per = random.random()*temp
                                a = random.choice(range(num_separators))
                                b = random.choice(range(num_separators).remove(a))
                                separators[a], separators[b] = separators[b], separators[a]  
                separators.sort()
                return (separators,separators==self.separators)

        #done
        def complexity_estimate(self):
                return self.responses.len() + self.heuristics.len() + vision + memory + separators
                #TODO (later)
                #each action has complexity determined by the amount of info used
                #sum these, but perhaps weight heuristics differently
                #longer heuristic sequence implies more complex
                #longer action table implies more complex
                #return a number for taxing purposes
        def fitness_update(self):
                self.fitness = float(self.reproductions)/float(self.instantiations)

        #another iteration
        #def response_complexity(response):
                #return response[0].len()
        #def heuristics_complexity(heur):
                #return heur.len()

        #def asexual_birth(self,genome):
                #r = random.random()
                #if r <= mutation_rate:
                        #mutate(genome)
        #def sexual_birth(self,genomes):
                ##TODO
                #pass

        #done
        def random_action():
                absorb = int(1/random.beta(2,1))-1
                defend = int(1/random.beta(2,1))-1
                attack = int(1/random.beta(2,1))-1
                move = int(random.gauss(0,2))
                return (absorb,defend,attack,move)
        def random_configuration(vision,memory,separators):
            pos = random.randint(-vision,vision+1)
            mem = random.randint(0,memory)
            level = random.randint(0,separators)
            return (pos, mem, level)
        def random_response(vision,memory,separators):
                num_coordinates = int(random.betavariate(2,1))-1
                coords = tuple(random_configuration(vision,memory,separators) for i in range(num_coordinates))
                agent_action = random_action()
                return (coords,agent_action)
        def random_sep():
                return abs(int(random.gauss(0,100)))+1
        def prune(responses,heuristics,vision,memory,separators):
                
                for response in responses:
                        flag = False
                        for coord in response[0]:
                                if abs(coord[0]) > vision | abs(coord[1]) > memory | coord[2]> separators:
                                        flag = True
                        if flag:
                                responses.remove(response)
                for heuristic in heuristics:
                        flag = False
                        for coord in heuristic[0]:
                                if abs(coord[0]) > vision | abs(coord[1]) > memory | coord[2]> separators:
                                        flag = True
                        if flag:
                                heuristics.remove(heuristic)
                if heuristics == []:
                        heuristics.add(random_action())

