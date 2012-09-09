#!/usr/bin/python

# Test Harness, Test Chat Lobby List.

# Message Definitions.
from pyrs.proto import core_pb2
from pyrs.proto import peers_pb2
from pyrs.proto import system_pb2
from pyrs.proto import chat_pb2

import pyrs.test.harness

import time

print "TestHarness for ChatLobby Listing"
harness = pyrs.test.harness.Harness();

# create connection.
harness.connect();

for i in range(5):
  # send some messages.
  print "Cycle (%d)" % (i);

  # Create some requests....
  # Send all your Requests first.
  requests = [];

  # Get List of Peers and System Info First.
  rp = peers_pb2.RequestPeers();
  rp.set = peers_pb2.RequestPeers.CONNECTED;
  rp.info = peers_pb2.RequestPeers.ALLINFO;

  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.PEERS, peers_pb2.MsgId_RequestPeers, False);

  print "Sending Request for Peers:";
  harness.send_request(msg_id, rp)

  rp = system_pb2.RequestSystemStatus();
  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.SYSTEM, system_pb2.MsgId_RequestSystemStatus, False);
  print "Sending Request for SystemStatus:";
  harness.send_request(msg_id, rp)

  # Request for Chat Lobbies.
  rp = chat_pb2.RequestChatLobbies();
  rp.lobby_set = chat_pb2.RequestChatLobbies.LOBBYSET_ALL;

  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_RequestChatLobbies, False);
  print "Sending Request for ChatLobbies:";
  harness.send_request(msg_id, rp)

  print "Checking for Responses"
  timeout = 1.0;
  harness.check_responses(1.0);
  # wait for a bit, and retry.
  print "Sleeping:";
  time.sleep(5);

harness.close();


