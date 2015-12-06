'''
iTunes Feed Grabber: transforms iTunes podcasts to RSS XML feeds.

Copyright (C) 2015  Yan Foto, Nima Fotouhi Tehrani

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import webapp2
from StringIO import StringIO
from grabber import Grabber

# This is required so that fetch requests doesn't time out!
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(60)


class Archiver(webapp2.RequestHandler):

    def get(self, api):
        memory_file = StringIO()
        g = Grabber(api)
        g.grab(memory_file)
        self.response.headers['Content-Type'] = 'application/zip'
        self.response.headers[
            'Content-Disposition'] = ('attachment;filename={}.zip'.format(api))
        self.response.write(memory_file.getvalue())
        memory_file.close()


app = webapp2.WSGIApplication([
    webapp2.Route('/archive/<api>', Archiver, name='api-archive'),
], debug=True)
