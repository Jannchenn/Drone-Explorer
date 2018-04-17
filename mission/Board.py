# ======================================================================
# FILE:        Board.py
#
# DESCRIPTION: This file contains Threading class, and this file will
#               initiate the board to be explored
#
# ======================================================================

import Arena
import time
#import thread
import threading
import Distribution

try:
    f1 = open("paras.txt", "r")
    f2 = open("boardinput.txt", "r")
except IOError:
    print "Cannot open paras.txt"
else:
    paras = f1.read().split('\n')
    lambdas = f2.read().split('\n')[0].split()
    f1.close()
    f2.close()

row = int(paras[0].split()[0])
col = int(paras[0].split()[1])
dis = paras[1]

buf_dist = Distribution.Distribution(float(lambdas[0]))
dur_dist = Distribution.Distribution(float(lambdas[1]))
if dis == "expo":
    board_info = Arena.Arena(-35.36323782441763, 149.16522927736207, time.time(), dur_dist.exponential,
                             buf_dist.random20, row,col)
else:
    board_info = Arena.Arena(-35.36323782441763, 149.16522927736207, time.time(), dur_dist.exponential,
                             buf_dist.random20, row, col)
# pass board thread to drone
board = board_info.get_longlat()


class Threading(object):
    """ Threading class
    The run() method will start and it will run in the background until application exists

    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        """ Method runs forever
        """
        while True:
            board_info.update_board()
            time.sleep(self.interval)
