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
from collections import defaultdict
from Event import EventFix
from Event import EventMove
from Event import Event


class Arena():
    # Tile Structure
    class __Tile:
        start_fix_time = 0
        finish_fix_time = 0
        buf = 0
        dur = 0
        lat = 0
        long = 0
        id = 0

    # ===============================================================
    # =                         Constructor
    # ===============================================================

    def __init__(self, my_lat, my_lon, my_time, row, col, etype, dur_dis_fix, dur_dis_move, buf_dis, initial):
        """Initializes board with 10 x 10 dimensions
        :param my_lat: the initial latitude
        :param my_lon: the initial longitude
        :param my_time: current time
        :param buf_dis: buffer time between events
        :param dur_dis_fix: duration time of fixed events
        :param dur_dis_move: duration time of moving events
        :param initial: percentage of sectors have events initially
        """
        self.__total_events = 0
        self.__total_buf = 0
        self.__total_dur_fix = 0
        self.__total_dur_move = 0
        self.__buf_dis = buf_dis
        self.__dur_dis_fix = dur_dis_fix
        self.__dur_dis_move = dur_dis_move
        # may update other features and parameters later

        self.__colDimension = col
        self.__rowDimension = row
        self.__time = my_time
        self.__type = etype  # Type of events that the board will have: fix, move, both
        self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
        self.__addLongLat(my_lat, my_lon)
        self.__initial = initial
        self.events = defaultdict(list)  # Record list of events for every sector

        self.__addEventTimes()

    # ===============================================================
    # =             Arena Generation Functions
    # ===============================================================
    def __addLongLat(self, lat, lon):
        """
        This method assigns longitude and latitude to the board
        :param lat: the start latitude
        :param lon: the start longitude
        :return: None
        """
        dNorth = 0
        dEast = 0
        earth_radius = 6378137.0  # Radius of "spherical" earth
        self.__board[0][0].lat = lat
        self.__board[0][0].long = lon
        for c in range(1, self.__colDimension):
            dEast += 10
            dLat = dNorth / earth_radius
            dLon = dEast / (earth_radius * math.cos(math.pi * lat / 180))
            self.__board[c][0].lat = lat + (dLat * 180 / math.pi)
            self.__board[c][0].long = lon + (dLon * 180 / math.pi)
        dEast = 0
        for r in range(1, self.__rowDimension):
            dNorth += 10
            for c in range(0, self.__colDimension):
                dLat = dNorth / earth_radius
                dLon = dEast / (earth_radius * math.cos(math.pi * lat / 180))
                self.__board[c][r].lat = lat + (dLat * 180 / math.pi)
                self.__board[c][r].long = lon + (dLon * 180 / math.pi)
                dEast += 10
            dEast = 0

    def setUpEvent(self):
        """
        initializes event's id and event dictionary
        for now, one sector may have multiple events initially
        :return: None
        """
        for _ in range(self.__rowDimension * self.__colDimension * self.__initial):
            c = random.randint(self.__colDimension)
            r = random.randint(self.__rowDimension)
            new_event = EventMove(self.__dur_dis_move, self.__colDimension, self.__rowDimension)
            self.events[(c, r)].append(new_event)
            new_event.update_next_sector(c, r)
            self.__board[c][r].id += 1
            self.__total_events += 1

    def __addEventTimes(self):
        """
        This method add event times when the board first created
        :return: None
        """
        self.setUpEvent()

        if self.__type != "move":
            for r in range(self.__rowDimension):
                for c in range(self.__colDimension):
                    new_event = EventFix(self.__dur_dis_fix, self.__buf_dis)
                    self.events[(c, r)].append(new_event)
                    self.__board[c][r].id += 1
                    self.__total_events += 1

        # set start times for event
        for k, v in self.events.items():
            for e in v:
                dur_time = e.get_dur_time()
                if type(e) is EventMove:
                    e.start_time = self.__time
                    self.__total_dur_move += dur_time
                elif type(e) is EventFix:
                    buf_time = e.get_buf_time()
                    self.__total_buf += buf_time
                    e.start_time = self.__time + buf_time
                    self.__total_dur_fix += dur_time
                e.finish_time = e.start_time + dur_time


    # ===============================================================
    # =             Arena Fetch Functions
    # ===============================================================
    def update_board(self):
        """
        This method keeps updating the board with new events
        :return: None
        """
        time_now = time.time()
        new_events = []
        passed_events = []
        for k, v in self.events.items():
            c = k[0]
            r = k[1]
            for e in v:
                if type(e) is EventFix:
                    if time_now > e.finish_time:
                        new_event = EventFix(self.__dur_dis_fix, self.__buf_dis)
                        buf_time = new_event.get_buf_time()
                        new_event.start_time = e.finish_time + buf_time
                        self.__total_buf += buf_time
                        dur_time = new_event.get_dur_time()
                        new_event.finish_time = new_event.start_time + dur_time
                        self.__total_dur_fix += dur_time
                        passed_events.append((c, r, e))
                        new_events.append((c, r, new_event))
                elif type(e) is EventMove:
                    # post event duration
                    if time_now > e.finish_time:
                        # EventMove moves
                        next_coor = e.get_next_sector()
                        e.start_time = e.finish_time
                        dur_time = e.get_dur_time()
                        e.finish_time = e.start_time + dur_time
                        self.__total_dur_move += dur_time
                        e.update_next_sector(next_coor[0], next_coor[1])
                        # delete coordinate from event dictionary
                        passed_events.append((c, r, e))
                        # add new coordinate to event dictionary
                        new_events.append((next_coor[0], next_coor[1], e))

        # reset event dictionary
        self.delete_events(passed_events)
        self.add_events_to_dict(new_events)

    def add_events_to_dict(self, new_events):
        for e in new_events:
            c = e[0]
            r = e[1]
            event = e[2]
            self.events[(c, r)].append(event)
            self.__board[c][r].id += 1
            self.__total_events += 1

    def delete_events(self, passed_events):
        for e in passed_events:
            c = e[0]
            r = e[1]
            event = e[2]
            self.events[(c, r)].remove(event)

    def get_board(self):
        """
        This method get and print current board status(information)
        :param t: the current time
        :return: None, but will print this sector has event or not
        """
        for r in range(self.__rowDimension):
            for c in range(self.__colDimension):
                if len(self.events[(c, r)]) != 0:
                    print(self.__board[c][r].lat, self.__board[c][r].long, "HasEvent", self.__board[c][r].id)
                else:
                    print("NoEvent")

    def get_event(self, c, r):
        """
        This method will return if the sector has event or not
        :param c: the column of the board
        :param r: the row of the board
        :return: True if this sector at this time has event; false otherwise
        """
        return len(self.events[(c, r)]) != 0

    def get_current_event_status(self, c, r):
        """
        Get the current event status for a certain sector
        :return: Event list for a certain sector at certain time
        """
        return self.events[(c, r)]

    def get_id(self, c, r):
        """
        The method gets the current event id
        :param c: the column of the board
        :param r: the row of the board
        :param t: the current time
        :return: the event id of current event; result = ['EventFix':[], 'EventMove':[]]
        """
        result = defaultdict(list)
        events = self.events[(c, r)]
        for e in events:
            if type(e) is EventFix:
                result['EventFix'].append(e.id)
            else:
                result['EventMove'].append(e.id)
        return result

    def get_max_id(self, c, r):
        """
        The method gets the current max id from the current sector
        :param c: the column of the board
        :param r: the row of the board
        :return: the (current) max id of this sector, result = ['EventFix':0, 'EventMove':0]
        """
        result = defaultdict(int)
        events = self.events[(c, r)]
        max_move = 0
        max_fix = 0
        for e in events:
            if type(e) is EventFix and e.id > max_fix:
                result['EventFix'] = e.id
                max_fix = e.id
            elif type(e) is EventMove and e.id > max_move:
                result['EventMove'] = e.id
                max_move = e.id
        return result

    def get_max_both_id(self):
        """
        The method return the max ids for both EventMove and EventFix
        :return: [EventFix_max, EventMove_max]
        """
        return [EventFix.event_id-1, EventMove.event_id-1]

    def get_longlat(self):
        """
        :return: one dimension of board, [(lat,long,0,0),(lat,lon,0,1),(lat,lon,0,2),(lat,lon,2,1),....]
        """
        result = []
        for r in range(self.__rowDimension):
            if r % 2 == 0:
                for c in range(self.__colDimension):
                    result.append((self.__board[c][r].lat, self.__board[c][r].long, c, r))
            else:
                for c in range(self.__colDimension - 1, -1, -1):
                    result.append((self.__board[c][r].lat, self.__board[c][r].long, c, r))
        return result

    def get_average_buf(self):
        """
        This method will calculate the average buffer time
        :return: the average buffer time
        """
        if self.__total_events != 0:
            return self.__total_buf / self.__total_events
        return 0

    def get_average_dur_fix(self):
        """
        This method will calculate the average fix event duration time
        :return: the average duration time
        """
        total_fix_num = self.get_max_both_id()[0]
        if total_fix_num != 0:
            return self.__total_dur_fix / total_fix_num
        return 0

    def get_average_dur_move(self):
        """
        This method will calculate the average move event duration time
        :return: the average duration time
        """
        total_move_num = self.get_max_both_id()[1]
        if total_move_num != 0:
            return self.__total_dur_move / total_move_num
        return 0

    def get_board_info(self):
        """
        This function will return a tuple of information about the board
        :return: a tuple of information about the board
        """
        return self.__colDimension, self.__rowDimension, self.get_average_buf(), self.get_average_dur_fix(), self.get_average_dur_move()
