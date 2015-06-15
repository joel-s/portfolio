#! /usr/bin/env python

"""
Solve the 'eight queens' problem for a variable size chessboard.

Print out all solutions and the total number of solutions.
"""

import sys

def main():
    if len(sys.argv) == 2:
        qb = QueenBoard(int(sys.argv[1]))
    else:
        qb = QueenBoard(8)
    qb.solve()
    print("Total solutions: %d" % qb.get_sol_count())

class QueenBoard:

    def __init__(self, size):
        self.size = size
        self.queens = size * [0]
        self.sol_count = 0

    def solve(self, column=0):
        """Recursively solve the 'eight queens' problem.

        For each row in this column, check if we can place a queen there
        without it being under attack. If so, call solve() on the next column.
        """
        if column == self.size:
            self.sol_count += 1
            self.print_solution()

        for row in range(self.size):
            if self.check_solution(column, row):
                self.queens[column] = row
                self.solve(column + 1)

    def check_solution(self, column, row):
        """Check whether a solution is valid.

        Arguments:
        column -- the column we are currently looking at
        row -- the proposed position of the queen in that column

        This method checks all the columns above the current column and returns
        False if a queen is under attack, and True otherwise.
        """
        for c in reversed(range(column)):
            c_diff = column - c
            if self.queens[c] in (row - c_diff, row, row + c_diff):
                return False

        return True

    def print_solution(self):
        for q in self.queens:
            # Print a line with "##" representing the queen and "[]"
            # representing every other square
            print(q*"[]" + "##" + (self.size-q-1)*"[]")
        print("\n" + 16*"-" + "\n")

    def get_sol_count(self):
        return self.sol_count

if __name__ == "__main__":
    main()
