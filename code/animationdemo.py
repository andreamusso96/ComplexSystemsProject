from classes.world import *

num_agents = 50
num_sharing = 1
news_fitness = 0.5
news_truth = 1

frames = 10
interval = 100

path = './Animations/animation'

W = World(num_agents=num_agents, num_sharing=num_sharing, news_fitness=news_fitness, news_truth=news_truth)
W.animate(frames=frames, interval=interval, path=path)