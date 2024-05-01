from abc import ABCMeta, abstractmethod
from typing import Callable

import pygame
from pygame import surfarray, Surface, SurfaceType
from pygame.locals import KEYDOWN, K_BACKSPACE, QUIT, HWSURFACE, DOUBLEBUF
from numpy import ndarray


class SimulationWrapper(metaclass=ABCMeta):
    @abstractmethod
    def update_screen(
        self, screen: Surface | SurfaceType, screen_size: tuple[int, int]
    ):
        pass


UpdateSimulationCallable = Callable[[], None]
RGBTransformCallable = Callable[[], ndarray]


class SimulationNdArrayWrapper(SimulationWrapper):
    current_configuration: ndarray
    update_simulation_callback: UpdateSimulationCallable
    get_rgba_array_callback: RGBTransformCallable

    def __init__(
        self,
        update_simulation_callback: UpdateSimulationCallable,
        get_rgba_array_callback: RGBTransformCallable,
    ):
        self.update_simulation_callback = update_simulation_callback
        self.get_rgba_array_callback = get_rgba_array_callback

    def update_screen(
        self, screen: Surface | SurfaceType, screen_size: tuple[int, int]
    ):
        self.update_simulation_callback()
        simulation_data = self.get_rgba_array_callback()
        surface = pygame.Surface(simulation_data.shape[0:2])
        surfarray.blit_array(surface, simulation_data)
        surface = pygame.transform.scale(surface, screen_size)
        screen.blit(surface, (0, 0))


def pygame_loop(
    simulation_wrapper: SimulationWrapper,
    fps: float = 30,
    size: tuple[int, int] = (1600, 800),
):
    pygame.init()
    screen = pygame.display.set_mode(size, HWSURFACE | DOUBLEBUF)
    clock = pygame.time.Clock()
    while True:
        pygame.display.update()
        simulation_wrapper.update_screen(screen, size)
        clock.tick(fps)
        pygame.display.set_caption(f"Simulation View | fps: {clock.get_fps():.3}")
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    pygame.quit()
                    raise InterruptedError
            elif event.type == QUIT:
                pygame.quit()
                raise InterruptedError
