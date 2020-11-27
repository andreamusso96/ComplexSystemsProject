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

    def update(self):
        """
        Update function of the class world. When called it executes one time step.
        """

        # First, we update the parameters of the news.
        for nw in self.news.values():
            nw.update()

        # Second we identify which agents are changing state a time self.time
        agents_changing_state = {}

        for agent in self.agents.values(): # Iterate through the agents
            updated_states = agent.updated_states(self.news, self.agents)  # Compute the updated states of the agents
            if agent.states != updated_states: # If the updated states differ from the current states
                agents_changing_state[agent.name] = updated_states #Add the agent to the agents which are changing state

        # Third we modify the states of the agents who's states should be modified
        for agent_name in agents_changing_state:
            self.agents[agent_name].states = agents_changing_state[agent_name]

        # Note: we first find the agents that should change state and then we modify their states
        # We do so in order to not have some wierd cycles in which changing the state of an agent impacts if the states
        # of other agents should be changed

        self.time = self.time + 1

