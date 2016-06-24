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

    def update(self, path):
        # # We validate that the  input file follows dif 9.8.4
        # TODO: validate that it follows whatever schema/version its said to follow
        doc = etree.parse(path, parser=get_parser())
        xpath = XPath(doc, nsmap={'x':'http://gcmd.gsfc.nasa.gov/Aboutus/xml/dif/'})
        self.root = doc.getroot()
        id = xpath.string('//x:Entry_ID')
        self.id = id
        self.modified = datetime.datetime.now()
#         self.modified = xpath.date('//x:Last_DIF_Revision_Date')
        document_text = open(path).read()
        self.metadata = { 'dif' : document_text }


def get_parser():
    xsdPath = os.path.dirname(os.path.abspath(__file__)) + '/../dif_v9.8.4.xsd'
    with open(xsdPath, "r") as myfile:
        schemaString = myfile.read()
    schema_root = etree.XML(schemaString)
    schema = etree.XMLSchema(schema_root)
    parser = etree.XMLParser(schema=schema)
    return parser
