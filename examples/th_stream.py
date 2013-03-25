#!/usr/bin/python

# Test Harness, Test Transfer Lists.

# Message Definitions.
from pyrs.proto import core_pb2
from pyrs.proto import files_pb2
from pyrs.proto import stream_pb2

import pyrs.test.harness

import time

print "TestHarness for Streaming Files."

harness = pyrs.test.harness.Harness();

# create connection.
harness.connect();

# request Download
rp = files_pb2.RequestTransferList();
rp.direction = files_pb2.DIRECTION_DOWNLOAD;

msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.FILES, files_pb2.MsgId_RequestTransferList, False);
print "Sending Request for Download TransferList:";
list_req_id = harness.send_request(msg_id, rp)

time.sleep(1);
print "Checking for Responses"

rs = harness.rpc
parser = harness.parser
# manually extracting answer.
# wait for responses.

timeout = 1.0;
streams = []

ans = rs.response(list_req_id, timeout);
if ans:
    (msg_id, msg_body) = ans;
    print "Received Response: msg_id: %d" % (msg_id);
    list_resp = parser.construct(msg_id, msg_body);
    if list_resp:
        print "Parsed Msg:";
        print list_resp;

        # now iterate through listing and get any that have finished.
        for item in list_resp.transfers:
            if item.fraction == 1.0:
                print "Getting Completed Item: %s, size: %s, hash:%s " % (item.file.name, item.file.size, item.file.hash)
                streams.append(item.file)
    else:
        print "Unable to Parse Response";
else:
    print "No Response!";
    quit();


stream_map = {}
# now stream the files.
for stream in streams:
    stream_req = stream_pb2.RequestStartFileStream()
    stream_req.file.hash = stream.hash;
    stream_req.file.name = stream.name;
    stream_req.file.size = stream.size;
    #stream_req.file = stream;
    stream_req.rate_kbs = 50.0

    msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.STREAM, stream_pb2.MsgId_RequestStartFileStream, False);
    print "Sending Request for Download TransferList:";
    stream_req_id = harness.send_request(msg_id, stream_req)

    stream_map[stream_req_id] = stream


stream_data_msg_id = pyrs.msgs.constructMsgId(core_pb2.CORE, core_pb2.STREAM, stream_pb2.MsgId_ResponseStreamData, True);

# now we get response:
while (True):
    recved_stuff = False
    for req_id, stream in stream_map.iteritems():
        ans = rs.response(req_id, timeout);
        if ans:
            (msg_id, msg_body) = ans;
            print "Received Response: msg_id: %d" % (msg_id);
            stream_resp = parser.construct(msg_id, msg_body);
            if stream_resp:
                if (msg_id == stream_data_msg_id):
                    # we want to open the file, and write to the end of it.
                    print "streamId: %s, offset: %s, size: %s" % (stream_resp.data.stream_id, stream_resp.data.offset, stream_resp.data.size)
                    print "writing to file: %s" % stream.name
                    with open(stream.name, 'ab') as f:
                        f.write(stream_resp.data.stream_data)
                recved_stuff = True

            else:
                print "Unable to Parse Response";
        else:
            print "No Response!";

    if not recved_stuff:
        time.sleep(5);


harness.close();


