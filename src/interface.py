#!/usr/bin/env python3

"""interface.py: The file used to control and manage the interface."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"


import tkinter as tk
import logging
import re

from scan import ScanManager

IPV4_REGEX = re.compile('^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')


class Interface(object):
    def __init__(self):
        self.__root = tk.Tk()
        self.__make_gui()

    def __make_gui(self):
        self.__root.title('Rhys PortScanner V1')
        self.__root.geometry('500x400')

        self.__header0 = tk.Label(self.__root, text='IPv4 address to scan: ', font='Helvetica 18 bold')
        self.__header0.grid(row=0, column=0)

        self.__header1 = tk.Label(self.__root, text='Start port: ')
        self.__header1.grid(row=0, column=1)

        self.__header2 = tk.Label(self.__root, text='End port: ')
        self.__header2.grid(row=0, column=2)

        self.__header3 = tk.Label(self.__root, text='Open ports: ')
        self.__header3.grid(row=3, column=0)

        self.__header4 = tk.Label(self.__root, text='SCANNING', bg='red')

        self.__entry0 = tk.Entry()
        self.__entry0.delete(0, tk.END)
        self.__entry0.grid(row=1, column=0)

        self.__entry1 = tk.Entry()
        self.__entry1.delete(0, tk.END)
        self.__entry1.grid(row=1, column=1)

        self.__entry2 = tk.Entry()
        self.__entry2.delete(0, tk.END)
        self.__entry2.grid(row=1, column=2)

        self.__button = tk.Button(self.__root, text='SCAN', font='Helvetica 18 bold', command=self.__scan_button)
        self.__button.grid(row=2, column=0)

        self.__list = tk.Listbox(self.__root)
        self.__list.grid(row=3, column=1)

    def __scan_button(self):
        self.__list.delete(0, tk.END)

        if not self.__check_entries_valid():
            logging.info('Please enter valid data.')
            return

        self.__header4.grid(row=4, column=1)
        self.__root.update()

        address = self.__entry0.get()
        start_port = int(self.__entry1.get())
        end_port = int(self.__entry2.get()) + 1

        manager = ScanManager(5)
        ports = manager.scan_address(address, start_port, end_port)

        for port in ports:
            self.__list.insert(tk.END, port)

        self.__header4.grid_forget()
        self.__root.update()

        self.__list.insert(tk.END, 'END')

    def __check_entries_valid(self):
        if not re.match(IPV4_REGEX, self.__entry0.get()):
            logging.info('Invalid IPv4 address entered.')
            return False

        if not self.__entry1.get().isdigit() or not self.__entry1.get().isdigit():
            logging.info('Invalid port values entered.')
            return False

        return True

    def start(self):
        self.__root.mainloop()
