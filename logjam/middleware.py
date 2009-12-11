from client import send_exception
from util import format_exception


class LogJamMiddleware(object):
    def process_exception(self, request, exception):
        send_exception(request)

"""
http_load -parallel 20 -seconds 30 urls

http://localhost:8000/fail/

from random import random
def fail(request):
    random()/0
    
(had to take unique constraints off for rest of test)
    
-- jam best
3680 fetches, 20 max parallel, 4.49705e+06 bytes, in 30 seconds
1222.03 mean bytes/connection
122.667 fetches/sec, 149902 bytes/sec
msecs/connect: 92.3258 mean, 7010.8 max, 0.063 min
msecs/first-response: 43.4816 mean, 4515.77 max, 0.059 min
3478 bad byte counts
HTTP response codes:
  code 500 -- 3478
  
from random import random
def fail(request):
    __import__(str(random()))
    
-- jam worst
2976 fetches, 20 max parallel, 3.86270e+06 bytes, in 30 seconds
1297.95 mean bytes/connection
99.2 fetches/sec, 128757 bytes/sec
msecs/connect: 125.45 mean, 7006.4 max, 0.056 min
msecs/first-response: 56.9908 mean, 4506.49 max, 0.033 min
2765 bad byte counts
HTTP response codes:
  code 500 -- 2765
  
took out jam middleware
  
-- no pro
5365 fetches, 20 max parallel, 6.71455e+06 bytes, in 30.0005 seconds
1251.55 mean bytes/connection
178.83 fetches/sec, 223814 bytes/sec
msecs/connect: 68.8936 mean, 11010 max, 0.049 min
msecs/first-response: 28.9071 mean, 4505.87 max, 0.041 min
172 bad byte counts
HTTP response codes:
  code 500 -- 5193

added one ADMIN email to local postfix

-- email
1689 fetches, 20 max parallel, 2.06896e+06 bytes, in 30 seconds
1224.96 mean bytes/connection
56.3 fetches/sec, 68965.2 bytes/sec
msecs/connect: 207.113 mean, 6975.96 max, 0.063 min
msecs/first-response: 112.159 mean, 12412.5 max, 0.031 min
208 bad byte counts
HTTP response codes:
  code 500 -- 1481
  
2,500 more requests per minute on a bad day
4,000 most of the time
"""