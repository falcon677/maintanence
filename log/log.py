#!./python/bin/python
# -*- coding: utf-8 -*-
import time
import os
import sys
import ConfigParser
import functools

cur_dir = os.path.split(os.path.realpath(__file__))[0]
CONFIG_FILE = os.sep.join([cur_dir, 'migrate.log'])
CONF = ConfigParser.ConfigParser()

instance_uuid = "this_is_a_test"

def get_progress(instance_uuid):
    CONF.read(CONFIG_FILE)
    if not CONF.has_section(instance_uuid):
        CONF.add_section(instance_uuid)
        CONF.write(open(CONFIG_FILE, 'a'))
    progress_info  = dict(CONF.items(instance_uuid))
    return progress_info

def log_progress(instance_uuid=None):

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kw):
            step  = dict(CONF.items(instance_uuid))
            if func.__name__ in step:
                print "====================================================================="
                print("get result from log file !")
                print("%s : %s" %(func.__name__, step[func.__name__]) )
                print "====================================================================="
                return step[func.__name__]
            res = func(*args, **kw)
            CONF.set(instance_uuid, func.__name__, res)
            CONF.write(open(CONFIG_FILE, 'w'))
            return res
        return wrapper
    return decorator


@log_progress(instance_uuid)
def step_1():
    print "step_1 is running"
    return "aaaaaaaaaa"


@log_progress(instance_uuid)
def step_2():
    print "step_2 is running"
    return "bbbbbbbbbbb"


if __name__ == "__main__":
    get_progress(instance_uuid)
    res_1 = step_1()
    res_2 = step_2()
    print("res_1: %s,  res_2: %s ." % (res_1, res_2))
    with open(CONFIG_FILE, 'r') as f:
        for line in f:
            print line
