# ======================================================================
# FILE:        Event.py
#
# DESCRIPTION: This file contains Event class, which will represent each
#               Event in the map
#
# ======================================================================

import Distribution
from collections import defaultdict
import random


class Event:
    event_id = 1

    def __init__(self, prob, lifetime, col, row):
        """
        The class has two parameters
        :param prob: The probability the the event will move
        :param lifetime: The exponential distribution of the life time of the event
        :param expo: The duration that the event will stay in the same place(sector)
        :param col: The column dimension of the map
        :param row: The row dimension of the map
        """
        self.col_dim = col
        self.row_dim = row
        self.probability = prob
        self.life_time_expo = lifetime()
        self.die_time = 0
        self.finish_time = 0
        self.id = Event.event_id
        Event.event_id += 1
        self.travel_history = defaultdict(int)
        self.cur_c = -1
        self.cur_r = -1
        self.next_c = -1
        self.next_r = -1

    def update_sector(self, c, r):
        """
        This function updates the travel history of this event
        :param c: col coordinate
        :param r: row coordinate
        :return:
        """
        self.cur_c = c
        self.cur_r = r
        self.travel_history[(c, r)] += 1

    def update_next_sector(self):
        numbers = [i for i in range(100)]
        stay = numbers[:self.probability*100]
        i = random.randint(0, 99)
        cur_quadrant = quadrant(self.cur_c, self.cur_r, self.row_dim, self.col_dim)
        if i in stay:
            self.next_c, self.next_r = random_from_quadrant(self.col_dim, self.row_dim, cur_quadrant)
        else:
            quads = [1, 2, 3, 4].remove(cur_quadrant)
            remove_not_neighbor(quads, cur_quadrant)
            goto_quad = quads[random.randint(0, 1)]
            self.next_c, self.next_r = random_from_quadrant(self.col_dim, self.row_dim, goto_quad)

    def update_die_time(self, cur_time):
        """
        This function will update the death time as soon as an event set up
        :param cur_time: the current time
        :return:
        """
        self.die_time = cur_time + self.life_time_expo

    def update_next_move_time(self, dur_time):
        """
        This function will update the next move time of the event
        :param dur_time: The duration time of the event
        :return:
        """
        self.finish_time += dur_time


def quadrant(c, r, col_dim, row_dim):
    """
    This function will tell you which quadrant the sector is
    :param c: current column
    :param r: current row
    :param col_dim: Col num in the board
    :param row_dim: Row num in the board
    :return: The quadrant
    """
    mid_row = int((row_dim-1)/2)
    mid_col = int((col_dim-1)/2)

    if mid_row < r < row_dim and mid_col < c < col_dim:
        return 1
    elif 0 <= r <= mid_row and mid_col < c < col_dim:
        return 2
    elif 0 <= c <= mid_col and 0 <= r <= mid_row:
        return 3
    else:
        return 4


def random_from_quadrant(col_dim, row_dim, q):
    """
    This function finds a random sector in the given quadrant
    :param col_dim: column number on the board
    :param row_dim: row number on the board
    :param q: quadrant number
    :return: the (x, y) coordinate of the next step in the given quadrant
    """
    mid_row = int((row_dim-1)/2)
    mid_col = int((col_dim-1)/2)
    if q == 1:
        return random.randint(mid_row+1, row_dim-1), random.randint(mid_col+1, col_dim-1)
    if q == 2:
        return random.randint(0, mid_row), random.randint(mid_col+1, col_dim-1)
    if q == 3:
        return random.randint(0, mid_row), random.randint(0, mid_col)
    if q == 4:
        return random.randint(mid_row+1, row_dim-1), random.randint(0, mid_col)


def remove_not_neighbor(quads, cur_quadrant):
    """
    This function will delete the quadrant that are not the neighbor of the current quadrant
    :param quads: The quadrant list
    :param cur_quadrant: current quadrant
    :return:
    """
    if cur_quadrant == 1:
        quads.remove(3)
    elif cur_quadrant == 2:
        quads.remove(4)
    elif cur_quadrant == 3:
        quads.remove(1)
    else:
        quads.remove(2)







