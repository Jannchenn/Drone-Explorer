# ======================================================================
# FILE:        Event.py
#
# DESCRIPTION: This file contains EventFix and EventMove class.
#               This class will handle the fix event (distribution...),
#               and another EventMove class will handle movement events
#
# ======================================================================

from collections import defaultdict
import random


class Event:
    sector_id = defaultdict(int)

    def __init__(self, dur_dis):
        self.dur = dur_dis
        self.start_time = 0
        self.finish_time = 0

    def update_sector_id(self, c, r):
        """
        This function will update event id for corresponding sectors. It just record how many events
        a sector already has
        :param c: the sector column
        :param r: the sector row
        """
        self.sector_id[(c, r)] += 1

    def get_sector_ids(self):
        return self.sector_id

    def get_dur_time(self):
        """
        This function will return a duration time for a curtain event.
        :return: a float that indicating duration time based on certain distribution
        """
        return self.dur()


class EventFix(Event):
    event_id = 1

    def __init__(self, dur_dis, buf_dis):
        """
        :param buf_dis: buffer time beween events
        :param dur_dis: duration time of events
        """
        Event.__init__(self, dur_dis)
        # may update other features and parameters later
        self.buf = buf_dis
        self.id = EventFix.event_id
        EventFix.event_id += 1

    def get_buf_time(self):
        """
        This function will return a buffer time for a curtain event.
        :return: a float that indicating buffer time based on certain distribution
        """
        return self.buf()


class EventMove(Event):
    event_id = 1

    def __init__(self, dur_dis, col, row):
        Event.__init__(self, dur_dis)
        self.next_coor = (0, 0)
        self.col_dim = col
        self.row_dim = row
        self.id = EventMove.event_id
        EventMove.event_id += 1

    def update_next_sector(self, c, r):
        """
        This method will update the next available coordinate for the event
        :param c: the current column
        :param r: the current row
        """
        left = (c - 1, r)
        right = (c + 1, r)
        up = (c, r + 1)
        down = (c, r - 1)

        if c == 0 and r == 0:
            available = [up, right]
            self.next_coor = available[random.randint(2)]
        elif c == 0 and r == self.row_dim:
            available = [down, right]
            self.next_coor = available[random.randint(2)]
        elif c == self.col_dim and r == 0:
            available = [left, up]
            self.next_coor = available[random.randint(2)]
        elif c == self.col_dim and r == self.row_dim:
            available = [left, down]
            self.next_coor = available[random.randint(2)]
        elif c == 0:
            available = [up, down, right]
            self.next_coor = available[random.randint(3)]
        elif c == self.col_dim:
            available = [left, up, down]
            self.next_coor = available[random.randint(3)]
        elif r == 0:
            available = [left, right, up]
            self.next_coor = available[random.randint(3)]
        elif r == self.row_dim:
            available = [left, right, down]
            self.next_coor = available[random.randint(3)]
        else:
            available = [left, right, up, down]
            self.next_coor = available[random.randint(4)]

    def get_next_sector(self):
        """
        This method will get the next avaliable coordinate for the event
        """
        return self.next_coor


