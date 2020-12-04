from classes.agent import AgentState


class World:
    def __init__(self, agents, news, graph):
        """
        :param news: dictionary, key = name of news, value = news object (see class News)
        :param agents: dictionary, key = name of the agent, value = agent object (see class Agent)
        :param graph: nx.DiGraph, a directed graph representing the connections between the agents
        """
        self.agents = agents
        self.news = news
        self.graph = graph
        self.time = 0

    def update(self, verbose=False):
        """
        Executes one update step for the world.

        We first find the agents that should change state and then we modify their states.
        We do so in order to prevent cycles in which changing the state of one agent could lead to changing the state
        of other agents in the same time step.

        :param verbose: bool, If true the function will return the number of agents that changed their state during
                              this update.
        """

        agents_changing_state = {}
        for agent in self.agents.values():
            updated_states = agent.updated_states(self.news, self.agents)
            # If the updated states differ from the current states add the agent to the agents which are changing state
            if agent.states != updated_states:
                agents_changing_state[agent.name] = updated_states

        # Modify the states of the agents who's states should be modified
        for agent_name in agents_changing_state:
            self.agents[agent_name].states = agents_changing_state[agent_name]

        # Update the parameters of the news
        for nw in self.news.values():
            nw.update()

        # Update time
        self.time = self.time + 1

        if verbose:
            return len(agents_changing_state.keys())

    def full_dynamics(self, max_iter=100):
        """
        Updates the world until convergence.

        :param max_iter: int, Maximal number of iterations
        """

        iteration = 0
        while iteration < max_iter and self.update(verbose=True):
            iteration += 1

        if len(self.news.keys()) > 1:
            number_active = {}
            for news_name in self.news.keys():
                number_active[news_name] = len([agent for agent in self.agents.values() if agent.states[news_name] == AgentState.ACTIVE])
        else:
            number_active = len([agent for agent in self.agents.values() if agent.is_active()])

        number_inactive = len([agent for agent in self.agents.values() if agent.is_inactive()])
        number_ignorant = len([agent for agent in self.agents.values() if agent.is_ignorant()])

        return number_active, number_inactive, number_ignorant
