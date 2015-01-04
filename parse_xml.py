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
import collections

es = rawes.Elastic('http://localhost:9200')

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

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
    
    xml = sys.argv[-1]
    observables = parseString(xml)
    ob_dict = observables.to_dict()
    #print "length of observables   " + str(len(ob_dict['observables']))
    if(len(ob_dict['observables'])>1):
        for i,val in enumerate(ob_dict['observables']):
            if('object' in ob_dict['observables'][i]):
                flat_ob_dict = flatten(ob_dict['observables'][i]['object']['properties'])    
                ob_dict['observables'][i]['object']['properties'] = flat_ob_dict

    elif('object' in ob_dict['observables'][0]):
        flat_ob_dict = flatten(ob_dict['observables'][0]['object']['properties'])    
        ob_dict['observables'][0]['object']['properties'] = flat_ob_dict
    
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