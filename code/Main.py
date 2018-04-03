# ======================================================================
# FILE:        Main.py
#
# DESCRIPTION: This file contains main function for the board running
#               in the background
#
# ======================================================================

import time
#import thread
import threading
import Drone

board_info = Drone.board_info
board = board_info.get_longlat()
drone = Drone.Drone(board,"random")


class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            board_info.update_board()
            print('Doing something imporant in the background')

            time.sleep(self.interval)

example = ThreadingExample()
time.sleep(3)
print('Checkpoint')
time.sleep(2)
board_info.get_board(time.time())
print('Bye')

drone.run()
drone.stats()



#board_info = Arena.board_info

#try:
#    thread.start_new_thread(board_info.update_board(), ("Thread-1", 2,))

#except:
#    print "Error: unable to start thread"

#time.sleep(10)
#thread.start_new_thread(board_info.get_board(time.time()), ("Thread-2", 4,))
