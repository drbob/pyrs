""" RsPy::RPC : message passing interface """


########################
# The idea here, is that we create a handler which we can pass responder functions.
# and it will choose the correct fn, and call it with the message.
#
# Responders can either be ReqId specific, or MsgId specific - or Both!
#


# An example Responder, that accepts everything, and just ignores it.
# Use this as the last generic responder - to cleanup unknown msgs.
class RsIgnoreResponder(object):
  def __init__(self):
    pass
  def handlemsg(req_id, msg_id, msg_body, rpc, parser):
    return True;

# Responder Shell for the ResponderGroup.
class RsSpecificResponder(object):
  def __init__(self, req_id, msg_id, responder):
    self.responder = responder
    self.req_id = req_id
    self.msg_id = msg_id
    pass

  def isReqIdSpecific(self):
    if (self.req_id):
      return True;
    return False;
  
  def isMsgIdSpecific(self):
    if (self.msg_id):
      return True;
    return False;
  
  def isReqIdMatch(self, req_id):
    if (self.req_id):
      return (self.req_id == req_id)
    return True;
  
  def isMsgIdMatch(self, msg_id):
    if (self.msg_id):
      return (self.msg_id == msg_id)
    return True;

  def handlemsg(self, req_id, msg_id, msg_body, rpc, parser):
    return self.responder(req_id, msg_id, msg_body, rpc, parser)


# 
class RsResponderGroup(object):
  def __init__(self, rpc, parser):
    self.rpc = rpc
    self.parser = parser

    self.nolevels = 10
    self.resp_idx = []
    self.gen_responders = []
    self.other_msgs = []

    for i in range(self.nolevels):
      self.resp_idx.append([])

  def addGenericResponder(self, genresp):
    self.gen_responders.append(genresp)

  def addSpecificResponder(self, lvl, resp):
    # range check input.
    if (lvl < 0) or (lvl >= self.nolevels):
      raise Exception

    # check that resp is either MsgId or ReqId specific.
    if (not resp.isReqIdSpecific()) and (not resp.isMsgIdSpecific()):
      raise Exception

    self.resp_idx[lvl].append(resp)

  # send msg.
  def sendmsg(self, msg_id, protomsg):
    self.rpc.request(msg_id, protomsg)

  # check responses.
  def handleresponses(self):
    # try to get a response.
    self.rpc.fetch_responses();
    ans = self.rpc.first_response();
    if not ans:
      return False

    (req_id, msg_id, msg_body) = ans
    # iterate through resp_idx, and try and find a handler.
    handled = False;
    for i in range(self.nolevels):
      for responder in self.resp_idx[i]:
        if responder.isReqIdMatch(req_id) and responder.isMsgIdMatch(msg_id):
          # match! handle it.
          handled = responder.handlemsg(req_id, msg_id, msg_body, self.rpc, self.parser)
        
        if handled:
          break
      # break out of second loop too.
      if handled:
        break

    # try generic handler 
    if not handled:
      for responder in self.gen_responders:
        handled = responder.handlemsg(req_id, msg_id, msg_body, self.rpc, self.parser)
        if handled:
          break

    # if still not handled - stick in queue.
    self.other_msgs.append( (req_id, msg_id, msg_body) )
    return True

  def unhandledCount(self):
    # if there is no generic, the responses queue up.
    return len(self.other_msgs)

  def getUnhandledMsg(self):
    if (len(self.other_msgs) > 0):
      return self.other_msgs.pop(0)
    return None

