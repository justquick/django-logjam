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
                print 'Failed to connect'
            self.socket = None
    
    def close(self):
        return self.socket.close()
    
    def all(self):
        for sha in self.run('LIST').splitlines():
            yield sha
            
    def get_first(self):
        for sha in self.all():
            return self.get(sha)
            
    def get_all(self):
        for sha in self.all():
            yield self.get(sha.strip())
            
    def get(self, sha):
        return deserialize(self.run('GET%s' % sha))
    
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
            print 'Ignoring %s' % sha
            self.close()
            return
    
        print 'Sending %s' % sha
        self.socket.send(serialize(request2dict(request, exception, sha)))
        self.close()