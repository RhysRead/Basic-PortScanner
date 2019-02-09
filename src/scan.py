#!/usr/bin/env python3

"""scan.py: The file used to execute scans of remote hosts."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import socket
import logging
import threading
import queue
import time

TIMEOUT = 2


class Task(object):
    def __init__(self, address, port):
        self._address = address
        self._port = port

    def get_address(self):
        return self._address

    def get_port(self):
        return self._port


class ScanManager(object):
    def __init__(self, thread_count):
        self.__thread_count = thread_count

        self.__threads = []
        self.__results = []

        self.__tasks = queue.Queue()

        self.__create_threads()

    def __add_tasks(self, address, start_port, end_port):
        added = []

        for port in range(start_port, end_port):
            task = Task(address, port)

            self.__tasks.put(task)
            added.append(task)

        return added

    def __thread(self):
        while True:
            if self.__tasks.empty():
                continue

            task = self.__tasks.get()

            if check_port_open(task.get_address(), task.get_port()):
                self.__results.append(task.get_port())

    def __create_threads(self):
        for i in range(0, self.__thread_count):
            thread = threading.Thread(target=self.__thread, daemon=True)
            thread.start()

            self.__threads.append(thread)

    def scan_address(self, address, start_port, end_port):
        self.__add_tasks(address, start_port, end_port)
        while not self.__tasks.empty():
            continue

        # Todo: Find better way of finding when all threads are complete as sleeping is hacky
        # Sleeping for timeout duration to avoid missing slow threads
        time.sleep(TIMEOUT)

        logging.info('Scan complete on host {}'.format(address))
        return self.__results


def check_port_open(address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)

    logging.info('Scanning port {} on host {}'.format(str(port), address))

    result = sock.connect_ex((address, port)) == 0
    sock.close()

    return result
