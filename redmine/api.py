import urllib2
import json
import core.consts as consts

class Api():
    def __init__(self):
        self.url = consts.redmineUrl + "/%(method)s/%(value)s.%(format)s"
        self.apikey = consts.redmineApiKey

        self.format = 'json'

    def _call(self, method, value):
        request = urllib2.Request(self.url % {'method': method, 'value': value, 'format': self.format})
        request.add_header('X-Redmine-API-Key ', self.apikey)
        return request

    def issue(self, issue):
        try:
            response = urllib2.urlopen(self._call('issues', issue))
        except urllib2.HTTPError, e:
            if e.code == 404:
                # XXX raise exception
                return dict()
            else:
                raise e
        except urllib2.URLError:
            # XXX raise exception
            return dict()
        return json.loads(response.read())
