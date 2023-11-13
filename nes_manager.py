import socket
import asyncio
from delimiter import Delimiter
from messages_pb2 import (Ping, Response, Request, CreateEmulator, Renderer,
                          FrameContents, GetFrame, TakeAction, ControllerInput)
from google.protobuf.message import Message
from typing import Optional


# noinspection PyUnresolvedReferences
class Nes:
    emulator_id: int
    manager: object

    # Memory Requests gets details like marios position.
    # Key is anything (look at response).
    async def get_frame(self, memory_requests: Optional[dict[str, int]] = None) -> FrameContents:
        if memory_requests is None:
            memory_requests = {}

        await self.manager.send_packet(Request(get_frame=GetFrame(
            emulator_id=self.emulator_id,
            memory_requests=memory_requests
        )))

        response = await self.manager.wait_for_response()

        assert response.frame_details.emulator_id == self.emulator_id

        return response.frame_details.frame

    async def take_action(self, controller: ControllerInput, skip_frames: int,
                          memory_requests: Optional[dict[str, int]] = None) -> Optional[FrameContents]:
        if memory_requests is None:
            memory_requests = {}

        await self.manager.send_packet(Request(take_action=TakeAction(
            emulator_id=self.emulator_id,
            skip_frames=skip_frames,
            input=controller,
            memory_requests=memory_requests
        )))

        response = await self.manager.wait_for_response()

        assert response.action_result.emulator_id == self.emulator_id

        if response.action_result.error.message != '':
            print("Action Error: " + response.action_result.error.message)

            return None

        return response.action_result.frame

    def __init__(self, manager: object, emulator_id: int):
        self.emulator_id = emulator_id
        self.manager = manager


class NesManager:
    sock: socket.socket
    delimiter: Delimiter

    async def send_packet(self, message: Message):
        loop = asyncio.get_event_loop()

        content = message.SerializeToString()

        size_bytes = len(content).to_bytes(8, 'big')

        print(size_bytes, len(content))

        await loop.sock_sendall(self.sock, size_bytes)
        await loop.sock_sendall(self.sock, content)

    async def wait_for_raw_packet(self) -> bytearray:
        packet = self.delimiter.pop()

        while packet is None:
            response = self.sock.recv(1024)

            if len(response) == 0:
                raise Exception("Connection closed by server.")

            print(f"Got bytes {len(response)} back from server.")

            self.delimiter.push(response)

            packet = self.delimiter.pop()

        return packet

    async def wait_for_response(self) -> Response:
        packet = await self.wait_for_raw_packet()

        response = Response()
        response.ParseFromString(packet)

        return response

    async def create_emulator(self, renderer: Renderer = Renderer.RENDERER_SOFTWARE) -> Nes:
        await self.send_packet(Request(create_emulator=CreateEmulator(
            renderer=renderer
        )))

        response = await self.wait_for_response()

        emulator_id = response.emulator_details.emulator_id

        return Nes(self, emulator_id)

    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.delimiter = Delimiter()


async def create_nes_manager(address: (str, int)) -> NesManager:
    loop = asyncio.get_event_loop()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Created socket!")

    client.connect(address)

    manager = NesManager(client)

    await manager.send_packet(Request(ping=Ping(content="NesManager Client")))
    response = await manager.wait_for_response()

    print(response)

    print(response.pong.content)

    if response.pong.content != "NesManager Client":
        print("Failed to connect: Server response was not EmServer.")

        raise Exception("Server response was not valid.")

    return manager
