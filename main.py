import asyncio
import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_x, K_z, K_l, K_RETURN

from messages_pb2 import ControllerInput
from nes import create_nes


async def run_client():
    # Manager will probably leak the socket here.
    nes = await create_nes(("127.0.0.1", 9013), 1)

    pygame.init()

    display = pygame.display.set_mode((256 * 2, 240 * 2))

    pygame.display.set_caption("EmServer Server")

    state = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    state = await nes.get_state()

                if event.key == pygame.K_o and state is not None:
                    await nes.set_state(state)

            if event.type == pygame.QUIT:
                running = False

        pressed = pygame.key.get_pressed()

        controller = ControllerInput()
        controller.a = pressed[K_x]
        controller.b = pressed[K_z]
        controller.select = pressed[K_RETURN]
        controller.start = pressed[K_l]
        controller.up = pressed[K_UP]
        controller.down = pressed[K_DOWN]
        controller.left = pressed[K_LEFT]
        controller.right = pressed[K_RIGHT]

        memory_requests = {"mario_x": 0x86, "page": 0x6d, "coins": 0x075e,
                           "digits_1": 0x07d8, "digits_2": 0x07d9, "digits_3": 0x07da,
                           "digits_4": 0x07db, "digits_5": 0x07dc, "digits_6": 0x07dd}

        frame = await nes.take_action(controller, 1,
                                      memory_requests=memory_requests)

        image = pygame.image.frombuffer(frame.frame, (256, 240), 'RGBA')
        image = pygame.transform.scale(image, (256 * 2, 240 * 2))
        display.blit(image, (0, 0))

        pygame.display.update()


if __name__ == '__main__':
    asyncio.run(run_client())
