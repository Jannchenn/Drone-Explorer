# ======================================================================
# FILE:        Stats.py
#
# DESCRIPTION: This file conmpute and analyze the result that drone
#              collected
#
# ======================================================================


from time import gmtime, strftime
import Board


def stats(info):
    """
    collects the data: total different events catched; event information;
    total time visit
    """
    date = strftime("%d_%b_%H_%M_%S", gmtime())
    file_name = "report_" + date + ".txt"
    total_events = info[0]
    count_different = info[1]
    missed_events = info[2]
    rowDim = info[3]
    colDim = info[4]
    times_hasEvent = info[5]
    total_visit = info[6]
    report = open(file_name,"w+")
    report.write("Lambda Buffer: ")
    report.write(Board.lambdas[0])  # str(lambda_buffer))
    report.write("\n")
    report.write("Lambda Duration: ")
    report.write(Board.lambdas[1])  # str(lambda_duration))
    report.write("\n")
    report.write("Total num event caught: ")
    report.write(str(total_events))
    report.write("\n")
    report.write("Total diff num event caught: ")
    report.write(str(count_different))
    report.write("\n")
    report.write("Total missed events: ")
    report.write(str(missed_events))
    report.write("\n")
    report.write("Event for each sector: \n")
    for row in range(rowDim):
        for col in range(colDim):
            if (col, row) in times_hasEvent.keys():
                for each in times_hasEvent[(col,row)].keys():
                    report.write(str(each))
                    report.write(",")
                    report.write(str(times_hasEvent[(col,row)][each]))
                    report.write(";")
                report.write("\t")
            else:
                report.write("0\t")
        report.write("\n")

    report.write("Total sectors visited: ")
    report.write(str(total_visit))
    report.write("\n")
    report.close()
