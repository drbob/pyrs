""" RsPy::RPC : message passing interface """

import struct
import datetime, time

kMAGICID     = 0x137f0001
kHEADERSIZE  = 16;

class RsRpc(object):
 
  def __init__(self, comms):
    # Dictionaries for outstanding requests / responses.
    # self.requests = {};
    self.responses = {}; 
    self.comms = comms;
    self.next_req_id = 1;
    self.msgpacker = MsgPacker(comms);

  def request(self, msg_type, pb_msg):
    req_id = self.gen_req_id();
    msg_body = pb_msg.SerializeToString();
    msg_size = len(msg_body);
    #self.store_request(req_id, msg_type);
    self.msgpacker.send_msg(req_id, msg_type, msg_size, msg_body);
    return req_id;

  def cancel_request(self, req_id):
    pass;

  def response(self, req_id, timeout):
    if __debug__: 
        print "RsRpc::response: req_id: %d, timeout: %f" % (req_id, timeout);
    # special case - no timeout, non-blocking.
    if (not timeout): 
      if __debug__: 
        print "RsRpc::response: no timeout => get & return";
      self.fetch_responses();
      return response_stored(req_id);

    # otherwise we need a little loop.
    now = datetime.datetime.now();
    expiry_time = now + datetime.timedelta(seconds=timeout);
    while(now < expiry_time):
      if __debug__: 
        print "RsRpc::response: try fetch cycle...";

      # check for more data.
      self.fetch_responses();
      ans = self.response_stored(req_id);
      if ans:
        return ans;

      # sleep a bit.
      time.sleep(0.1);
      now = datetime.datetime.now();

    if __debug__: 
        print "RsRpc::response: timeout: No Response";
    return None;

  def response_stored(self, req_id):
    if req_id in self.responses:
      ans = self.responses[req_id].pop(0);
      if (len(self.responses[req_id]) == 0):
        del self.responses[req_id];
      if __debug__: 
        print "RsRpc::response_stored(%d) Found!" % (req_id);
      return ans;
    if __debug__: 
        print "RsRpc::response_stored(%d) No received!" % (req_id);
    return None;

  def first_response(self):
    for req_id, response_list in self.responses.items():
      (msg_id, msg_body) = self.response_stored(req_id);
      return (req_id, msg_id, msg_body);
    return None;

  def fetch_responses(self):
    if __debug__: 
        print "RsRpc::fetch_responses()";
    if self.comms.recv_ready():
      if __debug__: 
        print "RsRpc::fetch_responses() Data Ready";
      ans = self.msgpacker.read_msg();
      if not ans:
        if __debug__: 
            print "RsRpc::fetch_responses() Bad Answer";
        return None;

      # put in responses map.
      msg_type = ans[0];
      req_id = ans[1];
      msg_body = ans[2];

      if __debug__: 
        print "RsRpc::fetch_responses() Storing Answer (%d, %d, len(%d))" % (msg_type, req_id, len(msg_body));

      if req_id not in self.responses:
        self.responses[req_id] = [];
      self.responses[req_id].append( (msg_type, msg_body) );

  def clear(self):
    self.responses = {};

  def gen_req_id(self):
    req_id = self.next_req_id;
    self.next_req_id += 1;
    return req_id;
    

class  MsgPacker:
  def __init__(self, comms):
    self.comms = comms;

  def send_msg(self, req_id, msg_type, msg_size, msg_body):
    # pack the data. 16 bytes for [ Magic ][ Type ] [ ReqId ] [ Size ] [ Data ].
    # >  is big-endian (network byte order).
    # L  is unsigned long.
    msgheader = struct.pack('>LLLL', kMAGICID, msg_type, req_id, msg_size);
    msg = msgheader + msg_body;

    self.comms.send(msg);

  def read_msg(self):
    # unpack the data. 16 bytes for [ Magic ][ Type ] [ ReqId ] [ Size ] [ Data ].

    req_id = 0;
    msg_type = 0;
    msg_size = 0;

    header = '';
    while(len(header) < kHEADERSIZE):
      header += self.comms.recv(kHEADERSIZE - len(header));

    (magic_id, msg_type, req_id, msg_size) = struct.unpack_from('>LLLL', header);
    # The reasons for MagicId are:
    #  - ensure that client / server are compatible.
    #  - ensure that we haven't lost our place in the byte stream.
    if not (magic_id == kMAGICID):
      raise Exception;  
 
    # now read body.
    # ensure we read the whole message.
    # probably need an emergency exit clause.
    msg_body = '';
    while(len(msg_body) < msg_size):
      msg_body += self.comms.recv(msg_size - len(msg_body));

    return (msg_type, req_id, msg_body);


