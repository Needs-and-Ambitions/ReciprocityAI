"""
    Allocation Problem - Auxiliary file with menu bar for GUI

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

# import auxiliary file for plotting dynamic variables
import project_functions


class MenuBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)

        # file menu
        file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=file_menu)
        file_menu.add_command(label='Reset', command=parent.reset_program)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", underline=1, command=parent.destroy)

        # plot menu
        plot_menu = tk.Menu(self, tearoff=False)
        plot_menu.add_command(
            label='Total payoff',
            command=lambda: project_functions.diagram1(parent.totpaydyn)
        )
        plot_menu.add_command(
            label='Individual payoffs',
            command=lambda: project_functions.diagram2(parent.indpayH, parent.indpayL)
        )
        plot_menu.add_command(
            label='Individual contributions',
            command=lambda: project_functions.diagram3(parent.indcontH, parent.indcontL)
        )
        plot_menu.add_command(
            label='Reward',
            command=lambda: project_functions.diagram4(parent.reward_hist)
        )
        plot_menu.add_command(
            label='Kindness',
            command=lambda: project_functions.diagram5(parent.kindness)
        )
        self.add_cascade(
            label="History",
            menu=plot_menu,
            underline=0
        )

        # info menu
        info_menu = tk.Menu(self, tearoff=False)
        info_menu.add_command(
            label='About',
            command=lambda: parent.info(),  # display copyright notice
        )
        self.add_cascade(
            label="?",
            menu=info_menu,
            underline=0
        )
