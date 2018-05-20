#! /usr/bin/env python
# coding=utf-8

def reverse_list(l):
    n = len(l) / 2
    i = 0
    while n > 0:
        t = l[i]
        l[i] = l[len(l) - 2 * i - 1]
        l[len(l) - 2 * i - 1] = t
        n -= 1
    return l


count = 1
number = {}


class node:
    def __init__(self, left, right, val):
        self.left = left
        self.right = right
        self.val = val


def inorder(node):
    if node.left != 0:
        inorder(node.left)
    global number
    global count
    number[node.val] = count
    count += 1
    if node.right != 0:
        inorder(node.right)


if __name__ == "__main__":
    # init all the nodes
    n8 = node(0, 0, 8)
    n7 = node(0, 0, 7)
    n6 = node(0, n8, 6)
    n5 = node(0, 0, 5)
    n4 = node(0, n7, 4)
    n3 = node(n6, 0, 3)
    n2 = node(n4, n5, 2)
    n1 = node(n2, n3, 1)
    inorder(n1)
    print number