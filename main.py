
from schedule import Schedule
import store

TIMEPERIOD = 5

def start_monitoring():
    sched = Schedule(TIMEPERIOD)
    sched.schedule(store.monitorStore)

def main():
    start_monitoring()

if __name__ == '__main__':
    main()