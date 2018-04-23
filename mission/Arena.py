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
        start_time = 0
        finish_time = 0
        lat = 0
        long = 0
        id = 0

    # ===============================================================
    # =                         Constructor
    # ===============================================================

    def __init__(self, my_lat, my_lon, my_time, dur_dis, buf_dis, row, col):
        """Initializes board with 10 x 10 dimensions
        :param my_lat: the initial latitude
        :param my_lon: the initial longtitude
        :param my_time: current time
        :param start_dis: buffer time beween events
        :param dur_dis: duration time of events
        """
        self.__getsEvent = False
        self.__agentX = 0
        self.__agentY = 0
        self.__agentdir = 0
        self.__eventqueue = []
        # may update other features and parameters later
        self.__buf_dis = buf_dis
        self.__dur_dis = dur_dis

        self.__colDimension = col
        self.__rowDimension = row
        self.__time = my_time
        self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
        self.__addLongLat(my_lat, my_lon)
        self.__addEventTimes()

    # ===============================================================
    # =             Arena Generation Functions
    # ===============================================================
    def __addEventTimes(self):
        for r in range(self.__rowDimension):
            for c in range(self.__colDimension):
                self.__board[c][r].start_time = self.__time + self.__buf_dis()  # don't need __add_time() function
                self.__board[c][r].id += 1
                self.__board[c][r].finish_time = self.__board[c][r].start_time + self.__dur_dis()

    def __addLongLat(self, lat, lon):
        dNorth = 0
        dEast = 0
        earth_radius = 6378137.0  # Radius of "spherical" earth
        self.__board[0][0].lat = lat
        self.__board[0][0].long = lon
        # Coordinate offsets in radians
        # for r in range(self.__rowDimension):
        #     for c in range(self.__colDimension):
        #         if (r == 0 and c == 0):
        #             continue
        #         else:
        #             dEast += 10
        #             dLat = dNorth / earth_radius
        #             dLon = dEast / (earth_radius * math.cos(math.pi * lat / 180))
        #             self.__board[c][r].lat = lat + (dLat * 180 / math.pi)
        #             self.__board[c][r].long = lon + (dLon * 180 / math.pi)
        #     dNorth += 10
        #     dEast = 0
        for c in range(1,self.__colDimension):
            dEast += 10
            dLat = dNorth / earth_radius
            dLon = dEast / (earth_radius * math.cos(math.pi * lat / 180))
            self.__board[c][0].lat = lat + (dLat * 180 / math.pi)
            self.__board[c][0].long = lon + (dLon * 180 / math.pi)
        dEast = 0
        for r in range(1,self.__rowDimension):
            dNorth += 10
            for c in range(0,self.__colDimension):
                dLat = dNorth / earth_radius
                dLon = dEast / (earth_radius * math.cos(math.pi * lat / 180))
                self.__board[c][r].lat = lat + (dLat * 180 / math.pi)
                self.__board[c][r].long = lon + (dLon * 180 / math.pi)
                dEast += 10
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
                        self.__board[c][r].start_time = self.__board[c][r].finish_time + self.__buf_dis()
                        self.__board[c][r].id += 1
                        self.__board[c][r].finish_time = self.__board[c][r].start_time + self.__dur_dis()

    def get_board(self, time):
        for r in range(self.__rowDimension):
            for c in range(self.__colDimension):
                if (time > self.__board[c][r].start_time):
                    print((self.__board[c][r].lat, self.__board[c][r].long, "HasEvent", self.__board[c][r].id))
                else:
                    print("NoEvent")

    def get_event(self, c, r, time):
        if (time > self.__board[c][r].start_time):
            return True
        return False

    def get_id(self, c, r, time):
        if (time > self.__board[c][r].start_time):
            return self.__board[c][r].id
        return 0

    def get_max_id(self, c, r):
        return self.__board[c][r].id

    def get_longlat(self):
        result = []
        for r in range(self.__rowDimension):
            if (r % 2 == 0):
                for c in range(self.__colDimension):
                    result.append((self.__board[c][r].lat, self.__board[c][r].long, c, r))
            else:
                for c in range(self.__colDimension - 1, -1, -1):
                    result.append((self.__board[c][r].lat, self.__board[c][r].long, c, r))
        return result

        # board_info = Arena(33.24532, 53.12354, time.time())
