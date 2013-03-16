
#import libvirt
import sys
from lxml import etree
import webapp2
import simplejson as json
import mimerender

mimerender = mimerender.Webapp2MimeRender()

render_xml = lambda message: '<message>%s</message>'%message

# Pack every arguments as dict then render it using dump.
render_json = lambda **args: json.dump(args) 
render_txt = lambda message: message
render_html = lambda message: '<html><body>%s</body></html>'%message

class Lxc(webapp2.RequestHandler):

    # Need to add decoration upon every method.
    
    @mimerender(
        default = 'html'
    ,   html = render_html
    ,   json = render_json
    ,   xml = render_xml
    ,   txt = render_txt
    )
    def get(self, _id ):
        if not _id:
            return {'message': 'GET /lxc/'}
        else:
            return {'message': 'GET /lxc/%s/'%_id}

    @mimerender(
        default = 'html'
    ,   html = render_html
    ,   json = render_json
    ,   xml = render_xml
    ,   txt = render_txt
    )
    def put(self, _id):
        if not _id:
            return {'message': 'PUT /lxc/'}
        else:
            return {'message': 'PUT /lxc/%s/'%_id}

    @mimerender(
        default = 'html'
    ,   html = render_html
    ,   json = render_json
    ,   xml = render_xml
    ,   txt = render_txt
    )
    def post(self, _id):
        if not _id:
            return {'message': 'POST/lxc/'}
        else:
            return {'message': 'POST /lxc/%s/'%_id}

    @mimerender(
        default = 'html'
    ,   html = render_html
    ,   json = render_json
    ,   xml = render_xml
    ,   txt = render_txt
    )
    def delete(self, _id):
        if not _id:
            return {'message': 'DELETE /lxc/'}
        else:
            return {'message': 'DELETE /lxc/%s/'%_id}

app = webapp2.WSGIApplication([
    ('/lxc/(.*)', Lxc)
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
