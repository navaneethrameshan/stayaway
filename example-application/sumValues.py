import random
import time
import sys
import signal

random.seed()

throughput_threshold = 0.05
time_period = 15

throughput = []
timestamp = []

def genList (size):
    randomList = []

    flag = True
    count = 0

    sleep_flag = False
    start_time = time.time()

    #initialize random list with values between 0 and 100
    for i in range(size):
        randomList.append(random.randint(0,10000))


    for i in range(size):
        if flag:
            count = 0
            start_time = time.time()
            flag= False

        #randomList.append(random.randint(0,100000))
        sumList(randomList)
        count += 1

#        prob = random.randint(0,5)
#        if prob < 1 :
#            time.sleep(1)

#        if i > 10000 and i < 10010:
#            time.sleep(2)

        end_time = time.time()
        if (end_time-start_time) > time_period:
            tput = float(count/(time_period * 1000.0))
            throughput.append(tput)
            print tput
            write_to_file(str(end_time)+ ','+str(tput))

            timestamp.append(end_time)
            flag= True

    print throughput
    print timestamp
    return throughput, timestamp

def write_to_file(value):
    f_handle = open("violation", 'w+')
    f_handle.write(str(value))
    f_handle.close()

def sumList(inList):
    finalSum = 0

    #iterate over all values in the list, and calculate the cummulative sum
    for value in inList:
        finalSum = finalSum + value
    return finalSum


def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    print throughput

   # plot.plot(timestamp,throughput, 'throughput-sum')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    N = 500000
    #mark the start time
    startTime = time.time()
    #create a random list of N integers
    throughput, timestamp = genList (N)

    #mark the end time
    endTime = time.time()
    #calculate the total time it took to complete the work
    workTime =  endTime - startTime

    #print results
    print "The job took " + str(workTime) + " seconds to complete"
   # print "The final sum was: " + str(finalSum)

    #plot.plot(timestamp,throughput, 'throughput-SUM')
