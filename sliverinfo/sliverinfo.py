from subprocess import check_output
import lxc
from lxc import utils
import csv

all_values_list= []  # contains corresponding values from each metric. Ex: [at Time1[VM1-cpu, VM1-memory, VM2-cpu, VM2-memory,..],at Time2[],[],..]

def collectData(container):
    container_info = {}
    all_info = {}

    container_info['container'] = container
    container_info.update(utils.container_mem_usage(container))
    container_info.update(utils.container_cpu_usage(container))

    all_info[container] = container_info
    #    print all_info.items()
    return all_info


def collectAllData():
    container_info = {}
    all_info_dict = {}

    container_list = lxc.utils.getRunningContainers()
    print 'Monitoring all started containers: ', container_list
    for container in container_list:
            container_info.update(collectData(container))

    all_info_dict['slivers'] = container_info

    #store the info locally in a ordered fashion and write to a file
    ordered_info = get_store_ordered_list (container_info)
    append_to_file(ordered_info)

    return (all_info_dict, ordered_info)


def get_store_ordered_list (container_info):
    ordered_info = [] # contains corresponding values from each metric. Ex: [VM1-cpu, VM1-memory, VM2-cpu, VM2-memory]

    for  key,value in container_info.items():
       # temp_value_list.append(key)
        ordered_info.append(value['cpu']['cpu_usage'])
        ordered_info.append(value['memory'] ['mem_used'])

    print ordered_info
    # write to all value list!
    all_values_list.append(ordered_info)
    return ordered_info

def append_to_file(ordered_list):
    file = open('vm_values.data', 'a')
    writer = csv.writer(file)

    writer.writerow([value for value in ordered_list])
    file.close()

def get_all_values_list():
    return all_values_list