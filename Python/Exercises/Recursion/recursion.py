#!/usr/bin/env python3

"""
Solves the problem described in the README, recursively.

Usage:
    python3 recursion.py <input.txt >actual.txt
    diff -c output.txt actual.txt    # compare expected output to actual 

"""

import sys
import os

def main():
    values = sys.stdin.readline().split(",")
    values = map(int, values)
    create_and_show_tree(values)


def create_and_show_tree(values):
    t = Tree()
    for val in values:
        t.add_breadth_first(val)
    t.show_depth_first()


class Tree:
    """
    A binary tree containing 0 or more nodes
    """

    def __init__(self):
        self.root = None

    def add_breadth_first(self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            self.root.add_breadth_first(val)

    def show_depth_first(self):
        if self.root is None:
            return
        self.root.show_depth_first()


class Node:
    """
    A node in a binary tree with a value and possibly left and right nodes.
    """

    def __init__(self, val):
        self.value = val
        self.left = None
        self.right = None

    def add_breadth_first(self, val):
        if self.left is None:
            self.left = Node(val)
            return
        elif self.right is None:
            self.right = Node(val)
            return

        if self.left.min_depth() <= self.right.min_depth():
            self.left.add_breadth_first(val)
        else:
            self.right.add_breadth_first(val)

    def min_depth(self):
        if self.left is None:
            return 0
        else:
            left_depth = self.left.min_depth()

        if self.right is None:
            return 0
        else:
            right_depth = self.right.min_depth()

        return 1 + min(left_depth, right_depth)

    def show_depth_first(self):
        print(self.value)
        if self.left is not None:
            self.left.show_depth_first()
        if self.right is not None:
            self.right.show_depth_first()


if __name__ == "__main__":
    main()
