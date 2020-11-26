import numpy as np


class News:
    def __init__(self, name, sensation, decay_parameter):
        """

        :param name: integer, name of the news
        :param sensation: float in [0,1], measures how much the news is sensational
        :param decay_parameter: float, measures how much the sensationality of the news decays with time.
        """
        self.name = name
        self.sensation = sensation
        self.decay_parameter = decay_parameter
        self.time_out = 0

    def update(self):
        """
        Updates the parameters of the news. That is, it increases by one the time the news has been out and it decreases
        the sensationality of the news via the decay parameter.
        """
        self.sensation = self.sensation * np.exp(-self.decay_parameter * self.time_out)
        self.time_out = self.time_out + 1

    def __str__(self):
        info_news_string = 'News: ' + str(self.name) + ', sensation: ' + str(self.sensation) + ', decay parameter: ' + str(self.decay_parameter)
        return info_news_string

    def __repr__(self):
        info_news_string = 'News: ' + str(self.name) + ', sensation: ' + str(self.sensation) + ', decay parameter: ' + str(self.decay_parameter)
        return info_news_string
