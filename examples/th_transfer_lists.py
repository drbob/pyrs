#!/usr/bin/python

# Test Harness, Test Transfer Lists.

# Message Definitions.
from pyrs.proto import core_pb2
from pyrs.proto import files_pb2

import pyrs.test.harness

import time

print "TestHarness for Transfer List."

harness = pyrs.test.harness.Harness();

# create connection.
harness.connect();

for i in range(30):

  # request Upload
  rp = files_pb2.RequestTransferList();
  rp.direction = files_pb2.DIRECTION_UPLOAD;

  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.FILES, files_pb2.MsgId_RequestTransferList, False);
  print "Sending Request for Upload TransferList:";
  harness.send_request(msg_id, rp)

  time.sleep(1);
  print "Checking for Responses"
  timeout = 1.0;
  harness.check_responses(1.0);

  # request Download
  rp = files_pb2.RequestTransferList();
  rp.direction = files_pb2.DIRECTION_DOWNLOAD;

  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.FILES, files_pb2.MsgId_RequestTransferList, False);
  print "Sending Request for Upload TransferList:";
  harness.send_request(msg_id, rp)

  time.sleep(1);
  print "Checking for Responses"
  timeout = 1.0;
  harness.check_responses(1.0);

  print "Sleeping for a bit"
  time.sleep(10);

harness.close();


