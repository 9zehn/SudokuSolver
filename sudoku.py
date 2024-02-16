import sys

"""
# A sudoku solver, uses forward checking and simple heuristics.
# @Author: Leon Gruber
# @Date: October 2023
"""

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def isSolved(board):
    for item in board:
        if board[item] == 0:
            return False
    return True


def check_all(board):
    queue = []

    for tile in board:
        if board[tile] == 0:
            legal_values = set()
            rows = tile[0]
            columns = tile[1]

            for i in range(9):
                if board[rows+str(i+1)] != 0:
                    legal_values.add(board[rows+str(i+1)])

            for i in range(9):
                if board[ROW[i]+columns] != 0:
                    legal_values.add(board[ROW[i]+columns])

            for i in range(3):
                index_y = int(ROW.index(rows)) // 3
                index_x = (int(columns) - 1) // 3
                for x in range(3):
                    if board[ROW[index_y*3+i]+str(index_x*3+x+1)] != 0:
                        legal_values.add(board[ROW[index_y*3+i]+str(index_x*3+x+1)])

            strong = ''.join(num for num in COL if int(num) not in legal_values)
            queue.append([tile,strong])
    return queue


# Implement maybe: forward checking relation between unassigned variables
def forward_checking(queue,tile,updated_value):
    rows = tile[0]
    columns = tile[1]
    index_rm = 0

    for item in queue:
        if item[0] == tile:
            index_rm = queue.index(item)
        elif item[0][0] == rows or item[0][1] == columns:
            item[1] = item[1].replace(updated_value,'')
        elif int(ROW.index(rows)) // 3 == int(ROW.index(item[0][0])) // 3 and \
                (int(columns)-1) // 3 == (int(item[0][1])-1) // 3:
            item[1] = item[1].replace(updated_value,'')

        if len(item[1]) == 0:
            return False
    queue.pop(index_rm)
    return True


def mrv(queue):
    min_item = queue[0]
    for item in queue:
        if len(item[1]) < len(min_item[1]):
            min_item = item
    return min_item


def backtracking(board):
    queue = check_all(board)

    solved_board = backtrack_help(board,queue)
    return solved_board


def backtrack_help(board,queue):
    if len(queue) == 0 and isSolved(board):
        return board

    var = mrv(queue)

    for value in var[1]:
        new_queue =[inner[:] for inner in queue]
        if forward_checking(new_queue,var[0],value):
            new_board = board.copy()
            new_board[var[0]] = value

            result = backtrack_help(new_board,new_queue)
            if result:
                return result
    return False


if __name__ == '__main__':
    if len(sys.argv) > 1:

        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}

        solved_board = backtracking(board)

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        times = []

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            #print_board(board)
            start_time = time.time()
            # Solve with backtracking
            solved_board = backtracking(board)

            end_time = time.time()
            times.append(end_time-start_time)

            #print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        # Print Statistics

        min_time = 1000
        max_time = 0
        count = 0
        for t in times:
            count += t
            if t < min_time:
                min_time = t
            elif t > max_time:
                max_time = t
        mean = count / len(times)
        sd = 0
        for t in times:
            sd += (t-mean)**2

        sd = sd / len(times)

        print("Total: ",count)
        print("Puzzles: ",len(times))
        print("Min: ",min_time)
        print("Max: ",max_time)
        print("Mean: ",mean)
        print("SD: ",sd)


        print("Finishing all boards in file.")
