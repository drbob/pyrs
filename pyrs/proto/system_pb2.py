# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import core_pb2

DESCRIPTOR = descriptor.FileDescriptor(
  name='system.proto',
  package='rsctrl.system',
  serialized_pb='\n\x0csystem.proto\x12\rrsctrl.system\x1a\ncore.proto\"\x15\n\x13RequestSystemStatus\"\xf6\x02\n\x14ResponseSystemStatus\x12#\n\x06status\x18\x01 \x02(\x0b\x32\x13.rsctrl.core.Status\x12\x10\n\x08no_peers\x18\x02 \x02(\r\x12\x14\n\x0cno_connected\x18\x03 \x02(\r\x12?\n\nnet_status\x18\x04 \x02(\x0e\x32+.rsctrl.system.ResponseSystemStatus.NetCode\x12(\n\x08\x62w_total\x18\x05 \x02(\x0b\x32\x16.rsctrl.core.Bandwidth\"\xa5\x01\n\x07NetCode\x12\x0f\n\x0b\x42\x41\x44_UNKNOWN\x10\x00\x12\x0f\n\x0b\x42\x41\x44_OFFLINE\x10\x01\x12\x0e\n\nBAD_NATSYM\x10\x02\x12\x11\n\rBAD_NODHT_NAT\x10\x03\x12\x13\n\x0fWARNING_RESTART\x10\x04\x12\x12\n\x0eWARNING_NATTED\x10\x05\x12\x11\n\rWARNING_NODHT\x10\x06\x12\x08\n\x04GOOD\x10\x07\x12\x0f\n\x0b\x41\x44V_FORWARD\x10\x08\"\x81\x01\n\x11RequestSystemQuit\x12<\n\tquit_code\x18\x01 \x02(\x0e\x32).rsctrl.system.RequestSystemQuit.QuitCode\".\n\x08QuitCode\x12\x11\n\rCLOSE_CHANNEL\x10\x01\x12\x0f\n\x0bSHUTDOWN_RS\x10\x02\"9\n\x12ResponseSystemQuit\x12#\n\x06status\x18\x01 \x02(\x0b\x32\x13.rsctrl.core.Status*K\n\rRequestMsgIds\x12\x1d\n\x19MsgId_RequestSystemStatus\x10\x01\x12\x1b\n\x17MsgId_RequestSystemQuit\x10\x02*N\n\x0eResponseMsgIds\x12\x1e\n\x1aMsgId_ResponseSystemStatus\x10\x01\x12\x1c\n\x18MsgId_ResponseSystemQuit\x10\x02')

_REQUESTMSGIDS = descriptor.EnumDescriptor(
  name='RequestMsgIds',
  full_name='rsctrl.system.RequestMsgIds',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='MsgId_RequestSystemStatus', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='MsgId_RequestSystemQuit', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=634,
  serialized_end=709,
)


_RESPONSEMSGIDS = descriptor.EnumDescriptor(
  name='ResponseMsgIds',
  full_name='rsctrl.system.ResponseMsgIds',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='MsgId_ResponseSystemStatus', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='MsgId_ResponseSystemQuit', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=711,
  serialized_end=789,
)


MsgId_RequestSystemStatus = 1
MsgId_RequestSystemQuit = 2
MsgId_ResponseSystemStatus = 1
MsgId_ResponseSystemQuit = 2


_RESPONSESYSTEMSTATUS_NETCODE = descriptor.EnumDescriptor(
  name='NetCode',
  full_name='rsctrl.system.ResponseSystemStatus.NetCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='BAD_UNKNOWN', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='BAD_OFFLINE', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='BAD_NATSYM', index=2, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='BAD_NODHT_NAT', index=3, number=3,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='WARNING_RESTART', index=4, number=4,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='WARNING_NATTED', index=5, number=5,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='WARNING_NODHT', index=6, number=6,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='GOOD', index=7, number=7,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ADV_FORWARD', index=8, number=8,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=276,
  serialized_end=441,
)

_REQUESTSYSTEMQUIT_QUITCODE = descriptor.EnumDescriptor(
  name='QuitCode',
  full_name='rsctrl.system.RequestSystemQuit.QuitCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='CLOSE_CHANNEL', index=0, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='SHUTDOWN_RS', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=527,
  serialized_end=573,
)


_REQUESTSYSTEMSTATUS = descriptor.Descriptor(
  name='RequestSystemStatus',
  full_name='rsctrl.system.RequestSystemStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=43,
  serialized_end=64,
)


_RESPONSESYSTEMSTATUS = descriptor.Descriptor(
  name='ResponseSystemStatus',
  full_name='rsctrl.system.ResponseSystemStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='status', full_name='rsctrl.system.ResponseSystemStatus.status', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='no_peers', full_name='rsctrl.system.ResponseSystemStatus.no_peers', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='no_connected', full_name='rsctrl.system.ResponseSystemStatus.no_connected', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='net_status', full_name='rsctrl.system.ResponseSystemStatus.net_status', index=3,
      number=4, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='bw_total', full_name='rsctrl.system.ResponseSystemStatus.bw_total', index=4,
      number=5, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _RESPONSESYSTEMSTATUS_NETCODE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=67,
  serialized_end=441,
)


_REQUESTSYSTEMQUIT = descriptor.Descriptor(
  name='RequestSystemQuit',
  full_name='rsctrl.system.RequestSystemQuit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='quit_code', full_name='rsctrl.system.RequestSystemQuit.quit_code', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _REQUESTSYSTEMQUIT_QUITCODE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=444,
  serialized_end=573,
)


_RESPONSESYSTEMQUIT = descriptor.Descriptor(
  name='ResponseSystemQuit',
  full_name='rsctrl.system.ResponseSystemQuit',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='status', full_name='rsctrl.system.ResponseSystemQuit.status', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=575,
  serialized_end=632,
)

_RESPONSESYSTEMSTATUS.fields_by_name['status'].message_type = core_pb2._STATUS
_RESPONSESYSTEMSTATUS.fields_by_name['net_status'].enum_type = _RESPONSESYSTEMSTATUS_NETCODE
_RESPONSESYSTEMSTATUS.fields_by_name['bw_total'].message_type = core_pb2._BANDWIDTH
_RESPONSESYSTEMSTATUS_NETCODE.containing_type = _RESPONSESYSTEMSTATUS;
_REQUESTSYSTEMQUIT.fields_by_name['quit_code'].enum_type = _REQUESTSYSTEMQUIT_QUITCODE
_REQUESTSYSTEMQUIT_QUITCODE.containing_type = _REQUESTSYSTEMQUIT;
_RESPONSESYSTEMQUIT.fields_by_name['status'].message_type = core_pb2._STATUS
DESCRIPTOR.message_types_by_name['RequestSystemStatus'] = _REQUESTSYSTEMSTATUS
DESCRIPTOR.message_types_by_name['ResponseSystemStatus'] = _RESPONSESYSTEMSTATUS
DESCRIPTOR.message_types_by_name['RequestSystemQuit'] = _REQUESTSYSTEMQUIT
DESCRIPTOR.message_types_by_name['ResponseSystemQuit'] = _RESPONSESYSTEMQUIT

class RequestSystemStatus(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REQUESTSYSTEMSTATUS
  
  # @@protoc_insertion_point(class_scope:rsctrl.system.RequestSystemStatus)

class ResponseSystemStatus(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESPONSESYSTEMSTATUS
  
  # @@protoc_insertion_point(class_scope:rsctrl.system.ResponseSystemStatus)

class RequestSystemQuit(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REQUESTSYSTEMQUIT
  
  # @@protoc_insertion_point(class_scope:rsctrl.system.RequestSystemQuit)

class ResponseSystemQuit(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESPONSESYSTEMQUIT
  
  # @@protoc_insertion_point(class_scope:rsctrl.system.ResponseSystemQuit)

# @@protoc_insertion_point(module_scope)
