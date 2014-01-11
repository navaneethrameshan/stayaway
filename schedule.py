import time

class Schedule:

    def __init__(self, time_period):
            self.time_period = time_period


    def schedule (self, function):
        previous_processing_time = 0
        while(1):
            previous_processing_time = function( previous_processing_time )
            print "Last processing took %d secs" %previous_processing_time
            time.sleep(self.time_period)
            print "scheduling next run"
