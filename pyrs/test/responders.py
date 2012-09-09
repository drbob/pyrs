# Responders for testing,

import pyrs.msgs

from pyrs.proto import core_pb2

########################################
# Define some Responders.
########################################

class RsPrintResponder(object):
  def handlemsg(self, req_id, msg_id, msg_body, rpc, parser):
    print "RsPrintResponder asked to handlemsg(req_id: %d, msg_id: %d)" % (req_id, msg_id)

    resp = parser.construct(msg_id, msg_body);
    if not resp:
      print "RsPrintResponder Failed to Parse Msg... returning True anyway!"
      return True;

    print "RsPrintResponder Response:";
    print resp;

    return True;


class RsCheckStatusResponder(object):
  def handlemsg(self, req_id, msg_id, msg_body, rpc, parser):
    print "RsCheckStatusResponder asked to handlemsg(req_id: %d, msg_id: %d)" % (req_id, msg_id)

    resp = parser.construct(msg_id, msg_body);
    if not resp:
      print "RsCheckStatusResponder Failed to Parse Msg... returning True anyway!"
      raise Exception;
      return False;

    print "RsCheckStatusResponder Response:";
    print resp;

    if (resp.status.code == core_pb2.Status.SUCCESS):
      print "RsCheckStatusResponder Response GOOD";
    else:
      print "RsCheckStatusResponder Response ERROR";
      raise Exception;

    return True;


