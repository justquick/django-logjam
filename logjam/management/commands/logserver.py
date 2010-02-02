from SocketServer import BaseRequestHandler, ThreadingMixIn, TCPServer
from django.core.management.base import BaseCommand, CommandError
from logjam import settings
from logjam.util import *
from pprint import pprint
from atexit import register
from datetime import datetime
from optparse import make_option
import fcntl
import os
import sys


class ExceptionHandler(BaseRequestHandler):
    def all(self):
        return cache.get(ctrl, ())
    
    def dump(self, file=settings.DUMP_FILE):
        pickle.dump(map(self.get, self.all()), open(datetime.now().strftime(file), 'w'), -1)
            
    def get(self, sha):
        return cache.get('%s%s' % (settings.PREFIX, sha), '(dp0\n.')
        
    def handle(self):
        try:
            data = self.request.recv(40)
            if sha_re.match(data):
                key = prefix(data)
                cached = cache.get(key)
                if cached is None:
                    print >>settings.LOG_FILE, 'Saving %s' % data
                    self.request.send('\x01')
                    content = ''
                    while 1:
                        bit = self.request.recv(1024)
                        if not bit: break
                        content += bit
                    if not content:
                        print >>settings.ERROR_FILE, 'No content to save'
                        return
                    cache.set(key, content, 36000)
                    cache.set(ctrl, cache.get(ctrl, ()) + (data,), 36000)
                    #log_report(deserialize(content))
                else:
                    print >>settings.LOG_FILE, 'Ignoring %s' % data
                    self.request.send('\x00')
            elif data.startswith('DUMP'):
                self.dump()
            elif data.startswith('LIST'):
                self.request.send('\n'.join(self.all()))
            elif data.startswith('GET'):
                data += self.request.recv(3)
                data = data[3:]
                self.request.send(self.get(data))
            elif data.startswith('DEL'):
                data += self.request.recv(3)
                data = data[3:]
                cache.delete(data)
        except Exception, e:
            import traceback
            print >>settings.ERROR_FILE, 'Server Error: %s' % traceback.format_exc()

class LogJamServer(ThreadingMixIn, TCPServer):
    pass
    #from OpenSSL import SSL
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
    option_list = BaseCommand.option_list + (
        make_option('-p', '--pidfile', dest='pidfile',default=settings.PIDFILE,
            help='File to write daemon\'s process id'),
        make_option('-d', '--daemonize', action='store_true', dest='daemonize', default=settings.DAEMONIZE,
            help='Forks a unix daemon, writing pid file'),
        make_option('-k', '--kill', action='store_true', dest='kill', default=False,
            help='Kills an already running daemon using pidfile'),
    )
    help = 'Runs the logjam TCP service.'
    args = '[optional port number, or ipaddr:port]'
    
    def handle(self, addrport='', *args, **options):
        pidfile = options.get('pidfile',settings.PIDFILE)
        
        if options.get('kill',False):
            os.system('kill -9 `cat %r`' % str(pidfile))
            os.system('rm -f %r' % str(pidfile))
            return
            
        if not addrport:
            addr = settings.HOST
            port = settings.PORT
        else:
            try:
                addr, port = addrport.split(':')
            except ValueError:
                addr, port = settings.HOST, addrport
        
        try:
            port = int(port)
        except TypeError:
            raise CommandError("%r is not a valid port number." % port)        
        
        server = LogJamServer((addr, port), ExceptionHandler)

        logger = None
        std_pipes_to_logger = True
        # Used docs by Levent Karakas 
        # http://www.enderunix.org/documents/eng/daemon.php
        # as a reference for this section.
    
        if options.get('daemonize', settings.DAEMONIZE):
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
                for descriptor in (sys.stdin, sys.stdout, settings.LOG_FILE):
                    descriptor.close()
                    descriptor = null_descriptor
        
            # Set umask to default to safe file permissions when running
            # as a root daemon. 027 is an octal number.
            os.umask(027)
        
            pidfile = open(options.get('pidfile', settings.PIDFILE), 'w')
            # Try to get an exclusive lock on the file.  This will fail
            # if another process has the file locked.
            #fcntl.lockf(pidfile, fcntl.LOCK_EX|fcntl.LOCK_NB)
        
            # Record the process id to the pidfile.  This is standard
            # practice for daemons.
            pidfile.write('%s' %(os.getpid()))
            pidfile.flush()
    
        print >>settings.LOG_FILE, 'Development server is running at %s:%s' % (addr, port) 
        
        #register(server.socket.close)
        try:
            server.serve_forever()
        except:
            #server.shutdown()
            sys.exit(0)
