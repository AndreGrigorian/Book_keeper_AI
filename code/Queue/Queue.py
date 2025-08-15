from ctypes import sizeof
from distutils.command.build_scripts import first_line_re


import Node


class Queue:
    size = 0
    first = None
    last = None

    def add(self, item):
        prevLast = self.last
        self.last = Node()
        self.last.item = item
        if(self.size == 0):
            self.first = self.last
        else:
            prevLast.next = self.last
        size+=1

    def poll(self):
        prevFirst = self.first
        self.first = self.first.next
        size -= 1
        return prevFirst

    def peek(self):
        return self.first.item

    def isEmpty(self):
        return self.size == 0

    def size(self):
        return self.size

    def contains(self, item):
        current = self.first
        while(current != None):
            if(current.item == item):
                return True
            current = current.next

        return False



