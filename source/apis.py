
# 1. Low level: Find the XML in database and allow user use RESTful way to manipulate it,
# then commit and to let libvirt run it.
#
# 2. High level: Provide some basic APIs to manipulate containers, not directly expose XMLs.

import pdb

import libvirt
import yaml
import sys
import shutil
from os import path
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

class LXC():

    class BuildDomain:

        """start build a domain.
        
        :param path: dict contain paths to put all container related things like rootfs, and where the OS template is.
                containers: where to put containers 
                ostemplate: where the OS template is
                xmltemplate: where to load a vanilla XML
        :return: BuildDomain 
        """
        def __init__(self, path):
            self.pathcontainers = path['containers']
            self.pathostemplate = path['ostemplate']
            self.pathxmltemplate = path['xmltemplate']

            self.xmlref = etree.parse(self.pathxmltemplate) 

        """update or create a new one in the tree; find it according to the tag name.

        :param tree: ElementTree from etree; will be modified directly.
        :param tag: String
        :param text: String
        :param attrs: dict with all attributes
        :returns: ElementTree 
        """
        @staticmethod
        def __setelement(tree, tag, text="", attrs={}):
            e = tree.find(tag)
            if e is None:
                e = etree.Element(tag)
                tree.append(e)
            e.text = text
            
            for k, v in attrs.items():
                e.set(k, v)                        

            return tree

        """static method to start building.

        :param env, dict own such properties:
            path:
                containers: where to put containers 
                ostemplate: where the OS template is
                xmltemplate: where to load a vanilla XML

        :return: BuildDomain 
        """
        @staticmethod
        def init(env):
            return LXC.BuildDomain(**env)

        def vcpu(self, num):
            '''set the domain's one attribute. '''
            self.__setelement(self.xmlref, 'vcpu', str(num))
            return self

        def memory(self, num):
            '''set the domain's one attribute. '''
            self.__setelement(self.xmlref, 'memory', str(num))
            return self

        def rootfs(self, name):
            '''set the source to one named rootfs, under the path previously setted . '''
            self.rootfs = path.join(self.pathcontainers, name)
            e_rootmount = self.xmlref.xpath('/domain/devices/filesystem[target[@dir="/"]]')[0]
            self.__setelement(e_rootmount, 'source', '', {'dir': self.rootfs})
            return self

        def commit(self):
            '''do whatever the system need to do.'''

            # 1. Copy the OS template to the container path.
            shutil.copytree(self.pathostemplate, self.rootfs)
            return self

        def str(self):
            '''return the stringified result.'''
            return etree.tostring(self.xmlref)
        

class APIs(webapp2.RequestHandler):

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
            # Testing the builder.
            # The later `vcpu` should only replace the former, not append a new one into the XML.
            resource = LXC.BuildDomain.init(self.app.config['build-domain']).vcpu(3).vcpu(5).rootfs('test-lxc').str()
            return {'message': 'GET XPath /lxc/%s/'%_id, 'resource': resource}

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


def readconfig(path):
    '''read configs from the YAML file'''
    with open(path) as f:
        datamap = yaml.load(f)
    return datamap

def main():
    pathconfig = sys.argv[1]

    app = webapp2.WSGIApplication([
        ('/lxc/(.*)', APIs)
    ], debug=True, config=readconfig(pathconfig))

    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
