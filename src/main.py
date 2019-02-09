#!/usr/bin/env python3

"""mmain.py: The main file used to execute PortScanner."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"


import logging

from interface import Interface

logging.basicConfig(level=logging.DEBUG)


class Main(object):
    def __init__(self):
        self.__interface = Interface()

    def start(self):
        self.__interface.start()


if __name__ == '__main__':
    main = Main()
    main.start()
