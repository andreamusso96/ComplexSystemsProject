""" News class """


class News:
    """
    Represents news on the network.

    Make sure to call the update() function to update the state of the news.
    The state may be important to calculate the excitement an Agent has about the news.

    Attributes:
        fitness: float between 0 and 1
            Indicates how 'eye-catching' the news is for its audience
        truth_value: News.REAL or News.FAKE
            the truth value of the news
        time: int
            the number of time steps the news already has been around

    Methods:
        update()
            Updates the state of the news
    """

    # Possible truth values
    REAL = 1
    FAKE = -1

    def __init__(self, fitness, truth_value):
        """
        Represents a news on the network

        :param fitness: float in [0, 1]
            indicates how 'eye-catching' the news is for its audience
        :param truth_value: News.REAL or News.FAKE
            the truth value of the news
        """
        assert 0 <= fitness <= 1, 'Invalid value for fitness. Value should be between 0 and 1'
        assert truth_value in [News.FAKE, News.REAL], 'Invalid value for truth_value. Use constants from News class'

        self.fitness = fitness
        self.truth_value = truth_value
        self.time = 0

    def update(self):
        """ Updates the state of the news """
        self.time += 1

    def __str__(self):
        if self.truth_value == News.FAKE:
            return f'Fake news with fitness {self.fitness}'
        return f'News with fitness {self.fitness}'
