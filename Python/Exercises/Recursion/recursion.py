#!/usr/bin/env python3

"""
for each item:
    add to next "empty branch" in tree

def show_tree(tree):
    if tree.root:
        print(tree.root)
    if left:
        show_tree(left)
    if right:
        show_tree(right)
"""

import sys
import os

def main():
    values = sys.stdin.readline().split(",")
    create_and_show_tree(values)

def depth_test():
    assert(create_and_show_tree([1]) == 1)
    assert(create_and_show_tree([1, 2]) == 2)

def create_and_show_tree(values):
    t = Tree()
    for item in values:
        val = int(item)
        t.add_breadth_first(val)

    t.show_depth_first()


class Tree:
    def __init__(self, val=None):
        self.root = val
        self.left = None
        self.right = None

    def add_breadth_first(self, val):
        if self.root is None:
            self.root = val
            return
        elif self.left is None:
            self.left = Tree(val)
            return
        elif self.right is None:
            self.right = Tree(val)
            return

        if self.left.size() // 2 <= self.right.size() // 2:
            self.left.add_breadth_first(val)
        else:
            self.right.add_breadth_first(val)

    def depth(self):
        if self.root is None:
            return 0

        if self.left is None:
            left_depth = 0
        else:
            left_depth = self.left.depth()

        if self.right is None:
            right_depth = 0
        else:
            right_depth = self.right.depth()

        return 1 + max(left_depth, right_depth)

    def size(self):
        if self.root is None:
            return 0

        if self.left is None:
            left_depth = 0
        else:
            left_depth = self.left.depth()

        if self.right is None:
            right_depth = 0
        else:
            right_depth = self.right.depth()

        return 1 + left_depth + right_depth

    def show_depth_first(self):
        if self.root is None:
            return
        print(self.root)
        if self.left is not None:
            self.left.show_depth_first()
        if self.right is not None:
            self.right.show_depth_first()

if __name__ == "__main__":
    #depth_test()
    main()
