from random import random

def fail(request):
    random()/0
    
def fail2(request):
    __import__(str(random()))