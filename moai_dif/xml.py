from lxml import etree
import os

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
        ## We validate that the  input file follows moai_dif 9.8.4
        # TODO: validate that it follows whatever schema/version its said to follow
        doc = etree.parse(path, parser=get_parser())
        xpath = XPath(doc, nsmap={'x':'http://gcmd.gsfc.nasa.gov/Aboutus/xml/moai_dif/'})
        self.root = doc.getroot()

        id = xpath.string('//x:Entry_ID')
        self.id = id
        self.modified = xpath.date('//x:Last_DIF_Revision_Date')
        self.metadata = {}
        self.metadata['moai_dif'] = extract_node(self.root)


def extract_node(node):
    element = []
    if (len(node.getchildren()) == 0):
       if node.text:
           val = (node.tag.split("}")[1], node.text)
           element.append(val)
    else:
        for node2 in node:
            tag = node2.tag.split("}")[1]
            val = None
            if (len(node2.getchildren()) == 0):
                if node2.text:
                    val = node2.text
            else:
                val = extract_node(node2)
            if (val):
                val = (tag, val)
                element.append(val)
    return element


def get_parser():
    xsdPath = os.path.dirname(os.path.abspath(__file__)) + '/dif_v9.8.4.xsd'
    with open(xsdPath, "r") as myfile:
        schemaString = myfile.read()
    schema_root = etree.XML(schemaString)
    schema = etree.XMLSchema(schema_root)
    parser = etree.XMLParser(schema=schema)
    return parser