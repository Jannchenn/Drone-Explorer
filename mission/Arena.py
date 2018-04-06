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
import thread
import numpy as np 


class Arena():
    # Tile Structure
    class __Tile:
        start_time = 0
        finish_time = 0
        lat = 0
        long = 0
        id = 0

    # ===============================================================
    # =                         Constructor
    # ===============================================================

    def __init__(self, lat1, long1, time, distribution1, distribution2):
        # Agent Initialization
        self.__getsEvent = False
        self.__agentX = 0
        self.__agentY = 0
        self.__agentdir = 0
        self.__eventqueue = []
        # may update other features and parameters later
        self.__distribution = (distribution1,distribution2)

        self.__colDimension = 3
        self.__rowDimension = 3
        self.__time = time
        self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
        self.__addLongLat(lat1, long1)
        self.__addEventTimes()

    # ===============================================================
    # =             Arena Generation Functions
    # ===============================================================
    def __addEventTimes(self):
        for r in range(self.__rowDimension):
            for c in range(self.__colDimension):
                self.__board[c][r].start_time = self.__time + self.__addTime(self.__distribution[0])
                self.__board[c][r].id += 1
                self.__board[c][r].finish_time = self.__board[c][r].start_time + self.__addTime(self.__distribution[1]) * 3

    def __addTime(self,dist):
        time = 0
        num = 0
        target = 250
        beta = 1.0/target
        if dist=="random20":
            while (num != 1):
                time += 1
                num = random.randint(1, 5)
        elif dist=="exponential":
            time = np.random.exponential(beta,5000)
        return time

    def __addLongLat(self, lat, lon):
        dNorth = 0
        dEast = 0
        earth_radius = 6378137.0  # Radius of "spherical" earth
        self.__board[0][0].lat = lat
        self.__board[0][0].long = lon
        # Coordinate offsets in radians
        for r in range(self.__rowDimension):
            for c in range(self.__colDimension):
                if (r==0 and c==0):
                    continue
                else:
                    dEast += 15
                    dLat = dNorth / earth_radius
                    dLon = dEast / (earth_radius * math.cos(math.pi * lat / 180))
                    self.__board[c][r].lat = lat + (dLat * 180 / math.pi)
                    self.__board[c][r].long = lon + (dLon * 180 / math.pi)
            dNorth += 15
            dEast = 0

    # ===============================================================
    # =             Arena Fetch Functions
    # ===============================================================
    def update_board(self):
        while True:
            time.sleep(1)  # *60
            time_now = time.time()
            for r in range(self.__rowDimension):
                for c in range(self.__colDimension):
                    if (time_now > self.__board[c][r].finish_time):
                        self.__board[c][r].start_time = self.__board[c][r].finish_time + self.__addTime(self.__distribution[0]) * 3
                        self.__board[c][r].id += 1
                        self.__board[c][r].finish_time = self.__board[c][r].start_time + self.__addTime(self.__distribution[1]) * 3

    def get_board(self, time):
        for r in range(self.__rowDimension):
            for c in range(self.__colDimension):
                if (time > self.__board[c][r].start_time):
                    print((self.__board[c][r].lat, self.__board[c][r].long, "HasEvent", self.__board[c][r].id))
                else:
                    print("NoEvent")

    def get_event(self, c,r, time):
        if (time > self.__board[c][r].start_time):
            return True
        return False

    def get_id(self, c, r, time):
        if (time > self.__board[c][r].start_time):
            return self.__board[c][r].id
        return 0


                    #   def print_world(self):
                    #      for r in range(10):
                    #         for c in range(10):
                    #            print((self.__board[c][r].lat, self.__board[c][r].long))

                    # board_info = Arena(33.24532,53.12354,time.time())
                    # board_info.update_board()

    def get_longlat(self):
        result = []
        for r in range(self.__rowDimension):
            if (r%2==0):
                for c in range(self.__colDimension):
                    result.append((self.__board[c][r].lat,self.__board[c][r].long,c,r))
            else:
                for c in range(self.__colDimension-1,-1,-1):
                    result.append((self.__board[c][r].lat,self.__board[c][r].long,c,r))
        return result

#board_info = Arena(33.24532, 53.12354, time.time())
