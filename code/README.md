# Code 

This folder contains the code for the model and for the experiments/simulations.

### `model`
The folder `model` contains the classes where the considered model is implemented. The most central classes are
* [`News`](classes/news.py): Represents the news
* [`Agent`](classes/agent.py): Represents the agents which can share the news
* [`World`](classes/world.py): Combines the agents and a network and allows for the simulation of the interactions betweeen the agents according to the connections in the network.

The remaining classes are either used to store the simulation data or for the visualization of the network.

### `experiments`
In the `experiments` folder we added Jupyter notebooks and Python files which contain the experiments we conducded. 
* [`agent_phase_diagram.ipynb`](notebooks/agent_phase_diagram.ipynb): Contains phase diagrams for the cascade size depending on different model parameters
* [`animation_example.ipynb`](notebooks/animation_example.ipynb): Contains an example on how to create an animation. Examples included [here](../other/).
* [`graph_structure.ipynb`](notebooks/graph_structure.ipynb): Contains the experiments for **Q1** concerning the graph structure.
* [`greedy_evaluation.ipynb`](notebooks/greedy_evaluation.ipynb): Contains experiments for **Q2** concerning the best choice of initial spreaders.
* [`multiple_news_random.ipynb`](notebooks/multiple_news_random.ipynb) and [`multiple_news_out_degree.ipynb`](notebooks/multiple_news_out_degree.ipynb): Contains experiments for **Q2** concerning the behaviour of two different news in a network with the focus on the inital spreaders where `random` and `out_degree` refer to the way the initial spreader are chosen.
* [`multiple_news_delay.ipynb`](notebooks/multiple_news_delay.ipynb): Contains experiments for **Q2** concerning the behaviour of the different news in a network with the focus on the the delay within which the news are launched.
* [`counternews.py`](notebooks/counternews.py): Creates animation for the experiment when to start counter news. Example included [here](../other/).

Before running the code you have to install the requirements. You can use the `requirements.txt` file which is included in this folder, using
```
pip install -r requirements.txt
```
