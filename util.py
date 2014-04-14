import config
import time
from subprocess import Popen, PIPE

total_utilization = []

# scale numpy array
def scale(X):
    for i in xrange(0,len(X[0])):
        max_value = config.dimensions_range[i%config.number_vms]
        new_list = abs(X[:,i])/max_value
        #print "new list: ", new_list
        X[:,i] = ['%.2f' % elem for elem in new_list ]
    #print "Scaled values: ", X
    return X

def get_current_system_timestamp():
    timestamp = time.time()
    return timestamp

def pause_process(process):
    pid = get_pid(process)
    if pid:
        p1 = Popen(['kill', '-STOP', pid], stdout= PIPE)

def continue_process(process):
    pid= get_pid(process)
    if pid:
        p1 = Popen(['kill', '-CONT', pid], stdout= PIPE)

def get_pid(process):
    fd = Popen(['ps', '-ef'], stdout = PIPE)
    p1 = Popen(['grep', process ], stdin= fd.stdout, stdout = PIPE)
    p2 = Popen(['grep', '-v', 'grep'], stdin= p1.stdout, stdout = PIPE)
    s = p2.stdout.readline().split()
    if s:
        return s[1]

def scale_list(list1):
    list2= []
    for i in xrange(0,len(list1)):
        max_value = config.dimensions_range[i%config.number_vms]
        list2.append( "{0:.2f}".format(abs(list1[i])/max_value))
    return list2

def compute_utilization(value):
    current_utilization = sum(float(i) for i in value)
    total_utilization.append(current_utilization)
    print " Total Utilization is: ", total_utilization

if __name__ == '__main__' :
    pid= get_pid('tunkrank')
    print pid
    pause_process('tunkrank')
    continue_process('tunkrank')