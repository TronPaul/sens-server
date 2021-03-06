import time
from werkzeug.serving import BaseRequestHandler

class TimedRequestHandler(BaseRequestHandler):
    """Extend werkzeug request handler to suit our needs."""
    def handle(self):
        self.fancyStarted = time.time()
        rv = super(TimedRequestHandler, self).handle()
        return rv

    def send_response(self, *args, **kw):
        self.fancyProcessed = time.time()
        super(TimedRequestHandler, self).send_response(*args, **kw)

    def log_request(self, code='-', size='-'):
        duration = int((self.fancyProcessed - self.fancyStarted) * 1000)
        self.log('info', '"{0}" {1} {2} [{3}ms]'.format(self.requestline, code,
size, duration))
