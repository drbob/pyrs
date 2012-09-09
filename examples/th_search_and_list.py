#!/usr/bin/python

# Test Harness, Test Chat Lobby List.

# Message Definitions.
from pyrs.proto import core_pb2
from pyrs.proto import search_pb2

import pyrs.test.harness

import time

print "TestHarness for Search & List."

harness = pyrs.test.harness.Harness();

# create connection.
harness.connect();

if True:

  # request Search
  rp = search_pb2.RequestBasicSearch();
  term = rp.terms.append('green');

  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.SEARCH, search_pb2.MsgId_RequestBasicSearch, False);
  print "Sending Request for Search:";
  harness.send_request(msg_id, rp)

  time.sleep(1);
  print "Checking for Responses"
  timeout = 1.0;
  harness.check_responses(1.0);

  print "Wait for a bit for results....";
  time.sleep(20);

  # request Search Results.
  rp = search_pb2.RequestSearchResults();
  # Empty SearchIds

  msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.SEARCH, search_pb2.MsgId_RequestSearchResults, False);
  print "Sending Request for SystemQuit:";
  harness.send_request(msg_id, rp)

  time.sleep(1);
  print "Checking for Responses"
  timeout = 1.0;
  harness.check_responses(1.0);

  # close Search Results.
  # need to get searchId first --- improvements required to test harness :(

  time.sleep(1);
  print "Checking for Responses"
  timeout = 1.0;
  harness.check_responses(1.0);

harness.close();


