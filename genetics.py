import pdb
import random
#import numpy
try:
        import cPickle as pickle
except:
        import pickle
#import hashlib

class Genome(object):
        #default genome is completely random
        #TODO For some reason, genomes are added to the world multiple times (sometimes not simultaneously)
            #these ones are also treated as unrelated
            #one might expect them to be just the most likely ones, but they are definitely not
            #heredity seems to hold for some and not for others
            #the highest generation is always 1 WHY?
            #Problem A: somehow there are genomes with multiple copies of the same separator
            #    B: somehow htere are genomes with no separators
            #vision tends to be zero
            #responses always have empty coordinates regardless of vision
        def __init__(self,parents=None,separators=None,vision=None,memory=None,responses=None,heuristics=None):
                self.parents=parents
                self.generation = 0
                if self.parents != None:
                    self.generation = self.generation + 1
                    if self.generation >1:
                        print "Generation 2 reached"
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
                       num_separators = abs(int(random.gauss(0,1)))+1
                       self.separators = []
                       #TODO Problem A
                       for i in range(num_separators):
                           self.separators = self.separators + [random_sep()]
                       self.separators.sort()
                else:
                        self.separators=separators
                if responses==None:
                        num_responses = int(random.betavariate(2,1))-1
                        self.responses = []
                        for i in range(num_responses):
                                num_coordinates = int(random.betavariate(2,1))-1
                                coords = tuple(random_configuration(vision,memory,separators) for i in range(num_coordinates))
                                agent_action = random_action()
                                if coords != []:
                                        self.responses.append((coords,agent_action))
                else:
                        self.responses= responses


                if heuristics==None:
                        self.heuristics=[]
                        num_heuristics = int(1/random.betavariate(2,1))
                        for i in range(num_heuristics):
                                agent_action = random_action()
                                self.heuristics.append(agent_action)
                        if num_heuristics == 0:
                                self.heuristics.append(random_action())
                else:
                        self.heuristics= heuristics

                self.complexity = self.complexity_estimate()
                #assign the minimum fitness of parents
                self.fitness =0
                self.reproductions = 0

        #done
        def mutate(self,life_conditions):
                vision= self.vision_mutate(life_conditions)
                memory= self.memory_mutate(life_conditions)
                separators= self.separators_mutate(life_conditions)
                responses= self.responses_mutate(life_conditions)
                heuristics= self.heuristics_mutate(life_conditions)
                #pruning eliminates actions which utilize vision and memory beyond the agent's capacity
                prune(responses,heuristics,vision,memory,separators)
                #TODO You must do this another way making changes can be undone
                #    by pruning, resulting in a "new" genome with the exact same properties
                vision_has_changed = vision==self.vision
                memory_has_changed = memory==self.memory
                sep_has_changed = separators==self.separators
                resp_has_changed = responses==self.responses
                heur_has_changed = heuristics==self.heuristics
                has_changed = not (vision_has_changed and memory_has_changed and sep_has_changed and resp_has_changed and heur_has_changed)
                if has_changed:
                        #TODO There is a problem here where the information passed as the parent is lost in the return call
                        #HERE
                        return Genome(self,separators,vision,memory,responses,heuristics)
                else:
                        return self


        #Done
        def vision_mutate(self,life_conditions):
                temp = life_conditions['temperature']
                vision_mutation_rate = life_conditions['vision mutation rate']
                max_vision = life_conditions['max vision']
                vision = self.vision
                r = random.random()*temp
                if r < vision_mutation_rate:
                        b = random.choice(["up","down"])
                        if (b == "up") and (self.vision < max_vision):
                                vision+=1
                        elif (b == "down") and (self.vision >0):
                                vision -= 1
                        else:
                               pass
                return vision
        def memory_mutate(self,life_conditions):
                temp = life_conditions['temperature']
                memory_mutation_rate = life_conditions['memory mutation rate']
                max_memory = life_conditions['max memory']
                memory = self.memory
                r = random.random()*temp
                if r < memory_mutation_rate:
                        b = random.choice(["up","down"])
                        if (b == "up") and (self.memory < max_memory):
                                memory+=1
                        elif (b == "down") and (self.memory >0):
                                memory-=1
                        else:
                                pass
                return memory
        def responses_mutate(self,life_conditions):
                temp = life_conditions['temperature']
                response_insertion_rate = life_conditions['response insertion rate']
                response_deletion_rate = life_conditions['response deletion rate']
                response_permutation_rate = life_conditions['response permutation rate']
                response_replacement_rate = life_conditions['response replacement rate']
                num_responses = len(self.responses)
                responses = self.responses
                if num_responses > 0:
                        delete =random.random()*temp
                        if delete < response_deletion_rate:
                                r = random.choice(responses)
                                responses.remove(r)
                                num_responses-=1
                replace =random.random()*temp
                if (replace < response_replacement_rate) and (num_responses > 0):
                        index = random.choice(range(len(responses)))
                        responses[index]=random_response(self.vision,self.memory,self.separators)
                insert =random.random()*temp
                if insert < response_insertion_rate:
                        responses.append(random_response(self.vision,self.memory,self.separators))
                per =random.random()*temp
                while per < response_permutation_rate:
                        per = random.random()*temp
                        random.shuffle(responses)
                return responses
        def heuristics_mutate(self,life_conditions):
                temp = life_conditions['temperature']
                heuristic_insertion_rate = life_conditions['heuristic insertion rate']
                heuristic_deletion_rate = life_conditions['heuristic deletion rate']
                heuristic_permutation_rate = life_conditions['heuristic permutation rate']
                heuristic_replacement_rate = life_conditions['heuristic replacement rate']
                num_heuristics = len(self.heuristics)
                heuristics = self.heuristics
                if num_heuristics > 1:
                        delete =random.random()*temp
                        if delete < heuristic_deletion_rate:
                                r = random.choice(heuristics)
                                heuristics.remove(r)
                replace =random.random()*temp
                if replace < heuristic_replacement_rate:
                        index = random.choice(range(len(heuristics)))
                        heuristics[index]=random_action()
                insert =random.random()*temp
                if insert < heuristic_insertion_rate:
                        heuristics.append(random_action())
                per =random.random()*temp
                while per < heuristic_permutation_rate:
                        per = random.random()*temp
                        random.shuffle(heuristics)
                return heuristics
        #TODO check this
        def separators_mutate(self,life_conditions):
                temp = life_conditions['temperature']
                separator_insertion_rate = life_conditions['separator insertion rate']
                separator_deletion_rate = life_conditions['separator deletion rate']
                separators = self.separators
                if separators!=[]:
                        delete =random.random()*temp
                        if delete < separator_deletion_rate:
                                r = random.choice(separators)
                                separators.remove(r)

                change =random.random()*temp
                if (change < separator_insertion_rate) and (separators!=[]):
                        index = random.choice(range(len(separators)))
                        separators[index]=random_sep()
                add =random.random()*temp
                if add < separator_insertion_rate:
                        separators.append(random_sep())
                separators.sort()
                return separators

        #done
        def complexity_estimate(self):
                return len(self.responses) + len(self.heuristics) + self.vision + self.memory + len(self.separators)

                #TODO (later)
                #each action has complexity determined by the amount of info used
                #sum these, but perhaps weight heuristics differently
                #longer heuristic sequence implies more complex
                #longer action table implies more complex
                #return a number for taxing purposes
        def fitness_update(self):
                #TODO there is some weirdness allowing fitness > 1
                #broken instantiation counter?
                self.fitness = float(self.reproductions)/float(self.instantiations)
        def show(self):
                return pickle.dumps(self)

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
        absorb = int(1/random.betavariate(2,1))-1
        defend = int(1/random.betavariate(2,1))-1
        attack = int(1/random.betavariate(2,1))-1
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
        if heuristics == []:
                heuristics.add(random_action())
