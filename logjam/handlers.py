from django.core.handlers import modpython, wsgi, base

class LogJamHandler(base.BaseHandler):
    def handle_uncaught_exception(self, request, resolver, exc_info):
        """
        Sends request to logjam server for recording instead of mailing admins
        
        Be *very* careful when overriding this because the error could be
        caused by anything, so assuming something like the database is always
        available would be an error.
        """
        from django.conf import settings

        if settings.DEBUG_PROPAGATE_EXCEPTIONS:
            raise

        if settings.DEBUG:
            from django.views import debug
            return debug.technical_500_response(request, *exc_info)

        # Send exception to logjam server
        from logjam.client import send_exception
        send_exception(request, exc_info)
       
        # Return an HttpResponse that displays a friendly error message.
        callback, param_dict = resolver.resolve500()
        return callback(request, **param_dict)


class WSGIHandler(LogJamHandler, wsgi.WSGIHandler): pass
class ModPythonHandler(LogJamHandler, modpython.ModPythonHandler): pass
        

