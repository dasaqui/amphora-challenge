#!/usr/bin/env python

# Here resides the codes needed to plot and generate all the required graphs.

import my_constants as c
from matplotlib import pyplot as plt

# plot_by is a helper code to plot given data grouped by a condition in a
# 3d Scattered plot
def plot_by( fig, index, pca_data, labels, group_by, title=""):
    # Prepare the grid
    if len( index) == 3:
        rows,cols,index = index
    else:
        rows,cols = (1,2)
    ax = fig.add_subplot(rows,cols,index,projection='3d')

    # Plot by group
    groups = set( labels[ group_by])
    for group in groups:
        # Split data by superpopulation
        rows = [number for number,code in enumerate( labels[group_by]) if code == group]

        # get the coordinates for each point
        xs = pca_data[ rows, 0]
        ys = pca_data[ rows, 1]
        zs = pca_data[ rows, 2]

        ax.scatter( xs, ys, zs)

    # Labels and legends
    ax.legend( [k for k in groups])
    ax.set_xlabel("first component")
    ax.set_ylabel("second component")
    ax.set_zlabel("third component")

    # Write a title
    if title != "": ax.set_title( title)


def plot_F1( fig, index, f1_macro, f1_by_groups, labels_dict):
    # minimum score to show
    MIN = 0.8

    # Prepare the grid
    if len( index) == 3:
        rows,cols,index = index
    else:
        rows,cols = (1,2)
    ax = fig.add_subplot(rows,cols,index)

    # Plot scores by group
    for code in labels_dict:
        i = labels_dict[ code]
        ax.barh( -i, f1_by_groups[i] - MIN, left=MIN)
        ax.text( 1.01*MIN, -i-0.1, "%.3f" % f1_by_groups[i])

    # Plot global score
    ax.barh( -i-1, f1_macro - MIN, left=MIN)
    ax.text( 1.01*MIN, -i-1.1, "%.3f" % f1_macro)
    
    # set labels for each bar and title
    ax.set_yticklabels( ["","Global"]+[key for key in labels_dict][::-1])
    ax.set_title("F1 score grouped by superpopulation")