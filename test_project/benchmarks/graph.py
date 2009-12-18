from glob import glob

data = {}

lookup = {
    'email':'Email notification',
    'log-worst': 'LogJam: Worst case',
    'log-best': 'LogJam: Best case',
    'none': 'No notification'
}

"""
email - Uses django's mail_admins feature
    requires functional email settings and
    some admins to mail.
    
log-worst - Worst case cenario. Every error reported
    is unique. This is done by setting UNIQUE to False, and
    sending a lot of random data down the drain.
    
log-best - Best case cenario. Every error reported
    is a duplicate. Set UNIQUE to True.
    
none - No notifications at all. Comment out the
    logjam middleware and any email settings.

"""

for bench in glob('*.txt'):
    d = data[lookup[bench[:-4]]] = {}
    f = open(bench)
    a = f.readline().split()
    d['fetches'] = a[0]
    d['max_parallel'] = a[2]
    d['bytes'] = a[5]
    d['seconds'] = a[8]

    a = f.readline().split()
    d['mean_bytes_per_conn'] = a[0]

    a = f.readline().split()
    d['fetches_per_sec'] = a[0]        
    d['bytes_per_sec'] = a[2]
    
    a = f.readline().split()
    d['mean_per_conn'] = a[1]
    d['max_per_conn'] = a[3]
    d['min_per_conn'] = a[5]
    
    a = f.readline().split()
    d['mean_first_response'] = a[1]
    d['max_first_response'] = a[3]
    d['min_first_response'] = a[5]
    
    rest = f.readlines()
    d['responses'] = int(rest[-1].strip().split()[-1])
    f.close()

from pprint import pprint

from GChartWrapper import *

def graph_factory(name, scale=(0,11000), symbol='f'):
    values = [(k, x[name]) for k,x in data.items()]
    values.sort(lambda x,y: cmp(x[0],y[0]))
    G = VerticalBarGroup([[x[1]] for x in values],encoding='text')
    G.title(lookup2[name],'black',20)
    G.scale(*scale)
    G.size(600,500)
    G.bar(50,10)
    G.legend(*[x[0] for x in values])
    G.color('red','224499','76A4FB','80C65A')
    G.legend_pos('l')
    
    for i in range(4):
        G.marker('N*%s*'%symbol,'black',i,1,11)
    G.save('graphs/%s'%name)
    print G
    
lookup2 = {
    'responses':'Total Responses Returned',
    'bytes':'Total Bytes Returned',
    'fetches_per_sec': 'Page Fetches per Second',
    'bad_byte_counts': 'Number of Pages with Bad Byte Counts',
    'mean_first_response': 'Average Time Until Frist Response',
    'mean_per_conn': 'Average Time Until First Connection'
}
graph_factory('responses', (0,60000))
#graph_factory('bytes', (10**6, 10**7.2), 'e')
graph_factory('fetches_per_sec', (0,900))
#graph_factory('bad_byte_counts')
graph_factory('mean_first_response',(0,120))
#graph_factory('mean_per_conn', (0.5, .1))

"""
10224 fetches, 20 max parallel, 1.37046e+07 bytes, in 60 seconds
1340.43 mean bytes/connection
170.4 fetches/sec, 228409 bytes/sec
msecs/connect: 74.7478 mean, 7007.02 max, 0.05 min
msecs/first-response: 30.9129 mean, 18919 max, 0.036 min
9810 bad byte counts
HTTP response codes:
  code 500 -- 9810

9193 fetches, 20 max parallel, 1.22573e+07 bytes, in 60 seconds
1333.33 mean bytes/connection
153.217 fetches/sec, 204288 bytes/sec
msecs/connect: 83.7515 mean, 7007.3 max, 0.041 min
msecs/first-response: 36.2251 mean, 18918.6 max, 0.035 min
419 bad byte counts
HTTP response codes:
  code 500 -- 8774

"""