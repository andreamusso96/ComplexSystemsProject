import networkx as nx
from graphplot import ColorMaps
import matplotlib.pyplot as plt
from matplotlib.patches import ArrowStyle
from matplotlib.animation import FuncAnimation
import matplotlib
import numpy as np
from matplotlib.patches import Patch

plt.rcParams['animation.ffmpeg_path'] = '/Users/andreamusso/opt/anaconda3/envs/COSS/bin/ffmpeg'


class Plotting:

    def __init__(self, simulation):
        self.simulation = simulation
        self.color_values_nodes = self.init_color_values_nodes()
        self.legend = self.init_legend()

        self.animation_figure, self.animation_axis = plt.subplots(1, 1)
        self.animation_figure.set_size_inches(12, 12)

    def init_color_values_nodes(self):
        # Color values
        colors = np.linspace(0, 1, len(self.simulation.world.news) + 2)  # All possible color value for all news
        color_values = {'ignorant': ColorMaps.coolwarm(colors[0]),
                        'inactive': ColorMaps.coolwarm(
                            colors[1])}  # Create a dictionary key = state of agent, value = color of that state
        counter = 2
        for n in self.simulation.world.news.values():
            color_values[n.name] = ColorMaps.coolwarm(
                colors[counter])  # Complete the dictionary with (name_news, color) pairs for active nodes
            counter = counter + 1

        return color_values

    def init_legend(self):
        legend_elements = []
        for state in self.color_values_nodes:
            legend_elements.append(Patch(facecolor=self.color_values_nodes[state], label=state))

        return legend_elements

    def plot_world(self, world):
        fig, ax = plt.subplots(1, 1)
        fig.set_size_inches(12, 12)

        nx.draw_networkx(world.graph,
                         pos=nx.circular_layout(world.graph),
                         ax=ax,
                         arrowstyle=ArrowStyle.CurveFilledB(head_length=0.5, head_width=0.3),
                         arrowsize=max(-0.04 * world.graph.order() + 10, 1),
                         with_labels=True,
                         node_size=500,
                         node_color=[self.determine_color_node(agent) for agent in world.agents.values()],
                         alpha=0.8,
                         linewidths=0.0,
                         width=0.2)

        ax.legend(handles=self.legend)

        return fig, ax

    def determine_color_node(self, agent):
        color_node = self.color_values_nodes['ignorant']
        if agent.is_active():
            for news_name in agent.states:
                if agent.states[news_name] == 2:
                    color_node = self.color_values_nodes[news_name]
        else:
            for news_name in agent.states:
                if agent.states[news_name] == 1:
                    color_node = self.color_values_nodes['inactive']

        return color_node

    def animate(self, frames=10, interval=1000, path='animation'):
        animation = FuncAnimation(self.animation_figure, self._next_frame, init_func=self.init_animation, frames=frames,
                                  interval=interval)
        animation.save(path + '.mp4', writer='ffmpeg')

    def init_animation(self):
        return self.animation_axis.plot()

    def _next_frame(self, t):
        """Calls update function and then draws the graph at frame n as part of the animation."""
        print(t, end='\r')
        self.animation_axis.clear()
        world = self.simulation.simulation_data[t]
        nx.draw_networkx(world.graph,
                         pos=nx.circular_layout(world.graph),
                         ax=self.animation_axis,
                         arrowstyle=ArrowStyle.CurveFilledB(head_length=0.5, head_width=0.3),
                         arrowsize=max(-0.04 * world.graph.order() + 10, 1),
                         with_labels=True,
                         node_size=500,
                         node_color=[self.determine_color_node(agent) for agent in world.agents.values()],
                         alpha=0.8,
                         linewidths=0.0,
                         width=0.2)
        self.animation_axis.legend(handles=self.legend)
        self.animation_axis.set_title('Frame ' + str(t))
        return self.animation_axis.plot()
