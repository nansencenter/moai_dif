from lxml import etree
import os
import datetime

from moai.utils import XPath

class XMLContent(object):
    def __init__(self, provider):
        self.provider = provider
        self.id = None
        self.modified = None
        self.deleted = False
        self.sets = {u'normap': {u'name':u'normap',
                                                   u'description':u'NORMAP data'}}
        self.metadata = None

    def update(self, data):
        self.id = unicode(data['id'][:-3])
        svninfo = data['svn']
        self.modified = svninfo.date
        self.deleted = svninfo.deleted
        document = svninfo.get() #urllib.urlopen(svninfo.path)
        root = etree.fromstring(document)
        xpath = XPath(root, nsmap={'x':'http://gcmd.gsfc.nasa.gov/Aboutus/xml/dif/'})
        self.metadata = {'dif': etree.tostring(root)}