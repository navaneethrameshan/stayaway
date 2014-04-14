import os
import config

previous_frame_count = None
previous_timestamp = None

def check_violation(current_frame_count, current_timestamp):
    global  previous_frame_count
    global  previous_timestamp

    if previous_frame_count and current_timestamp-previous_timestamp > 0:
        frames_encoded_sec = (current_frame_count - previous_frame_count)/(current_timestamp-previous_timestamp)
        print "No. of Frames encoded in the one sec: %d"  %(frames_encoded_sec)

        write_to_file(frames_encoded_sec)

        if float(frames_encoded_sec) < config.qos_metric:
            previous_frame_count = current_frame_count
            previous_timestamp = current_timestamp
            return True
        else:
            previous_frame_count = current_frame_count
            previous_timestamp = current_timestamp
            return False
    else:
        previous_frame_count = current_frame_count
        previous_timestamp = current_timestamp
        return False


def write_to_file(qos_metric):
    f_handle = open("qos.data", 'a')
    f_handle.write(str(qos_metric)+',')
    f_handle.close()
