""" 
generates an animation for a 2 news
takes very long to run!
saves every frame in folder "animation"
"""
import matplotlib.pyplot as plt
from matplotlib.patches import ArrowStyle
import matplotlib.gridspec as gridspec
import numpy as np
import networkx as nx
from copy import deepcopy

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.agent import Agent
from model.world import World
from model.color_maps import ColorMaps
from model.utils import *
from model.news import News
from model.agent import AgentState

def find_degreecentral_nodes(world, k, blacklist, news):
    degree_centrality = []
    for _ in range(k):
        best = None
        bdeg = -1
        for a in world.graph.nodes():
            if world.agents[a] in degree_centrality or world.agents[a] in blacklist:
                continue
            d = world.graph.out_degree(a)
            if d > bdeg:
                bdeg = d
                best = world.agents[a]
        degree_centrality.append(best)
    s2 = {}
    for agent in degree_centrality:
        s2[agent] = news.name
    return s2

def activate_agents(agents):
    for agent in agents.keys():
        agent.states[agents[agent]] = AgentState.ACTIVE


fake_news = News(0, 0.9, 0.5)
counter_news = News(1, 0.5, 0.1)
news_cycle = {fake_news.name: fake_news, counter_news.name: counter_news}
number_agents = 500
names_agents = [_ for _ in range(number_agents)]
threshold = np.clip(np.random.normal(0.5, 0.1, number_agents), 0.0, 1.0) #mu = 0.5, sigma = 0.1
independence = np.full(number_agents, 0.1)#np.clip(np.random.normal(0.5, 0.1, number_agents), 0.0, 1.0) #mu = 0.5, sigma = 0.1
w = construct_world(names_agents, threshold, independence, news_cycle)
fakenews_spreader = find_degreecentral_nodes(w, 1, [], fake_news)
counternews_spreader = find_degreecentral_nodes(w, 5, [a for a in fakenews_spreader.keys()], counter_news)

steps = 30
delay = 6
fig = plt.figure(figsize=(24,18), dpi=500)
fig.suptitle("Spread of two news with a delay of " + str(delay), fontsize=20)
spec = gridspec.GridSpec(ncols=4, nrows=3, figure=fig)
g_ax = fig.add_subplot(spec[:,:-1])
s_ax = fig.add_subplot(spec[:,-1])
starting_points = {0: fakenews_spreader, delay: counternews_spreader}
layout = nx.spring_layout(w.graph)
for d in starting_points.values():
    for agent in d.keys():
        agent.independence = 1.0 
cascade = lambda agents, news: sum([1 if a.states[news] == AgentState.ACTIVE else 0 for a in agents])
t = []
fake = []
counter = []

for step in range(steps):
    if step in starting_points.keys():
        activate_agents(starting_points[step])
    t.append(step)
    fake.append(cascade(w.agents.values(), 0))
    counter.append(cascade(w.agents.values(), 1))
    s_ax.clear()
    s_ax.set_xlim(0, step + 1)
    s_ax.set_ylim(0, number_agents)
    s_ax.plot(t, fake, "r", label="fake news")
    s_ax.plot(t, counter, "b", label="true news")
    s_ax.set_xlabel("timestep")
    s_ax.set_ylabel("cascade size")
    s_ax.legend()
    
    g_ax.clear()
    clrs = [ColorMaps.coolwarm(1.0) if a in fakenews_spreader.keys() else
            ColorMaps.coolwarm(0.0) if a in counternews_spreader.keys() else
            ColorMaps.coolwarm(0.97) if a.states[0] == AgentState.ACTIVE else 
            ColorMaps.coolwarm(0.02) if a.states[1] == AgentState.ACTIVE else (0.0,0.0,0.0)
            for a in w.agents.values()]

    nx.draw_networkx(w.graph,
                     pos=layout,
                     ax=g_ax,
                     arrowstyle=ArrowStyle.CurveFilledB(head_length=0.5, head_width=0.3),
                     arrowsize=max(-0.04 * w.graph.order() + 10, 1),
                     with_labels=False,
                     node_size=200,
                     node_color=clrs,
                     alpha=0.9,
                     linewidths=0.0,
                     width=0.2)
    plt.savefig("animation/counternews" + str(step) + ".png")
    x = w.update(verbose=True)
    #if x == 0 and step > max(starting_points.keys()): break
    print(step, end=", ", flush=True)
print("done")


