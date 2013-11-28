
from schedule import Schedule
import coordinator
import config


def start_monitoring():
    sched = Schedule(config.TIMEPERIOD)
    sched.schedule(coordinator.monitorStore)

def main():
    start_monitoring()

if __name__ == '__main__':
    main()