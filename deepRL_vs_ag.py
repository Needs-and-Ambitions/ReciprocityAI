"""
    Allocation Problem - Auxiliary file to train Deep RL algorithm

    The following code is based on an example taken from an online course by Thomas Simonini:
    https://huggingface.co/learn/deep-rl-course/unit4/hands-on

    Specific code elements taken from this example include:
    - the Policy class
    - the reinforce function, except for the section marked as "new elements" and the calculation of returns
        which Hugging Face attributes to https://github.com/Chris1nexus

    All other code elements (and any mistakes introduced by modifying the original code):
    Copyright (C) 2024, Needs and Ambitions

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import numpy as np

from collections import deque

# PyTorch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical

# import auxiliary file to plot evaluation results
import project_functions

# import game environment
from allocation_game import AllocationGame

# create instance of allocation game with set game duration
ag = AllocationGame(max_periods=200)

"Setup for neural network"
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

print(device)

# input
s_size = 3  # state: two observed contribution values plus kindness

# output
eq_user_input = [0, 2, 4, 6, 8, 10]  # action: single contribution
a_size = len(eq_user_input)  # output is mixture over possible actions (mixed strategy)


class Policy(nn.Module):
    def __init__(self, s_size, a_size, h_size):
        super(Policy, self).__init__()
        self.fc1 = nn.Linear(s_size, h_size)  # hidden layer, size left undetermined
        self.fc2 = nn.Linear(h_size, a_size)  # output layer

    def forward(self, x):
        x = F.relu(self.fc1(x))  # ReLU activation function
        x = self.fc2(x)
        return F.softmax(x, dim=1)  # weights are normalized to probabilities

    # function returns action as a number (instead of tensor) and logarithms of mixed-strategy probabilities
    def act(self, state):
        # convert input to tensor, encode as float, change dimension, send to device
        state = torch.from_numpy(state).float().unsqueeze(0).to(device)
        probs = self.forward(state).cpu()
        m = Categorical(probs)  # retrieve mixed-strategy distribution
        action = m.sample()  # sample action based on mixed-strategy distribution
        return action.item(), m.log_prob(action)


def reinforce(policy, optimizer, n_training_episodes, max_t, gamma, print_every):
    # calculate score during training
    scores_deque = deque(maxlen=100)  # record of 100 tries
    scores = []

    for i_episode in range(1, n_training_episodes + 1):
        saved_log_probs = []
        rewards = []
        time_step = 0

        # new elements [START]
        state = np.zeros((s_size, ), dtype=int)  # one [s_size] previous payoff pair(s) of zero

        ag.reset()  # reset allocation game

        for t in range(max_t):  # play the game once
            action, log_prob = policy.act(state)
            saved_log_probs.append(log_prob)

            # input current action into calculate function
            payoff_h, payoff_l, contribution_h, contribution_l, reward_q, r, count, period, done = ag.calculate(action)

            # update state of network
            state = np.array([contribution_h / 5 - 0.5, contribution_l / 5 - 0.5, r])
            rewards.append((payoff_h + payoff_l)/42)
            time_step += 1
            if done:
                break

        # new elements [END]

        # track averages of collected rewards
        scores_deque.append(sum(rewards)/time_step)
        scores.append(sum(rewards)/time_step)

        # calculate the discounted returns
        returns = deque(maxlen=max_t)
        n_steps = len(rewards)

        for t in range(n_steps)[::-1]:
            disc_return_t = returns[0] if len(returns) > 0 else 0
            returns.appendleft(gamma * disc_return_t + rewards[t])

        returns = torch.tensor(returns)
        returns = returns - returns.mean()

        # calculate loss of currently played mixed strategy
        policy_loss = []
        for log_prob, disc_return in zip(saved_log_probs, returns):
            policy_loss.append(-log_prob * disc_return)
        policy_loss = torch.cat(policy_loss).sum()

        # backward induction via gradient descent
        optimizer.zero_grad()
        policy_loss.backward()
        optimizer.step()

        # feedback about learning progress (average scores)
        if i_episode % print_every == 0:
            print("Episode {}\tAverage Score: {:.4f}".format(i_episode, np.mean(scores_deque)))

    return scores


nn_hyperparameters = {
    "h_size": 5,  # size of hidden layer
    "n_training_episodes": 10000,
    "n_evaluation_episodes": 10,
    "max_t": 1000,  # maximum game length (overridden by allocation game)
    "gamma": 0.99,  # discount factor
    "lr": 1e-2,  # learning rate
    "state_space": s_size,
    "action_space": a_size,
}

# Create policy and place it to the device
nn_policy = Policy(
    nn_hyperparameters["state_space"],
    nn_hyperparameters["action_space"],
    nn_hyperparameters["h_size"],
).to(device)
nn_optimizer = optim.Adam(nn_policy.parameters(), lr=nn_hyperparameters["lr"])

# train the neural network
# scores = reinforce(
#     nn_policy,
#     nn_optimizer,
#     nn_hyperparameters["n_training_episodes"],
#     nn_hyperparameters["max_t"],
#     nn_hyperparameters["gamma"],
#     10,
# )

# save the trained model
# torch.save({
#     'model_state_dict': nn_policy.state_dict(),
#     'optimizer_state_dict': nn_optimizer.state_dict()
# }, "deepRL_vs_ag_10000.pt")

# load a saved checkpoint
checkpoint = torch.load("checkpoints/deepRL_vs_ag_10000.pt")
nn_policy.load_state_dict(checkpoint['model_state_dict'])
nn_optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

"Evaluation"

# prepare lists for data collection
totpaydyn = []
indpayH = []
indpayL = []
indcontH = []
indcontL = []
kindness = []
reward_hist = []


def evaluate_agent(max_steps, policy):
    state = np.zeros((s_size, ), dtype=int)  # reset state
    ag.reset()  # reset game

    for step in range(max_steps):  # play the game once and collect same data as GUI version
        action, _ = policy.act(state)

        # input action into calculate function
        payoff_h, payoff_l, contribution_h, contribution_l, reward_q, r, count, period, done = ag.calculate(action)

        # update payoff histories for plots
        totpaydyn.append(payoff_h + payoff_l)
        indpayL.append(payoff_l)
        indpayH.append(payoff_h)
        indcontL.append(contribution_l)
        indcontH.append(contribution_h)
        reward_hist.append(reward_q)
        kindness.append(r)

        if done:
            break

        state = np.array([contribution_h/5 - 0.5, contribution_l/5 - 0.5, r])


evaluate_agent(nn_hyperparameters["max_t"], nn_policy)

# data shown on exit screen of GUI version
# print(round(np.sum(reward_hist) / len(reward_hist), 2))
# print(round(np.sum(totpaydyn) / (len(totpaydyn) * 42), 2))
# print(round(np.sum(indcontH) / len(indcontH), 2))
# print(round(np.sum(indcontL) / len(indcontL), 2))

# plot functions also available in GUI version
# project_functions.diagram1(totpaydyn)  # total payoffs
# project_functions.diagram2(indpayH, indpayL)  # individual payoffs
project_functions.diagram3(indcontH, indcontL)  # individual contributions
# project_functions.diagram4(reward_hist)  # rewards earned by Q learning algorithm
# project_functions.diagram5(kindness)  # kindness
