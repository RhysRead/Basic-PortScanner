#!/usr/bin/env python3

"""scan.py: The file used to execute scans of remote hosts."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import socket
import logging


def get_open_ports(address, start_port, end_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    results = {}
    for port in range(start_port, end_port):
        logging.info('Scanning port {} on host {}'.format(str(port), address))
        results[port] = sock.connect_ex((address, port))

    return [i for i in results.keys() if results[i] == 0]
