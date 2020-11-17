import unittest

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import Agent
from news import News


class AgentTestClass(unittest.TestCase):
    def setUp(self):
        share_threshold = 0.5
        truth_weight = 0.8

        self.news = News(fitness=0.4, truth_value=-1)
        self.agent = Agent('1', share_threshold, truth_weight)
        self.providers = [Agent('2', share_threshold, truth_weight), Agent('3', share_threshold, truth_weight)]
        self.trust_in_providers = {'2': 0.8, '3': 0.2}

    def test_activation_when_providers_not_active(self):
        self.assertFalse(self.agent.activates(self.news, self.providers, self.trust_in_providers))

    def test_activation_when_providers_active(self):
        for agent in self.providers:
            agent.activate()

        self.assertTrue(self.agent.activates(self.news, self.providers, self.trust_in_providers))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AgentTestClass)
    unittest.TextTestRunner(verbosity=2).run(suite)
