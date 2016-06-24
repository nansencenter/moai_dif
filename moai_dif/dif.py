import re
import uuid
import sys
import lxml.etree

from lxml.builder import ElementMaker

XSI_NS = 'http://www.w3.org/2001/XMLSchema-instance'

class DIF(object):
    """This is the GCMD DIF format

    It is registered as prefix 'dif'.'
    """

    def __init__(self, prefix, config, db):
        self.prefix = prefix
        self.config = config
        self.db = db

        self.ns = {
                   'dif' : 'http://gcmd.gsfc.nasa.gov/Aboutus/xml/dif/'
        }

        # TODO: Mofidy this hard coded schema
        # to follow whatever the input schema say
        # BUT: make sure it is some DIF version
        self.schemas = {
           'dif' : 'http://gcmd.nasa.gov/Aboutus/xml/dif/dif_v9.8.4.xsd'
        }

    def get_namespace(self):
        return self.ns[self.prefix]

    def get_schema_location(self):
        return self.schemas[self.prefix]
    
    def __call__(self, element, metadata):
        element.append(document(metadata))

def document(metadata):
    data = metadata.record
    record = metadata.record['metadata']['dif']
    record = record.encode('utf8')
    return lxml.etree.XML(record)