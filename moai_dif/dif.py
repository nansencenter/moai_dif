import re
import uuid
import sys

from lxml.builder import ElementMaker

XSI_NS = 'http://www.w3.org/2001/XMLSchema-instance'

class DIF(object):
    """This is the GCMD DIF format

    It is registered as prefix 'moai_dif'.'
    """

    def __init__(self, prefix, config, db):
        self.prefix = prefix
        self.config = config
        self.db = db

        self.ns = {
                   None : 'http://gcmd.gsfc.nasa.gov/Aboutus/xml/moai_dif/'
        }

        # TODO: Mofidy this hard coded schema
        # to follow whatever the input schema say
        # BUT: make sure it is some DIF version
        self.schemas = {
           None: 'http://gcmd.nasa.gov/Aboutus/xml/moai_dif/dif_v9.8.4.xsd'
        }

    def get_namespace(self):
        return self.ns[self.prefix]

    def get_schema_location(self):
        return self.schemas[self.prefix]

    def __call__(self, element, metadata):
        data = metadata.record
        DIF = ElementMaker(namespace=self.ns[None], nsmap=self.ns)
        dif = DIF.dif()
        create_xml(data['metadata']['moai_dif'], dif, DIF)
        dif.attrib['{%s}schemaLocation' % XSI_NS] = '%s %s' % (
                        self.ns[None],
                        self.schemas[None])
        element.append(dif)


def create_xml(inElement, root, em):
    for tag, val in inElement:
        if isinstance(val, list):
            element = []
            create_xml(val, element, em)
            root.append(em(tag, *element))
        else:
            root.append(em(tag, val))