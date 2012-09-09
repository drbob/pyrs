# Test harness for pyrs.
#
# Sets up everything....
# accepts a bunch of requests.
# then waits for responses, prints them out and ensures 'success'
# 

import pyrs.comms
import pyrs.rpc
import pyrs.msgs
import pyrs.responder

import pyrs.test.auth
import pyrs.test.responders

import time, datetime

class Harness:
  def __init__(self):

    # load Auth from file 'auth.txt'
    self.auth = pyrs.test.auth.Auth()
    
    # Construct a Msg Parser.
    self.parser = pyrs.msgs.RpcMsgs();

    # create comms object.
    self.comms = pyrs.comms.SSHcomms(self.auth.user, self.auth.pwd, self.auth.host, self.auth.port);
    self.rpc = pyrs.rpc.RsRpc(self.comms); 

    # build responder (with Response Checker)
    self.responder = pyrs.responder.RsResponderGroup(self.rpc, self.parser);
    check_responder = pyrs.test.responders.RsCheckStatusResponder();
    self.responder.addGenericResponder(check_responder);

  def connect(self):
    self.comms.connect();

  def close(self):
    self.comms.close();

  def send_request(self, msg_id, msg):
    req_id = self.rpc.request(msg_id, msg);
    return req_id;

  def check_responses(self, timeout):

    now = datetime.datetime.now() - datetime.timedelta(seconds=1); # force one cycle at least.
    expiry_time = now + datetime.timedelta(seconds=timeout);
    while(now < expiry_time):
      print 'Doing handle responses cycle'
      more_resp = True;
      while(more_resp):
        # wait for responses.
        more_resp = self.responder.handleresponses()

      time.sleep(0.1);
      now = datetime.datetime.now();

