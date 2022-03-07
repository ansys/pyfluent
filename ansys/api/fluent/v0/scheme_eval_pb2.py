# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scheme_eval.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import ansys.api.fluent.v0.scheme_pointer_pb2 as scheme__pointer__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='scheme_eval.proto',
  package='grpcRemoting',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11scheme_eval.proto\x12\x0cgrpcRemoting\x1a\x14scheme_pointer.proto\"<\n\x0b\x45xecRequest\x12\x0f\n\x07\x63ommand\x18\x01 \x03(\t\x12\x0c\n\x04wait\x18\x02 \x01(\x08\x12\x0e\n\x06silent\x18\x03 \x01(\x08\"\x1e\n\x0c\x45xecResponse\x12\x0e\n\x06output\x18\x01 \x01(\t\"\"\n\x11StringEvalRequest\x12\r\n\x05input\x18\x01 \x01(\t\"$\n\x12StringEvalResponse\x12\x0e\n\x06output\x18\x01 \x01(\t2\xde\x01\n\nSchemeEval\x12@\n\x04\x45val\x12\x1b.grpcRemoting.SchemePointer\x1a\x1b.grpcRemoting.SchemePointer\x12=\n\x04\x45xec\x12\x19.grpcRemoting.ExecRequest\x1a\x1a.grpcRemoting.ExecResponse\x12O\n\nStringEval\x12\x1f.grpcRemoting.StringEvalRequest\x1a .grpcRemoting.StringEvalResponseb\x06proto3'
  ,
  dependencies=[scheme__pointer__pb2.DESCRIPTOR,])




_EXECREQUEST = _descriptor.Descriptor(
  name='ExecRequest',
  full_name='grpcRemoting.ExecRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='command', full_name='grpcRemoting.ExecRequest.command', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='wait', full_name='grpcRemoting.ExecRequest.wait', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='silent', full_name='grpcRemoting.ExecRequest.silent', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=57,
  serialized_end=117,
)


_EXECRESPONSE = _descriptor.Descriptor(
  name='ExecResponse',
  full_name='grpcRemoting.ExecResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='output', full_name='grpcRemoting.ExecResponse.output', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=119,
  serialized_end=149,
)


_STRINGEVALREQUEST = _descriptor.Descriptor(
  name='StringEvalRequest',
  full_name='grpcRemoting.StringEvalRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='input', full_name='grpcRemoting.StringEvalRequest.input', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=151,
  serialized_end=185,
)


_STRINGEVALRESPONSE = _descriptor.Descriptor(
  name='StringEvalResponse',
  full_name='grpcRemoting.StringEvalResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='output', full_name='grpcRemoting.StringEvalResponse.output', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=187,
  serialized_end=223,
)

DESCRIPTOR.message_types_by_name['ExecRequest'] = _EXECREQUEST
DESCRIPTOR.message_types_by_name['ExecResponse'] = _EXECRESPONSE
DESCRIPTOR.message_types_by_name['StringEvalRequest'] = _STRINGEVALREQUEST
DESCRIPTOR.message_types_by_name['StringEvalResponse'] = _STRINGEVALRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ExecRequest = _reflection.GeneratedProtocolMessageType('ExecRequest', (_message.Message,), {
  'DESCRIPTOR' : _EXECREQUEST,
  '__module__' : 'scheme_eval_pb2'
  # @@protoc_insertion_point(class_scope:grpcRemoting.ExecRequest)
  })
_sym_db.RegisterMessage(ExecRequest)

ExecResponse = _reflection.GeneratedProtocolMessageType('ExecResponse', (_message.Message,), {
  'DESCRIPTOR' : _EXECRESPONSE,
  '__module__' : 'scheme_eval_pb2'
  # @@protoc_insertion_point(class_scope:grpcRemoting.ExecResponse)
  })
_sym_db.RegisterMessage(ExecResponse)

StringEvalRequest = _reflection.GeneratedProtocolMessageType('StringEvalRequest', (_message.Message,), {
  'DESCRIPTOR' : _STRINGEVALREQUEST,
  '__module__' : 'scheme_eval_pb2'
  # @@protoc_insertion_point(class_scope:grpcRemoting.StringEvalRequest)
  })
_sym_db.RegisterMessage(StringEvalRequest)

StringEvalResponse = _reflection.GeneratedProtocolMessageType('StringEvalResponse', (_message.Message,), {
  'DESCRIPTOR' : _STRINGEVALRESPONSE,
  '__module__' : 'scheme_eval_pb2'
  # @@protoc_insertion_point(class_scope:grpcRemoting.StringEvalResponse)
  })
_sym_db.RegisterMessage(StringEvalResponse)



_SCHEMEEVAL = _descriptor.ServiceDescriptor(
  name='SchemeEval',
  full_name='grpcRemoting.SchemeEval',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=226,
  serialized_end=448,
  methods=[
  _descriptor.MethodDescriptor(
    name='Eval',
    full_name='grpcRemoting.SchemeEval.Eval',
    index=0,
    containing_service=None,
    input_type=scheme__pointer__pb2._SCHEMEPOINTER,
    output_type=scheme__pointer__pb2._SCHEMEPOINTER,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Exec',
    full_name='grpcRemoting.SchemeEval.Exec',
    index=1,
    containing_service=None,
    input_type=_EXECREQUEST,
    output_type=_EXECRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='StringEval',
    full_name='grpcRemoting.SchemeEval.StringEval',
    index=2,
    containing_service=None,
    input_type=_STRINGEVALREQUEST,
    output_type=_STRINGEVALRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SCHEMEEVAL)

DESCRIPTOR.services_by_name['SchemeEval'] = _SCHEMEEVAL

# @@protoc_insertion_point(module_scope)
