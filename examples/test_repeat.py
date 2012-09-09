#!/usr/bin/python

# Basic Example to connect to rs-nogui.
# You must edit this file with your username and password before running it.

# This example repeatly logs in, sends commands, and closes connection.

import pyrs.comms
import pyrs.rpc
import pyrs.msgs
import time

# Message Definitions.
from pyrs.proto import core_pb2
from pyrs.proto import peers_pb2
from pyrs.proto import system_pb2

import pyrs.test.auth

# This will load auth parameters from file 'auth.txt'
# ONLY use for tests - make the user login properly.
auth = pyrs.test.auth.Auth()

## Alternatively - specify here.
#auth.setUser('user');
#auth.setHost('127.0.0.1');
#auth.setPort(7022);
#auth.setPwd('password');

# Construct a Msg Parser.
parser = pyrs.msgs.RpcMsgs();

while(1):

  print "Starting new connect cycle";

  # create comms object.
  comms = pyrs.comms.SSHcomms(auth.user, auth.pwd, auth.host, auth.port)
  comms.connect();
  #comms = pyrs.comms.commsLoopback();
  rs = pyrs.rpc.RsRpc(comms); 

  # Create some requests....
  # Send all your Requests first.
  requests = [];

  rp = peers_pb2.RequestPeers();
  rp.set = peers_pb2.RequestPeers.ALL;
  rp.info = peers_pb2.RequestPeers.ALLINFO;

  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.PEERS, peers_pb2.MsgId_RequestPeers, False);

  print "Sending Request for Peers:";
  req_id = rs.request(msg_id, rp)
  requests.append(req_id);

  # 
  rp = peers_pb2.RequestAddPeer();
  rp.gpg_id = "IdontKnow";
  rp.cmd = peers_pb2.RequestAddPeer.EXAMINE;

  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.PEERS, peers_pb2.MsgId_RequestAddPeer, False);
  print "Sending Request to AddPeer:";
  req_id = rs.request(msg_id, rp)
  requests.append(req_id);

  # 
  rp = peers_pb2.RequestModifyPeer();
  rp.cmd = peers_pb2.RequestModifyPeer.DYNDNS;

  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.PEERS, peers_pb2.MsgId_RequestModifyPeer, False);
  print "Sending Request ModifyPeer:";
  req_id = rs.request(msg_id, rp)
  requests.append(req_id);


  # 
  rp = system_pb2.RequestSystemStatus();
  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.SYSTEM, system_pb2.MsgId_RequestSystemStatus, False);
  print "Sending Request for SystemStatus:";
  req_id = rs.request(msg_id, rp)
  requests.append(req_id);


  # Now iterate through all the responses.
  for peer_req_id in requests:

    # wait for responses.
    timeout = 0.5

    ans = rs.response(peer_req_id, timeout);
    if ans:
      (msg_id, msg_body) = ans;
      print "Received Response: msg_id: %d" % (msg_id);
      resp = parser.construct(msg_id, msg_body);
      if resp:
        print "Parsed Msg:";
        print resp;
      else:
        print "Unable to Parse Response";
  
    else:
      print "No Response!";
      continue;
  
  comms.close();
  # wait for a bit, and retry.
  print "Sleeping:";
  time.sleep(5);

