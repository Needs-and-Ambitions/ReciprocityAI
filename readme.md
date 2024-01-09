# Reciprocity AI
This project allows an artificial decision maker to reciprocate user behavior with kind or unkind actions. Although only a proof of concept, the project shows that an AI can be given human-like traits by modifying its objective function. The capability to reciprocate user behavior is useful in all kinds of situations, first and foremost negotiations between user and AI.


## Theoretical Background
The algorithm assumes an objective function ("utility") that reflects other-regarding preferences according to the reciprocity model by Charness & Rabin (2002). Let $m$ and $o$ respectively denote the payoffs of the decision maker ("mine") and the user ("other"). The decision maker's objective function $U_m$ can then be defined piecewise by
$$U_m = a\cdot m + r\cdot (1-a)\cdot o$$   
if   
$$m \ge o$$
and
$$U_m = b\cdot m + r\cdot (1-b)\cdot o$$   
if   
$$m < o$$
where $a$, $b$, and $r$ are real numbers.

Kerschbamer (2015) distinguishes nine preference types depending on the choice of parameters $a$ and $b$ (letting $r = 1$). The additional kindness parameter $r$ changes the AI's preferences in reaction to kind or unkind actions of the user. Specifically, $r$ increases (decreases) if $m > (<) o$.

If $a=b=1$, the decision maker is "selfish" so that $U_m=m$, independent of the user's payoff $o$ and kindness $r$. 


## Teaching the AI to be kind
The file `main.py` describes a simple reinforcement learning algorithm based on Q learning that adapts to opponent behavior in a burden-sharing task. The task is to jointly allocate a workload in hours between the AI and the opponent. Each agent, AI and opponent, can work from 0, 2, 4, 8 to 10 whole hours each period. Working is costly, though, with 1 hour costing the AI $1 and the opponent $3; the AI is more efficient. If the total sum of working hours in a given period equals or exceeds 8 hours, each agent receives a completion bonus of $25 (minus the cost of working).

There are any number of ways in which the target workload of 8 hours per period can be divided among the two agents. This is therefore a coordination problem. To complicate matters, different social norms can motivate different allocations, e.g. equal contributions (4,4) or equal cost of working (6,2).

The standard setup has a human agent (in the role of opponent) performing this task repeatedly with the AI until a stable agreement is reached. The AI uses Q learning to

* reach an allocation whose sum equals 8 hours (coordination) and
* adapt kindness $r$ in reaction to earned payoffs.

Kindness $r$ influences the AI's other-regarding preferences $U_m$ and thus the utility of each allocation of the workload. In particular, the Q values of the learning algorithm are updated by using utility as reward. Default starting parameters set $0 < a , b < 1$ (exact values determined randomly) and $r=0$. Kindness $r$ is updated incrementally by adding or subtracting a sensitivity parameter (set equal to 1); there is no upper or lower bound.


## References
* G. Charness & M. Rabin (2002): Understanding social preferences with simple tests, Quarterly Journal of Economics, Vol. 117, No. 3, pp. 817-869.
* R. Kerschbamer (2015): The geometry of distributional preferences and a non-parametric identification approach: The Equality Equivalence Test, European Economic Review, Vol. 76, pp. 85-103.

## User manual
The allocation game can be started by running `main.py` in a Python console.

To choose your ("Player H") working hours, select the corresponding number in the field "Hours H", then click the "Calculate" button. This will generate the AI's ("Player L") workload for that period. Also displayed are the resulting payoffs.

The game ends automatically if the same allocation of hours occurs in five consecutive rounds. This triggers an exit window with several game statistics. Click the button to end the program.

At any other time, you can access the "File" menu to restart the game via the "Reset" option or to "Exit" the game manually. Alternatively, the "History" menu can be used to generate plots of results from previous periods such as "Total contribution" or "Individual payoffs". The "Reward" and "Kindness" plots may offer helpful information about the AI's learning progress.

## How to contribute
There are several ways in which the program could be adapted or expanded:
* Most real-life negotiations are much more complex than the burden-sharing problem described here. It might therefore be interesting to add more features to the game, such as "cheap talk" between user and AI.
* The current graphics are rather plain. Add some colors. Maybe replace the kindness function with a suitable range of emojis (e.g. from angry to happy).
* Learning is more difficult if there are more actors or more possible actions, maybe too difficult for Q learning. How do more powerful learning algorithms (e.g. Deep Q Learning) handle such a task.
* Similarly: How good are different computer algorithms at playing the allocation game? (First define a suitable measure of "goodness".)
* Use additional user data to determine if behavior is kind or unkind. Do they use insulting language or make compliments (sentiment analysis)? Are they honest or dishonest (pattern recognition applied to physical cues)?

## List of files
* `main.py`: Main file (allocation game)
* `project_functions.py`: Auxiliary file (functions to plot dynamic variables)
* `readme.md`: This file

Copyright (C) 2024, Needs and Ambitions
