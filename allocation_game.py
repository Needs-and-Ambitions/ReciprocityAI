"""
    Allocation Problem - Auxiliary file with game specifications

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

"""Setup for environment: allocation game against Qlearning algorithm"""


class AllocationGame:
    def __init__(self,
                 alpha0=0.05,
                 decay=0.005,
                 gamma_q=0.9,
                 exploration_periods=100,
                 max_periods=1000,
                 sensitivity=0.1,
                 player_type="low"):
        super(AllocationGame, self).__init__()
        self.rewards_l = [
            [0.0, 0.0, 0.0, 0.0, 25.0, 25.0],  # own contribution = 0
            [-2.0, -2.0, -2.0, 23.0, 23.0, 23.0],  # own contribution = 2
            [-4.0, -4.0, 21.0, 21.0, 21.0, 21.0],  # own contribution = 4
            [-6.0, 19.0, 19.0, 19.0, 19.0, 19.0],  # own contribution = 6
            [17.0] * 6,  # own contribution = 8
            [15.0] * 6  # own contribution = 10
        ]
        self.rewards_h = [  # contribution 3x as costly as l
            [0.0, 0.0, 0.0, 0.0, 25.0, 25.0],  # own contribution = 0
            [-6.0, -6.0, -6.0, 19.0, 19.0, 19.0],  # own contribution = 2
            [-12.0, -12.0, 13.0, 13.0, 13.0, 13.0],  # own contribution = 4
            [-18.0, 7.0, 7.0, 7.0, 7.0, 7.0],  # own contribution = 6
            [1.0] * 6,  # own contribution = 8
            [-5.0] * 6  # own contribution = 10
        ]

        self.player_type = player_type  # "high" and "low" players have different marginal contribution costs

        if self.player_type == "low":
            self.rewards_matrix = [self.rewards_l] * 6  # same payoff matrix for each of 6 states
        else:
            self.rewards_matrix = [self.rewards_h] * 6

        self.possible_actions = [[0, 1, 2, 3, 4, 5]] * 6  # own contribution each state
        self.Q_values = np.full((6, 6), 0)  # create 6x6 matrix with entries of zero

        # hyperparameters
        self.alpha0 = alpha0  # initial learning rate
        self.decay = decay  # decay of learning rate
        self.gamma_q = gamma_q  # discounting factor
        self.exploration_periods = exploration_periods  # length of exploration phase
        self.max_periods = max_periods  # maximum length of game
        self.sensitivity = sensitivity  # increment of changes to kindness

        # preference parameters
        self.a = np.random.rand()  # decision weight for advantageous inequality, "greed"
        self.b = np.random.rand()  # d.w. for disadvantageous ineq., "envy"

        # initialization
        self.count = 0
        self.contribution_h_old = 0
        self.contribution_l_old = 0
        self.period = 0
        self.r = 0  # initial kindness

    # function that allows the algorithm to randomize in order to experience different game outcomes
    def epsilon_greedy_policy(self, state, epsilon):
        if np.random.rand() < epsilon:
            return np.random.choice(self.possible_actions[state])
        else:
            return np.argmax(self.Q_values[state])

    # reset all variables
    def reset(self):
        self.count = 0  # change to global variable and remove from class?
        self.contribution_h_old = 0
        self.contribution_l_old = 0
        self.a = np.random.rand()
        self.b = np.random.rand()
        self.r = 0
        self.period = 0

        for state_q, actions_q in enumerate(self.possible_actions):
            self.Q_values[state_q, actions_q] = 0.0

    # advance the game one period
    def calculate(self, action):
        epsilon = max(1 - self.period / self.exploration_periods, 0.01)  # determine probability of random choice

        # determine computer agent's next action, accounting for player type
        if self.player_type == "low":
            state_q = int(self.contribution_h_old / 2)  # determine previous state
            action_q = self.epsilon_greedy_policy(state_q, epsilon)  # determine next action

            contribution_l = 2 * action_q
            contribution_h = 2 * action  # user's input
            own_costs = contribution_l
            other_costs = 3 * contribution_h
        else:
            state_q = int(self.contribution_l_old / 2)  # determine previous state
            action_q = self.epsilon_greedy_policy(state_q, epsilon)  # determine next action

            contribution_h = 2 * action_q
            contribution_l = 2 * action  # user's input
            other_costs = contribution_l
            own_costs = 3 * contribution_h

        next_state = int(action / 2)  # convert user input into action

        # update endgame counter
        if contribution_h == self.contribution_h_old and contribution_l == self.contribution_l_old:
            self.count += 1
        else:
            self.count = 0

        # calculate reward and payoffs
        if contribution_h + contribution_l >= 8:
            bonus = 25
        else:
            bonus = 0

        own_payoff = bonus - own_costs
        other_payoff = bonus - other_costs

        # determine computer agent's utility (cf. Charness & Rabin, 2002, QJE) and update kindness
        if own_payoff >= other_payoff:  # user is kind to agent
            reward_q = self.a * own_payoff + self.r * (1 - self.a) * other_payoff
            self.r = self.r + self.sensitivity
        else:  # user appears to take advantage of agent
            reward_q = self.b * own_payoff + self.r * (1 - self.b) * other_payoff
            self.r = self.r - self.sensitivity

        next_value = np.max(self.Q_values[next_state])  # determine best response to user's current action
        alpha = self.alpha0 / (1 + self.period * self.decay)  # determine learning rate
        self.Q_values[state_q, action_q] *= 1 - alpha  # discount previous Q values
        self.Q_values[state_q, action_q] += alpha * (reward_q + self.gamma_q * next_value)  # update Q values

        # prepare next period
        self.contribution_h_old = contribution_h
        self.contribution_l_old = contribution_l
        self.period += 1

        # check if game should be terminated
        if self.count >= 5 or self.period == self.max_periods:
            done = True
        else:
            done = False

        return other_payoff, own_payoff, contribution_h, contribution_l, reward_q, self.r, self.count, self.period, done
