dimensions_range = [100.00, 1073741824.00] #cpu max, memory max is 1GB in bytes
number_vms = 2
TIMEPERIOD = 3

application_file_path = '/var/lib/lxc/vm2/rootfs/home/ubuntu/vlc-installed-2.0.5/bin/count'
batch_app = 'lol'
latency_app = 'vlc'
results= 'results/vlc-phase/'

most_recent_count = 0

#a,b,c values for Gaussian function
a = 0.8
b = 0
c = 4


# Application QoS Metric Threshold
qos_metric = 15 #Min no of frames for vlc
