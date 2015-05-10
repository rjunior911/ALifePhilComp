import world.py
def stringify(agent):
        #TODO

def main():

        #stuff for visualization purposes
        world_file = "world.txt"
        agents_file= "agents.txt"
        world_buffer = open(world_file,'w')
        agents_buffer = open(agents_file,'w')

        #planetary conditions
        max_size = 10**2
        end_of_time = 10**4
        #energy fed into the system at each time step (dispersed randomly)
        sunshine = 50
        #size of sunlight chunks dispersed
        energy_packet=5
        #proportionally increases cost of movement with how much energy one has
        friction = 0

        #life restrictions
        max_agents= 2000
        #individual life restrictions
        initial_temp= 1
        max_memory = 10
        max_vision = 10
        max_separators = 3

        #in units of energy per timestep
        existence_cost = 1

        #a tax on complexity of organisms so that random purposeless behavior is not rewarded
        complexity_cost = .05

        #steps to spawn new life
        reproduction_rate = 10

        #initial rate of mutation which is decreased for each mutation correspondingly; 
        #also decreased according to temperature
        mutation_rate = .25

        #steps allowed to gain energy required to stay alive
        grace_period = 10

        physics = {"max size":max_size,
                    "end_of_time ":end_of_time,
                    "sunshine":sunshine,
                    "energy packet":energy_packet,
                    "friction":friction,
                    "max_agents":max_agents,
                    "initial_temp":initial_temp,
                    "max_memory":max_memory,
                    "max_vision":max_vision,
                    "max_separators":max_separators,
                    "existence_cost":existence_cost,
                    "complexity_cost":complexity_cost,
                    "reproduction_rate":reproduction_rate,
                    "mutation_rate":mutation_rate,
                    "grace_period":grace_period
                    }

        world = World(physics)
        while world.time != end_of_time:
                world.update()
                if world.time % 100 ==0:
                        agents_buffer.write('at time '+ str(world.time)+' the fittest genomes were:\n')
                        for i in range(10):
                                agents_buffer.write(world.fittest)
                        agents_buffer.write('\n')
                world_buffer.write(world.show())
        #not sure if this is the correct way to destruct
        #world.del()
