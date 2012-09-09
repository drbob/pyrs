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

username='user'
password='hellohello'
host='127.0.0.1'
port=7022  

# Construct a Msg Parser.

parser = pyrs.msgs.RpcMsgs();


# create comms object.
comms = pyrs.comms.SSHcomms(username, password, host, port);
comms.connect();
#comms = pyrs.comms.commsLoopback();
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
rp.nickname = "PyEchoBot";

msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_RequestSetLobbyNickname, False);
print "Sending PyEchoBot Nickname:"
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
while(True): # for more cycles.

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

	  # check if its a ChatMsg.
          if (msg_id == chatevent_msg_id):
              # respond.
              rp = chat_pb2.RequestSendMessage();

              rp.msg.id.chat_type = resp.msg.id.chat_type;
              rp.msg.id.chat_id = resp.msg.id.chat_id;

              rp.msg.msg = resp.msg.msg;
              msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.CHAT, chat_pb2.MsgId_RequestSendMessage, False);
              print "Echoing Message back to ChatLobby %s" % (rp.msg.msg);
              req_id = rs.request(msg_id, rp)
              requests.append(req_id);

        else:
          print "Unable to Parse Response";
      else:
        #print "No Response!";
        more_resp = False;
  

comms.close();

