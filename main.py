import sys
from world import *

#TODO MAJOR Problems:
    #there is broken heredity for some reason

def main(argv=sys.argv):

        #TODO allow for continuation of previous worlds by file input
        #world_input = argv[0]
        #agents_input = argv[1]
        #genomes_input = argv[2]


        #stuff for visualization purposes
        world_file = "world.txt"
        agents_file= "agents.txt"
        genomes_file= "genomes.txt"
        world_buffer = open(world_file,'w')
        agents_buffer = open(agents_file,'w')
        genomes_buffer = open(genomes_file,'w')

        #planetary conditions
        world_size = 3
        end_of_time = 1000

        #energy fed into the system at each time step (dispersed randomly)
        sunshine = 300

        #size of sunlight chunks dispersed
        energy_packet=5

        #proportionally increases cost of movement with how much energy one has
        friction = 1

        #life restrictions
        initial_biodiversity = 20
        initial_population =10
        max_diversity = 100 #not actually used here
        max_agents= 2000 #not actually used here

        #individual life restrictions
        initial_temp= 1
        max_memory = 10
        max_vision = 10
        max_separators = 3

        #in units of energy per timestep
        existence_cost = 50

        #a tax on complexity of organisms so that random purposeless behavior is not rewarded
        complexity_cost = 10
        absorption_cost = 1
        defense_cost = 1
        attack_cost = 1
        packet_size = 10

        #steps to spawn new life
        reproduction_age = 5
        reproduction_energy = 5
        reproduction_likelihood = .5

        mutation_rate = .25
        response_permutation_rate = 0.05
        response_insertion_rate= 1
        response_deletion_rate = .1
        response_replacement_rate =.1
        heuristic_deletion_rate = .1
        heuristic_insertion_rate =.1
        heuristic_permutation_rate =.1
        heuristic_replacement_rate =.1
        separator_deletion_rate = .1
        separator_insertion_rate =.1
        separator_replacement_rate =.1
        vision_mutation_rate = .02
        memory_mutation_rate = .02

        #time steps allowed to gain the energy required to stay alive
        grace_period = 3

        life_conditions = {
                        "response permutation rate":response_permutation_rate,
                        "response insertion rate":response_insertion_rate,
                        "response deletion rate":response_deletion_rate,
                        "response replacement rate":response_replacement_rate,
                        "heuristic deletion rate": heuristic_deletion_rate,
                        "heuristic insertion rate":heuristic_insertion_rate,
                        "heuristic permutation rate":heuristic_permutation_rate,
                        "heuristic replacement rate":heuristic_replacement_rate,
                        "separator deletion rate": separator_deletion_rate,
                        "separator insertion rate":separator_insertion_rate,
                        "separator replacement rate":separator_replacement_rate,
                        "vision mutation rate":vision_mutation_rate,
                        "memory mutation rate":memory_mutation_rate,
                        "initial population": initial_population,
                        "initial biodiversity": initial_biodiversity,
                        "initial temp":initial_temp,
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
                        "packet size":packet_size,
                        "temperature":initial_temp
                        }
        physics = {"world size":world_size,
                    "end of time":end_of_time,
                    "sunshine":sunshine,
                    "energy packet":energy_packet,
                    "friction":friction
                    }

        world = World(physics,life_conditions)
        while world.time != end_of_time:
                world.update()
                print world.time
                if (world.time % 100) == 0:
                    genomes_buffer.write('at time '+ str(world.time)+' the fittest genomes were:\n')
                    for i in range(min(10,len(world.genomes))):
                            genomes_buffer.write(world.fittest[i].show())
                    genomes_buffer.write('\n')
                world_buffer.write(world.show_state())
        #pdb.set_trace()
        #world.show_best()
        world.doom()

if __name__ == "__main__": main()
