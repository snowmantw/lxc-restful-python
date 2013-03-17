
# Find the XML in database and allow user use RESTful way to manipulate it,
# then commit and to let libvirt run it.

import libvirt
import sys
from lxml import etree
import webapp2
import simplejson as json
import mimerender
import cStringIO

mimerender = mimerender.Webapp2MimeRender()

render_xml = lambda message, resource="": '<message>%s<resource>%s</resource></message>'% (message, resource)

# Pack every arguments as dict then render it using dump.
render_json = lambda **args: json.dump(args) 
render_txt = lambda message, resource="": '%s %s'% (message, resource)
render_html = lambda message, resource="": '<html><body>%s<p>%s</p></body></html>'% (message, resource)

# Test retrieve one XML, then binding URL to XPath for traversing it.

conn = libvirt.openReadOnly('lxc:///')
vdomain = conn.lookupByName('vanilla')
vxml = vdomain.XMLDesc(libvirt.VIR_DOMAIN_XML_INACTIVE)

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
            tree = etree.parse(cStringIO.StringIO(vxml))
            resource = tree.xpath('/'+_id)
            return {'message': 'GET XPath /lxc/%s/'%_id, 'resource': resource[0].tag}

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
