from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Renderer(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RENDERER_SOFTWARE: _ClassVar[Renderer]
    RENDERER_HARDWARE: _ClassVar[Renderer]
RENDERER_SOFTWARE: Renderer
RENDERER_HARDWARE: Renderer

class Ping(_message.Message):
    __slots__ = ("content",)
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: str
    def __init__(self, content: _Optional[str] = ...) -> None: ...

class Pong(_message.Message):
    __slots__ = ("server", "content")
    SERVER_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    server: str
    content: str
    def __init__(self, server: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class GetFrame(_message.Message):
    __slots__ = ("memory_requests",)
    class MemoryRequestsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    MEMORY_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    memory_requests: _containers.ScalarMap[str, int]
    def __init__(self, memory_requests: _Optional[_Mapping[str, int]] = ...) -> None: ...

class FrameContents(_message.Message):
    __slots__ = ("frame", "memory_values")
    class MemoryValuesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    FRAME_FIELD_NUMBER: _ClassVar[int]
    MEMORY_VALUES_FIELD_NUMBER: _ClassVar[int]
    frame: bytes
    memory_values: _containers.ScalarMap[str, int]
    def __init__(self, frame: _Optional[bytes] = ..., memory_values: _Optional[_Mapping[str, int]] = ...) -> None: ...

class FrameDetails(_message.Message):
    __slots__ = ("frame",)
    FRAME_FIELD_NUMBER: _ClassVar[int]
    frame: FrameContents
    def __init__(self, frame: _Optional[_Union[FrameContents, _Mapping]] = ...) -> None: ...

class ControllerInput(_message.Message):
    __slots__ = ("a", "b", "select", "start", "up", "down", "left", "right")
    A_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    SELECT_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    UP_FIELD_NUMBER: _ClassVar[int]
    DOWN_FIELD_NUMBER: _ClassVar[int]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    a: bool
    b: bool
    select: bool
    start: bool
    up: bool
    down: bool
    left: bool
    right: bool
    def __init__(self, a: bool = ..., b: bool = ..., select: bool = ..., start: bool = ..., up: bool = ..., down: bool = ..., left: bool = ..., right: bool = ...) -> None: ...

class TakeAction(_message.Message):
    __slots__ = ("skip_frames", "input", "memory_requests")
    class MemoryRequestsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    SKIP_FRAMES_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    skip_frames: int
    input: ControllerInput
    memory_requests: _containers.ScalarMap[str, int]
    def __init__(self, skip_frames: _Optional[int] = ..., input: _Optional[_Union[ControllerInput, _Mapping]] = ..., memory_requests: _Optional[_Mapping[str, int]] = ...) -> None: ...

class ActionError(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class ActionResult(_message.Message):
    __slots__ = ("frame", "error")
    FRAME_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    frame: FrameContents
    error: ActionError
    def __init__(self, frame: _Optional[_Union[FrameContents, _Mapping]] = ..., error: _Optional[_Union[ActionError, _Mapping]] = ...) -> None: ...

class GetState(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StateDetails(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: bytes
    def __init__(self, state: _Optional[bytes] = ...) -> None: ...

class SetState(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: bytes
    def __init__(self, state: _Optional[bytes] = ...) -> None: ...

class SetStateResult(_message.Message):
    __slots__ = ("parse_error",)
    PARSE_ERROR_FIELD_NUMBER: _ClassVar[int]
    parse_error: str
    def __init__(self, parse_error: _Optional[str] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ("ping", "get_frame", "take_action", "get_state", "set_state")
    PING_FIELD_NUMBER: _ClassVar[int]
    GET_FRAME_FIELD_NUMBER: _ClassVar[int]
    TAKE_ACTION_FIELD_NUMBER: _ClassVar[int]
    GET_STATE_FIELD_NUMBER: _ClassVar[int]
    SET_STATE_FIELD_NUMBER: _ClassVar[int]
    ping: Ping
    get_frame: GetFrame
    take_action: TakeAction
    get_state: GetState
    set_state: SetState
    def __init__(self, ping: _Optional[_Union[Ping, _Mapping]] = ..., get_frame: _Optional[_Union[GetFrame, _Mapping]] = ..., take_action: _Optional[_Union[TakeAction, _Mapping]] = ..., get_state: _Optional[_Union[GetState, _Mapping]] = ..., set_state: _Optional[_Union[SetState, _Mapping]] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("pong", "frame_details", "action_result", "state_details", "set_state_result")
    PONG_FIELD_NUMBER: _ClassVar[int]
    FRAME_DETAILS_FIELD_NUMBER: _ClassVar[int]
    ACTION_RESULT_FIELD_NUMBER: _ClassVar[int]
    STATE_DETAILS_FIELD_NUMBER: _ClassVar[int]
    SET_STATE_RESULT_FIELD_NUMBER: _ClassVar[int]
    pong: Pong
    frame_details: FrameDetails
    action_result: ActionResult
    state_details: StateDetails
    set_state_result: SetStateResult
    def __init__(self, pong: _Optional[_Union[Pong, _Mapping]] = ..., frame_details: _Optional[_Union[FrameDetails, _Mapping]] = ..., action_result: _Optional[_Union[ActionResult, _Mapping]] = ..., state_details: _Optional[_Union[StateDetails, _Mapping]] = ..., set_state_result: _Optional[_Union[SetStateResult, _Mapping]] = ...) -> None: ...
