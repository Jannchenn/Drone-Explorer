# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 02:07:39 2018
Drone Fixed Duration Graph
@author: hahnara
"""
#note to Hahnara: plot board stats on same graph could help gain perspective

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

class Graph():
    def __init__(self, data):
        self.data = data
        # self.files = glob.glob(self.path)
        self.pick_X()
        self.col_arr()
        self.cols

    def col_arr(self):
        self.cols = ['probability', 'eventlife_lambda', 'arrival_num',
                'duration_lambda']
        self.cols.remove(self.x_val)

    def pick_X(self):
        if self.data == 'arr_die_var.csv':
            self.x_val = 'eventlife_lambda'
        if self.data == 'arr_num_var.csv':
            self.x_val = 'arrival_num'
            print(self.x_val)
        if self.data == 'dur_var.csv':
            self.x_val = 'duration_lambda'
            print(self.x_val)
        if self.data == 'prob_var.csv':
            self.x_val = 'probability'
            print(self.x_val)

    def make_plot(self):
        """
        Plots points in graph using aggregated csv files merged in Graph.sh
        Figures are saved in directory defined in Graph.sh

        Args:
            plt_identifier: assigns figure a number. ie. Figure "plt_identifier"
            title: Title of graph to show what data graph is showing. ie. Total Events, Missed Events, etc..
            x_type: labels x axis
            y_type: labels y axis
            x_col: x data
            y_col: y data
        """
        # Graph Labels 
        title = self.data
        y_type = 'Catch Rate Include Same'
        
        # Dataset Labels
        y_col1 = 'catch_rate'
        y_col2 = 'catch_rate_include_same'

        # Extract X dataset
        dataset = pd.read_csv(self.data)
        random_ds = dataset[(dataset['random'] == 1)]
        roomba_ds = dataset[(dataset['random'] == 0)]

        # Extract Y dataset
        # Note: random_data and roomba_ds have same data for y2 to y4
        X_axis = random_ds[self.x_val]
        y2 = random_ds[self.cols[0]].div(100)
        y3 = random_ds[self.cols[1]].div(100)
        y4 = random_ds[self.cols[2]].div(100)
        #y_random_catch = random_ds[y_col1]
        #y_roomba_catch = roomba_ds[y_col1]
        y_random_catch = random_ds[y_col2]          # same
        y_roomba_catch = roomba_ds[y_col2]          # same 
        
        # line graph
        plt.plot(X_axis, y_random_catch, 'b-',X_axis, y_roomba_catch, 'r-',
                X_axis, y2, 'c-', X_axis, y3, 'y-',X_axis, y4, 'g-')
        
        # scatter plot
        plt.plot(X_axis, y_random_catch, 'bo',  X_axis, y_roomba_catch, 'ro',
                 X_axis, y2, 'co', X_axis, y3, 'yo', X_axis, y4, 'go')

        plt.legend(['Random', 'Roomba', self.cols[0], self.cols[1],
                   self.cols[2]], loc='upper right')

        plt.savefig(self.x_val + "_graph_catch_same.png")

        # label graph
        plt.xlabel(self.x_val)
        plt.title(title)
        plt.ylabel(y_type)

        plt.show()


# give Graph object path to find file
# note to Hahnara to edit: pass file name sent from script
# graph = Graph('sample.csv')
# graph.make_plot()
graph3 = Graph('dur_var.csv')
graph3.make_plot()

graph1 = Graph('arr_die_var.csv')
graph2 = Graph('arr_num_var.csv')
graph4 = Graph('prob_var.csv')

graph1.make_plot()
graph2.make_plot()
graph4.make_plot()

