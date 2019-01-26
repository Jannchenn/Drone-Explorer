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
    total_events = Board.board_info.get_total_events()
    total_caught_events = drone.get_total_caught_event()
    simple_stats.stats(total_events, total_caught_events)
    update_thread.stop = True
    update_thread.join()

