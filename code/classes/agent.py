""" Agent class """
import numpy as np


class Agent:
    """
    Represents an agent in the network

    Attributes:
        share_threshold: float between 0 and 1
            how much excitement about a news an agent needs before he shares it.
        truth_weight: float between 0 and 1
            how important it is for the agent that the news have a high truth likelihood.
        is_active: bool
            if the agent is active (has shared the news)
        activatable: bool
            if the agent can be activated (if is_active can be set to True)

    Methods:
        compute_truth_likelihood(provider, trust_in_providers)
            computes the truth likelihood of the news
        compute_excitement(news, truth_likelihood)
            computes the excitement score of the news
        is_sharing(news)
            returns True if the agent will share the news
        update()
            updates the state of the agent
    """

    def __init__(self, name, share_threshold, truth_weight):
        """
        Represents an agent in the network

        :param share_threshold: float in [0, 1]
            how much excitement about a news an agent needs before he shares it.
        :param truth_weight: float in [0, 1]
            how important it is that the news have a high truth likelihood
        """
        assert 0 <= share_threshold <= 1, 'Invalid value for share_threshold. Value should be between 0 and 1'
        assert 0 <= truth_weight <= 1, 'Invalid value for truth_weight. Value should be between 0 and 1'

        self.name = name
        self.share_threshold = share_threshold
        self.truth_weight = truth_weight
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
        assert np.isclose(1, np.sum(list(trust_in_providers.values()))), 'Invalid value for trust_in_providers. Array ' \
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
        excitement_score = (self.truth_weight * truth_likelihood + (1 - self.truth_weight) * news.fitness) * np.exp(
            -0.01 * news.time)
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
        self.is_active = True

    def __str__(self):
        return f'Agent: \n' \
               f'\tshare threshold: {self.share_threshold}\n' \
               f'\ttruth weight {self.truth_weight}\n' \
               f'\tactive: {self.is_active}'
