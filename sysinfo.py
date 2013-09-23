#!/usr/bin/env python

# Initial script that will work like top execution
# use dictioanry or json/sqlite3 database to store all values
# use python-daemon
# see zeroMQ

import os
import time
import psutil

def uptime():
    date_time = time.strftime("%Y%m%d %H%M%S", time.localtime())
    date = date_time.split()[0]
    ptime = date_time.split()[1]
    with open('/proc/uptime', 'r') as f:
        uptime_data = float(f.read().split()[0])
    min1, min5, min15 = os.getloadavg()
    up_time = {
               "Date" : date,
               "Current time" : ptime,
               "Uptime" : uptime_data,
               "min1avg" : min1,
               "min5avg" : min5,
               "min15avg" : min15
              }
    return up_time

def mem_data():
    vert_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()
    memory_data = {
                   "Virtual memory" : {
                                "Total" : vert_mem.total,
                                "Used" : vert_mem.used,
                                "Free" : vert_mem.free,
                                "Buffers" : vert_mem.buffers
                               },
                   "Swap memory" : {
                                "Total" : swap_mem.total,
                                "Used" : swap_mem.used,
                                "Free" : swap_mem.free
                              }
                  }
    return memory_data

def process_data():
    p_data = []
    for process in psutil.process_iter():
        p_data.append({
                            "PID" : process.pid,
                            "USER": process.username,
                            "NI" : process.get_nice(),
                            "VIRT" : int(process.get_memory_info().vms)/1024,
                            "RES" : int(process.get_memory_info().rss)/1024,
                            "STATE" : process.status,
                            "TIME" : process.get_cpu_times().user + process.get_cpu_times().system,
                            "NAME" : process.name,
                            "MEMPERCENT" : process.get_memory_percent(),
                           })  
    return p_data

if __name__ == '__main__':
    ut = uptime()
    md = mem_data()
    pd = process_data()
