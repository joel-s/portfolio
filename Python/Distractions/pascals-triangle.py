#! /usr/bin/env python3

"""
Print patterns based on Pascal's Triangle.
"""

class Triangle:
    """Represents a Pascal's Triangle which can be rendered as text.

    """
    def __init__(self, num_rows):
        self.num_rows = num_rows
        self.rows = [[1]]
        prev_row = [1]
        for row_num in range(1, num_rows):
            this_row = [1]
            for col_num in range(1, row_num):
                this_row.append(prev_row[col_num-1] + prev_row[col_num])
            this_row.append(1)
            self.rows.append(this_row)
            prev_row = this_row

    def printAsChars(self, modulus, chars=None):
        assert modulus > 1, "modulus too small"
        if chars is None:
            chars = "*" + " "*(modulus-1)
        if len(chars) < modulus:
            chars += " "*(modulus - len(chars))

        for row in self.rows:
            print(" " * (self.num_rows - len(row)), end=" ")
            for i in row:
                print(chars[i % modulus], end=" ")
            print()

def main():
    tri = Triangle(16)
    print(tri.rows)
    tri.printAsChars(2)
    tri.printAsChars(4)
    tri.printAsChars(4, " +X+")
    tri.printAsChars(4, " .oO")


main()
