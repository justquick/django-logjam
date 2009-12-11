from operator import itemgetter
from client import Client
import settings


class MapReduce(object):
    def __init__(self, source=None):
        if source is None:
            source = Client().get_all()
        self.source = source
        
    def run(self):
        return self.reduce(self.map(self.source))
        
    def map(self, items):
        return items

    def reduce(self, items):
        return items


class Mailer(MapReduce):
    
    def map(self, requests):
        from django.core.mail import mail_admins
        for request in requests:
            mail_admins('LogJam Request Exception %s' % request['path'], settings.LOG_FORMAT % request)

    
class WordCounter(MapReduce):
    def map(self, requests):
        for request in requests:
            for word in request['exception'].split():
                yield word
    
    def reduce(self, words):
         
        word_count = {}
         
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
         
        sorted_word_count = sorted(word_count.items(), key=itemgetter(1))
         
        for word, count in sorted_word_count:
            yield word, count
        
        