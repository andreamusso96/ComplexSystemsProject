#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[50]:


# I suppose the idea is to have a sensation decay as follow:
# sensation(t)= initial_sensation * exp( -c*t)
# but in this case the result by updating the news 20 times is much more smaller than expected
k=20

initial_sensation=1 #set maximal value for initial sensation
n = News(1, initial_sensation, 1)

for i in range(k):
    n.update()
#after time +20
print(n.sensation)
print(initial_sensation*np.exp(-k))#expected result


# In[ ]:


# I would change the line in news.py as follow
# self.sensation = self.sensation * np.exp(-self.decay_parameter)

