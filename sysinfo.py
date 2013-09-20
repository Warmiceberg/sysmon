#!/usr/bin/env python

# Initial script that will work like top execution
# use dictioanry or json/sqlite3 database to store all values
# use python-daemon
# see zeroMQ

import os
import time
import psutil

def uptime():
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    date = date_time.split()[0]
    ptime = date_time.split()[1]
    with open('/proc/uptime', 'r') as f:
        data = float(f.read().split()[0])
        hour, minute = int(data/3600), int(data%3600/60)
    min1, min5, min15 = os.getloadavg()
    print "date: %s" %date, "current time: %s" %ptime, "uptime: %s:%s" %(hour, minute), "load average: %s, %s, %s" %(min1, min5, min15)

def mem_data():
    kb = 1024
    vert_mem = psutil.virtual_memory()
    print "Mem: " + str(vert_mem.total/kb) + "k total, " + str(vert_mem.used/kb) + "k used, " + str(vert_mem.free/kb) + "k free, " + str(vert_mem.buffers/kb) + "k buffers"
    swap_mem = psutil.swap_memory()
    print "Swap: " + str(swap_mem.total/kb) + "k total, " + str(swap_mem.used/kb) + "k used, " + str(swap_mem.free/kb) + "k free, "

def process_data():
    print "  PID         OWNER    NI        VIRT          RES      STATUS  %MEM       TIME+                  NAME"
    for process in psutil.process_iter():
        process_pid = process.pid
        process_owner = process.username
        process_virt = int(process.get_memory_info().vms)/1024
        process_res = int(process.get_memory_info().rss)/1024
        process_mempercent = process.get_memory_percent()
        process_cputime = process.get_cpu_times().user + process.get_cpu_times().system
        process_name = process.name
        process_status = process.status
        process_nice_value = process.get_nice()
        print "%5s %12s %5s %12s %12s %12s %5.2f %10s %25s" %(process_pid, process_owner, process_nice_value, process_virt, process_res, process_status, process_mempercent, process_cputime, process_name) 

if __name__ == '__main__':
#     while 1:
         uptime()
         mem_data()
         process_data()
         time.sleep(1)
