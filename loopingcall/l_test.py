from loopingcall import LoopingCallDone
from loopingcall import FixedIntervalLoopingCall
import random

def _is_job_finished(retries):

    print "retries %s" % (retries)
    aa = random.uniform(0, 10) 
    if aa > 8:
        raise Exception('geml raise')
    if retries > 7:
        return True
    return False

def _wait_for_job_complete(kwargs):

    if kwargs['retries'] > kwargs['maxJobRetries']:
        reason = "timeout"
        raise LoopingCallDone(reason)
    
    if kwargs['function'](kwargs['retries']):
        
        reason = "downloaded"
        print reason
        raise LoopingCallDone()
    kwargs['retries'] = kwargs['retries'] + 1


kwargs = {'retries': 0,
          'maxJobRetries': 10,
          'function':_is_job_finished}
intervalInSecs = 0.5
timer = FixedIntervalLoopingCall(_wait_for_job_complete, kwargs)
aa = timer.start(interval=intervalInSecs).wait()
print aa

