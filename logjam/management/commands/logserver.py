from SocketServer import BaseRequestHandler, ThreadingMixIn, TCPServer
from django.core.management.base import BaseCommand
from django.core.cache import get_cache
from logjam import settings
from logjam.util import *
from pprint import pprint
from atexit import register
import fcntl
import os
import sys


cache = get_cache(settings.CACHE)
ctrl = '%s%s' % (settings.PREFIX, 'ctrl')

class ExceptionHandler(BaseRequestHandler):
    def handle(self):
        sha = self.request.recv(40)
        if is_hex(sha):
            key = '%s%s' % (settings.PREFIX, sha)
            cached = cache.get(key)
            if cached:
                print 'Ignoring %s' % sha
                self.request.send('\x00')
            else:
                print 'Saving %s' % sha
                self.request.send('\x01')
                content = ''
                while 1:
                    bit = self.request.recv(1024)
                    if not bit: break
                    content += bit 
                cache.set(key, content)
                cache.set(ctrl, cache.get(ctrl, ()) + (sha,))
                log_report(deserialize(content))
        elif sha.startswith('LIST'):
            self.request.send('\n'.join(cache.get(ctrl, ())))
        elif sha.startswith('GET'):
            sha += self.request.recv(3)
            sha = sha[3:]
            print 'Getting %s' % sha
            self.request.send(cache.get('%s%s' % (settings.PREFIX, sha), '(dp0\n.'))

from OpenSSL import SSL
import socket
            
class LogJamServer(ThreadingMixIn, TCPServer):
    pass

    #def __init__(self, server_address, HandlerClass):
    #    TCPServer.__init__(self, server_address, HandlerClass)
    #    ctx = SSL.Context(SSL.SSLv23_METHOD)
    #    #server.pem's location (containing the server private key and
    #    #the server certificate).
    #    fpem = '/Users/jquick/Projects/SOAPpy/validate/server.pem'
    #    ctx.use_privatekey_file (fpem)
    #    ctx.use_certificate_file(fpem)
    #    self.socket = SSL.Connection(ctx, socket.socket(self.address_family,
    #                                                    self.socket_type))
    #    self.server_bind()
    #    self.server_activate()

class Command(BaseCommand):
    def handle(self, *args, **options):
        server = LogJamServer((settings.HOST, settings.PORT), ExceptionHandler)

        logger = None
        std_pipes_to_logger = True
        # Used docs by Levent Karakas 
        # http://www.enderunix.org/documents/eng/daemon.php
        # as a reference for this section.
    
        if settings.DAEMONIZE:
            # Fork, creating a new process for the child.
            process_id = os.fork()
            if process_id < 0:
                # Fork error.  Exit badly.
                sys.exit(1)
            elif process_id != 0:
                # This is the parent process.  Exit.
                sys.exit(0)
            # This is the child process.  Continue.
        
            # Stop listening for signals that the parent process receives.
            # This is done by getting a new process id.
            # setpgrp() is an alternative to setsid().
            # setsid puts the process in a new parent group and detaches its
            # controlling terminal.
            process_id = os.setsid()
            if process_id == -1:
                # Uh oh, there was a problem.
                sys.exit(1)
    
        null_descriptor = open(getattr(os, 'devnull', '/dev/null'), 'rw')
        if not settings.DEBUG:
            for descriptor in (sys.stdin, sys.stdout, sys.stderr):
                descriptor.close()
                descriptor = null_descriptor
    
        # Set umask to default to safe file permissions when running
        # as a root daemon. 027 is an octal number.
        os.umask(027)
    
        pidfile = open(settings.PIDFILE, 'w')
        # Try to get an exclusive lock on the file.  This will fail
        # if another process has the file locked.
        #fcntl.lockf(pidfile, fcntl.LOCK_EX|fcntl.LOCK_NB)
    
        # Record the process id to the pidfile.  This is standard
        # practice for daemons.
        pidfile.write('%s' %(os.getpid()))
        pidfile.flush()
    
        register(server.socket.close)
        server.serve_forever()
