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

import Drone
import Policy
import Board
import simple_stats
from time import time


def get_paras():
    """
    This function returns a list of parameters
    :return: a list of parameters
    """
    try:
        f = open("paras.txt","r")
    except IOError:
        print "Cannot open paras.txt"
    else:
        paras = f.read().split('\n')
        f.close()
        return paras

def get_avg(file_name):
    record = open(file_name, "w")
    total = 0
    counter = 0
    for line in record.readlines():
        if line != "":
            total += float(line)
            counter += 1
    record.close()
    return total/counter



if __name__ == "__main__":
    #Parameters.Parameters().run()
    paras = get_paras()
    row = int(paras[0].split()[0])
    col = int(paras[0].split()[1])

    board = Board.board
    policy = Policy.Policy(board, (0, 0), (0, row-1), col, row)
    update_thread = Board.Threading()
    if paras[-3] == "roomba":
        drone = Drone.Drone(board, policy.roomba, paras[-2], (int(paras[-1]) if paras[-2] == "movement" else float(paras[-1])), row, col)
    else:
        drone = Drone.Drone(board, policy.random, paras[-2], (int(paras[-1]) if paras[-2] == "movement" else float(paras[-1])), row, col)
    drone.run()
    #drone_info = drone.get_stats_info()
    #drone_info = drone_info + (paras[-3], )
    board_info = Board.board_info.get_board_info()
    t = drone.get_time()
    simple_stats.stats(board_info)
    #Stats.drone_stats(drone_info)
    #Stats.drone_total_stats(drone_info)
    #Stats.time_info(t[0], t[1])
    update_thread.stop = True
    update_thread.join()

