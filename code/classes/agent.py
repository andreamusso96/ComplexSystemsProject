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
        has_shared: bool
            if the agent has already shared the news

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

    def __init__(self, share_threshold, truth_weight):
        """
        Represents an agent in the network

        :param share_threshold: float in [0, 1]
            how much excitement about a news an agent needs before he shares it.
        :param truth_weight: float in [0, 1]
            how important it is that the news have a high truth likelihood
        """
        assert 0 <= share_threshold <= 1, 'Invalid value for share_threshold. Value should be between 0 and 1'
        assert 0 <= truth_weight <= 1, 'Invalid value for truth_weight. Value should be between 0 and 1'

        self.share_threshold = share_threshold
        self.truth_weight = truth_weight
        self.has_shared = False
        self.activatable = False

    def compute_truth_likelihood(self, providers, trust_in_providers):
        """
        Computes the truth likelihood of the news based on the trust in the information providers

        :param providers: list (list of Agents)
            represents the information providers
        :param trust_in_providers: numpy.ndarray (normalized)
            represents the trust in the information providers
        :return: float
            Truth likelihood of the news
        """
        assert np.isclose(1, np.sum(trust_in_providers)), 'Invalid value for trust_in_providers. Array should be normalized'

        sharing_providers = [idx for idx, provider in enumerate(providers) if provider.has_shared]
        return np.sum(trust_in_providers[sharing_providers]) + (np.random.rand()-0.5)/100  # adding 1% random stochastic noise

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
        
        return (self.truth_weight * truth_likelihood + (1 - self.truth_weight) * news.fitness) * np.exp(-news.time)

    def is_sharing(self, news, providers, trust_in_providers):
        """
        If the agent will share the news.

        Functions returns True if
         - the agent has not shared the news before
         - and, the excitement score is bigger than the share threshold

        :param news: News
            News that is shared in the network
        :param providers: list (list of Agents)
            represents the information providers
        :param trust_in_providers: numpy.ndarray (normalized)
            represents the trust in the information providers
        :return: bool
            If the agent shares the news
        """
        assert len(providers) == len(trust_in_providers), 'provider and trust_in_providers must have the same length'

        if self.has_shared or not self.activatable:
            return False

        truth_likelihood = self.compute_truth_likelihood(providers, trust_in_providers)
        excitement_score = self.compute_excitement(news, truth_likelihood)

        if excitement_score >= self.share_threshold:
            return True
        return False

    def update(self):
        """
        Update the state of the agent.

        Sets the has_shared attribute to True.
        """
        self.has_shared = True

    def make_activatable(self):
        self.activatable = True

    def __str__(self):
        return f'Agent: \n' \
               f'\tshare threshold: {self.share_threshold}\n' \
               f'\ttruth weight {self.truth_weight}\n' \
               f'\talready shared news: {self.has_shared}'
