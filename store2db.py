#!/usr/bin/env python

import sqlite3
from sysinfo import *

def store_it(datetime, memorydata, processdata):
    database = sqlite3.connect('data.db')
    database_cursor = database.cursor()
    database_cursor.execute(
            """
               CREATE TABLE IF NOT EXISTS system_info
               (
               date BLOB NOT NULL,
               time BLOB NOT NULL,
               uptime BLOB NOT NULL,
               loadavg1m REAL NOT NULL,
               loadavg5m REAL NOT NULL,
               loadavg15m REAL NOT NULL,
               totalvirtmem REAL NOT NULL,
               usedvirtmem REAL NOT NULL,
               freevirtmem REAL NOT NULL,
               buffersvirtmem REAL NOT NULL,
               totalswpmem REAL NOT NULL,
               usedswpmem REAL NOT NULL,
               freeswpmem REAL NOT NULL
               )
            """
                           )
    database_cursor.execute(
            """
               CREATE TABLE IF NOT EXISTS process_info
               (
               PID, USER, NI, VIRT, RES, STATE, TIME, NAME, MEM
               )
            """
)
    database_cursor.execute(
            """
               INSERT INTO system_info (
               date, time, uptime, loadavg1m, loadavg5m, loadavg15m, totalvirtmem, usedvirtmem,
               freevirtmem, buffersvirtmem, totalswpmem, usedswpmem, freeswpmem
               )
               values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);

            """, (
      datetime["Date"],
      datetime["Current time"],
      datetime["Uptime"],
      datetime["min1avg"],
      datetime["min5avg"],
      datetime["min15avg"],
      memorydata["Virtual memory"]["Total"],
      memorydata["Virtual memory"]["Used"],
      memorydata["Virtual memory"]["Free"],
      memorydata["Virtual memory"]["Buffers"],
      memorydata["Swap memory"]["Total"],
      memorydata["Swap memory"]["Used"],
      memorydata["Swap memory"]["Free"]
      )
      )
    for process in processdata:
        database_cursor.execute(
           """
              INSERT INTO process_info (
              PID, USER, NI, VIRT, RES, STATE, TIME, NAME, MEM
               )
               values (?, ?, ?, ?, ?, ?, ?, ?, ?);
           """, (
      process["PID"],
      process["USER"],
      process["NI"],
      process["VIRT"],
      process["RES"],
      process["STATE"],
      process["TIME"],
      process["NAME"],
      process["MEMPERCENT"]
      )
      )

if __name__ == '__main__':
    ut = uptime()
    md = mem_data()
    pd = process_data()
    store_it(ut, md, pd)
