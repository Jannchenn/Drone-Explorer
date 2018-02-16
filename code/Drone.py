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

board_info = Board.board_info



# --Connect to the vehicle
import argparse

class Drone():

    def __init__(self,board):

        self.parser = argparse.ArgumentParser(description='commands')
        self.parser.add_argument('--connect')
        self.args = self.parser.parse_args()

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


    def run(self):


        # ------ MAIN PROGRAM
        self.arm_and_takeoff(10)

        # ------ set the default speed
        self.vehicle.airspeed = 7

        # ------ Go to wpl
        print("Go to wpl")

	for i in range(10):
	    i = randrange(100)

	    lat = self.board[i][0]
	    lon = self.board[i][1]
	    c = self.board[i][2]
	    r = self.board[i][3]
            wpl = LocationGlobalRelative(lat, lon, 10)

            self.vehicle.simple_goto(wpl)

	    while (get_distance_metres(self.vehicle.location.global_relative_frame,wpl)>1):
	    	time.sleep(0.5)
		print("NOT ARRIVED")
	    time.sleep(5)
	    print("ARRIVED")
	    print("EVENT: " +  board_info.get_event(c,r,time.time()))

        # ------ Here you can call your magic
        time.sleep(60)

        # ------ Coming back
        print("Coming back")
        self.vehicle.mode = VehicleMode("RTL")

        time.sleep(60)

        # ------ Close connection
        self.vehicle.close()

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







