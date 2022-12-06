""" 2020
    Created by Dariya
    charts function
"""
import os
import matplotlib.pyplot as plt
from numpy import random as rnd


def get_chart(folder, data, labels):
    """get graph"""
    plt.figure()
    plt.bar(labels, data)
    plt.title("проверки состояния асфальта")
    plt.legend()
    unique_num = rnd.randint(999999999)
    file_name = os.path.join(folder, f"pie_figure_{unique_num}.jpg")
    plt.savefig(file_name, bbox_inches = "tight", facecolor="grey")
    return file_name
