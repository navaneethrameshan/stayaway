from sliverinfo import sliverinfo
from analyse import mds
import util
import config
import os


def monitorStore(processing_time):
    """
    Get monitored information
    find timestamp
    read violation-file
    if violation happened in the last period, attach violation label
    send to mds
    """
   # commented to use psutil system info system_info = systeminfo.get_all_info()

    system_info = {}
    violation_label = False
    monitored_timestamp = util.get_current_system_timestamp()
    info_dict, current_info_list = sliverinfo.collectAllData()
    system_info.update(info_dict)
    violation_timestamp = read_violation_file()

    print "Monitored Timestamp: ", monitored_timestamp
    print "Violation Timestamp: ", violation_timestamp

    if violation_timestamp and abs(violation_timestamp - monitored_timestamp) < config.TIMEPERIOD + processing_time:
        violation_label = True
        print "HIT!!! Label as Violation"

    mds.iso_map_dynamic(current_info_list, violation_label)
    end_timestamp = util.get_current_system_timestamp()
    processing_time = end_timestamp - monitored_timestamp
    print "Processing Time: ", processing_time

    return processing_time

def read_violation_file():
    if os.path.exists(config.application_file_path):
        f_handle = open(config.application_file_path, 'r')
        violation_timestamp = float(f_handle.readline())
        f_handle.close()
        return violation_timestamp