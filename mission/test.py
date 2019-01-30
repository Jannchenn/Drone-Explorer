class __Tile:
    start_time = 0
    finish_time = 0
    # buf = 0
    # dur = 0
    lat = 0
    long = 0
    id = 0
    event_list = list()
    num_of_events = 0
    time_with_events = 0


board = [[__Tile() for j in range(10)] for i in range(10)]
copy = list(board[0][0].event_list)
copy.append(1)
copy.append(2)
copy.append(3)
board[0][0].event_list = copy
board[0][0].event_list.remove(1)
print(board[0][0].event_list)
print(board[0][1].event_list)
