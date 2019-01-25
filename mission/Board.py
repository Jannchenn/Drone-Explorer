# ======================================================================
# FILE:        Board.py
#
# DESCRIPTION: This file includes Threading class that will start the 
#               board to update. Also, it will initialize the board
#               information
#
# ======================================================================

import Arena
import time
import threading
import Distribution

try:
    f1 = open("fix_paras.txt", "r")
    f2 = open("boardinput.txt", "r")
except IOError:
    print "Cannot open"
else:
    paras = f1.read().split('\n')
    indep_var = f2.read().split('\n')[0].split()
    f1.close()
    f2.close()

    row = int(paras[0].split()[0])
    col = int(paras[0].split()[1])
    event_attr = paras[1].split()

    prob = float(indep_var[0])
    dur_dist = Distribution.Distribution(float(indep_var[1]))
    arrival_rate = Distribution.Distribution(float(event_attr[0])) #expo
    arrival_num = int(event_attr[1])
    die_rate = Distribution.Distribution(float(event_attr[2])) #expo
    board_info = Arena.Arena(-35.36323782441763, 149.16522927736207, row, col, arrival_rate.exponential, arrival_num,
                             prob, dur_dist.exponential, die_rate.exponential)
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
        self.thread = threading.Thread(target=self.run, args=())
        self.stop = False
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        """ Method runs forever
        """
        while not self.stop:
            board_info.update_board()
        print "Stop updating board"

    def join(self):
        self.thread.join()
