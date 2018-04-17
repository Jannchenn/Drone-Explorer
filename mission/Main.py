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
import Stats


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


if __name__ == "__main__":
    #Parameters.Parameters().run()
    paras = get_paras()
    row = int(paras[0].split()[0])
    col = int(paras[0].split()[1])

    for _ in range(10): #remember to edit
        board = Board.board
        policy = Policy.Policy(board, (0, 0), (0, row-1), col, row)
        update_thread = Board.Threading()
        if paras[-3] == "roomba":
            drone = Drone.Drone(board, policy.roomba, paras[-2], (int(paras[-1]) if paras[-2] == "movement" else float(paras[-1])), row, col)
        else:
            drone = Drone.Drone(board, policy.random, paras[-2], (int(paras[-1]) if paras[-2] == "movement" else float(paras[-1])), row, col)
        drone.run()
        info = drone.get_stats_info()
        Stats.stats(info)

