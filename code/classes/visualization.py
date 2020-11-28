import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import ArrowStyle
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.patches import Patch

from agent import AgentState
from color_maps import ColorMaps


class Visualization:

    def __init__(self, simulation):
        """
        :param simulation: class Simulation, the simulation you want to plot
        """
        self.simulation = simulation

        # Color values of the nodes to plot the graph of the simulation
        self.color_values_nodes = self.init_color_values_nodes()

        # Legend for plotting the graph of the simulation
        self.legend = self.init_legend()

        # Figure on which one executes the animation
        self.animation_figure, self.animation_axis = plt.subplots(1, 1)
        self.animation_figure.set_size_inches(12, 12)

    def init_color_values_nodes(self):
        """
        Assigns a color to each state a node can be in. To simplify matters we assume that there is one color all
        ignorant nodes and one color for all inactive nodes (no matter the news they are inactive about).

        :return: color_values: dictionary, key = name of news/ ignorant/ inactive, value = rgb triple to color the node\
        """
        # Create possible color values
        colors = np.linspace(0, 1, len(self.simulation.world.news) + 2)

        # Initialise colors of ignorant and inactive nodes
        color_values = {
            'ignorant': ColorMaps.coolwarm(colors[0]),
            'inactive': ColorMaps.coolwarm(colors[1])
        }

        # Complete the dictionary with (name_news, color) pairs for active nodes wrt to name_news
        counter = 2
        for n in self.simulation.world.news.values():
            color_values[n.name] = ColorMaps.coolwarm(colors[counter])
            counter = counter + 1

        return color_values

    def init_legend(self):
        """
        Creates the legend for plotting graphs (i.e. to each possible color_value_nodes we associate a label telling us
        what that color means

        :return: list of Patch object (see matplotlib), this list is exactly what the legend needs
        """
        legend_elements = []
        for state in self.color_values_nodes:
            legend_elements.append(Patch(facecolor=self.color_values_nodes[state], label=state))

        return legend_elements

    def plot_world(self, world):
        """
        :param world: class World, the world we want to plot
        :return: fig, ax:  a figure and an axes (matplotlib), these contain the plot of the world
        """
        # Declare figure and axis
        fig, ax = plt.subplots(1, 1)
        fig.set_size_inches(12, 12)

        # Draw graph (see draw_networkx for all possible parameters)
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

        # Add a legend to the plot
        ax.legend(handles=self.legend)

        return fig, ax

    def determine_color_node(self, agent):
        """
        Determines the color a node in the graph should have based on the state of the agent representing that node.

        :param agent: Agent class, the agent of whom we want to determine the color
        :return: a triple rgb, with the color with which the agent should be colored in the graph
        """
        # Initially, the agent is colored as an ignorant agent by default
        color_node = self.color_values_nodes['ignorant']

        # Color the agent with the color corresponding to the news wrt which he is active, else color as inactive
        if agent.is_active():
            color_node = self.color_values_nodes[agent.name_news_active()]
        else:
            # Color the agent as inactive if he is inactive wrt at least one news
            for news_name in agent.states:
                if agent.states[news_name] == AgentState.INACTIVE:
                    color_node = self.color_values_nodes['inactive']

        return color_node

    def animate(self, frames, interval=1000, path='animation'):
        """
        Creates an animation of the network dynamics (i.e. graph with nodes changing colors) and then saves it in path

        :param frames: integer, number of frames the animation should last
        :param interval: integer, speed of the animation 0 = very fast, 1000 = slow
        :param path: string, the path where the animation should be saved (mp4 file).
        """
        # We use the class FuncAnimation from matplotlib. Basically, what happens is that at every frame,
        # the function self._next_frame is called and the return from that function is plotted.
        animation = FuncAnimation(self.animation_figure, self._next_frame, init_func=self.init_animation, frames=frames,
                                  interval=interval)
        # Saves animation at path
        animation.save(path + '.mp4', writer='ffmpeg')

    def init_animation(self):
        """
        Initialises the animation (it tells the animation function what it should plot, self.animation_axis.plot())
        """
        return self.animation_axis.plot()

    def _next_frame(self, t):
        """
        Creates plot for the next frame in the animation.

        :param t: integer, the time step in the animation
        :return: matplotlib.plot, a plot which is the next frame in the animation
        """
        print(t, end='\r')
        # Clear the axis from the previous plot
        self.animation_axis.clear()

        # Fill the axis with the new plot
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

        # Add legend and title
        self.animation_axis.legend(handles=self.legend)
        self.animation_axis.set_title('Frame ' + str(t))

        # Return the plot
        return self.animation_axis.plot()
