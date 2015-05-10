import random
import hashlib

class Genome(object):
        def __init__(self,separators,vision,memory,actions,heuristics):
                self.separators= separators
                self.vision= vision
                self.memory= memory
                self.actions= actions
                self.heuristics= heuristics
                self.name = create_name()
                self.complexity = complexity_estimate()

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

        def create_name(self):
                seps="".join(map(str,separators))
                acts = map(lambda action:map(str,action))
                heurs=
                hash_obj=hashlib.md5(seps+str(vision)+str(memory)+acts+heurs)

        def complexity_estimate(self):
                #TODO
                #pretty much just multiply vision by memory by number of separators
