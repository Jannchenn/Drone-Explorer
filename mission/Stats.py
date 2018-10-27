# ======================================================================
# FILE:        Stats.py
#
# DESCRIPTION: This file compute and analyze the result that drone
#              collected
#
# ======================================================================


from time import gmtime, strftime, time
import Board


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
    board = info[2]
    total_dur_avg = info[3]

    report = open(file_name, "w")
    report.write("dim_column,dim_row,duration_seconds,duration_lambda,probability,"
                 "eventlife_seconds,eventlife_lambda,arrival_num,arrival_seconds,arrival_lambda,"
                 "column,row,average_duration_time,total_board_avg_dur\n")
    for r in range(row):
        for c in range(col):
            report.write(str(col) + delimiter +
                         str(row) + delimiter +
                         str(cal_second(float(Board.indep_var[1]))) + delimiter +
                         Board.indep_var[1] + delimiter +
                         Board.prob + delimiter +
                         str(cal_second(float(Board.event_attr[0]))) + delimiter +
                         Board.event_attr[0] + delimiter +
                         Board.event_attr[1] + delimiter +
                         str(cal_second(float(Board.event_attr[2]))) + delimiter +
                         Board.event_attr[2] + delimiter +
                         str(c) + delimiter +
                         str(r) + delimiter +
                         str(board[c][r].time_with_events/board[c][r].num_of_events) + delimiter +
                         str(total_dur_avg) + "\n")

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
    count_different = info[1]
    rowDim = info[2]
    colDim = info[3]
    times_hasEvent = info[4]
    total_visit = info[5]
    round = info[6]
    speed = info[7]
    random = 1 if info[8] == "random" else 0
    board_stats = Board.board_info
    arrival_rate = Board.event_attr[0]
    arrival_num =Board.event_attr[1]
    die_rate = Board.event_attr[2]
    probability = Board.indep_var[0]
    lam_Dur = Board.indep_var[1]
    report = open(file_name, "w+")
    report.write("col,row,time,event_id,dim_col,dim_row,round,drone_speed,probability,arrival_rate,arrival_num,die_rate,sec_Dur,lam_Dur,random\n")
    hyper_params_vals = (str(colDim) + delimiter + str(rowDim) + delimiter + str(round) + delimiter + str(speed)
                         + delimiter + str(probability) + delimiter + str(arrival_rate) + delimiter + str(arrival_num)
                         + delimiter + str(die_rate) + delimiter + str(cal_second(lam_Dur)) + delimiter
                         + str(lam_Dur) + delimiter + str(random) + "\n")
    for event in times_hasEvent:
        for sector in times_hasEvent[event]:
            for time in times_hasEvent[event][sector]:
                line = (str(event.get_id()) + delimiter + str(sector[0]) + delimiter + str(sector[1]) + delimiter + str(time) + hyper_params_vals)
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
    count_different = info[1]
    total_missed_events = info[3]
    rowDim = info[4]
    colDim = info[5]
    total_visit = info[7]
    round = info[8]
    speed = info[9]
    count = info[10]
    random = 1 if info[10] == "random" else 0
    lam_Buf = Board.lambdas[0]
    lam_Dur = Board.lambdas[1]
    report = open(file_name, "w+")
    report.write("dim_col,dim_row,round,drone_speed,sec_Buf,sec_Dur,lam_Buf,lam_Dur,random,"
                 "ttl_evnts,ttl_diff_evnts,ttl_mssd_evnts,ttl_vistd_sctrs,ttl_evnt_generate\n")
    hyper_params_vals = (str(colDim) + delimiter + str(rowDim) + delimiter + str(round) + delimiter + str(speed)
                         + delimiter + str(cal_second(lam_Buf)) + delimiter + str(cal_second(lam_Dur)) + delimiter
                         + str(lam_Buf) + delimiter + str(lam_Dur) + delimiter + str(random) + delimiter)
    line = (str(total_events) + delimiter + str(count_different) + delimiter
            + str(total_missed_events) + delimiter + str(total_visit) + delimiter + str(count) + "\n")
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
