import copy

from agent import AgentState
from utils import construct_world_constant_parameters


class Simulation:

    def __init__(self, number_agents, threshold, independence, news, simulation_time, initial_active_agents):
        """
        Data object for the network simulations.

        :param number_agents: integer, the number of agents
        :param threshold: float in [0,1], threshold for becoming active
        :param independence: float in [0,1], the level of influence other agents have on the agent
        :param news: dictionary, key = name of news, value = news object (see class Agent)
        :param initial_active_agents: dictionary, key = name of active agent, value = news wrt which the agent is active
        :param simulation_time: integer, the number of iterations for our simulation
        """
        self.simulation_time = simulation_time
        self.world = construct_world_constant_parameters(number_agents, threshold, independence, news)

        # This is a dictionary with key  = time and value = copy of world at that time
        self.simulation_data = dict.fromkeys(list(range(simulation_time)))

        # Active the nodes in initial_active_nodes
        self.activate_agents(initial_active_agents)

    def activate_agents(self, agents_to_activate):
        """
        Activates the agents wrt to a designated news
        :param agents_to_activate: dictionary, key = name of agent to activate, value = news wrt which the agent should be activated
        """
        for name_agent in agents_to_activate:
            self.world.agents[name_agent].states[agents_to_activate[name_agent]] = AgentState.ACTIVE

    def run_simulation(self):
        """
        This function runs the simulation
        """

        # Save initial state
        self.simulation_data[0] = copy.deepcopy(self.world)

        for t in range(self.simulation_time):
            print('Time:', t+1)
            # Update the world
            self.world.update()
            # Save current state
            self.simulation_data[t+1] = copy.deepcopy(self.world)
