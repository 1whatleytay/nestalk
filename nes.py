import socket
import asyncio
from delimiter import Delimiter
from messages_pb2 import (Ping, InitializeRequest, EmulatorRequest, StreamRequest, GetStream, InitializeType, FrameContents, GetFrame,
                          ActionResult, GetState, SetState, TakeAction, ControllerInput, Pong, StreamDetails)
from google.protobuf.message import Message
from typing import Optional, TypeVar

T = TypeVar("T")


class ConnectionBase:
    sock: socket.socket
    delimiter: Delimiter

    async def send_packet(self, message: Message):
        loop = asyncio.get_event_loop()

        content = message.SerializeToString()

        size_bytes = len(content).to_bytes(8, 'big')

        await loop.sock_sendall(self.sock, size_bytes)
        await loop.sock_sendall(self.sock, content)

    async def wait_for_raw_packet(self) -> bytes:
        packet = self.delimiter.pop()

        while packet is None:
            response = self.sock.recv(1024)

            if len(response) == 0:
                raise Exception("Connection closed by server.")

            self.delimiter.push(response)

            packet = self.delimiter.pop()

        return packet

    async def wait_for_response(self, response: T) -> T:
        packet = await self.wait_for_raw_packet()

        response.ParseFromString(packet)

        return response

    def __init__(self, sock: socket.socket, delimiter: Delimiter):
        self.sock = sock
        self.delimiter = delimiter


# noinspection PyUnresolvedReferences
class Nes(ConnectionBase):
    stream_id: int

    async def get_state(self) -> bytes:
        await self.send_packet(EmulatorRequest(get_state=GetState()))
        response = await self.wait_for_response(StateDetails())

        return response.state

    async def set_state(self, data: bytes):
        await self.send_packet(EmulatorRequest(set_state=SetState(state=data)))
        response = await self.wait_for_response(SetStateResult())

        if response.parse_error != '':
            raise Exception(f'Failed to set stated with error {response.set_state_result.parse_error}')

    # Memory Requests gets details like marios position.
    # Key is anything (look at response).
    async def get_frame(self, memory_requests: Optional[dict[str, int]] = None) -> FrameContents:
        if memory_requests is None:
            memory_requests = {}

        await self.send_packet(EmulatorRequest(get_frame=GetFrame(
            memory_requests=memory_requests
        )))

        response = await self.wait_for_response(FrameDetails())

        return response.frame

    async def take_action(self, controller: ControllerInput, skip_frames: int,
                          memory_requests: Optional[dict[str, int]] = None) -> FrameContents:
        if memory_requests is None:
            memory_requests = {}

        await self.send_packet(EmulatorRequest(take_action=TakeAction(
            skip_frames=skip_frames,
            input=controller,
            memory_requests=memory_requests,
            stream_id=self.stream_id
        )))

        response = await self.wait_for_response(ActionResult())

        if response.error.message != '':
            raise Exception(f"Error occurred during action: {response.action_result.error.message}")

        return response.frame

    def __init__(self, sock: socket.socket, stream_id: Optional[int]):
        super(Nes, self).__init__(sock, Delimiter())

        self.stream_id = stream_id


class StreamNes(ConnectionBase):
    async def get_frame(self, stream_id: int) -> StreamDetails:
        await self.send_packet(StreamRequest(
            get_stream=GetStream(stream_id=stream_id)
        ))

        response = await self.wait_for_response(StreamDetails())

        return response

    def __init__(self, sock: socket.socket):
        super(StreamNes, self).__init__(sock, Delimiter())


async def check_pong(client: ConnectionBase):
    await client.send_packet(InitializeRequest(ping=Ping(content="NesManager Client")))
    response = await client.wait_for_response(Pong())

    if response.content != "NesManager Client":
        raise Exception("Server response was not valid.")


async def create_nes(address: tuple[str, int], stream_id: Optional[int] = None) -> Nes:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(address)

    nes = Nes(client, stream_id)

    await check_pong(nes)
    await nes.send_packet(InitializeRequest(initialize=InitializeType.CREATE_EMULATOR))

    return nes


async def create_stream_nes(address: tuple[str, int]) -> StreamNes:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(address)

    nes = StreamNes(client)

    await check_pong(nes)
    await nes.send_packet(InitializeRequest(initialize=InitializeType.OPEN_STREAM))

    return nes
