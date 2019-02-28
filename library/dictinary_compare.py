#!/bin/env python
from ansible.module_utils.basic import *
import os, json
import re, sys
ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'core',
                    'version': '1.0'}
KEYNOTFOUND = 'DEPLOY'       # KeyNotFound for dictDiff


def dict_display(src, dest):
    KEYNOTFOUND = "NA"
    """ Setting the Variable KEYNOTFOUND to NA """
    """ Creating the Empty dictionary with name diff """
    
    diff = {}
    """ staritng the for loop for all the keys of src dictinary """
    for key in src.keys():
        """ checking the source key exist on destination dictionary, if not then execute below"""
        if (not dest.has_key(key)):
            diff[key] = (src[key], KEYNOTFOUND)
        else:
            diff[key] = (src[key], dest[key])
    for key in dest.keys():
        if (not src.has_key(key)):
            diff[key] = ( KEYNOTFOUND, dest[key])
    if len(diff) == 0:
        diff ={ KEYNOTFOUND: KEYNOTFOUND }
    out_lines = ''
    for key in diff.keys():
        out_lines  =  out_lines  + key + "," + str(diff[key]) + "\n"
    return out_lines

    #return diff

def dict_diff(src, dest):
    diff = {}
    # Check all keys in src dict

    for key in src.keys():
        if (not dest.has_key(key)):
            diff[key] = (src[key])
        elif (src[key] != dest[key]):
            if src[key] > dest[key]:
                diff[key] = (src[key])
    # Check all keys in dest dict to find missing
    if len(diff) == 0:
        diff = { "Noting to Deploy" : "Nothing to Deploy"}
    out_lines = ''
    for key in diff.keys():
        out_lines  =  out_lines + "ModuleName :  " + key + " ,\nVersionNumber : " + str(diff[key]) + "\n"
    return out_lines
    #return diff


def main():
    module = AnsibleModule(
        argument_spec = dict(
            src       = dict(required=True, type='dict'),
            dest      = dict(required=True, type='dict'),
            opt      = dict(type='bool'),
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
    if params['opt'] is False:
        opt = False
    else:
        opt =  True
    if opt == True:
        msg  =    dict_diff(src,dest)
        module.exit_json(changed=False, msg=msg)
    else:
        msg = dict_display(src,dest)
        module.exit_json(changed=False, msg=msg)

if __name__ == '__main__':
    main()
