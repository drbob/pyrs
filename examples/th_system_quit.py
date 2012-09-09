#!/usr/bin/python

# Test Harness, Test Chat Lobby List.

# Message Definitions.
from pyrs.proto import core_pb2
from pyrs.proto import system_pb2

import pyrs.test.harness

import time

print "TestHarness for System Status & Quit."
print "NOTE: COMMANDS NOT WORKING YET! TEST DISABLED"
exit()

harness = pyrs.test.harness.Harness();

# create connection.
harness.connect();

for i in range(5):
  # send some messages.
  print "Cycle (%d)" % (i);

  # request System Status.
  rp = system_pb2.RequestSystemStatus();
  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.SYSTEM, system_pb2.MsgId_RequestSystemStatus, False);
  print "Sending Request for SystemStatus:";
  harness.send_request(msg_id, rp)

  # request System Quit.
  rp = system_pb2.RequestSystemQuit();
  #rp.quit_code = system_pb2.RequestSystemQuit.CLOSE_CHANNEL;
  rp.quit_code = system_pb2.RequestSystemQuit.SHUTDOWN_RS;

  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.SYSTEM, system_pb2.MsgId_RequestSystemQuit, False);
  print "Sending Request for SystemQuit:";
  harness.send_request(msg_id, rp)

  print "Checking for Responses"
  timeout = 1.0;
  harness.check_responses(1.0);
  # wait for a bit, and retry.
  print "Sleeping:";
  time.sleep(20);

harness.close();


