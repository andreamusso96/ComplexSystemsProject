import copy


class Agent:
    def __init__(self, name, states, threshold, independence, providers=None, receivers=None,
                 weights_providers=None, weights_receivers=None):
        """
        :param name: integer, the name of the agent
        :param states: dictionary, key = name of news, value = state in which the agent is wrt that news.
        There are three possible states 0 = ignorant, 1 = inactive, 2 = active
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
        :return: updated_states, dictionary, key = name of the news, value = state in which the agent is wrt that news
        There are three possible states 0 = ignorant, 1 = inactive, 2 = active
        """

        # Initialise variables
        updated_states = copy.deepcopy(self.states)
        excitement_scores = dict([(n.name, 0) for n in news.values()])

        # Compute the excitement score
        for provider in self.providers:  # Iterate through the providers
            if agents[provider].is_active():  # If a provider is active
                name_news_active = agents[provider].name_news_active()  # Find the news wrt which the provider is active
                excitement_scores[name_news_active] = excitement_scores[name_news_active] + (1 - self.independence) * \
                                                      self.weights_providers[
                                                          provider]  # add the weight of the provider to the excitement score of the news wrt which the provider is active
                if updated_states[name_news_active] == 0:  # If the agent is ignorant
                    updated_states[name_news_active] = 1  # Update his state to being inactive

        # Compute if excitement score is above threshold and adjust the state accordingly
        for n in news.values():  # Iterate through the news

            if excitement_scores[n.name] >= self.threshold * (
                    1 - n.sensation):  # If a news has a score higher than the threshold

                # There are two options: either the agent is active wrt some other news or he is not.
                # We treat the first case first
                incumbent = False
                for nw in news.values():
                    if self.states[nw.name] == 2:  # If the agent is active with respect to some other news
                        incumbent = True

                        # If the excitement score of the other news (news nw) is below the one of the current news under consideration (news n)
                        # the agent becomes active with respect to the news n. If not he remains active wrt news nw
                        if excitement_scores[n.name] > excitement_scores[nw.name]:
                            updated_states[n.name] = 2
                            updated_states[nw.name] = 1

                # If the agent was not active with respect to any other news (i.e. no incuments), we update his state to active
                if not incumbent:
                    updated_states[n.name] = 2

            # If the excitement score of an agent is below the threshold he becomes inactive
            elif excitement_scores[n.name] < self.threshold * (1 - n.sensation) and self.states[n.name] == 2:
                updated_states[n.name] = 1

        return updated_states

    def is_active(self):
        """
        Checks if agent is active with respect to some news

        :return: bool, true if agent is active false if not
        """
        for s in self.states: # Iterate through the states (i.e. the names of the news)
            if self.states[s] == 2: # If agent is active wrt some news return True
                return True

        return False

    def name_news_active(self):
        """
        Checks with respect to which news an agent is active

        :return: integer, name of the news wrt which the agent is active
        """
        if self.is_active():
            for news_name in self.states: # Iterate through the states (i.e. the names of the news)
                if self.states[news_name] == 2: # If the agent is active wrt to some news return the name of the news
                    return news_name
        else:
            print('Error: provider is inactive')

    def agent_node_color(self):
        """
        :return: integer, name of the news with respect which the agent is active = node color
        """
        # If the agent is active agent_node_color =  name of the news with respect to which he is active (i.e. an integer).
        if self.is_active():
            agent_node_color = self.name_news_active()
        else:
            agent_node_color = 0
        return agent_node_color

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
