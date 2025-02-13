# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: go.chromium.org/luci/buildbucket/proto/backend.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from bb.go.chromium.org.luci.buildbucket.proto import common_pb2 as go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_common__pb2
from bb.go.chromium.org.luci.buildbucket.proto import launcher_pb2 as go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_launcher__pb2
from bb.go.chromium.org.luci.buildbucket.proto import task_pb2 as go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_task__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='go.chromium.org/luci/buildbucket/proto/backend.proto',
  package='buildbucket.v2',
  syntax='proto3',
  serialized_options=b'Z4go.chromium.org/luci/buildbucket/proto;buildbucketpb',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n4go.chromium.org/luci/buildbucket/proto/backend.proto\x12\x0e\x62uildbucket.v2\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x33go.chromium.org/luci/buildbucket/proto/common.proto\x1a\x35go.chromium.org/luci/buildbucket/proto/launcher.proto\x1a\x31go.chromium.org/luci/buildbucket/proto/task.proto\"\xfc\x06\n\x0eRunTaskRequest\x12\x0e\n\x06target\x18\x01 \x01(\t\x12#\n\x1bregister_backend_task_token\x18\x02 \x01(\t\x12\r\n\x05realm\x18\x03 \x01(\t\x12=\n\x05\x61gent\x18\x04 \x01(\x0b\x32..buildbucket.v2.RunTaskRequest.AgentExecutable\x12\x12\n\nagent_args\x18\x05 \x03(\t\x12-\n\x07secrets\x18\x06 \x01(\x0b\x32\x1c.buildbucket.v2.BuildSecrets\x12\x18\n\x10\x62uildbucket_host\x18\x07 \x01(\t\x12\x10\n\x08\x62uild_id\x18\x08 \x01(\t\x12\x36\n\ndimensions\x18\t \x03(\x0b\x32\".buildbucket.v2.RequestedDimension\x12\x32\n\x0estart_deadline\x18\n \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x34\n\x11\x65xecution_timeout\x18\x0b \x01(\x0b\x32\x19.google.protobuf.Duration\x12/\n\x0cgrace_period\x18\x0c \x01(\x0b\x32\x19.google.protobuf.Duration\x12*\n\x06\x63\x61\x63hes\x18\r \x03(\x0b\x32\x1a.buildbucket.v2.CacheEntry\x12/\n\x0e\x62\x61\x63kend_config\x18\x0e \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x13\n\x0b\x65xperiments\x18\x0f \x03(\t\x12\x12\n\nrequest_id\x18\x10 \x01(\t\x12\x14\n\x0cpubsub_topic\x18\x11 \x01(\t\x1a\x88\x02\n\x0f\x41gentExecutable\x12J\n\x06source\x18\x01 \x03(\x0b\x32:.buildbucket.v2.RunTaskRequest.AgentExecutable.SourceEntry\x1a>\n\x0b\x41gentSource\x12\x0e\n\x06sha256\x18\x01 \x01(\t\x12\x12\n\nsize_bytes\x18\x02 \x01(\x03\x12\x0b\n\x03url\x18\x03 \x01(\t\x1ai\n\x0bSourceEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12I\n\x05value\x18\x02 \x01(\x0b\x32:.buildbucket.v2.RunTaskRequest.AgentExecutable.AgentSource:\x02\x38\x01\"5\n\x0fRunTaskResponse\x12\"\n\x04task\x18\x01 \x01(\x0b\x32\x14.buildbucket.v2.Task\"=\n\x11\x46\x65tchTasksRequest\x12(\n\x08task_ids\x18\x01 \x03(\x0b\x32\x16.buildbucket.v2.TaskID\"9\n\x12\x46\x65tchTasksResponse\x12#\n\x05tasks\x18\x01 \x03(\x0b\x32\x14.buildbucket.v2.Task\">\n\x12\x43\x61ncelTasksRequest\x12(\n\x08task_ids\x18\x01 \x03(\x0b\x32\x16.buildbucket.v2.TaskID\":\n\x13\x43\x61ncelTasksResponse\x12#\n\x05tasks\x18\x01 \x03(\x0b\x32\x14.buildbucket.v2.Task\"\xae\x01\n\x16ValidateConfigsRequest\x12\x45\n\x07\x63onfigs\x18\x01 \x03(\x0b\x32\x34.buildbucket.v2.ValidateConfigsRequest.ConfigContext\x1aM\n\rConfigContext\x12\x0e\n\x06target\x18\x01 \x01(\t\x12,\n\x0b\x63onfig_json\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\"\x92\x01\n\x17ValidateConfigsResponse\x12J\n\rconfig_errors\x18\x01 \x03(\x0b\x32\x33.buildbucket.v2.ValidateConfigsResponse.ErrorDetail\x1a+\n\x0b\x45rrorDetail\x12\r\n\x05index\x18\x01 \x01(\x05\x12\r\n\x05\x65rror\x18\x02 \x01(\t2\xf2\x02\n\x0bTaskBackend\x12L\n\x07RunTask\x12\x1e.buildbucket.v2.RunTaskRequest\x1a\x1f.buildbucket.v2.RunTaskResponse\"\x00\x12U\n\nFetchTasks\x12!.buildbucket.v2.FetchTasksRequest\x1a\".buildbucket.v2.FetchTasksResponse\"\x00\x12X\n\x0b\x43\x61ncelTasks\x12\".buildbucket.v2.CancelTasksRequest\x1a#.buildbucket.v2.CancelTasksResponse\"\x00\x12\x64\n\x0fValidateConfigs\x12&.buildbucket.v2.ValidateConfigsRequest\x1a\'.buildbucket.v2.ValidateConfigsResponse\"\x00\x42\x36Z4go.chromium.org/luci/buildbucket/proto;buildbucketpbb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,google_dot_protobuf_dot_duration__pb2.DESCRIPTOR,google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_common__pb2.DESCRIPTOR,go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_launcher__pb2.DESCRIPTOR,go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_task__pb2.DESCRIPTOR,])




_RUNTASKREQUEST_AGENTEXECUTABLE_AGENTSOURCE = _descriptor.Descriptor(
  name='AgentSource',
  full_name='buildbucket.v2.RunTaskRequest.AgentExecutable.AgentSource',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='sha256', full_name='buildbucket.v2.RunTaskRequest.AgentExecutable.AgentSource.sha256', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='size_bytes', full_name='buildbucket.v2.RunTaskRequest.AgentExecutable.AgentSource.size_bytes', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='buildbucket.v2.RunTaskRequest.AgentExecutable.AgentSource.url', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1050,
  serialized_end=1112,
)

_RUNTASKREQUEST_AGENTEXECUTABLE_SOURCEENTRY = _descriptor.Descriptor(
  name='SourceEntry',
  full_name='buildbucket.v2.RunTaskRequest.AgentExecutable.SourceEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='buildbucket.v2.RunTaskRequest.AgentExecutable.SourceEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='buildbucket.v2.RunTaskRequest.AgentExecutable.SourceEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1114,
  serialized_end=1219,
)

_RUNTASKREQUEST_AGENTEXECUTABLE = _descriptor.Descriptor(
  name='AgentExecutable',
  full_name='buildbucket.v2.RunTaskRequest.AgentExecutable',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='source', full_name='buildbucket.v2.RunTaskRequest.AgentExecutable.source', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_RUNTASKREQUEST_AGENTEXECUTABLE_AGENTSOURCE, _RUNTASKREQUEST_AGENTEXECUTABLE_SOURCEENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=955,
  serialized_end=1219,
)

_RUNTASKREQUEST = _descriptor.Descriptor(
  name='RunTaskRequest',
  full_name='buildbucket.v2.RunTaskRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='target', full_name='buildbucket.v2.RunTaskRequest.target', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='register_backend_task_token', full_name='buildbucket.v2.RunTaskRequest.register_backend_task_token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='realm', full_name='buildbucket.v2.RunTaskRequest.realm', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='agent', full_name='buildbucket.v2.RunTaskRequest.agent', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='agent_args', full_name='buildbucket.v2.RunTaskRequest.agent_args', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='secrets', full_name='buildbucket.v2.RunTaskRequest.secrets', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='buildbucket_host', full_name='buildbucket.v2.RunTaskRequest.buildbucket_host', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='build_id', full_name='buildbucket.v2.RunTaskRequest.build_id', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dimensions', full_name='buildbucket.v2.RunTaskRequest.dimensions', index=8,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_deadline', full_name='buildbucket.v2.RunTaskRequest.start_deadline', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='execution_timeout', full_name='buildbucket.v2.RunTaskRequest.execution_timeout', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='grace_period', full_name='buildbucket.v2.RunTaskRequest.grace_period', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='caches', full_name='buildbucket.v2.RunTaskRequest.caches', index=12,
      number=13, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='backend_config', full_name='buildbucket.v2.RunTaskRequest.backend_config', index=13,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='experiments', full_name='buildbucket.v2.RunTaskRequest.experiments', index=14,
      number=15, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_id', full_name='buildbucket.v2.RunTaskRequest.request_id', index=15,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pubsub_topic', full_name='buildbucket.v2.RunTaskRequest.pubsub_topic', index=16,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_RUNTASKREQUEST_AGENTEXECUTABLE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=327,
  serialized_end=1219,
)


_RUNTASKRESPONSE = _descriptor.Descriptor(
  name='RunTaskResponse',
  full_name='buildbucket.v2.RunTaskResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task', full_name='buildbucket.v2.RunTaskResponse.task', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1221,
  serialized_end=1274,
)


_FETCHTASKSREQUEST = _descriptor.Descriptor(
  name='FetchTasksRequest',
  full_name='buildbucket.v2.FetchTasksRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_ids', full_name='buildbucket.v2.FetchTasksRequest.task_ids', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1276,
  serialized_end=1337,
)


_FETCHTASKSRESPONSE = _descriptor.Descriptor(
  name='FetchTasksResponse',
  full_name='buildbucket.v2.FetchTasksResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tasks', full_name='buildbucket.v2.FetchTasksResponse.tasks', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1339,
  serialized_end=1396,
)


_CANCELTASKSREQUEST = _descriptor.Descriptor(
  name='CancelTasksRequest',
  full_name='buildbucket.v2.CancelTasksRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_ids', full_name='buildbucket.v2.CancelTasksRequest.task_ids', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1398,
  serialized_end=1460,
)


_CANCELTASKSRESPONSE = _descriptor.Descriptor(
  name='CancelTasksResponse',
  full_name='buildbucket.v2.CancelTasksResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tasks', full_name='buildbucket.v2.CancelTasksResponse.tasks', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1462,
  serialized_end=1520,
)


_VALIDATECONFIGSREQUEST_CONFIGCONTEXT = _descriptor.Descriptor(
  name='ConfigContext',
  full_name='buildbucket.v2.ValidateConfigsRequest.ConfigContext',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='target', full_name='buildbucket.v2.ValidateConfigsRequest.ConfigContext.target', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='config_json', full_name='buildbucket.v2.ValidateConfigsRequest.ConfigContext.config_json', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1620,
  serialized_end=1697,
)

_VALIDATECONFIGSREQUEST = _descriptor.Descriptor(
  name='ValidateConfigsRequest',
  full_name='buildbucket.v2.ValidateConfigsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='configs', full_name='buildbucket.v2.ValidateConfigsRequest.configs', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_VALIDATECONFIGSREQUEST_CONFIGCONTEXT, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1523,
  serialized_end=1697,
)


_VALIDATECONFIGSRESPONSE_ERRORDETAIL = _descriptor.Descriptor(
  name='ErrorDetail',
  full_name='buildbucket.v2.ValidateConfigsResponse.ErrorDetail',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='buildbucket.v2.ValidateConfigsResponse.ErrorDetail.index', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='error', full_name='buildbucket.v2.ValidateConfigsResponse.ErrorDetail.error', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1803,
  serialized_end=1846,
)

_VALIDATECONFIGSRESPONSE = _descriptor.Descriptor(
  name='ValidateConfigsResponse',
  full_name='buildbucket.v2.ValidateConfigsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='config_errors', full_name='buildbucket.v2.ValidateConfigsResponse.config_errors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_VALIDATECONFIGSRESPONSE_ERRORDETAIL, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1700,
  serialized_end=1846,
)

_RUNTASKREQUEST_AGENTEXECUTABLE_AGENTSOURCE.containing_type = _RUNTASKREQUEST_AGENTEXECUTABLE
_RUNTASKREQUEST_AGENTEXECUTABLE_SOURCEENTRY.fields_by_name['value'].message_type = _RUNTASKREQUEST_AGENTEXECUTABLE_AGENTSOURCE
_RUNTASKREQUEST_AGENTEXECUTABLE_SOURCEENTRY.containing_type = _RUNTASKREQUEST_AGENTEXECUTABLE
_RUNTASKREQUEST_AGENTEXECUTABLE.fields_by_name['source'].message_type = _RUNTASKREQUEST_AGENTEXECUTABLE_SOURCEENTRY
_RUNTASKREQUEST_AGENTEXECUTABLE.containing_type = _RUNTASKREQUEST
_RUNTASKREQUEST.fields_by_name['agent'].message_type = _RUNTASKREQUEST_AGENTEXECUTABLE
_RUNTASKREQUEST.fields_by_name['secrets'].message_type = go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_launcher__pb2._BUILDSECRETS
_RUNTASKREQUEST.fields_by_name['dimensions'].message_type = go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_common__pb2._REQUESTEDDIMENSION
_RUNTASKREQUEST.fields_by_name['start_deadline'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_RUNTASKREQUEST.fields_by_name['execution_timeout'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_RUNTASKREQUEST.fields_by_name['grace_period'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_RUNTASKREQUEST.fields_by_name['caches'].message_type = go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_common__pb2._CACHEENTRY
_RUNTASKREQUEST.fields_by_name['backend_config'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_RUNTASKRESPONSE.fields_by_name['task'].message_type = go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_task__pb2._TASK
_FETCHTASKSREQUEST.fields_by_name['task_ids'].message_type = go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_task__pb2._TASKID
_FETCHTASKSRESPONSE.fields_by_name['tasks'].message_type = go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_task__pb2._TASK
_CANCELTASKSREQUEST.fields_by_name['task_ids'].message_type = go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_task__pb2._TASKID
_CANCELTASKSRESPONSE.fields_by_name['tasks'].message_type = go_dot_chromium_dot_org_dot_luci_dot_buildbucket_dot_proto_dot_task__pb2._TASK
_VALIDATECONFIGSREQUEST_CONFIGCONTEXT.fields_by_name['config_json'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_VALIDATECONFIGSREQUEST_CONFIGCONTEXT.containing_type = _VALIDATECONFIGSREQUEST
_VALIDATECONFIGSREQUEST.fields_by_name['configs'].message_type = _VALIDATECONFIGSREQUEST_CONFIGCONTEXT
_VALIDATECONFIGSRESPONSE_ERRORDETAIL.containing_type = _VALIDATECONFIGSRESPONSE
_VALIDATECONFIGSRESPONSE.fields_by_name['config_errors'].message_type = _VALIDATECONFIGSRESPONSE_ERRORDETAIL
DESCRIPTOR.message_types_by_name['RunTaskRequest'] = _RUNTASKREQUEST
DESCRIPTOR.message_types_by_name['RunTaskResponse'] = _RUNTASKRESPONSE
DESCRIPTOR.message_types_by_name['FetchTasksRequest'] = _FETCHTASKSREQUEST
DESCRIPTOR.message_types_by_name['FetchTasksResponse'] = _FETCHTASKSRESPONSE
DESCRIPTOR.message_types_by_name['CancelTasksRequest'] = _CANCELTASKSREQUEST
DESCRIPTOR.message_types_by_name['CancelTasksResponse'] = _CANCELTASKSRESPONSE
DESCRIPTOR.message_types_by_name['ValidateConfigsRequest'] = _VALIDATECONFIGSREQUEST
DESCRIPTOR.message_types_by_name['ValidateConfigsResponse'] = _VALIDATECONFIGSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RunTaskRequest = _reflection.GeneratedProtocolMessageType('RunTaskRequest', (_message.Message,), {

  'AgentExecutable' : _reflection.GeneratedProtocolMessageType('AgentExecutable', (_message.Message,), {

    'AgentSource' : _reflection.GeneratedProtocolMessageType('AgentSource', (_message.Message,), {
      'DESCRIPTOR' : _RUNTASKREQUEST_AGENTEXECUTABLE_AGENTSOURCE,
      '__module__' : 'go.chromium.org.luci.buildbucket.proto.backend_pb2'
      # @@protoc_insertion_point(class_scope:buildbucket.v2.RunTaskRequest.AgentExecutable.AgentSource)
      })
    ,

    'SourceEntry' : _reflection.GeneratedProtocolMessageType('SourceEntry', (_message.Message,), {
      'DESCRIPTOR' : _RUNTASKREQUEST_AGENTEXECUTABLE_SOURCEENTRY,
      '__module__' : 'go.chromium.org.luci.buildbucket.proto.backend_pb2'
      # @@protoc_insertion_point(class_scope:buildbucket.v2.RunTaskRequest.AgentExecutable.SourceEntry)
      })
    ,
    'DESCRIPTOR' : _RUNTASKREQUEST_AGENTEXECUTABLE,
    '__module__' : 'go.chromium.org.luci.buildbucket.proto.backend_pb2'
    # @@protoc_insertion_point(class_scope:buildbucket.v2.RunTaskRequest.AgentExecutable)
    })
  ,
  'DESCRIPTOR' : _RUNTASKREQUEST,
  '__module__' : 'go.chromium.org.luci.buildbucket.proto.backend_pb2'
  # @@protoc_insertion_point(class_scope:buildbucket.v2.RunTaskRequest)
  })
_sym_db.RegisterMessage(RunTaskRequest)
_sym_db.RegisterMessage(RunTaskRequest.AgentExecutable)
_sym_db.RegisterMessage(RunTaskRequest.AgentExecutable.AgentSource)
_sym_db.RegisterMessage(RunTaskRequest.AgentExecutable.SourceEntry)

RunTaskResponse = _reflection.GeneratedProtocolMessageType('RunTaskResponse', (_message.Message,), {
  'DESCRIPTOR' : _RUNTASKRESPONSE,
  '__module__' : 'go.chromium.org.luci.buildbucket.proto.backend_pb2'
  # @@protoc_insertion_point(class_scope:buildbucket.v2.RunTaskResponse)
  })
_sym_db.RegisterMessage(RunTaskResponse)

FetchTasksRequest = _reflection.GeneratedProtocolMessageType('FetchTasksRequest', (_message.Message,), {
  'DESCRIPTOR' : _FETCHTASKSREQUEST,
  '__module__' : 'go.chromium.org.luci.buildbucket.proto.backend_pb2'
  # @@protoc_insertion_point(class_scope:buildbucket.v2.FetchTasksRequest)
  })
_sym_db.RegisterMessage(FetchTasksRequest)

FetchTasksResponse = _reflection.GeneratedProtocolMessageType('FetchTasksResponse', (_message.Message,), {
  'DESCRIPTOR' : _FETCHTASKSRESPONSE,
  '__module__' : 'go.chromium.org.luci.buildbucket.proto.backend_pb2'
  # @@protoc_insertion_point(class_scope:buildbucket.v2.FetchTasksResponse)
  })
_sym_db.RegisterMessage(FetchTasksResponse)

CancelTasksRequest = _reflection.GeneratedProtocolMessageType('CancelTasksRequest', (_message.Message,), {
  'DESCRIPTOR' : _CANCELTASKSREQUEST,
  '__module__' : 'go.chromium.org.luci.buildbucket.proto.backend_pb2'
  # @@protoc_insertion_point(class_scope:buildbucket.v2.CancelTasksRequest)
  })
_sym_db.RegisterMessage(CancelTasksRequest)

CancelTasksResponse = _reflection.GeneratedProtocolMessageType('CancelTasksResponse', (_message.Message,), {
  'DESCRIPTOR' : _CANCELTASKSRESPONSE,
  '__module__' : 'go.chromium.org.luci.buildbucket.proto.backend_pb2'
  # @@protoc_insertion_point(class_scope:buildbucket.v2.CancelTasksResponse)
  })
_sym_db.RegisterMessage(CancelTasksResponse)

ValidateConfigsRequest = _reflection.GeneratedProtocolMessageType('ValidateConfigsRequest', (_message.Message,), {

  'ConfigContext' : _reflection.GeneratedProtocolMessageType('ConfigContext', (_message.Message,), {
    'DESCRIPTOR' : _VALIDATECONFIGSREQUEST_CONFIGCONTEXT,
    '__module__' : 'go.chromium.org.luci.buildbucket.proto.backend_pb2'
    # @@protoc_insertion_point(class_scope:buildbucket.v2.ValidateConfigsRequest.ConfigContext)
    })
  ,
  'DESCRIPTOR' : _VALIDATECONFIGSREQUEST,
  '__module__' : 'go.chromium.org.luci.buildbucket.proto.backend_pb2'
  # @@protoc_insertion_point(class_scope:buildbucket.v2.ValidateConfigsRequest)
  })
_sym_db.RegisterMessage(ValidateConfigsRequest)
_sym_db.RegisterMessage(ValidateConfigsRequest.ConfigContext)

ValidateConfigsResponse = _reflection.GeneratedProtocolMessageType('ValidateConfigsResponse', (_message.Message,), {

  'ErrorDetail' : _reflection.GeneratedProtocolMessageType('ErrorDetail', (_message.Message,), {
    'DESCRIPTOR' : _VALIDATECONFIGSRESPONSE_ERRORDETAIL,
    '__module__' : 'go.chromium.org.luci.buildbucket.proto.backend_pb2'
    # @@protoc_insertion_point(class_scope:buildbucket.v2.ValidateConfigsResponse.ErrorDetail)
    })
  ,
  'DESCRIPTOR' : _VALIDATECONFIGSRESPONSE,
  '__module__' : 'go.chromium.org.luci.buildbucket.proto.backend_pb2'
  # @@protoc_insertion_point(class_scope:buildbucket.v2.ValidateConfigsResponse)
  })
_sym_db.RegisterMessage(ValidateConfigsResponse)
_sym_db.RegisterMessage(ValidateConfigsResponse.ErrorDetail)


DESCRIPTOR._options = None
_RUNTASKREQUEST_AGENTEXECUTABLE_SOURCEENTRY._options = None

_TASKBACKEND = _descriptor.ServiceDescriptor(
  name='TaskBackend',
  full_name='buildbucket.v2.TaskBackend',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1849,
  serialized_end=2219,
  methods=[
  _descriptor.MethodDescriptor(
    name='RunTask',
    full_name='buildbucket.v2.TaskBackend.RunTask',
    index=0,
    containing_service=None,
    input_type=_RUNTASKREQUEST,
    output_type=_RUNTASKRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='FetchTasks',
    full_name='buildbucket.v2.TaskBackend.FetchTasks',
    index=1,
    containing_service=None,
    input_type=_FETCHTASKSREQUEST,
    output_type=_FETCHTASKSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CancelTasks',
    full_name='buildbucket.v2.TaskBackend.CancelTasks',
    index=2,
    containing_service=None,
    input_type=_CANCELTASKSREQUEST,
    output_type=_CANCELTASKSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ValidateConfigs',
    full_name='buildbucket.v2.TaskBackend.ValidateConfigs',
    index=3,
    containing_service=None,
    input_type=_VALIDATECONFIGSREQUEST,
    output_type=_VALIDATECONFIGSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TASKBACKEND)

DESCRIPTOR.services_by_name['TaskBackend'] = _TASKBACKEND

# @@protoc_insertion_point(module_scope)
