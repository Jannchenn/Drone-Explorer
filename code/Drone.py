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

board_info = Board.board_info



# --Connect to the vehicle
import argparse

class Drone():

    def __init__(self,board,policy):

        self.parser = argparse.ArgumentParser(description='commands')
        self.parser.add_argument('--connect')
        self.args = self.parser.parse_args()
        self.times_arrived = defaultdict(int)
        self.times_hasEvent = defaultdict(int)
        self.total_visit = 0
        self.total_events = 0
        self.policy = policy

        self.connection_string = self.args.connect

        print("Connection to the vehicle on %s" % self.connection_string)
        self.vehicle = connect(self.connection_string, wait_ready=True)
        self.board = board


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

    def stats(self):
	report = open("report.txt","w+")
	report.write("Times Arrived: \n")
	for r in range(10):
	    for c in range(10):
		report.write(self.times_arrived[(r,c)])
		report.write("    ")
	    report.write("\n")
	report.write("Times has events: \n")
	for r in range(10):
	    for c in range(10):
		report.write(self.times_hasEvent[(r,c)])
		report.write("    ")
	    report.write("\n")
	report.write("Total sectors visited: \n")
	report.write(self.total_visit)
	report.write("\nTotal events detected: \n")
	report.write(self.total_events)
	report.close()


    def run(self):


        # ------ MAIN PROGRAM
        self.arm_and_takeoff(10)

        # ------ set the default speed
        self.vehicle.airspeed = 7

        # ------ Go to wpl
        print("Go to wpl")

	for _ in range(3):
	    if (self.policy=="random"):
	    	i = randrange(100) # i,j; what's next(policy)
	    	coor = change_to_coordinate(i)
	    	lat = self.board[i][0]
	    	lon = self.board[i][1]
	    	c = self.board[i][2]
	    	r = self.board[i][3]
            	wpl = LocationGlobalRelative(lat, lon, 10)
	    elif (self.policy == "inorder"):
	    	coor = change_to_coordinate(_)
	    	lat = self.board[_][0]
	    	lon = self.board[_][1]
	    	c = self.board[_][2]
	    	r = self.board[_][3]

            self.vehicle.simple_goto(wpl)

	    while (get_distance_metres(self.vehicle.location.global_relative_frame,wpl)>1):
	    	time.sleep(0.5)
		print("NOT ARRIVED")
	    print("ARRIVED")
	    self.total_visit += 1
	    self.times_arrived[coor] += 1
	
	    has_event = board_info.get_event(c,r,time.time())
	    if has_event=="HasEvent":
		self.total_events += 1
		self.times_hasEvent[coor] += 1
	    print("EVENT: " +  has_event)
	    time.sleep(5)

        # ------ Here you can call your magic
        time.sleep(1)

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

def change_to_coordinate(index):
    """
    Given the index i, returns its corresponding coordinates
    """
    x = index / 10
    if x%2 == 0:
	y = index % 10
    else:
	y = 9 - index % 10
    return (int(x),int(y))







