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

board_info = Board.board_info #The board that keeps updating events



# --Connect to the vehicle
import argparse

class Drone():
    # Tile Structure
    class __Tile:
        last_time_visit = 0
        has_event = False
        id = 0

    def __init__(self,board,policy):

        self.parser = argparse.ArgumentParser(description='commands')
        self.parser.add_argument('--connect')
        self.args = self.parser.parse_args()
        self.times_arrived = defaultdict(int)
        val = lambda:defaultdict(int)
        self.times_hasEvent = defaultdict(val)
        self.total_visit = 0
        self.total_events = 0
        self.policy = policy
        self.__colDimension = 3
        self.__rowDimension = 3

        self.connection_string = self.args.connect

        print("Connection to the vehicle on %s" % self.connection_string)
        self.vehicle = connect(self.connection_string, wait_ready=True)
        self.board = board # The board has long, lat, col and row
        self.explore = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)] # The board includes information that drone catches


    # --Define the function for takeoff
    def arm_and_takeoff(self, tgt_altitude):
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


    def count_event(self):
        result=0
        for each in self.times_hasEvent.values():
            result += len(each)

        return result

    def stats(self):

        report = open("report.txt","w+")
        report.write("Total num event catched: ")
        report.write(str(self.count_event()))
        report.write("\n")
        report.write("Event for each sector: \n")
        for row in range(self.__rowDimension):
            for col in range(self.__colDimension):
                if (col, row) in self.times_hasEvent.keys():
                    for each in self.times_hasEvent[(col,row)].keys():
                        report.write(str(each))
                        report.write(",")
                        report.write(str(self.times_hasEvent[(col,row)][each]))
                        report.write(";")
                    report.write("\t")
                else:
                    report.write("0\t")
            report.write("\n")

        report.write("Total sectors visited: ")
        report.write(str(self.total_visit))
        report.write("\n")
        report.close()


    def collect_data(self,c,r,wpl):
        while (get_distance_metres(self.vehicle.location.global_relative_frame, wpl) > 1):
            time.sleep(0.5)
            print("NOT ARRIVED")
        print("ARRIVED")
        # Collect and update explore map
        self.total_visit += 1
        self.times_arrived[(c, r)] += 1

        now_time = time.time()
        self.explore[c][r].last_time_visit = now_time
        has_event = board_info.get_event(c, r, now_time)
        event_id = board_info.get_id(c, r, now_time)
        if has_event:
            self.total_events += 1
            self.times_hasEvent[(c, r)][event_id] += 1
        self.explore[c][r].has_event = has_event
        self.explore[c][r].id = event_id

        print("EVENT: " + str(has_event))
        time.sleep(5)

    def run(self):


        # ------ MAIN PROGRAM
        self.arm_and_takeoff(10)

        # ------ set the default speed
        self.vehicle.airspeed = 7

        # ------ Go to wpl
        print("Go to wpl")

        if (self.policy == "random"):
            for _ in range(5): # Change the number of sectors the drone would like to fly
                i = randrange(len(self.board)) # i,j; what's next(policy)
                #coor = change_to_coordinate(i)
                lat = self.board[i][0]
                lon = self.board[i][1]
                c = self.board[i][2]
                r = self.board[i][3]
                wpl = LocationGlobalRelative(lat, lon, 10)
                self.vehicle.simple_goto(wpl)
                self.collect_data(c,r,wpl)
        elif (self.policy == "inorder"):
            for _ in range(len(self.board)):
                #coor = change_to_coordinate(_)
                lat = self.board[_][0]
                lon = self.board[_][1]
                c = self.board[_][2]
                r = self.board[_][3]
                wpl = LocationGlobalRelative(lat, lon, 10)
                self.vehicle.simple_goto(wpl)
                self.collect_data(c,r,wpl)

            # while (get_distance_metres(self.vehicle.location.global_relative_frame,wpl)>1):
            #     time.sleep(0.5)
            #     print("NOT ARRIVED")
            # print("ARRIVED")
            # # Collect and update explore map
            # self.total_visit += 1
            # self.times_arrived[(c,r)] += 1
            #
            # now_time = time.time()
            # self.explore[c][r].last_time_visit = now_time
            # has_event = board_info.get_event(c, r, now_time)
            # event_id = board_info.get_id(c, r, now_time)
            # if has_event:
            #     self.total_events += 1
            #     self.times_hasEvent[(c, r)][event_id] += 1
            # self.explore[c][r].has_event = has_event
            # self.explore[c][r].id = event_id
            #
            #
            # print("EVENT: " + has_event)
            # time.sleep(5)

        # ------ Coming back
        print("Coming back")
        self.vehicle.mode = VehicleMode("RTL")

        time.sleep(60)

        # ------ Close connection
        self.vehicle.close()

        self.stats()


def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

# def change_to_coordinate(index):
#     """
#     Given the index i, returns its corresponding coordinates
#     """
#     x = index / 10
#     if x%2 == 0:
#         y = index % 10
#     else:
#         y = 9 - index % 10
#     return (int(x),int(y))
