import socket
import asyncio
from delimiter import Delimiter
from messages_pb2 import (Ping, Response, Request, FrameContents, GetFrame,
                          GetState, SetState, TakeAction, ControllerInput)
from google.protobuf.message import Message
from typing import Optional


# noinspection PyUnresolvedReferences
class Nes:
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

    async def wait_for_response(self) -> Response:
        packet = await self.wait_for_raw_packet()

        response = Response()
        response.ParseFromString(packet)

        return response

    async def get_state(self) -> bytes:
        await self.send_packet(Request(get_state=GetState()))
        response = await self.wait_for_response()

        return response.state_details.state

    async def set_state(self, data: bytes):
        await self.send_packet(Request(set_state=SetState(state=data)))
        response = await self.wait_for_response()

        if response.set_state_result.parse_error != '':
            raise Exception(f'Failed to set stated with error {response.set_state_result.parse_error}')

    # Memory Requests gets details like marios position.
    # Key is anything (look at response).
    async def get_frame(self, memory_requests: Optional[dict[str, int]] = None) -> FrameContents:
        if memory_requests is None:
            memory_requests = {}

        await self.send_packet(Request(get_frame=GetFrame(
            memory_requests=memory_requests
        )))

        response = await self.wait_for_response()

        return response.frame_details.frame

    async def take_action(self, controller: ControllerInput, skip_frames: int,
                          memory_requests: Optional[dict[str, int]] = None) -> FrameContents:
        if memory_requests is None:
            memory_requests = {}

        await self.send_packet(Request(take_action=TakeAction(
            skip_frames=skip_frames,
            input=controller,
            memory_requests=memory_requests
        )))

        response = await self.wait_for_response()

        if response.action_result.error.message != '':
            raise Exception(f"Error occurred during action: {response.action_result.error.message}")

        return response.action_result.frame

    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.delimiter = Delimiter()


async def create_nes(address: (str, int)) -> Nes:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(address)

    nes = Nes(client)

    await nes.send_packet(Request(ping=Ping(content="NesManager Client")))
    response = await nes.wait_for_response()

    if response.pong.content != "NesManager Client":
        raise Exception("Server response was not valid.")

    return nes
