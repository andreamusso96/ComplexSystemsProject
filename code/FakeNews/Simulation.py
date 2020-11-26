import Functions


class Simulation:

    def __init__(self, number_agents, threshold, independence, news, simulation_time, initial_active_agents):
        """
        This class is meant to make simulations easier to handle.
        :param number_agents: integer, the number of agents
        :param threshold: float in [0,1], threshold for becoming active
        :param independence: float in [0,1], the level of influence other agents have on the agent
        :param news: dictionary, key = name of news, value = news object (see class Agent)
        :param initial_active_agents: dictionary, key = name of active agent, value = news wrt which the agent is active
        :param simulation_time: integer, the number of iterations for our simulation
        """

        self.simulation_time = simulation_time
        self.world = Functions.construct_world_constant_parameters(number_agents, threshold, independence,
                                                                   news)
        # self.simulation_data = dict.fromkeys(list(range(simulation_time)))

        # Active the nodes in initial_active_nodes
        self.activate_agents(initial_active_agents)

    def activate_agents(self, agents_to_activate):
        """
        Activates the agents wrt to a designated news
        :param agents_to_activate: dictionary, key = name of agent to activate, value = news wrt which the agent should be activated
        """
        for name_agent in agents_to_activate:
            self.world.agents[name_agent].state[agents_to_activate[name_agent]] = 2

    def run_simulation(self):
        """
        This function runs the simulation
        """

        for t in range(self.simulation_time):  # For each time step
            print('Time: ', t)
            self.world.update()  # Update the world
            for agent in self.world.agents.values():
                print(' ')
                print('--------------------')
                print(agent)
                print('--------------------')
                print(' ')
            # self.simulation_data[t] = copy.deepcopy(self.world)
