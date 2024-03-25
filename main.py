"""
    Allocation Problem - Main file with GUI

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

import tkinter as tk
from tkinter import ttk, N, W, S, E, StringVar

import numpy as np

# import game environment
from allocation_game import AllocationGame

# import menu bar
from appmenu import MenuBar

# initialize game
ag = AllocationGame(max_periods=200)
ag.reset()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        "main window"

        # menu
        menubar = MenuBar(self)
        self.config(menu=menubar)

        # window setup
        self.geometry("440x200")
        self.title("Allocation problem")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        # output of counters
        self.time_step = StringVar()
        self.counter = StringVar()
        ttk.Label(mainframe, text="Period").grid(column=0, row=0, sticky=tk.E)
        ttk.Label(mainframe, textvariable=self.time_step).grid(column=1, row=0, sticky=tk.W)
        ttk.Label(mainframe, text="Counter").grid(column=2, row=0, sticky=tk.E)
        ttk.Label(mainframe, textvariable=self.counter).grid(column=3, row=0, sticky=tk.W)

        # input user contribution
        ttk.Label(mainframe, text="Hours H:").grid(column=0, row=1, sticky=tk.E)
        self.qH = StringVar()
        ttk.Spinbox(
            mainframe,
            from_=0,
            to=10,
            increment=2,
            textvariable=self.qH
        ).grid(column=1, row=1, sticky=tk.W)

        # output agent contribution
        ttk.Label(mainframe, text="Hours L:").grid(column=2, row=1, sticky=tk.E)
        self.qL = StringVar()
        ttk.Label(mainframe, textvariable=self.qL).grid(column=3, row=1, sticky=tk.W)

        # output of individual payoffs
        ttk.Label(mainframe, text="Payoff H:").grid(column=0, row=2, sticky=tk.E)
        self.payH = StringVar()
        ttk.Label(mainframe, textvariable=self.payH).grid(column=1, row=2, sticky=tk.E)
        ttk.Label(mainframe, text="Euro").grid(column=2, row=2, sticky=tk.W)

        ttk.Label(mainframe, text="Payoff L:").grid(column=0, row=3, sticky=tk.E)
        self.payL = StringVar()
        ttk.Label(mainframe, textvariable=self.payL).grid(column=1, row=3, sticky=tk.E)
        ttk.Label(mainframe, text="Euro").grid(column=2, row=3, sticky=tk.W)

        # button
        ttk.Button(
            mainframe,
            text="Calculate",
            command=lambda: self.next_step(float(self.qH.get())/2)  # ag input requires int between 0 and 5
        ).grid(column=1, row=5, sticky=tk.W, padx=5, pady=5)

        # padding for main window
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # lists for data collection
        self.totpaydyn = []
        self.indpayH = []
        self.indpayL = []
        self.indcontH = []
        self.indcontL = []
        self.kindness = []
        self.reward_hist = []

        # output on exit window
        self.greed = StringVar()
        self.greed.set(round(ag.a, 2))
        self.envy = StringVar()
        self.envy.set(round(ag.b, 2))
        self.avg_reward = StringVar()
        self.avg_efficiency = StringVar()
        self.periodstr = StringVar()
        self.avg_contributionH = StringVar()
        self.avg_contributionL = StringVar()

    # function to reset game environment and data collected by the app
    def reset_program(self):
        ag.reset()

        self.totpaydyn = []
        self.indpayH = []
        self.indpayL = []
        self.indcontH = []
        self.indcontL = []
        self.kindness = []
        self.reward_hist = []

    # function to advance the game one period
    def next_step(self, action):
        # retrieve algorithm's decision
        payoff_h, payoff_l, contribution_h, contribution_l, reward_q, r, count, period, done = ag.calculate(action)

        # prepare output to user
        self.time_step.set(int(period))
        self.payH.set(int(payoff_h))
        self.payL.set(int(payoff_l))
        self.qL.set(int(contribution_l))
        self.counter.set(int(count))

        # update payoff histories for plots
        self.totpaydyn.append(payoff_h + payoff_l)
        self.indpayL.append(payoff_l)
        self.indpayH.append(payoff_h)
        self.indcontL.append(contribution_l)
        self.indcontH.append(contribution_h)
        self.reward_hist.append(reward_q)
        self.kindness.append(r)

        # what to do when game terminates
        if done:
            self.avg_reward.set(round(np.sum(self.reward_hist) / len(self.reward_hist), 2))
            self.avg_efficiency.set(round(np.sum(self.totpaydyn) / (len(self.totpaydyn) * 42), 2))
            self.avg_contributionH.set(round(np.sum(self.indcontH) / len(self.indcontH), 2))
            self.avg_contributionL.set(round(np.sum(self.indcontL) / len(self.indcontL), 2))
            self.periodstr.set(period)
            self.exit_window()
        else:
            pass

    "info window"

    def info(self):
        # setup of about window
        Window = tk.Toplevel(self)
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

    "exit window"

    # function to call exit window if end of program is reached (see next_step function)
    def exit_window(self):
        # setup of exit window
        Window = tk.Toplevel(self)
        Window.grab_set()
        Window.geometry("440x150")
        Window.title("Allocation successful!")
        exitframe = ttk.Frame(Window, padding="3 3 12 12")
        exitframe.grid(column=0, row=0, sticky=(N, W, E, S))
        Window.columnconfigure(0, weight=1)
        Window.rowconfigure(0, weight=1)

        # text elements and output
        ttk.Label(exitframe, text="Greed parameter:").grid(column=1, row=1, sticky=E)
        ttk.Label(exitframe, textvariable=self.greed).grid(column=2, row=1, sticky=W)

        ttk.Label(exitframe, text="Envy parameter:").grid(column=4, row=1, sticky=(W, E))
        ttk.Label(exitframe, textvariable=self.envy).grid(column=5, row=1, sticky=W)

        ttk.Label(exitframe, text="Average contribution H:").grid(column=1, row=2, sticky=E)
        ttk.Label(exitframe, textvariable=self.avg_contributionH).grid(column=2, row=2, sticky=W)

        ttk.Label(exitframe, text="Average contribution L:").grid(column=4, row=2, sticky=E)
        ttk.Label(exitframe, textvariable=self.avg_contributionL).grid(column=5, row=2, sticky=W)

        ttk.Label(exitframe, text="Average reward:").grid(column=1, row=3, sticky=E)
        ttk.Label(exitframe, textvariable=self.avg_reward).grid(column=2, row=3, sticky=W)

        ttk.Label(exitframe, text="Average efficiency:").grid(column=4, row=3, sticky=(W, E))
        ttk.Label(exitframe, textvariable=self.avg_efficiency).grid(column=5, row=3, sticky=W)

        ttk.Label(exitframe, text="Total periods:").grid(column=1, row=4, sticky=E)
        ttk.Label(exitframe, textvariable=self.periodstr).grid(column=2, row=4, sticky=W)

        # button to end program
        ttk.Button(
            exitframe,
            text="Exit",
            command=lambda: self.destroy()
        ).grid(column=4, row=5, sticky=(W, E))

        # padding for exit window
        for child in exitframe.winfo_children():
            child.grid_configure(padx=5, pady=5)


# start app
if __name__ == "__main__":
    app = App()
    app.mainloop()
