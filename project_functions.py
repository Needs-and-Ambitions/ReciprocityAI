"""
    Allocation Problem - Auxiliary file to create plots of dynamic variables

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

import matplotlib.pyplot as plt


def diagram1(totpaydyn):
    plt.xlabel('Period')
    plt.ylabel('Total payoff')
    plt.plot(totpaydyn)
    plt.show()


def diagram2(indpay_h, indpay_l):
    plt.xlabel('Period')
    plt.ylabel('Individual payoff')
    plt.plot(indpay_h, 'r', label="Payoff Player H")
    plt.plot(indpay_l, 'b', label="Payoff Player L")
    plt.legend()
    plt.show()


def diagram3(indcont_h, indcont_l):
    plt.xlabel('Period')
    plt.ylabel('Individual contribution')
    plt.plot(indcont_h, 'r', label="Contribution Player H")
    plt.plot(indcont_l, 'b', label="Contribution Player L")
    plt.legend()
    plt.show()


def diagram4(reward_hist):
    plt.xlabel('Period')
    plt.ylabel('Reward Player L')
    plt.plot(reward_hist)
    plt.show()


def diagram5(kindness):
    plt.xlabel('Period')
    plt.ylabel('Kindness')
    plt.plot(kindness)
    plt.show()
