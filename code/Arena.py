# ======================================================================
# FILE:        Arena.py
#
# AUTHOR:      Anyi Chen
#
# DESCRIPTION: This file contains Arena class, which contains the map
#              that our agent(UAV) is going to explore
#
# ======================================================================

import time
import math

class Arena():

    # Tile Structure
    class __Tile:
        event   = False
        lat     = 0
        long    = 0

    # ===============================================================
    # =                         Constructor
    # ===============================================================

    def __init__(self, lat1, long1, lat2, long2):

        # Agent Initialization
        self.__getsEvent = False
        self.__agentX   = 0
        self.__agentY   = 0
        self.__agentdir = 0
        # may update other features and parameters later

        self.__colDimension = 10
        self.__rowDimension = 10
        self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
        self.__addFeatures(lat1, long1, lat2, long2)
        while True:
            self.__addEvent(self.__randomInt(10), self.__randomInt(10))
            time.sleep(60)

    # ===============================================================
    # =             Arena Generation Functions
    # ===============================================================
    def __addFeatures(self, lat1, long1, lat2, long2):
        if lat1 <= lat2 and long1 <= long2:
            self.__addLongLat1(lat1, long1)
        elif lat1 >= lat2 and long1 <= long2:
            lat1 = lat1 - 10/111111
            self.__addLongLat2(lat1, long1)
        elif lat1 >= lat2 and long1 >= long2:
            self.__addLongLat3(lat2, long2)
        elif lat1 <= lat2 and long1 >= long2:
            lat2 = lat2 - 10 / 111111
            self.__addLongLat4(lat2, long2)

    def __addEvent(self, c, r):
        self.__board[c][r].event = True
        time.sleep(180)
        self.__board[c][r].event = False

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

