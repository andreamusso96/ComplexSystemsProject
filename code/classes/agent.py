""" Agent class """
import numpy as np
import math

class Agent:
    """
    Represents an agent in the network

    Attributes:
        share_threshold: float between 0 and 1
            how much excitement about a news an agent needs before he shares it.
        truth_likelihood: float between 0 and 1
            how much the agent believes in the news. If the value is 0 the agent is sure the news is false.
        truth_weight: float between 0 and 1
            how important it is for the agent that the news have a high truth likelihood.
        trust_in_providers: numpy.ndarray (normalized)
            represents the trust in the information providers of the agent.
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

    def __init__(self, share_threshold, truth_likelihood, truth_weight, trust_in_providers):
        """
        Represents an agent in the network

        :param share_threshold: float in [0, 1]
            how much excitement about a news an agent needs before he shares it.
        :param truth_likelihood: float in [0, 1]
            how much the agent believes in the news.
        :param truth_weight: float in [0, 1]
            how important it is that the news have a high truth likelihood
        :param trust_in_providers: numpy.ndarray (normalized)
            represents the trust in the information providers
        """
        assert 0 <= share_threshold <= 1, 'Invalid value for share_threshold. Value should be between 0 and 1'
        assert 0 <= truth_likelihood <= 1, 'Invalid value for truth_likelihood. Value should be between 0 and 1'
        assert 0 <= truth_weight <= 1, 'Invalid value for truth_weight. Value should be between 0 and 1'
        assert np.isclose(1, np.sum(trust_in_providers)), 'Invalid value for trust_in_providers. Array should be normalized'

        # Constructor 
        self.share_threshold = share_threshold
        self.truth_likelihood = truth_likelihood
        self.truth_weight = truth_weight
        self.trust_in_providers = trust_in_providers
        self.has_shared = False
        pass

    def compute_truth_likelihood(self):
        """
        Computes the truth likelihood of the news based on the trust in the information providers
 
        :return: float
            Truth likelihood of the news
        """
        
        # one should before set to 0 the components in trust_in_providers which providers are not sharing the news, how ?
        self.truth_likelihood = np.sum(self.trust_in_providers)+ (np.random([1])-0.5)/100
        # adding 1% random stochastic noise
        return self.truth_likelihood
        
        
        pass

    def compute_excitement(self, news):
        """
        Computes the excitement score of the news based on its truth likelihood and fitness

        :param news: News
            News that is shared in the network
        :return: float
            Excitement score of the news
        """
        
        return (self.truth_weight * self.compute_truth_likelihood(self) + (1-self.truth_weight) * news.fitness) * math.exp(- news.time)
        # assuming news has attributes time (how much times has been around) and fitness
        
        pass

    def is_sharing(self, news):
        """
        If the agent will share the news.

        Functions returns True if
         - the agent has not shared the news before
         - and, the excitement score is bigger than the share threshold

        :param news: News
            News that is shared in the network
        :return: bool
            If the agent shares the news
        """
        # Sharing logic
        if self.has_shared == True: 
            return False
        if self.compute_excitement(self, news) >= self.share_threshold:
            self.has_shared = True
            return True 
        else:
            return False
        
        pass

    def __str__(self):
        return f'Agent: \n' \
               f'\tshare threshold: {self.share_threshold}\n' \
               f'\ttruth likelihood {self.truth_likelihood}\n' \
               f'\ttruth weight {self.truth_weight}\n' \
               f'\ttrust in information providers {self.trust_in_providers}\n' \
               f'\talready shared news: {self.has_shared}'
