import asyncio
import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_x, K_z, K_l, K_RETURN

from messages_pb2 import ControllerInput
from nes import create_stream_nes


async def run_client():
    # Manager will probably leak the socket here.
    nes = await create_stream_nes(("127.0.0.1", 9013))

    pygame.init()

    display = pygame.display.set_mode((256 * 2, 240 * 2))

    stream_id = 3
    pygame.display.set_caption(f"EmServer Stream {stream_id}")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        frame = await nes.get_frame(stream_id)

        image = pygame.image.frombuffer(frame.frame, (256, 240), 'RGBA')
        image = pygame.transform.scale(image, (256 * 2, 240 * 2))
        display.blit(image, (0, 0))

        pygame.display.update()


if __name__ == '__main__':
    asyncio.run(run_client())
