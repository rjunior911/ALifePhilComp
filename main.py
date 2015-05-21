import pdb
import sys
from world import *
def main(argv=sys.argv):

        #stuff for visualization purposes
        world_file = "world.txt"
        agents_file= "agents.txt"
        genomes_file= "genomes.txt"
        world_buffer = open(world_file,'w')
        agents_buffer = open(agents_file,'w')
        genomes_buffer = open(genomes_file,'w')

        #planetary conditions
        world_size = 3
        end_of_time = 5000

        #energy fed into the system at each time step (dispersed randomly)
        sunshine = 200

        #size of sunlight chunks dispersed
        energy_packet=10

        #proportionally increases cost of movement with how much energy one has
        friction = 1

        #life restrictions
        initial_biodiversity = 20
        max_diversity = 100#not actually used here
        initial_population =10 
        max_agents= 2000#not actually used here
        #individual life restrictions
        initial_temp= 1
        max_memory = 10 #not actually used here
        max_vision = 10#not actually used here
        max_separators = 3#not actually used here

        #in units of energy per timestep
        existence_cost = 5

        #a tax on complexity of organisms so that random purposeless behavior is not rewarded
        complexity_cost = 1
        absorption_cost = 1
        defense_cost = 1
        attack_cost = 1
        packet_size = 50

        #steps to spawn new life
        reproduction_age = 50
        reproduction_energy = 20
        reproduction_likelihood = .5

        mutation_rate = .25
        response_permutation_rate = 0.05
        response_insertion_rate= .05
        response_deletion_rate = .1
        heuristics_deletion_rate = .1
        heuristics_insertion_rate =.1
        vision_mutation_rate = .02
        memory_mutation_rate = .02

        #steps allowed to gain energy required to stay alive
        grace_period = 10

        life_conditions = {
                        "response permutation rate":response_permutation_rate,
                        "response insertion rate":response_insertion_rate,
                        "response deletion rate":response_deletion_rate,
                        "heuristics deletion rate": heuristics_deletion_rate,
                        "heuristics insertion rate":heuristics_insertion_rate,
                        "vision mutation rate":vision_mutation_rate,
                        "memory mutation rate":memory_mutation_rate,
                        "initial population": initial_population,
                        "initial biodiversity": initial_biodiversity,
                        "max agents":max_agents,
                        "max diversity": max_diversity,
                        "max memory":max_memory,
                        "max vision":max_vision,
                        "max separators":max_separators,
                        "existence cost":existence_cost,
                        "complexity cost":complexity_cost,
                        "reproduction age":reproduction_age,
                        "reproduction energy":reproduction_energy,
                        "reproduction likelihood":reproduction_likelihood,
                        "mutation rate":mutation_rate, 
                        "grace period":grace_period, #time allotted to remain below required energy level before death
                        "absorption cost":absorption_cost,
                        "defense cost":defense_cost,
                        "attack cost":attack_cost,
                        "packet size":packet_size
                        }
        physics = {"world size":world_size,
                    "end of time":end_of_time,
                    "sunshine":sunshine,
                    "energy packet":energy_packet,
                    "friction":friction,
                    "initial temp":initial_temp
                    }

        world = World(physics,life_conditions)
        while world.time != end_of_time:
                world.update()
                if (world.time % 100) == 0:
                        genomes_buffer.write('at time '+ str(world.time)+' the fittest genomes were:\n')
                        for i in range(min(10,len(world.genomes))):
                                genomes_buffer.write(str(world.fittest[i])+'\n')
                        genomes_buffer.write('\n')
                world_buffer.write(world.show())
        
if __name__ == "__main__": main()

