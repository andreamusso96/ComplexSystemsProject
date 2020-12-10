# Complex Social Systems - HS2020

> * Group Name: FATTJ
> * Group participants names: Falvio Dalessi, Andrea Musso, Thomas Rupf, Julian Schuhmacher, Tristan Strumann
> * Project Title: The spreading of (fake) news in social networks

## General Introduction
The spreading of false news on social media has become a major issue in recent years. The uncontrolled circulation of biased and false information is eroding fundamental pillars of liberal societies as fair elections, free speech and public debate, thereby leading to increasing division and polarisation. This issue has provoked wide interest in the scientific community, leading to many interdisciplinary research projects (see for instance [1], [2], [3]). However, "false news science" is still in its infancy and a solution to the false news problem is still far from sight. The aim of our project is to provide a small contribution to the understanding of this problem, via agent based models and simulations.

## The Model

We fix a directed graph $G = (V,E)$. Our goal is to model the diffusion of news within this directed graph. To each node $v \in V$, we associate two sets of nodes: (i) the set $P(v)$ of nodes with an edge directed towards $v$ (i.e. $w \rightarrow v$), which we call $v$'s \textbf{information providers}; (ii) the set $R(v)$ of nodes with an edge directed from $v$ towards them (i.e. $v \rightarrow w$), which we call $v$'s \textbf{information receivers}. The node $v$ can be in three states:  (i) \textbf{ignorant}: $v$ has not heard of the news yet (i.e. no information provider of $v$ is active); (ii) \textbf{inactive}:  $v$ has heard about the news but has not yet activated (i.e. at least one information provider of $v$ is active but $v$ is not active); (iii) \textbf{active}: $v$ has heard about the news and has activated  (i.e. at least one information provider of $v$ is active and $v$ is active). 
The idea is that an active node shares the news with his neighbours, an inactive node knows about the news but does not share it and an ignorant node does not know about the news. \\

How do nodes become active? Our model is based on the following simple principle: the probability of a node $v$ becoming active increases as more and more of his information providers become active. More precisely, each node $v$ gives a weight $r_{v,w}$ to all his information providers $w \in P(v)$. These weights should satisfy $\sum_{w \in P(v)} r_{v,w} = 1$. The value of $r_{v,w}$ represents the influence that information provider $w$ has on the decision of $v$ to become active. This model belongs to a well known class of models for innovation diffusion called threshold models \cite{watts2002simple}. \\

The activation dynamics run as follows. First, each node $v$ chooses a threshold $\phi_v \in [0,1]$ and an independence parameter $\alpha_v \in [0,0.1]$ via the uniform distribution; the threshold represents the weighted fractions of $v$'s information providers which have to be active in order to activate $v$; the independence parameter is meant to model the fact $v$'s decision is not totally dependent on the actions of his information providers. Then, we fix a set nodes $A_0$, which are initially active. These nodes are the initial spreaders of a news $N$ which has sensation $\rho \in [0,1]$; sensation parametrises how much a news is attractive. For each time step $t$ the process unfolds as follows:
\begin{enumerate}
\item If $t = 0$ all nodes in $V \setminus A_0$ are ignorant and all nodes in $A_0$ are active.
\item If $t > 0$ every node computes his excitement score $E_v$ with respect to the news $N$, which is given by:
\begin{align*}
E_v\Big((r_{v,w})_{w \in P(v)}, \alpha_v \Big) =  (1-\alpha_v)\sum_{w \in P(v)} \delta_a(w)r_{v,w}
\end{align*}
where $\delta_a(w) = 1$ if $w$ is active and zero otherwise. Next,
\begin{enumerate}
\item Any ignorant node with an active neighbour becomes inactive.
\item We activate any node $v$ with an excitement score $E_v$ satisfying:
\begin{align*}
E_v\Big((r_{v,w})_{w \in P(v)}, \alpha_v \Big) \geq \phi_v(1-\rho).
\end{align*}
\item Any active nodes with an excitement score $E_v$ satisfying $E_v < \phi_v(1-\rho)$ becomes inactive.
\end{enumerate}
Moreover, we update the sensation of the news by setting $\rho_{t+1} = \rho_{t}e^{-ct}$ for some constant $c$. This models the fact that a news becomes less sensational with time.
\item The dynamics end when no nodes change state for one time step.
\end{enumerate}

The graph model we use is a scale free network constructed via the algorithm proposed in the networkx package. The weights $r_{v,w}$  placed on edges are computed as follows. Node $v$ gives a weight:
\[ r_{v,w} = \frac{d_{out}(w)}{\sum_{u \in P(v) }d_{out}(u)} \]
to information provider $w$. This models the fact that nodes with higher out degree (i.e. with more information receivers) are considered more influential than nodes with low out degree. \\

Our main object of study will be the cascade size of a given news $N$, which we denote by $C(N)$. For us, cascade size is a number in $[0,1]$ computed as the ratio of active nodes over total nodes.


## Fundamental Questions

With our model and code we aspire to answer specific cases of the following three broad research questions:
* **Q1:** How does network structure impact the spreading of a news?
* **Q2:** What impact does the choice of initial spreaders have on the spreading of competing news? What is the best choice of spreaders when one aims to maximise cascade size?

## Expected Results

(What are the answers to the above questions that you expect to find before starting your research?)


## References 

[1]  Michela Del Vicario, Alessandro Bessi, Fabiana Zollo, Fabio Petroni, Antonio Scala,Guido Caldarelli, H Eugene Stanley, and Walter Quattrociocchi, The  spreading of misinformation online, Proceedings of the National Academy of Sciences, 113(2016), 3, 554–559, National Acad Sciences

[2]  Soroush Vosoughi, Deb Roy, and Sinan Aral, The spread of true and false news online, Science, 359(2018), 6380, 1146–1151, American Association for the Advancement of Science

[3]  David MJ Lazer, Matthew A Baum, Yochai Benkler, Adam J Berinsky, Kelly M Green-hill,  Filippo  Menczer,  Miriam  J  Metzger,  Brendan  Nyhan, Gordon  Pennycook, and David Rothschild, The science of fake news, Science,359(2018), 6380, 1094–1096, American Association for the Advancement of Science

## Research Methods

(Cellular Automata, Agent-Based Model, Continuous Modeling...) (If you are not sure here: 1. Consult your colleagues, 2. ask the teachers, 3. remember that you can change it afterwards)


## Other

(mention datasets you are going to use)
