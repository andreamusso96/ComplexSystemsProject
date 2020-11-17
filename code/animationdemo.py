from classes.world import *

num_agents = 100
num_sharing = 1
news_fitness = 0.5
news_truth = 1

frames = 10
interval = 1000

path = 'animation'

W = World(num_agents=num_agents, num_sharing=num_sharing, news_fitness=news_fitness, news_truth=news_truth)
W.animate(frames=frames, interval=interval, path=path)
