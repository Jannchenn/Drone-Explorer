# ======================================================================
# FILE:        Main.py
#
# DESCRIPTION: This file contains main function for the board running
#               in the background
#
# CHANGES MADE 04/08: inorder, graph
#
# CHANGES TO BE MADE: take out threading example
# ======================================================================

import time
#import thread
import threading
import Drone
import Policy
import Board
import Stats


board_info = Drone.board_info
board = board_info.get_longlat()

update_thread = Board.Threading() # board begins to update
time.sleep(3)
print('Checkpoint')
time.sleep(2)
board_info.get_board(time.time())
print('Bye')

policy = Policy.Policy(board,(0,0),(0,9),10,10)

drone = Drone.Drone(board,policy.roomba,"movement",32)
drone.run()
info = drone.get_stats_info()
Stats.stats(info)



#board_info = Arena.board_info

#try:
#    thread.start_new_thread(board_info.update_board(), ("Thread-1", 2,))

#except:
#    print "Error: unable to start thread"

#time.sleep(10)
#thread.start_new_thread(board_info.get_board(time.time()), ("Thread-2", 4,))