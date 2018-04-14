import Arena
import time
#import thread
import threading
import Distribution

start_dist = Distribution.Distribution(0.25)
dur_dist = Distribution.Distribution(0.1)
board_info = Arena.Arena(-35.36323782441763, 149.16522927736207, time.time(), start_dist.exponential, dur_dist.exponential)
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