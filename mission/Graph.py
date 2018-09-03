# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 02:07:39 2018
Drone Fixed Duration Graph 
@author: hahnara
"""
#note to Hahnara: plot board stats on same graph could help gain perspective

import matplotlib.pyplot as plt
import pandas as pd
import sys

class Graph():
    def __init__(self, random_path, roomba_path):
        self.random_path = random_path
        self.roomba_path = roomba_path
        # self.files = glob.glob(self.path)
       
        self.graph_dict = {}

        self.set_dict()

    def set_dict(self):
        """
        Creates dictionary of plot attributes for each graph created
        graph_dict[title] = [x label, y label, x data (col), y data (col)]
        """
        # note to Hahnara: use script to determine lambda duration or buffer
        # self.graph_dict['Total Events'] = [sys.argv[1], 'Total Events',
        #                                   'sec_Dur', 'avg_ttl_evnts']
        self.graph_dict['Total Events'] = ['Lambda Duration (sec)', 'Total Events',
                                                         'sec_Dur', 'avg_ttl_evnts']
        self.graph_dict['Missed Events'] = ['Lambda Duration (sec)', 'Missed Events',
                                                             'sec_Dur', 'avg_ttl_mssd_evnts']
        self.graph_dict['Different Events'] = ['Lambda Duration (sec)', 'Different Events',
                                                          'sec_Dur', 'avg_ttl_diff_evnts']
                                                          
        self.graph_dict['Total Visited'] = ['Lambda Duration (sec)', 'Total Visted Sectors',
                                                          'sec_Dur', 'avg_ttl_vistd_sctrs']
                                                          
    def make_graph(self):
        """
        Creates graph using self.make_plot()
        """
        fig_count = 0
        for key in self.graph_dict:
            fig_count += 1
            self.make_plot(fig_count, key, self.graph_dict[key][0], self.graph_dict[key][1],
                           self.graph_dict[key][2], self.graph_dict[key][3])

    def make_plot(self, plt_identifier, title, x_type, y_type, x_col, y_col):
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
        # label graph
        plt.figure(plt_identifier)
        plt.title(title)
        plt.xlabel(x_type)
        plt.ylabel(y_type)

        # sys.argv[2]
        dataset = pd.read_csv('random_fixed_buffer_merged.csv') # path
        X = dataset[x_col]                  # lambda buffer in seconds
        y = dataset[y_col]

        plt.scatter(X, y, color="blue", alpha=0.5)

        # sys.arv[3]
        dataset = pd.read_csv('roomba_fixed_buffer_merged.csv') # path
        X = dataset[x_col]                  # lambda buffer in seconds
        y = dataset[y_col]
        plt.scatter(X, y, color="red", alpha=0.5)
        plt.legend(['Random', 'Roomba'], loc='upper right')

        # need to save in directory (where to put directory?)
        plt.savefig("Figure_" + str(plt_identifier) + ".png")


# give Graph object path to find file
# note to Hahnara to edit: pass file name sent from script
graph = Graph('/home/hahnara/Documents/Research/reports/random/Drone_Total*.txt',
              '/home/hahnara/Documents/Research/reports/roomba/Drone_Total*.txt')
graph.make_graph()
plt.show()
