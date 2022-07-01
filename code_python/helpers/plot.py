#!/usr/bin/env python

# This file is to keep ordered aditional codes

from numba import njit
import numba
import my_constants as c
import numpy as np
from sklearn.cluster import KMeans

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
