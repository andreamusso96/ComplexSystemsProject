# Code 

This folder contains the code for the model and for the experiments/simulations.

### `model`
The folder `model` contains the classes where the considered model is implemented. The most central classes are
* `News`: Represents the news
* `Agent`: Represents the agents which can share the news
* `World`: Combines the agents and a network and allows for the simulation of the interactions betweeen the agents according to the connections in the network.

The remaining classes are either used to store the simulation data or for the visualization of the network.

### `experiments`
In the `experiments` folder we added Jupyter notebooks which contain the experiments we conducded. 
* `agent_phase_diagrams`: Contains phase diagrams for the cascade size depending on different model parameters
* `animation_example`: Contains an example on how to create an animation.
* `grap_structure`: Contains the experiments for **Q1** concerning the graph structure.
* `greedy_evaluation`: Contains experiments for **Q2** concerning the best choice of initial spreaders.
* `multiple_news`: Contains experiments for **Q2** concerning the behaviour of two different news in a network with the focus on the inital spreaders.
* `multiple_news_delay`: Contains experiments for **Q2** concerning the behaviour of the different news in a network with the focus on the the delay within which the news are launched.

Before running the code you have to install the requirements. You can use the `requirements.txt` file which is included in this folder, using
```
pip install -r requirements.txt
```
