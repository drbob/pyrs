#!/usr/bin/python

# Basic Example to connect to rs-nogui.
# You must edit this file with your username and password before running it.
# 

import pyrs.comms
import pyrs.rpc
import time

# Message Definitions.
from pyrs.proto import rspeers_pb2

username='user'
password='putyourpasswordhere'
host='127.0.0.1'
port=7022  

while(1):

  print "Starting new connect cycle";

  # create comms object.
  comms = pyrs.comms.SSHcomms(username, password, host, port);
  comms.connect();
  #comms = pyrs.comms.commsLoopback();
  rs = pyrs.rpc.RsRpc(comms); 

  # Create some requests....
  #msgIds = RsMsgIds_rb2.new();

  rp = rspeers_pb2.requestPeers();
  rp.options = "Hello";

  # Send all your Requests first.
  print "Sending Request:";
  peer_req_id = rs.request(17, rp) #msgIds.REQUEST_PEERS, rp);

  # wait for responses.
  timeout = 0.5

  ans = rs.response(peer_req_id, timeout);
  if not ans:
    print "No Response!";
    continue;
  (msg_id, msg_body) = ans;
  resp = rspeers_pb2.requestPeers();
  resp.ParseFromString(msg_body);


  print "Received Response: msg_id: %d" % (msg_id);
  print resp;


  comms.close();
  # wait for a bit, and retry.
  print "Sleeping:";
  time.sleep(5);

