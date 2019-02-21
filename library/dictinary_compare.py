#!/bin/env python
from ansible.module_utils.basic import *
import os, json
import re, sys
ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'core',
                    'version': '1.0'}
KEYNOTFOUND = 'DEPLOY'       # KeyNotFound for dictDiff



def dict_diff(src, dest):
    diff = {}
    # Check all keys in src dict

    for key in src.keys():
        if (not dest.has_key(key)):
            diff[key] = (src[key], KEYNOTFOUND)
        elif (src[key] != dest[key]):
            if src[key] > dest[key]:
                diff[key] = (src[key], KEYNOTFOUND )
    # Check all keys in dest dict to find missing
    if len(diff) == 0:
        diff = { "Noting to Deploy" : "Nothing to Deploy"}
    return diff


def main():
    module = AnsibleModule(
        argument_spec = dict(
            src       = dict(required=True, type='dict'),
            dest      = dict(required=True, type='dict'),
        ),
        supports_check_mode=True,
    )
    params = module.params
    if type(params['src']) is not dict:
        print "src is not dict type"
        sys.exit()
    if type(params['dest']) is not dict:
        print "dest is not dict type"
        sys.exit()
    src  =    params['src']
    dest =    params['dest']  
    msg  =    dict(dict_diff(src,dest))
    module.exit_json(changed=False, msg=msg)

if __name__ == '__main__':
    main()

#src = sys.argv[1]
#dest = sys.argv[2]
#data1=json.loads(src)
#data2=json.loads(dest)


#data = dict_diff(data1,data2)
#print data

