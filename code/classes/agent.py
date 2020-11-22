""" Agent class """
import numpy as np


class Agent:
    """
    Represents an agent in the network

    Attributes:
        share_threshold: float between 0 and 1
            how much excitement about a news an agent needs before he shares it.
        truthfulness_opinion: float between -1 and 1
            what agent thinks about the truthfulness of the news (−1: fake news, 1: true news)
        is_active: bool
            if the agent is active (has shared the news)
        State: string
            state of the agent: ignorant, inactivate or active    


    Methods:
        compute_truth_likelihood(provider, trust_in_providers)
            computes the truth likelihood of the news
        compute_excitement(news, truth_likelihood)
            computes the excitement score of the news
        is_sharing(news)
            returns True if the agent will share the news
    """

    def __init__(self, name, share_threshold, truthfulness_opinion):
        """
        Represents an agent in the network

        :param share_threshold: float in [0, 1]
            how much excitement about a news an agent needs before he shares it.
        :param truthfulness_opinion: float in [-1, 1]
            what the agent think about the truthfulness of the news
        """
        assert 0 <= share_threshold <= 1, 'Invalid value for share_threshold. Value should be between 0 and 1'
        assert -1 <= truthfulness_opinion <= 1, 'Invalid value for truthfulness_opinion. Value should be between -1 and 1'

        self.name = name
        self.share_threshold = share_threshold
        self.truthfulness_opinion = truthfulness_opinion
        self.State = 'ignorant'
        #just for reading info about state, not modifing state
        self.is_active = False
        

    def compute_truth_likelihood(self, providers, trust_in_providers):
        """
        Computes the truth likelihood of the news based on the trust in the information providers

        :param providers: list (list of Agents)
            represents the information providers
        :param trust_in_providers: dictionary (normalized) key = name of provider, value = trust in provider (float in [0,1])
            represents the trust in the information providers
        :return: float
            Truth likelihood of the news
        """
        assert (1 - np.sum(list(trust_in_providers.values()))>=0), 'Invalid value for trust_in_providers. Array ' \
                                                                         'should be normalized '

        truth_likelihood = (np.random.rand() - 0.5) / 100  # some noise
        for provider in providers:
            # For each active provider we add the trust in that provider to the truth likelihood
            if provider.is_active:
                truth_likelihood = truth_likelihood + trust_in_providers[provider.name]

        return truth_likelihood

    def compute_excitement(self, news, truth_likelihood):
        """
        Computes the excitement score of the news based on its truth likelihood and fitness

        :param news: News
            News that is shared in the network
        :param truth_likelihood: float in [0, 1]
            how much the agent believes in the news.
        :return: float
            Excitement score of the news
        """
        indipendent_thought = 1 - truth_likelihood
        excitement_score = (truth_likelihood + self.truthfulness_opinion * indipendent_thought + news.fitness) * np.exp(
            -0.01 * news.time)/2 # here we set c = 0.01
        return excitement_score

    def activates(self, news, providers, trust_in_providers):
        """
        Computes if the agent should activate or not.

        :param news: News
            News that is shared in the network
        :param providers: list (list of Agents)
            represents the information provider
        :param trust_in_providers: dictionary (normalized) key = name of provider, value = trust in provider (float in [0,1])
            represents the trust in the information providers
        :return: boolean
            True if agent activates in this round and false otherwise (is already active or does not activate)
        """
        assert len(providers) == len(trust_in_providers), 'provider and trust_in_providers must have the same length'

        if self.is_active:
            return False
        # if this function was called it's because the news reached the agent
        self.State = 'inactive'
        
        # check if agent should activate
        truth_likelihood = self.compute_truth_likelihood(providers, trust_in_providers)
        excitement_score = self.compute_excitement(news, truth_likelihood)

        if excitement_score >= self.share_threshold:
            return True
        return False

    def activate(self):
        """
        Activates the agent if it can be activated
        """
        self.State = 'active'
        self.is_active = True

    def __str__(self):
        return f'Agent: \n' \
               f'\tshare threshold: {self.share_threshold}\n' \
               f'\ttruthfulness opinion {self.truthfulness_opinion}\n' \
               f'\tactive: {self.is_active}\n' \
               f'\tstate: {self.state}'
