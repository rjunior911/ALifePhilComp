import random
try:
        import cPickle as pickle
except:
        import pickle
import hashlib

class Genome(object):
        #TODO create the basic genome
        #  fill in mutations
        def __init__(self,separators=None,vision=0,memory=0,actions=None,heuristics=[(0,0)]):
                self.separators= separators
                self.vision= vision
                self.memory= memory
                self.actions= actions
                self.heuristics= heuristics
                #potential problem using hash of initial data to create name
                #self.name = create_name()
                self.complexity = complexity_estimate()
                self.fitness =0

        def mutate(self,temperature,mate=None):
                r = random.random()
                #r1 = random.randrange(max)
                #r2 = random.randrange(max)


        def insertion(self):

        def deletion(self):

        def replacement(self):

        def mate(self, mate):
                #if there's anything new in the lookup table randomly add it unless it conflicts with something already had
                #choose some number of things to swap then randomly assign what blocks of that size to swap
                #choose some number of things to add then randomly 
                #if there is a difference in heuristic sequences

        #TODO Fix the recursive problem by making name only depend on actions, heuristics, and separators...plus vision and mem
        def create_name(self):
                #seps="".join(map(str,separators))
                #acts = map(lambda action:map(str,action))
                #heurs=

                self_string=pickle.dumps(self)
                hash_obj=hashlib.md5(self_string)
                name=hash_obj.hexdigest()

        def complexity_estimate(self):
                #TODO
                #each action has complexity determined by the amount of info used
                #sum these, but perhaps weight heuristics differently
                #longer heuristic sequence implies more complex
                #longer action table implies more complex
                #return a number for taxing purposes
        def fitness_update(self,data):
                #take the average energy of agents with this genome
                #average lifespan 
                #average age
