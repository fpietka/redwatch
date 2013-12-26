import urllib2
import json
from core.settings import SystemSettings


class Api():
    def __init__(self):
        settings = SystemSettings()
        self.url = settings.value('redmineUrl')
        self.callurl = self.url + "/%(method)s/%(value)s.%(format)s"
        self.apikey = settings.value('redmineApiKey')
        self.format = 'json'

    def _call(self, method, value):
        request = urllib2.Request(self.callurl % {'method': method, 'value': value, 'format': self.format})
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

    def statuses(self):
        try:
            url = '/'.join((self.url, 'issue_statuses.json'))
            request = urllib2.Request(url)
            request.add_header('X-Redmine-API-Key ', self.apikey)
            response = urllib2.urlopen(request)
        except ValueError:
            raise ApiException("Not an URL")
        except urllib2.HTTPError, e:
            if e.code == 404:
                raise ApiException("No service found on that URL")
            if e.code == 401:
                raise ApiException("Bad API key")
            if e.code == 400:
                raise ApiException("Bad request")
            else:
                raise e
        except urllib2.URLError:
            raise ApiException("An error occurred when fetching url")

        return json.loads(response.read())


class ApiException(Exception):
    pass
