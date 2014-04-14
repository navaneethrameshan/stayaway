from sliverinfo import sliverinfo
from analyse import mds
from analyse import distance
import util
import config
import os
import vlc.qos

learn_distance = 0.1
previous_violation_label = False
action_status = False
previous_scaled_monitored_list = None

def monitorStore(processing_time):
    """
    Get monitored information
    find timestamp
    read violation-file
    if violation happened in the last period, attach violation label
    send to mds
    """
   # commented to use psutil system info system_info = systeminfo.get_all_info()
    global previous_scaled_monitored_list
    global previous_violation_label
    global learn_distance

    system_info = {}

    violation_label = False
    transition = False
    closest_monitor_range = False
    application_timestamp = None
    qos_metric = None

    monitored_timestamp = util.get_current_system_timestamp()
    info_dict, current_monitored_list = sliverinfo.collectAllData()
    system_info.update(info_dict)
    file_values = read_violation_file()

    if file_values and len(file_values) ==2 :
        application_timestamp, qos_metric = file_values
        print "Total no. of Frames Encoded: ", qos_metric

   # print "Monitored Timestamp: ", monitored_timestamp
   # print "QoS Metric Timestamp: ", application_timestamp

    #Check if the current value falls within the range of monitor. The closest_monitor_range is the first
    # monitored value closest to the application timestamp
    if application_timestamp and abs(application_timestamp - monitored_timestamp) < config.TIMEPERIOD + processing_time :
        closest_monitor_range = True

    if qos_metric:
        if config.latency_app is not 'vlc':
            violation_label = check_violation(qos_metric)
        else:
            violation_label = vlc.qos.check_violation(qos_metric, application_timestamp)


    transition = check_transition(violation_label)

    # If an action has been taken, compare the measurement vectors to decide when to revoke the action
    if action_status:
        scaled_monitored_list = util.scale_list(current_monitored_list)
        if previous_scaled_monitored_list:
            dist = distance.calculate_distance_list(scaled_monitored_list, previous_scaled_monitored_list)
            print "Distance: ", dist
            if dist and dist > learn_distance:
                #revoke action and reset previous_monitored_list to None to start afresh
                revoke_action()
                previous_scaled_monitored_list = None
        else:
            previous_scaled_monitored_list = scaled_monitored_list


    #Transition check over. Safe to update previous violation label.
    if violation_label:
        previous_violation_label= True
        print "HIT!!! Label as Violation"

        # Pause the batch application.
        take_action()

    else:
        previous_violation_label = False

    mds.iso_map_dynamic(current_monitored_list, violation_label, transition, closest_monitor_range, action_status)
    end_timestamp = util.get_current_system_timestamp()
    processing_time = end_timestamp - monitored_timestamp
    #print "Processing Time: ", processing_time

    return processing_time

def revoke_action():
    util.continue_process(config.batch_app)
    global action_status
    action_status= False

def take_action():
    util.pause_process(config.batch_app)
    global action_status
    action_status= True

def check_transition(current_violation_label):
    if previous_violation_label is not current_violation_label:
        return True
    else:
        return False

def read_violation_file():
    if os.path.exists(config.application_file_path):
        f_handle = open(config.application_file_path, 'r')
        value = f_handle.readline().split(',')
        try:
            application_timestamp, qos_metric = float(value[0]), float(value[1])
        except:
            print "Exception caught in reading file!!"
            f_handle.close()
            return None

        f_handle.close()
        return (application_timestamp, qos_metric)
    else:
        return None

def check_violation(qos_metric):
    if float(qos_metric) < config.qos_metric:
        return True
    else:
        return False