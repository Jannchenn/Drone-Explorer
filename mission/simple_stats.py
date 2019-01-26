from time import gmtime, strftime, time
import Board
from Event import EventMove, EventFix

def stats(info, delimiter=","):
    file_name = "catch_rate.txt"
    report = open(file_name, "a")
    total_event = info[-3]
    caught_event = info[-2]
    report.write(str(caught_event / total_event) + '\n')