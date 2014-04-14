from __future__ import division
import os
import time
from sliverinfo.lxc.cgroup import cgroup
from sliverinfo import lxc
import sys

import urllib2
import json
import common

interval =1


def usage_percent(used, total, _round=None):
    """Calculate percentage usage of 'used' against 'total'."""

    try:
        ret = (used / total) * 100
    except ZeroDivisionError:
        ret = 0
    if _round is not None:
        return round(ret, _round)
    else:
        return ret



def getRunningContainers():
    containers, lxcdir = [], []

    if(os.path.exists(lxc.containerspath)):
        lxcdir=os.listdir(lxc.containerspath)

    else:
        return containers

    for entry in lxcdir:
        if os.path.isdir(os.path.join(lxc.containerspath, entry)):
            containers.append(entry)

    #ret = get_container_that_are_slivers(containers)

    return containers


def byte2MiByte(val):
    return val/1024/1024

def container_mem_usage(name):
    inst = cgroup('memory', name)

    memlimit = int(inst.getValue("memory.limit_in_bytes"))
    memswlimit = int(inst.getValue("memory.memsw.limit_in_bytes"))
    memused = int(inst.getValue("memory.usage_in_bytes"))
    memswused = int(inst.getValue("memory.memsw.usage_in_bytes"))

    mem_total = memlimit
    mem_used = memused
    mem_free = memlimit-memused
    mem_percent_used = usage_percent(mem_used, mem_total, _round=1)

    swap_total = memswlimit-memlimit
    swap_used = memswused-memused
    swap_free = swap_total -swap_used
    swap_percent_used = usage_percent(swap_used, swap_total, _round=1)

    total = memswlimit
    total_used = memswused
    total_free = memswlimit-memswused

    total_percent_used = usage_percent(total_used, total, _round=1)


    return {'memory':{'mem_total': mem_total, 'mem_used': mem_used, 'mem_free': mem_free, 'mem_percent_used': mem_percent_used,
                      'swap_total':swap_total, 'swap_used': swap_used, 'swap_free': swap_free, 'swap_percent_used': swap_percent_used,
                      'total': total, 'total_used': total_used, 'total_free': total_free, 'total_percent_used': total_percent_used}}


def container_cpu_usage( name):
    inst = cgroup('cpuacct', name)
    previous_cpu_usage = inst.getValue("cpuacct.usage")
    time.sleep(interval)
    current_cpu_usage = inst.getValue("cpuacct.usage")
    diff_cpu_usage = int(current_cpu_usage) - int(previous_cpu_usage)
    cpu_usage = float(diff_cpu_usage/(interval*1000000000))*100
    return {'cpu':{'cpu_usage': cpu_usage}}
