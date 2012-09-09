#!/usr/bin/python

# Basic Example to connect to rs-nogui.
# You must edit this file with your username and password before running it.
# 

import pyrs.comms
import pyrs.rpc
import pyrs.msgs
import time

# Message Definitions.
from pyrs.proto import core_pb2
from pyrs.proto import peers_pb2
from pyrs.proto import system_pb2
from pyrs.proto import chat_pb2

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

# create comms object.
comms = pyrs.comms.SSHcomms(auth.user, auth.pwd, auth.host, auth.port)
comms.connect();

rs = pyrs.rpc.RsRpc(comms); 

timeout = 0.5
requests = [];
# Firstly we subscribe to Chat Events.

# Request for Chat Lobbies.
rp = chat_pb2.RequestChatLobbies();
rp.lobby_set = chat_pb2.RequestChatLobbies.LOBBYSET_ALL;

msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_RequestRegisterEvents, False);
print "Sending Register for Chat Events:"
chat_register_id = rs.request(msg_id, rp)
requests.append(chat_register_id);

# change the default nickname to PyChatBot.
rp = chat_pb2.RequestSetLobbyNickname();
rp.nickname = "PyListenBot";

msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_RequestSetLobbyNickname, False);
print "Sending PyChatBot Nickname:"
req_id = rs.request(msg_id, rp)
requests.append(req_id);


# wait for responses for initial commands.
for peer_req_id in requests:
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
  
requests = [];

# Reference Msg IDs.
chatevent_msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_EventChatMessage, True);


time.sleep(10);

# This script only logs in once!
# while(True): # for more cycles.
for i in range(20):

  print "Starting new fetch cycle";
  # Create some requests....
  # Send all your Requests first.

  # Get List of Peers and System Info First.
  rp = peers_pb2.RequestPeers();
  rp.set = peers_pb2.RequestPeers.CONNECTED;
  rp.info = peers_pb2.RequestPeers.ALLINFO;

  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.PEERS, peers_pb2.MsgId_RequestPeers, False);

  print "Sending Request for Peers:";
  req_id = rs.request(msg_id, rp)
  requests.append(req_id);

  # 
  rp = system_pb2.RequestSystemStatus();
  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.SYSTEM, system_pb2.MsgId_RequestSystemStatus, False);
  print "Sending Request for SystemStatus:";
  req_id = rs.request(msg_id, rp)
  requests.append(req_id);

  # Request for Chat Lobbies.
  rp = chat_pb2.RequestChatLobbies();
  rp.lobby_set = chat_pb2.RequestChatLobbies.LOBBYSET_ALL;

  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_RequestChatLobbies, False);
  print "Sending Request for ChatLobbies:";
  chat_listing_id = rs.request(msg_id, rp)

  requests.append(chat_listing_id);

  # Now iterate through all the responses.
  next_req_cycle = [];
  for peer_req_id in requests:

    # wait for responses.

    ans = rs.response(peer_req_id, timeout);
    if ans:
      (msg_id, msg_body) = ans;
      print "Received Response: msg_id: %d" % (msg_id);
      resp = parser.construct(msg_id, msg_body);
      if resp:
        print "Parsed Msg:";
        print resp;
        # Handle chat_listing results....
        if (peer_req_id == chat_listing_id):
          print "Handling ChatLobby Response";
          for lobby in resp.lobbies:
            if lobby.lobby_state == chat_pb2.ChatLobbyInfo.LOBBYSTATE_PUBLIC:
              # lets try and join it!
              # Request to Join ChatLobby.
              rp = chat_pb2.RequestJoinOrLeaveLobby();
              rp.lobby_id = lobby.lobby_id;
              rp.action = chat_pb2.RequestJoinOrLeaveLobby.JOIN_OR_ACCEPT;
              msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_RequestJoinOrLeaveLobby, False);
              print "Sending Request to Join Public ChatLobby %s" % (lobby.lobby_name);
              req_id = rs.request(msg_id, rp)
              next_req_cycle.append(req_id);
            else:
              print "Ignoring Other Type of ChatLobby %s" % (lobby.lobby_name);
      else:
        print "Unable to Parse Response";
  
    else:
      print "No Response!";
      continue;

  # Add 
  requests = next_req_cycle;
 
  # wait for a bit, and retry.
  print "Waiting For Chat Events:";
  for i in range(5):
    #print "Sleeping Briefly";
    time.sleep(1);

    more_resp = True;
    while(more_resp):
      # wait for responses.
      ans = rs.response(chat_register_id, timeout);
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
        #print "No Response!";
        more_resp = False;
  

comms.close();

