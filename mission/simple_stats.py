from time import gmtime, strftime, time
import Board
from Event import EventMove, EventFix

def stats(total_events, total_caught_events):
    file_name = "catch_rate.txt"
    report = open(file_name, "a")
    report.write(str(total_events/total_caught_events) + '\n')
