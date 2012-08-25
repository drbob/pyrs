""" RsPy::msgs : loading messages """

# Message Definitions.
from proto import core_pb2
from proto import peers_pb2
from proto import system_pb2

class ProtoHolder(object):
  def __init__(self):
    self.ReqFns = {};
    self.RespFns = {};
 
  def construct(self, is_resp, sub_msg_id, data):
    fn = None;
    if is_resp:
      if sub_msg_id not in self.RespFns:
        print "ProtoHolder sub_msg not found in RespFns";
        return None;
      fn = self.RespFns[sub_msg_id];
    else:
      if sub_msg_id not in self.ReqFns:
        print "ProtoHolder sub_msg not found in ReqFns";
        return None;
      fn = self.ReqFns[sub_msg_id];

    obj = fn();
    try:
      obj.ParseFromString(data);
    except Exception, e:
      print "ProtoHolder error parsing string. Exception: %s" % (e);
      return None;

    return obj

#############################################################################################
#############################################################################################

class ProtoPeers(ProtoHolder):
  def __init__(self):
    # init parent.
    ProtoHolder.__init__(self);

    # dict of Requests.
    self.ReqFns[peers_pb2.MsgId_RequestPeers] = peers_pb2.RequestPeers
    self.ReqFns[peers_pb2.MsgId_RequestAddPeer] = peers_pb2.RequestAddPeer
    self.ReqFns[peers_pb2.MsgId_RequestModifyPeer] = peers_pb2.RequestModifyPeer

    # dict of Responses.
    self.RespFns[peers_pb2.MsgId_ResponsePeerList] = peers_pb2.ResponsePeerList
    self.RespFns[peers_pb2.MsgId_ResponseAddPeer] = peers_pb2.ResponseAddPeer
    self.RespFns[peers_pb2.MsgId_ResponseModifyPeer] = peers_pb2.ResponseModifyPeer

class ProtoSystem(ProtoHolder):
  def __init__(self):
    # init parent.
    ProtoHolder.__init__(self);

    # dict of Requests.
    self.ReqFns[system_pb2.MsgId_RequestSystemStatus] = system_pb2.RequestSystemStatus

    # dict of Responses.
    self.RespFns[system_pb2.MsgId_ResponseSystemStatus] = system_pb2.ResponseSystemStatus

#############################################################################################
#############################################################################################

class RpcMsgs(object):
  def __init__(self):
    self.ProtoDict = {};
    # build dict of objs.

    self.ProtoDict[core_pb2.PEERS] = ProtoPeers();
    self.ProtoDict[core_pb2.SYSTEM] = ProtoSystem();
    
  def construct(self, msg_id, data):
    # split the msg_id into bits.
    ext_id = getRpcMsgIdExtension(msg_id);
    service_id = getRpcMsgIdService(msg_id);
    submsg_id = getRpcMsgIdSubMsg(msg_id);
    is_resp = isRpcMsgIdResponse(msg_id);

    print "RpcMsgs::contruct() msg_id: (ext: %d, serv: %d, submsg: %d, is_resp: %d)" % (ext_id, service_id, submsg_id, is_resp);

    if not (ext_id == core_pb2.CORE):
      print "RpcMsgs::contruct() Only Handled CORE msg Types";
      return None;

    if service_id not in self.ProtoDict:
      print "RpcMsgs::contruct() Unknown service_id";
      return None;

    proto = self.ProtoDict[service_id];

    ans = proto.construct(is_resp, submsg_id, data);
    if not ans:
      print "RpcMsgs::contruct() ProtoHolder failed to Parse Msg";

    return ans;




# These have been translated from C++ versions.
def getRpcMsgIdSubMsg(msg_id):
  sub_msg_id = msg_id & 0xFF;
  return sub_msg_id;

# Middle 16 bits.
def getRpcMsgIdService(msg_id):
  service_id = (msg_id >> 8) & 0xFFFF;
  return service_id;

# Top 8 bits.
def getRpcMsgIdExtension(msg_id):
  ext_id = (msg_id >> 24) & 0xFE; # Bottom Bit is for Request / Response
  return ext_id;

def isRpcMsgIdResponse(msg_id):
  isresp = (msg_id >> 24) & 0x01;
  return isresp;


def constructMsgId(ext, service, submsg, is_response):
  # enforce bit sizes.
  ext &= 0xFF;
  service &= 0xFFFF;
  submsg &= 0xFF;
  
  if (is_response):
    ext |= 0x01; # Set Bottom Bit.
  else:
    ext &= 0xFE; # Clear Bottom Bit.
  
  msg_id = (ext << 24) + (service << 8) + (submsg);
  return msg_id;

    

