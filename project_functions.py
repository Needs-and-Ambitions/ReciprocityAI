"""
Allocation Problem
Author: Needs and Ambitions, Date: January 2024
Auxiliary file to create plots of dynamic variables
"""

import matplotlib.pyplot as plt

def diagram1(totpaydyn):
    plt.xlabel('Period')
    plt.ylabel('Total payoff')
    plt.plot(totpaydyn)
    plt.show()

def diagram2(indpayH, indpayL):
    plt.xlabel('Period')
    plt.ylabel('Individual payoff')
    plt.plot(indpayH, 'r', label="Payoff Player H")
    plt.plot(indpayL, 'b', label="Payoff Player L")
    plt.legend()
    plt.show()

def diagram3(indcontH, indcontL):
    plt.xlabel('Period')
    plt.ylabel('Individual contribution')
    plt.plot(indcontH, 'r', label="Contribution Player H")
    plt.plot(indcontL, 'b', label="Contribution Player L")
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
