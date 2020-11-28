import copy
from enum import Enum


class AgentState(Enum):
    """
    Possible states fro an agent
    """
    IGNORANT = 0
    INACTIVE = 1
    ACTIVE = 2


class Agent:
    def __init__(self, name, states, threshold, independence, providers=None, receivers=None,
                 weights_providers=None, weights_receivers=None):
        """
        :param name: integer, the name of the agent
        :param states: dictionary, key = name of news, value = state in which the agent is wrt that news (AgentState).
        :param threshold: float in [0,1], threshold for becoming active
        :param independence: float in [0,1], the level of influence other agents have on the agent
        :param providers: list of integers, list with the names of the information providers
        :param receivers: list of integers, list with the names of the information recievers
        :param weights_providers: dictionary, key = name of information provider, value = weight of information provider
        :param weights_receivers: dictionary, key = name of information receiver, value = weight of information receiver
        """
        self.name = name
        self.states = states
        self.threshold = threshold
        self.independence = independence
        self.providers = providers
        self.receivers = receivers
        self.weights_providers = weights_providers
        self.weights_receivers = weights_receivers

    def updated_states(self, news, agents):
        """
        Checks if and how the state of the agent should be updated

        :param news: dictionary, key = name of news, value = news object
        :param agents: dictionary, key = name of the agent, value = agent object
        :return: updated_states, dictionary, key = name of the news, value = state in which the agent is wrt that news.
        """

        # Initialise variables
        updated_states = copy.deepcopy(self.states)
        excitement_scores = dict([(n.name, 0) for n in news.values()])

        # Compute the excitement score
        for provider in self.providers:
            if agents[provider].is_active():
                # Find the news wrt which the provider is active
                name_news_active = agents[provider].name_news_active()

                # add the weight of the provider to the excitement score of the news wrt which the provider is active
                excitement_scores[name_news_active] = excitement_scores[name_news_active] + (1 - self.independence) * \
                                                      self.weights_providers[provider]

                # Updates the state to INACTIVE if the state was IGNORANT before
                if updated_states[name_news_active] == AgentState.IGNORANT:
                    updated_states[name_news_active] = AgentState.INACTIVE

        # Compute if excitement score is above threshold and adjust the state accordingly
        for n in news.values():
            # Check if excitement_score is bigger than threshold
            if excitement_scores[n.name] >= self.threshold * (1 - n.sensation):
                # Check if the agent is already active with respect to some other news
                incumbent = False
                for nw in news.values():
                    if nw != n and self.states[nw.name] == AgentState.ACTIVE:
                        incumbent = True

                        # If the excitement score of the other news (news nw) is below the one of the current news
                        # under consideration (news n) the agent becomes active with respect to the news n.
                        # If not he remains active wrt news nw
                        if excitement_scores[n.name] > excitement_scores[nw.name]:
                            updated_states[n.name] = AgentState.ACTIVE
                            updated_states[nw.name] = AgentState.INACTIVE

                # If the agent was not active with respect to any other news (i.e. no incumbents),
                # we update his state to active
                if not incumbent:
                    updated_states[n.name] = AgentState.ACTIVE

            # If the excitement score of an agent is below the threshold he becomes inactive
            elif excitement_scores[n.name] < self.threshold * (1 - n.sensation) and \
                    self.states[n.name] == AgentState.ACTIVE:
                updated_states[n.name] = AgentState.INACTIVE

        return updated_states

    def is_active(self):
        """
        Checks if agent is active with respect to some news

        :return: bool, True if agent is active, False if not
        """
        # Iterate through the states (i.e. the names of the news)
        for s in self.states.values():
            if s == AgentState.ACTIVE:
                return True

        return False

    def is_ignorant(self):
        """
        Checks if agent is ignorant with respect to all news
        """
        for s in self.states.values():
            if s != AgentState.IGNORANT:
                return False

        return True

    def is_inactive(self):
        """
        Checks if agent is inactive with respect to some news

        Agent is inactive if it is not active and not ignorant
        """
        return not self.is_active() and not self.is_ignorant()

    def name_news_active(self):
        """
        Checks with respect to which news an agent is active

        :return: integer, name of the news wrt which the agent is active
        """
        if self.is_active():
            # Iterate through the states (i.e. the names of the news)
            for news_name in self.states:
                if self.states[news_name] == AgentState.ACTIVE:
                    return news_name

        print('Error: provider is inactive')

    def __str__(self):
        info_agent_string = 'Agent: ' + str(self.name) \
                            + '\n' + 'states: ' + str(self.states) \
                            + '\n' + 'threshold: ' + str(self.threshold) \
                            + '\n' + 'independence: ' + str(self.independence) \
                            + '\n' + 'providers: ' + str(self.providers) \
                            + '\n' + 'receivers: ' + str(self.receivers) \
                            + '\n' + 'weights_providers: ' + str(self.weights_providers) \
                            + '\n' + 'weights_receivers: ' + str(self.weights_receivers)

        return info_agent_string

    def __repr__(self):
        info_agent_string = 'Agent: ' + str(self.name) \
                            + '\n' + 'states: ' + str(self.states) \
                            + '\n' + 'threshold: ' + str(self.threshold) \
                            + '\n' + 'independence: ' + str(self.independence) \
                            + '\n' + 'providers: ' + str(self.providers) \
                            + '\n' + 'receivers: ' + str(self.receivers) \
                            + '\n' + 'weights_providers: ' + str(self.weights_providers) \
                            + '\n' + 'weights_receivers: ' + str(self.weights_receivers)

        return info_agent_string
