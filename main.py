
from schedule import Schedule
import coordinator
import config
import argparse
import os
import ast
from analyse import mds



def start_monitoring():
    sched = Schedule(config.TIMEPERIOD)
    sched.schedule(coordinator.monitorStore)

def main():
    start_monitoring()

def load_template(template_file):
    if os.path.isfile(template_file):
        f_handle = open(template_file, 'r')
        mds.dynamic_all_values = ast.literal_eval(f_handle.readline())
        mds.violation_position = ast.literal_eval(f_handle.readline())
        f_handle.close()
    else:
        print "No such file"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--template', dest= 'template',
        help = "Use this argument to load a template file for repeatable experiments" )

    args = vars(parser.parse_args())

    if args['template']:
        print "Loading template from "+ args['template']
        load_template(args['template'])

    main()