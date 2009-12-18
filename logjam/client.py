import sys
import socket
from django.core.handlers.wsgi import WSGIHandler
from django.utils.hashcompat import sha_constructor
import settings
from util import serialize, deserialize, format_exception, request2dict


class Client(object):
        
    def connect(self, host=settings.HOST, port=settings.PORT, timeout=settings.TIMEOUT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(timeout)
        try:
            self.socket.connect((host,  port))
        except Exception, e:
            if e.errno == 61:
                print >>sys.stderr, 'Failed to connect'
            raise
        
    def close(self):
        return self.socket.close()
    
    def all(self):
        for sha in self.run('LIST').splitlines():
            yield sha.rstrip()
            
    def get_first(self):
        for sha in self.all():
            return self.get(sha)
            
    def get_all(self):
        for sha in self.all():
            yield self.get(sha)
            
    def get(self, sha):
        return deserialize(self.run('GET%s' % sha))
        
    def dump(self):
        self.run('DUMP')
    
    def run(self, command):
        self.connect()
        self.socket.send(command)
        content = ''
        while 1:
            bit = self.socket.recv(1024)
            if not bit: break
            content += bit
        self.close()
        return content
        
    def send_exception(self, request, exc_info=None):
        sha, exception = format_exception(exc_info)
        
        self.connect()
        self.socket.send(sha)
        
        if self.socket.recv(1) == '\x00':
            print >>sys.stderr, 'Ignoring %s' % sha
            self.close()
            return
    
        print >>sys.stderr, 'Sending %s' % sha
        try:
            d = request2dict(request, exception, sha)
        except Exception, e:
            print >>sys.stderr, 'Conversion error: %s'%e

        try:
            self.socket.send(serialize(d))
        except Exception, e:
            print >>sys.stderr, 'Client error %s' % e
        self.close()