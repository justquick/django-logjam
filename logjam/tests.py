import sys
import datetime
from django.test import TestCase
from django.http import HttpRequest
from client import Client
from mapreduce import WordCounter, Mailer

class MyReq(HttpRequest):
    def __init__(self):
        self.method = 'GET'
        self.timestamp = datetime.datetime(2009, 12, 11, 14, 4, 59, 257218)
        self.path = '/'
        self.GET = {}
        self.POST = {}
        self.COOKIES = {}
        self.META = {'DOCUMENT_ROOT': '/var/www/',
'GATEWAY_INTERFACE': 'CGI/1.1',
'HTTP_ACCEPT': '*/*',
'HTTP_ACCEPT_ENCODING': 'gzip, deflate',
'HTTP_ACCEPT_LANGUAGE': 'en-us',
'HTTP_COOKIE': '__qca=1170638018-7141480-61440722; __utma=119759246.1800635973.1174575396.1253731181.1254105505.86; __utmb=119759246.195.7.1254153099013; __utmc=119759246; __utmz=119759246.1254105506.86.70.utmcsr=drudgereport.com|utmccn=(referral)|utmcmd=referral|utmcct=/; AxData=; Axxd=1; s_sess=%20s_cc%3Dtrue%3B%20s_sq%3D%3B; s_vi=[CS]v1|485132E3000029AF-A000B4500001DC6[CE]; _csuid=4601392b11053074; SVWCUK200=130970_33/130968_25/130974_67; TheWashingtonTimes=71.112.92.213.273561158677753748; VWCUK200=L092809/Q32531_6359_5_092809_37_093009_130970x128779x092809x24x37/Q32532_6359_5_092709_80_093009_130974x128785x092809x52x80/Q32533_6359_5_092709_30_093009_130968x128786x092809x20x30',
'HTTP_HOST': 'www.washingtontimes.com',
'HTTP_REFERER': 'http://www.washingtontimes.com/news/2009/sep/28/liberals-seek-health-care-access-for-illegals/',
'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; en-us) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9',
'HTTP_X_FORWARDED_FOR': '173.64.164.220, 172.16.12.4',
'HTTP_X_VARNISH': '30673177',
'PATH': '/usr/local/bin:/usr/bin:/bin',
'PATH_INFO': u'/news/2009/sep/28/liberals-seek-health-care-access-for-illegals/\x7f/',
'PATH_TRANSLATED': '/var/code/washingtontimes/django.wsgi/news/2009/sep/28/liberals-seek-health-care-access-for-illegals/\x7f/',
'QUERY_STRING': '',
'REMOTE_ADDR': '173.64.164.220',
'REMOTE_PORT': '40474',
'REQUEST_METHOD': 'GET',
'REQUEST_URI': '/news/2009/sep/28/liberals-seek-health-care-access-for-illegals/%7F/',
'SCRIPT_FILENAME': '/var/code/washingtontimes/django.wsgi',
'SCRIPT_NAME': u'',
'SCRIPT_URI': 'http://www.washingtontimes.com/news/2009/sep/28/liberals-seek-health-care-access-for-illegals/\x7f/',
'SCRIPT_URL': '/news/2009/sep/28/liberals-seek-health-care-access-for-illegals/\x7f/',
'SERVER_ADDR': '172.16.12.48',
'SERVER_ADMIN': 'webmaster@washingtontimes.com',
'SERVER_NAME': 'www.washingtontimes.com',
'SERVER_PORT': '80',
'SERVER_PROTOCOL': 'HTTP/1.1',
'SERVER_SIGNATURE': '<address>Apache/2 Server at www.washingtontimes.com Port 80</address>\n',
'SERVER_SOFTWARE': 'Apache/2',
'mod_wsgi.application_group': 'margaret9.washingtontimes.com|',
'mod_wsgi.callable_object': 'application',
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
