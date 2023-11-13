import asyncio
import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_x, K_z, K_l, K_KP_ENTER

from messages_pb2 import ControllerInput
from nes_manager import create_nes_manager


async def run_client():
    # Manager will probably leak the socket here.
    manager = await create_nes_manager(("127.0.0.1", 9013))

    nes = await manager.create_emulator()

    pygame.init()

    display = pygame.display.set_mode((256 * 2, 240 * 2))

    pygame.display.set_caption("EmServer Streaming")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pressed = pygame.key.get_pressed()

        controller = ControllerInput()
        controller.a = pressed[K_x]
        controller.b = pressed[K_z]
        controller.select = pressed[K_KP_ENTER]
        controller.start = pressed[K_l]
        controller.up = pressed[K_UP]
        controller.down = pressed[K_DOWN]
        controller.left = pressed[K_LEFT]
        controller.right = pressed[K_RIGHT]

        frame = await nes.take_action(controller, 1)

        image = pygame.image.frombuffer(frame.frame, (256, 240), 'RGBA')
        display.blit(image, (0, 0))

        pygame.display.update()


if __name__ == '__main__':
    asyncio.run(run_client())
