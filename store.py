from sliverinfo import sliverinfo
from analyse import mds

def monitorStore():
    """
    Get monitored information
    Attach the sequence number
    Attach timestamp
    Store in the log file
    delete seen entries
    """
   # commented to use psutil system info system_info = systeminfo.get_all_info()

    system_info = {}
    info_dict, current_info_list = sliverinfo.collectAllData()
    system_info.update(info_dict)

    mds.iso_map_dynamic(current_info_list)
