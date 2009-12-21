import sys,os
from datetime import datetime
from django.test import TestCase
from django.http import HttpRequest
from client import Client
from mapreduce import WordCounter, Mailer
import settings
import pickle
from util import *


class MyReq(HttpRequest):
    def __init__(self):
        self.method = 'GET'
        #self.timestamp =    datetime(2009, 12, 11, 14, 4, 59, 257218)
        self.path = '/'
        self.GET = {}
        self.POST = {}
        self.COOKIES = {}
        self.FILES = {}
        self.META = {'DOCUMENT_ROOT': '/var/www/',
'GATEWAY_INTERFACE': 'CGI/1.1',
'HTTP_ACCEPT': '*/*',
'HTTP_ACCEPT_ENCODING': 'gzip, deflate',
'HTTP_ACCEPT_LANGUAGE': 'en-us',
'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; en-us) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9',
'QUERY_STRING': '',
'REMOTE_ADDR': '666.666.666.666',
'REMOTE_PORT': '40474',
'REQUEST_METHOD': 'GET',
'SCRIPT_NAME': u'',
'SERVER_ADDR': '127.0.0.1',
'SERVER_ADMIN': 'webmaster@.com',
'SERVER_NAME': 'www.com',
'SERVER_PORT': '80',
'SERVER_PROTOCOL': 'HTTP/1.1',
'SERVER_SOFTWARE': 'Apache/2',
'mod_wsgi.listener_host': '',
'mod_wsgi.listener_port': '80',
'mod_wsgi.process_group': '',
'mod_wsgi.reload_mechanism': '0',
'mod_wsgi.script_reloading': '1',
'wsgi.multiprocess': True,
'wsgi.multithread': True,
'wsgi.run_once': False,
'wsgi.url_scheme': 'http',
'wsgi.version': (1, 0)
}


class LogTest(TestCase):
    def setUp(self):
        self.client = Client()
    
        
    def send_exception(self, exc_func):
        try:
            exc_func()
        except:
            self.client.send_exception(MyReq())

    def test_zz(self):
        self.assertEqual(len(list(self.client.all())), 32)

    def test_words(self):
        l = list(WordCounter().run())
        from operator import itemgetter
        self.assertEqual(l, sorted(l, key=itemgetter(1)))

    def test_zdump(self):
        self.client.dump()
        self.assertEqual(len(pickle.load(open(datetime.now().strftime(settings.DUMP_FILE)))), 32)

    def test_za(self):
        self.assert_('is_ajax' in self.client.get_first())
        
    def test_mail(self):
        Mailer().run()

    # When in doubt, make unittests that just FAIL

    def test_name(self):
        self.send_exception(lambda: wtf)
    
    def test_zero(self):
        self.send_exception(lambda: 1/0)
        
    def test_typecast(self):
        self.send_exception(lambda: int(''))
        
    def test_raises(self):
        for attr in dir(self):
            if attr.startswith('raise_'):
                self.send_exception(getattr(self, attr))
                
    def raise_baseexception(self):
        raise BaseException

    def raise_exception(self):
        raise Exception

    def raise_standarderror(self):
        raise StandardError

    def raise_arithmeticerror(self):
        raise ArithmeticError

    def raise_lookuperror(self):
        raise LookupError

    def raise_assertionerror(self):
        raise AssertionError

    def raise_attributeerror(self):
        raise AttributeError

    def raise_eoferror(self):
        raise EOFError

    def raise_environmenterror(self):
        raise EnvironmentError

    def raise_floatingpointerror(self):
        raise FloatingPointError

    def raise_ioerror(self):
        raise IOError

    def raise_importerror(self):
        raise ImportError

    def raise_indexerror(self):
        raise IndexError

    def raise_keyerror(self):
        raise KeyError

    def raise_keyboardinterrupt(self):
        raise KeyboardInterrupt

    def raise_memoryerror(self):
        raise MemoryError

    def raise_nameerror(self):
        raise NameError

    def raise_notimplementederror(self):
        raise NotImplementedError

    def raise_oserror(self):
        raise OSError

    def raise_overflowerror(self):
        raise OverflowError

    def raise_referenceerror(self):
        raise ReferenceError

    def raise_runtimeerror(self):
        raise RuntimeError

    def raise_syntaxerror(self):
        raise SyntaxError

    def raise_systemerror(self):
        raise SystemError

    def raise_systemexit(self):
        raise SystemExit

    def raise_typeerror(self):
        raise TypeError

    def raise_valueerror(self):
        raise ValueError

    def raise_windowserror(self):
        raise WindowsError

    def raise_zerodivisionerror(self):
        raise ZeroDivisionError
