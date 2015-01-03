#!/usr/bin/env python

# Copyright (c) 2014, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.
#
"""Parses a CybOX Observables document and creates a python-cybox Observables instance.
Once parsed, the dictionary representation of the object is printed to stdout.
"""

import sys
import cybox.bindings.cybox_core as cybox_core_binding
from  cybox.core import Observables
import json
import rawes

es = rawes.Elastic('http://localhost:9200')

def parse(xml_file):
    observables_obj = cybox_core_binding.parse(xml_file) # create binding object from xml file
    observables = Observables.from_obj(observables_obj) # convert binding object into python-cybox object
    return observables

def parseString(xml):
    observables_obj = cybox_core_binding.parseString(xml) # create binding object from xml string
    observables = Observables.from_obj(observables_obj) # to python-cybox object
    return observables

def main():
    if len(sys.argv) != 2:
        print "[!] Please provide an xml file" 
        exit(1)
    
    print 'HELLLLLLLLLLLOOOOOOOOOOO'
    #xml_file = sys.argv[-1]
    xml = sys.argv[-1]
    #observables = parse(xml_file) 
    observables = parseString(xml)
    #print observables.to_dict() # example to_dict() call on returned object
    ob_dict = observables.to_dict()
    #print json.dumps(ob_dict) #print json
    properties = ob_dict['observables'][0]['object']['properties']
    del ob_dict['observables'][0]['object']['properties']
    ob_dict['observables'][0]['object']['properties'] = {}
    ob_dict['observables'][0]['object']['properties']['properties'] = properties
    ob_dict['observables'][0]['object']['properties']['type'] = 'nested'
    ob_json = json.dumps(ob_dict)
    #print ob_json
    try:
        es_index = es.post('cybox/data',data=ob_json)
        print es_index
    except Exception, e:
        print e        
        pass
    
    


if __name__ == "__main__":
    main()