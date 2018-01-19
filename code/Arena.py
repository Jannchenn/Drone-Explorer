# ======================================================================
# FILE:        Arena.py
#
# DESCRIPTION: This file contains Arena class, which contains the map
#              that our agent(UAV) is going to explore
#
# ======================================================================

import time
import math
import random


class Arena():

    # Tile Structure
    class __Tile:
        event        = False
        wait_time    = 0
        real_time    = 0
        dur_time     = 0
        lat          = 0
        long         = 0

    # ===============================================================
    # =                         Constructor
    # ===============================================================

    def __init__(self, lat1, long1):

        # Agent Initialization
        self.__getsEvent    = False
        self.__agentX       = 0
        self.__agentY       = 0
        self.__agentdir     = 0
        self.__eventqueue   = []
        self.count          = 0                 # REMENBER TO DELETE!!!!!!!!!!!!
        # may update other features and parameters later

        self.__colDimension = 10
        self.__rowDimension = 10
        self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
        self.__addLongLat(lat1, long1)
        self.__addEvent()
        while self.count<10:                                         # CHANGE CONDITION!!!!!!!
            self.__watiCount()
            self.__eventCount()
            self.print_world()
            self.count += 1


        # self.__addFeatures(lat1, long1, lat2, long2)
        # while True:
        #    self.__addEvent(self.__randomInt(10), self.__randomInt(10))
        #    time.sleep(60)

    # ===============================================================
    # =             Arena Generation Functions
    # ===============================================================
    def __watiCount(self):
        time.sleep(5)
        for r in range(self.__rowDimension):
            for c in range(self.__colDimension):
                if self.__board[c][r].real_time != 0:
                    self.__board[c][r].real_time -= 1
                else:
                    self.__board[c][r].event = True
                    self.__addDuration(c,r)

    def __eventCount(self):
        print ("eventcount")

    def __addDuration(self,c,r):
        self.__board[c][r].dur_time = random.randint(1,5)

    def __addEvent(self):
        for r in range(self.__rowDimension):
            for c in range(self.__colDimension):
                self.__board[c][r].wait_time = random.randint(1,10)
                self.__board[c][r].real_time = self.__board[c][r].wait_time

    def __addLongLat(self, lat, long):
        dNorth = 0
        dEast = 0
        earth_radius = 6378137.0  # Radius of "spherical" earth

        # Coordinate offsets in radians
        for r in range(self.__rowDimension):
            dNorth += 0.5
            for c in range(self.__colDimension):
                dEast += 0.5
                dLat = dNorth / earth_radius
                dLon = dEast / (earth_radius * math.cos(math.pi * lat / 180))
                self.__board[c][r].lat = lat + (dLat * 180 / math.pi)
                self.__board[c][r].long = long + (dLon * 180 / math.pi)


    # ===============================================================
    # =             Arena Fetch Functions
    # ===============================================================
    def get_board(self):
        return self.__board

    def print_world(self):
        for r in range(10):
            for c in range(10):
                if self.__board[c][r].event == True:
                    print((self.__board[c][r].lat, self.__board[c][r].long))