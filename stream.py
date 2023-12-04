import asyncio
import pygame
from pygame import Surface, Rect

from messages_pb2 import ControllerInput
from nes import create_stream_nes


def draw_alpha_rect(display: Surface, position: tuple[int, int], size: tuple[int, int], color: tuple, alpha: int):
    surface = Surface(size)

    surface.set_alpha(alpha)
    surface.fill(color)

    display.blit(surface, position)


def draw_controller(display: Surface, value: ControllerInput):
    pressed_opacity = 255
    unpressed_opacity = 100

    a_opacity = pressed_opacity if value.a else unpressed_opacity
    b_opacity = pressed_opacity if value.b else unpressed_opacity
    up_opacity = pressed_opacity if value.up else unpressed_opacity
    down_opacity = pressed_opacity if value.down else unpressed_opacity
    left_opacity = pressed_opacity if value.left else unpressed_opacity
    right_opacity = pressed_opacity if value.right else unpressed_opacity

    dir_pressed = value.down or value.up or value.left or value.right
    dir_opacity = pressed_opacity if dir_pressed else unpressed_opacity

    left, top = 60, 80
    width, height = 20, 20
    buttons_left = left + 120
    buttons_pad = 10
    size = (width, height)
    color = (21, 21, 71)

    draw_alpha_rect(display, (left + width, top), size, color, up_opacity)
    draw_alpha_rect(display, (left + width, top + 2 * height), size, color, down_opacity)
    draw_alpha_rect(display, (left, top + height), size, color, left_opacity)
    draw_alpha_rect(display, (left + 2 * width, top + height), size, color, right_opacity)
    draw_alpha_rect(display, (left + width, top + height), size, color, dir_opacity)

    draw_alpha_rect(display, (buttons_left, top + height), size, color, a_opacity)
    draw_alpha_rect(display, (buttons_left + width + buttons_pad, top + height), size, color, b_opacity)


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

        # Comment out to remove controller view:
        draw_controller(display, frame.input)

        # Limit FPS. Don't lock the AI all the time!
        await asyncio.sleep(1 / 15)

        pygame.display.update()


if __name__ == '__main__':
    asyncio.run(run_client())
