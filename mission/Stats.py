# ======================================================================
# FILE:        Stats.py
#
# DESCRIPTION: This file compute and analyze the result that drone
#              collected
#
# ======================================================================


from time import gmtime, strftime, time
import Board
from Event import EventMove, EventFix


def board_stats(info, delimiter=","):
    """
    write a report about the original board
    :param info: the information returned by the board
    :param delimiter: the delimiter of the data. Comma by default
    """
    GLO = time()
    file_name = "Board_" + str(GLO) + ".csv"
    col = info[0]
    row = info[1]
    total_buf_avg = info[2]
    total_dur_avg_fix = info[3]
    total_dur_avg_move = info[4]

    report = open(file_name, "w")
    report.write("dim_column,dim_row,buffer_seconds,duration_fix_seconds,duration_move_seconds"
                 ",buffer_lambda,duration_fix_lambda,duration_move_lambda,"
                 "column,row,"
                 "total_board_avg_buf,total_board_avg_dur_fix,total_board_avg_dur_move\n")
    for r in range(row):
        for c in range(col):
            report.write(str(col) + delimiter +
                         str(row) + delimiter +
                         str(cal_second(float(Board.lambdas[0]))) + delimiter +
                         str(cal_second(float(Board.lambdas[1]))) + delimiter +
                         str(cal_second(float(Board.lambdas[2]))) + delimiter +
                         Board.lambdas[0] + delimiter +
                         Board.lambdas[1] + delimiter +
                         Board.lambdas[2] + delimiter +
                         str(c) + delimiter +
                         str(r) + delimiter +
                         str(total_buf_avg) + delimiter +
                         str(total_dur_avg_fix) + delimiter +
                         str(total_dur_avg_move) + "\n")

    report.close()


def drone_stats(info, delimiter=","):
    """
    write a report about the real time information that drone collects
    :param info: the information catched by drone
    :param delimiter: the delimiter of the data. Comma by default
    """

    GLO = time()
    file_name = "Drone_RealTime_" + str(GLO) + ".csv"
    total_events = info[0]
    total_fix_events = info[1]
    total_move_events = info[2]
    count_different = info[3]
    total_missed_events = info[4]
    total_missed_fix_events = info[5]
    total_missed_move_events = info[6]
    rowDim = info[7]
    colDim = info[8]
    times_hasEvent = info[9]
    total_visit = info[10]
    round = info[11]
    speed = info[12]
    random = 1 if info[-1] == "random" else 0
    lam_Buf = Board.lambdas[0]
    lam_fix_Dur = Board.lambdas[1]
    lam_move_Dur = Board.lambdas[2]
    report = open(file_name, "w+")
    report.write("dim_col,dim_row,round,drone_speed,sec_Buf,sec_fix_Dur,sec_move_Dur,lam_Buf,lam_fix_Dur,lam_move_Dur,"
                 "random,col,row,time,event_type,event_id\n")
    hyper_params_vals = (str(colDim) + delimiter + str(rowDim) + delimiter + str(round) + delimiter + str(speed)
                         + delimiter + str(cal_second(lam_Buf)) + delimiter + str(cal_second(lam_fix_Dur)) + delimiter
                         + str(cal_second(lam_move_Dur)) + delimiter + str(lam_Buf) + delimiter
                         + str(lam_fix_Dur) + delimiter + str(lam_move_Dur) + delimiter + str(random) + delimiter)
    # for row in range(rowDim):
    #     for col in range(colDim):
    #         msd = "0"
    #         if (col, row) in missed_events:
    #             msd = str(missed_events[(col, row)])
    #         if (col, row) in times_hasEvent.keys():
    #             for id in times_hasEvent[(col, row)].keys():
    #                 for t in times_hasEvent[(col, row)][id]:
    #                     line = (str(col) + delimiter + str(row) + delimiter + str(t) + delimiter + str(id) + delimiter
    #                             + msd + "\n")
    #                     report.write(hyper_params_vals)
    #                     report.write(line)
    #         else:
    #             coor = (str(col) + delimiter + str(row) + delimiter + "0" + delimiter + "0" + delimiter
    #                    + msd + delimiter + "\n")
    #             report.write(hyper_params_vals)
    #             report.write(coor)
    for row in range(rowDim):
        for col in range(colDim):
            events = times_hasEvent[(col, row)]
            for e, times in events.items():
                for t in times:
                    line = str(str(col) + delimiter + str(row) + delimiter + str(t) + delimiter + str(type(e))
                               + delimiter + str(e.id))
                    report.write(hyper_params_vals)
                    report.write(line)
    report.close()


def drone_total_stats(info, delimiter=","):
    """
    write a report about the real time information that drone collects
    :param info: the information catched by drone
    :param delimiter: the delimiter of the data. Comma by default
    """
    GLO = time()
    file_name = "Drone_Total_" + str(GLO) + ".csv"
    total_events = info[0]
    total_fix_events = info[1]
    total_move_events = info[2]
    count_different_fix = info[3]['EventFix']
    count_different_move = info[3]['EventMove']
    total_missed_events = info[4]
    total_missed_fix_events = info[5]
    total_missed_move_events = info[6]
    rowDim = info[7]
    colDim = info[8]
    times_hasEvent = info[9]
    total_visit = info[10]
    round = info[11]
    speed = info[12]
    count = info[13]
    random = 1 if info[-1] == "random" else 0
    lam_Buf = Board.lambdas[0]
    lam_fix_Dur = Board.lambdas[1]
    lam_move_Dur = Board.lambdas[2]
    report = open(file_name, "w+")
    report.write("dim_col,dim_row,round,drone_speed,sec_Buf,sec_fix_Dur,sec_move_Dur,lam_Buf,lam_fix_Dur,lam_move_Dur,"
                 "random,ttl_evnts,ttl_fix_evnts,ttl_move_evnts,ttl_diff_fix_evnts,ttl_diff_move_evnts,ttl_mssd_evnts,"
                 "ttl_mssd_fix_evnts,ttl_mssd_move_evnts,ttl_vistd_sctrs,ttl_evnt_generate\n")
    hyper_params_vals = (str(colDim) + delimiter + str(rowDim) + delimiter + str(round) + delimiter + str(speed)
                         + delimiter + str(cal_second(lam_Buf)) + delimiter + str(cal_second(lam_fix_Dur)) + delimiter
                         + str(cal_second(lam_move_Dur)) + delimiter + str(lam_Buf) + delimiter + str(lam_fix_Dur)
                         + delimiter + str(lam_move_Dur) + delimiter + str(random) + delimiter)
    line = (str(total_events) + delimiter + str(total_fix_events) + delimiter + str(total_move_events) + delimiter +
            str(count_different_fix) + delimiter + str(count_different_move) + delimiter
            + str(total_missed_events) + delimiter + str(total_missed_fix_events) + delimiter
            + str(total_missed_move_events) + delimiter + str(total_visit) + delimiter + str(count) + "\n")
    report.write(hyper_params_vals)
    report.write(line)
    report.close()


def time_info(t1, t2):
    """
    This function will write the time result for each experiment
    :param t1: the starting time
    :param t2: the finishing time
    """
    file_name = "time.txt"
    report = open(file_name, 'a')
    report.write("\n" + str(t2-t1) + "\n")
    report.close()


def cal_second(lam):
    """
    This function will transfer lambda into seconds
    :param lam: the lambda, type:float
    :return: the transferred seconds
    """
    return 1/float(lam)
