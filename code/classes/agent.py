""" Agent class """
import numpy as np
from news import News


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
        compute_truth_likelihood()
            computes the truth likelihood of the news
        compute_excitement(news)
            computes the excitement score of the news
        is_sharing(news)
            returns True if the agent will share the news

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
        
        truth_likelihood = (np.random.rand()-0.5)/100  # adding 1% random stochastic noise
        for provider in providers:
            if provider.has_shared:
                truth_likelihood += trust_in_providers[providers.index(provider)]  
        
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

        if not self.has_shared and self.compute_excitement(news, compute_truth_likelihood(providers, trust_in_providers)) >= self.share_threshold:
            self.has_shared = True
            return True
        return False

    def __str__(self):
        return f'Agent: \n' \
               f'\tshare threshold: {self.share_threshold}\n' \
               f'\ttruth weight {self.truth_weight}\n' \
               f'\talready shared news: {self.has_shared}'
