"""
    Allocation Problem - Main file

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

# import standard modules
import tkinter as tk
from tkinter import ttk, N, W, S, E, StringVar, Menu, Tk

import numpy as np

# import auxiliary file for plotting dynamic variables
import project_functions

## Preparations for Q learning algorithm

# Actions available to computer agent by "state" (opponent action)
possible_actions = [[0, 1, 2, 3, 4, 5]] * 6  # own contribution each state

# Payoffs by (state, action) pair indicating own and other's contributions
rewards_q = [
    [0.0, 0.0, 0.0, 0.0, 25.0, 25.0],  # own contribution = 0
    [-2.0, -2.0, -2.0, 23.0, 23.0, 23.0],  # own contribution = 2
    [-4.0, -4.0, 21.0, 21.0, 21.0, 21.0],  # own contribution = 4
    [-6.0, 19.0, 19.0, 19.0, 19.0, 19.0],  # own contribution = 6
    [17.0] * 6,  # own contribution = 8
    [15.0] * 6  # own contribution = 10
]

rewards = [rewards_q] * 6  # same payoff matrix for each of 6 states (path independence)

# initialization of Q values
Q_values = np.full((6, 6), -np.inf)  # -np.inf for impossible actions (just in case)
for state, actions in enumerate(possible_actions):
    Q_values[state, actions] = 0.0  # same Q value for all possible (state, action) pairs

# preparation of greedy algorithm for choice sampling
def epsilon_greedy_policy(state, epsilon):
    if np.random.rand() < epsilon:
        return np.random.choice(possible_actions[state])
    else:
        return np.argmax(Q_values[state])

# hyper parameters for learning process
alpha0 = 0.05  # initial learning rate
decay = 0.005  # decay of learning rate
gamma = 0.90  # discounting factor
max_periods = 100  # length of exploration phase
sensitivity = 1  # increment of changes to kindness

# preference parameters
a = np.random.rand()  # decision weight for advantageous inequality, "greed"
b = np.random.rand()  # d.w. for disadvantageous ineq., "envy"

# initialization of variables
period = 0  # number of rounds
contributionHold = 0
contributionLold = 0
r = 0  # kindness
count = 0  # counter for end of program

# empty arrays for plots
totpaydyn = []
indpayH = []
indpayL = []
indcontH = []
indcontL = []
kindness = []
reward_hist = []

# function to calculate the computer agent's decision given previous state (called by user)
def calculate(*args):
    try:
        # call global variables
        global contributionHold
        global contributionLold
        global period
        global r
        global count

        # determine computer agent's next action
        state = int(contributionHold / 2)  # determine previous state

        epsilon = max(1 - period / max_periods, 0.01)  # determine probability of random choice

        action = epsilon_greedy_policy(state, epsilon)  # determine next action

        # determine outcome of actions
        contributionL = 2 * action
        contributionH = float(qH.get())  # user's manual input
        next_state = int(contributionH / 2)  # convert user input into action

        # update end of program counter (increases if allocation remains unchanged)
        if contributionH == contributionHold and contributionL == contributionLold:
            count += 1
        else:
            count = 0

        # calculate reward and payoffs (reaching target contribution awards bonus)
        if contributionH + contributionL >= 8:
            bonus = 25
        else:
            bonus = 0

        payoffH = bonus - 3 * contributionH  # user's payoff
        payoffL = bonus - contributionL  # computer agent's payoff

        # determine computer agent's utility (cf. Charness & Rabin, 2002, QJE) and update kindness
        if payoffL >= payoffH:  # user is kind to agent
            reward = a * payoffL + r * (1-a) * payoffH
            r = r + sensitivity
        else:  # user appears to take advantage of agent
            reward = b * payoffL + r * (1-b) * payoffH
            r = r - sensitivity

        next_value = np.max(Q_values[next_state])  # determine best response to user's current action
        alpha = alpha0 / (1 + period * decay)  # determine current learning rate
        Q_values[state, action] *= 1 - alpha  # discount previous Q values
        Q_values[state, action] += alpha * (reward + gamma * next_value)  # update Q values

        # prepare next period
        contributionHold = contributionH
        contributionLold = contributionL
        period += 1

        # prepare output to user
        time_step.set(int(period))
        payH.set(int(bonus - 3 * contributionH))
        payL.set(int(bonus - contributionL))
        qL.set(int(contributionL))
        counter.set(int(count))

        # update payoff histories for plots
        totpaydyn.append(payoffH + payoffL)
        indpayL.append(payoffL)
        indpayH.append(payoffH)
        indcontL.append(contributionL)
        indcontH.append(contributionH)
        reward_hist.append(reward)
        kindness.append(r)

        if count >= 5:  # check if end of program condition is reached (stable allocation)
            # prepare output to user
            avg_reward.set(round(np.sum(reward_hist) / len(reward_hist), 2))
            avg_efficiency.set(round(np.sum(totpaydyn) / (len(totpaydyn) * 42), 2))
            avg_contributionH.set(round(np.sum(indcontH) / len(indcontH), 2))
            avg_contributionL.set(round(np.sum(indcontL) / len(indcontL), 2))
            periodstr.set(period)

            # open exit window
            exit_window()
        else:
            pass

    except ValueError:  # failsafe (just in case)
        pass

# reset function to restart program
def reset():
    # call global variables
    global period
    global kindness
    global r
    global contributionHold
    global contributionLold
    global totpaydyn
    global indpayH
    global indpayL
    global Q_values
    global reward_hist

    # reset all variables
    period = 0
    contributionHold = 0
    contributionLold = 0
    r = 0
    totpaydyn = []
    indpayH = []
    indpayL = []
    kindness = []
    reward_hist = []
    for state, actions in enumerate(possible_actions):
        Q_values[state, actions] = 0.0



## Main window with inputs and outputs for given round
# setup of main window
root = Tk()
root.geometry("440x200")  # window size
root.title("Allocation problem")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))  # grid for easy placement of widgets
root.columnconfigure(0, weight=1)  # all columns have equal size
root.rowconfigure(0, weight=1)  # all rows have equal size

# input of user's contribution
qH = StringVar()
ttk.Spinbox(
    mainframe,
    from_=0,
    to=10,
    increment=2,
    textvariable=qH
).grid(column=2, row=2, sticky=(W, E))

# output of computer agent's contribution
qL = StringVar()
ttk.Label(mainframe, textvariable=qL).grid(column=4, row=2, sticky=(W, E))

# output of individual payoffs
payH = StringVar()
ttk.Label(mainframe, textvariable=payH).grid(column=2, row=3, sticky=E)
payL = StringVar()
ttk.Label(mainframe, textvariable=payL).grid(column=2, row=4, sticky=E)

# output of counters
time_step = StringVar()
ttk.Label(mainframe, textvariable=time_step).grid(column=2, row=1, sticky=W)
counter = StringVar()
ttk.Label(mainframe, textvariable=counter).grid(column=4, row=1, sticky=W)

# text elements
ttk.Label(mainframe, text="Hours H:").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="Hours L:").grid(column=3, row=2, sticky=(W, E))
ttk.Label(mainframe, text="Payoff H:").grid(column=1, row=3, sticky=E)
ttk.Label(mainframe, text="Euro").grid(column=3, row=3, sticky=(W, E))
ttk.Label(mainframe, text="Payoff L:").grid(column=1, row=4, sticky=E)
ttk.Label(mainframe, text="Euro").grid(column=3, row=4, sticky=(W, E))
ttk.Label(mainframe, text="Period").grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text="Counter").grid(column=3, row=1, sticky=(W, E))

# button on main screen
ttk.Button(
    mainframe,
    text="Calculate",
    command=calculate
).grid(column=2, row=5, sticky=W)

## Menubar for main screen
menubar = Menu(root)
root.config(menu=menubar)

# file menu (drop down)
file_menu = Menu(menubar, tearoff=False)
# file_menu.add_command(
#    label='Load Q values',
    # command=reset,
#)
#file_menu.add_command(
#    label='Save Q values',
    # command=reset,
#)
file_menu.add_command(
    label='Reset',
    command=reset,  # restarts program
)
file_menu.add_separator()
file_menu.add_command(
    label='Exit',
    command=root.destroy,  # ends program
)
menubar.add_cascade(
    label="File",
    menu=file_menu,
    underline=0
)

# plot menu (drop down, calls functions from auxiliary file)
plot_menu = Menu(menubar, tearoff=False)
plot_menu.add_command(
    label='Total payoff',
    command=lambda: project_functions.diagram1(totpaydyn),
)
plot_menu.add_command(
    label='Individual payoffs',
    command=lambda: project_functions.diagram2(indpayH, indpayL),
)
plot_menu.add_command(
    label='Individual contributions',
    command=lambda: project_functions.diagram3(indcontH, indcontL),
)
plot_menu.add_command(
    label='Reward',
    command=lambda: project_functions.diagram4(reward_hist)
)
plot_menu.add_command(
    label='Kindness',
    command=lambda: project_functions.diagram5(kindness)
)
menubar.add_cascade(
    label="History",
    menu=plot_menu,
    underline=0
)

# info menu (drop down)
info_menu = Menu(menubar, tearoff=False)
info_menu.add_command(
    label='About',
    command=lambda: info(),  # display copyright notice
)
menubar.add_cascade(
    label="?",
    menu=info_menu,
    underline=0
)

# padding for main window
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

## function to call about window
def info():
    # setup of about window
    Window = tk.Toplevel(root)
    Window.grab_set()
    Window.geometry("600x200")
    Window.title("About")
    aboutframe = ttk.Frame(Window, padding="3 3 12 12")
    aboutframe.grid(column=0, row=0, sticky=(N, W, E, S))
    Window.columnconfigure(0, weight=1)
    Window.rowconfigure(0, weight=1)

    # text elements
    ttk.Label(aboutframe, text="Allocation Game").grid(column=0, row=0, sticky=W)
    ttk.Label(aboutframe, text="Copyright (C) 2024, Needs and Ambitions").grid(column=0, row=1, sticky=W)
    ttk.Label(aboutframe, text="This program comes with ABSOLUTELY NO WARRANTY.").grid(column=0, row=2, sticky=W)
    ttk.Label(
        aboutframe,
        text="This is free software, and you are welcome to redistribute it under certain conditions."
    ).grid(column=0, row=3, sticky=E)
    ttk.Label(
        aboutframe,
        text="For details see the GNU General Public License, Version 3 or later."
    ).grid(column=0, row=4, sticky=W)

    # button to close window
    ttk.Button(
        aboutframe,
        text="OK",
        command=lambda: Window.destroy()
    ).grid(column=0, row=5, sticky=(W, E))

    # padding for about window
    for child in aboutframe.winfo_children():
        child.grid_configure(padx=5, pady=5)


## exit window
# output on exit window
greed = StringVar()
greed.set(round(a, 2))
envy = StringVar()
envy.set(round(b, 2))
avg_reward = StringVar()
avg_efficiency = StringVar()
periodstr = StringVar()
avg_contributionH = StringVar()
avg_contributionL = StringVar()

# function to call exit window if end of program is reached (see calculate function)
def exit_window():
    # setup of exit window
    Window = tk.Toplevel(root)
    Window.grab_set()
    Window.geometry("440x150")
    Window.title("Allocation successful!")
    exitframe = ttk.Frame(Window, padding="3 3 12 12")
    exitframe.grid(column=0, row=0, sticky=(N, W, E, S))
    Window.columnconfigure(0, weight=1)
    Window.rowconfigure(0, weight=1)

    # text elements and output
    ttk.Label(exitframe, text="Greed parameter:").grid(column=1, row=1, sticky=E)
    ttk.Label(exitframe, textvariable=greed).grid(column=2, row=1, sticky=W)

    ttk.Label(exitframe, text="Envy parameter:").grid(column=4, row=1, sticky=(W, E))
    ttk.Label(exitframe, textvariable=envy).grid(column=5, row=1, sticky=W)

    ttk.Label(exitframe, text="Average contribution H:").grid(column=1, row=2, sticky=E)
    ttk.Label(exitframe, textvariable=avg_contributionH).grid(column=2, row=2, sticky=W)

    ttk.Label(exitframe, text="Average contribution L:").grid(column=4, row=2, sticky=E)
    ttk.Label(exitframe, textvariable=avg_contributionL).grid(column=5, row=2, sticky=W)

    ttk.Label(exitframe, text="Average reward:").grid(column=1, row=3, sticky=E)
    ttk.Label(exitframe, textvariable=avg_reward).grid(column=2, row=3, sticky=W)

    ttk.Label(exitframe, text="Average efficiency:").grid(column=4, row=3, sticky=(W, E))
    ttk.Label(exitframe, textvariable=avg_efficiency).grid(column=5, row=3, sticky=W)

    ttk.Label(exitframe, text="Total periods:").grid(column=1, row=4, sticky=E)
    ttk.Label(exitframe, textvariable=periodstr).grid(column=2, row=4, sticky=W)

    # button to end program
    ttk.Button(
        exitframe,
        text="Exit",
        command=lambda: root.destroy()
    ).grid(column=4, row=5, sticky=(W, E))

    # padding for exit window
    for child in exitframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

# start program
root.mainloop()