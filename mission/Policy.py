# ======================================================================
# FILE:        Policy.py
#
# DESCRIPTION: Contains policies drone will fly including: random, roomba
#
# ======================================================================

from random import randrange
from dronekit import connect, VehicleMode, LocationGlobalRelative


class Policy():
    def __init__(self, board, start, end, col_dim, row_dim):
        self.board = board
        self.start = start
        self.end = end
        self.cur = (0, 0)
        self.switch = 0
        self.__colDimension = col_dim
        self.__rowDimension = row_dim

    def random(self):
        """
        This method provides drone to fly randomly
        :reutrn: the tuple of col, row, and wpl
        """
        i = randrange(len(self.board))
        lat = self.board[i][0]
        lon = self.board[i][1]
        c = self.board[i][2]
        r = self.board[i][3]
        wpl = LocationGlobalRelative(lat, lon, 10)
        return (c, r, wpl)

    def roomba(self):
        """
        This method provides drone to fly inorder
        :return: the tuple of col, row, and wpl
        """
        print(self.start)
        print(self.end)
        temp = (0, 0, 0)
        if self.start[0] == self.end[0]:
            temp = self._horizontal()
        elif self.start[1] == self.end[1]:
            temp = self._vertical()
        if self.switch == 1:
            self.switch = 0
            return self._horizontal()
        elif self.switch == 2:
            self.switch = 0
            return self._vertical()
        return temp

    def _find_dir(self, a, b):
        if (a < b):
            return 1
        else:
            return -1

    def _horizontal(self):
        """
        returns lat & long
        if at the end: go to vertical (start a new cycle)
        if at the end of some row: turn to the next upper/lower row (depends on dir)
        if at row 0, 2: ------->
        if at row 1, 3: <-------
        """
        c = self.cur[0]
        r = self.cur[1]
        dir = self._find_dir(self.start[1], self.end[1])
        if c == self.end[0] and r == self.end[1]:
            self.start = (self.end[0], self.end[1])
            self.end = (self.__colDimension - 1 - self.start[0], self.end[1])
            self.switch = 2
            return
        if (r % 2 == 0 and c == self.__colDimension - 1) or (r % 2 == 1 and c == 0):
            self.cur = (c, r + dir)
            return self.__getboardinfo__(c, r + dir)
        if r % 2 == 1:
            self.cur = (c - 1, r)
            return self.__getboardinfo__(c - 1, r)
        if r % 2 == 0:
            self.cur = (c + 1, r)
            return self.__getboardinfo__(c + 1, r)
        else:
            print("nothing\n")

    def _vertical(self):
        """
        returns lat & long
        if at the end: go to horizontal (start a new cycle)
        if at the end of some col: turn to the next left/right col (depends on dir)
        if at col 0, 2: go down
        if at col 1, 3: go up
        """
        c = self.cur[0]
        r = self.cur[1]
        dir = self._find_dir(self.start[0], self.end[0])
        if c == self.end[0] and r == self.end[1]:
            self.start = (self.end[0], self.end[1])
            self.end = (self.end[0], self.__rowDimension - 1 - self.start[1])
            self.switch = 1
            return
        if (c % 2 == 1 and r == self.__rowDimension - 1) or (c % 2 == 0 and r == 0):
            self.cur = (c + dir, r)
            return self.__getboardinfo__(c + dir, r)
        if c % 2 == 0:
            self.cur = (c, r - 1)
            return self.__getboardinfo__(c, r - 1)
        if c % 2 == 1:
            self.cur = (c, r + 1)
            return self.__getboardinfo__(c, r + 1)
        else:
            print("nothing")

    def __getboardinfo__(self, c, r):
        """
        For returning the wpl, we need to get information of the longtitude and latitude,
        so we need to return the board(sector) information
        :param c: the coloum of the board; r: the row of the board
        :return: the longtitude and latitude of the sector
        """
        for elem in self.board:
            if elem[2] == c and elem[3] == r:
                lat = elem[0]
                lon = elem[1]
                wpl = LocationGlobalRelative(lat, lon, 10)
                return (c, r, wpl)

