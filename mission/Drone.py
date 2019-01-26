# ======================================================================
# FILE:        Drone.py
#
# DESCRIPTION: This file control the drone action
#
# ======================================================================

from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math
from random import randrange
import Board
from collections import defaultdict
import Event

board_info = Board.board_info  # The board that keeps updating events

# --Connect to the vehicle
import argparse


class Drone:
    # Tile Structure
    class __Tile:
        last_time_visit = 0
        has_event = False
        id = defaultdict(list)

    def __init__(self, board, policy, fix, r, row, col):
        """
         Initializes drone flight characteristcs
        :param parser:
        :param my_time: current time
        :param time_arrived:
        :param policy: function of direction drone will fly
        :param fix: a string that determines if the drone's flight is limited to movement or time
        :param round: integer of number of times drone will look for an event if drone flies accorrding to a fixed movment
                      integer of number of minutes if drone flies according to fixed time
        """
        self.parser = argparse.ArgumentParser(description='commands')
        self.parser.add_argument('--connect')
        self.args = self.parser.parse_args()

        self.policy = policy
        self.fix = fix
        self.round = r
        self.__colDimension = col
        self.__rowDimension = row

        # self.times_arrived = defaultdict(int)
        val = lambda: defaultdict(list)
        self.times_hasEvent = defaultdict(val)
        self.total_visit = 0
        self.total_fix_events = 0
        self.total_move_events = 0
        self.movements = list()
        self.missed = defaultdict()
        self.start = 0
        self.end = 0
        self.count = 0

        self.connection_string = self.args.connect

        print("Connection to the vehicle on %s" % self.connection_string)
        self.vehicle = connect(self.connection_string, wait_ready=True)
        self.speed = 0
        self.board = board  # The board has long, lat, col and row
        self.explore = [[self.__Tile() for j in range(self.__colDimension)] for i in
                        range(self.__rowDimension)]  # The board includes information that drone catches

    # --Define the function for takeoff
    def arm_and_takeoff(self, tgt_altitude):
        """
        :param tgt_altitude: the artitude for taking off
        """
        print("Arming motors")

        while not self.vehicle.is_armable:
            time.sleep(1)

        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        print("Takeoff")
        self.vehicle.simple_takeoff(tgt_altitude)

        # --wait to reach the target altitude
        while True:
            altitude = self.vehicle.location.global_relative_frame.alt

            if altitude >= tgt_altitude - 1:
                print("Altitude reached")
                break

            time.sleep(1)

    def run(self):
        """
        flies vehicle according to fixed time or fixed movement, which is
        determined in main
        """
        # ------ MAIN PROGRAM
        self.arm_and_takeoff(10)

        # ------ set the default speed
        self.vehicle.airspeed = 10
        self.speed = 10

        # ------ Go to wpl
        print("Go to wpl")

        self.start = time.time()
        if self.fix == "time":
            timeout = time.time() + self.round  # round minutes from now
            while True:
                if time.time() > timeout:
                    break
                self.fly()

        elif self.fix == "movement":
            for _ in range(self.round):
                self.fly()

        self.end = time.time()
        #self.count = self.missed_events()

        # ------ Coming back
        print("Coming back")
        self.vehicle.mode = VehicleMode("RTL")

        time.sleep(60)

        # ------ Close connection
        self.vehicle.close()

        # self.stats()

    def fly(self):
        """
        fly the drone according to the policy
        """
        data = self.policy()
        c = data[0]
        r = data[1]
        wpl = data[2]
        self.vehicle.simple_goto(wpl)
        self.collect_data(c, r, wpl)

    def collect_data(self, c, r, wpl):
        """
        For each sector we reached, we need to collect information from it, aka fly log
        :param c: the coloum of the board; r: the row of the board; wpl: the loaction of the sector
        """
        while (get_distance_metres(self.vehicle.location.global_relative_frame, wpl) > 2):
            print(get_distance_metres(self.vehicle.location.global_relative_frame, wpl))
            time.sleep(0.1)
            #print("NOT ARRIVED")
        print("ARRIVED")
        # Collect and update explore map
        self.total_visit += 1
        self.movements.append((c, r))
        # self.times_arrived[(c, r)] += 1

        now_time = time.time()
        #self.explore[c][r].last_time_visit = now_time
        has_event = board_info.get_event(c, r)
        events = board_info.get_current_event_status(c, r)
        for event in events:
            self.times_hasEvent[(c, r)][event].append(now_time)
            if type(event) is Event.EventFix:
                self.total_fix_events += 1
            else:
                self.total_move_events += 1
        #event_id = board_info.get_id(c, r, now_time)  # it's a list result = ['EventFix':[], 'EventMove':[]]
        # if has_event:
        #     for k, v in event_id:
        #         if k == "EventFix":
        #             self.total_fix_events += 1
        #             self.times_hasEvent[(c,r)]['Fix'].extend(event_id['EventFix'])
        #         else:
        #             self.total_move_events += 1
        #             self.times_hasEvent[(c,r)]['Move'].extend(event_id['EventMove'])
                #self.total_events += 1
                #self.times_hasEvent[(c, r)][event_id].append(now_time)
        #self.explore[c][r].has_event = has_event
        #self.explore[c][r].id = event_id

        print("EVENT: " + str(has_event))

    def count_different(self):
        """
        :return: the number of different events; result={'EventMove':100, 'EventFix':193}
        """
        result = defaultdict(int)
        for each in self.times_hasEvent.values():
            for event in each.keys():
                if type(event) is Event.EventFix:
                    result['EventFix'] += 1
                else:
                    result['EventMove'] += 1
        return result

    def missed_events(self):
        """
        Updates self.missed so that track the missed events for each sector.
        :return: the total number of events generated
        """
        count = 0
        for row in range(self.__rowDimension):
            for col in range(self.__colDimension):
                max_id = board_info.get_max_id(col, row)
                count += max_id
                if (col, row) not in self.times_hasEvent.keys():
                    self.missed[(col, row)] += max_id
                else:
                    events = self.times_hasEvent[(col, row)].keys()
                    for i in range(max_id):
                        if i + 1 not in events:
                            self.missed[(col, row)] += 1
        return count

    def total_missed_events(self):
        """
        This method will count the TOTAL missed events
        """
        # result = 0
        # for val in self.missed.values():
        #     result += val
        # return result
        set_move = set()
        set_fix = set()
        max_id = board_info.get_max_both_id()
        fix = max_id[0]
        move = max_id[1]
        for each in self.times_hasEvent.values():
            for event in each.keys():
                if type(event) is Event.EventFix:
                    if event not in set_fix:
                        set_fix.add(event)
                        fix -= 1
                else:
                    if event not in set_move:
                        set_move.add(event)
                        move -= 1
        return [fix, move]

    def get_stats_info(self):
        """
        returns a tuple that contains all the information needed
        """
        missed_events = self.total_missed_events()
        missed_fix_events = missed_events[0]
        missed_move_events = missed_events[1]
        return (self.total_fix_events + self.total_move_events, self.total_fix_events, self.total_move_events,
                self.count_different(), missed_events, missed_fix_events, missed_move_events,
                self.__rowDimension, self.__colDimension,
                self.times_hasEvent, self.total_visit, self.round, self.speed, Event.EventFix.event_id+Event.EventMove.event_id-2)

    def get_total_caught_event(self):
        return self.total_fix_events + self.total_move_events

    def get_time(self):
        """
        This function will get the flying time
        :return: a tuple of start and end time
        """
        return self.start, self.end


def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    print ("target: " + str(aLocation2.lat) + " " + str(aLocation2.lon) + "/n")
    print ("reached: " + str(aLocation1.lat) + " " + str(aLocation1.lon) + "/n")
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5



