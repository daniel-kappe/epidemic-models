#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Callable

import pygame
from numpy import ndarray, stack
from pygame import Surface, SurfaceType, surfarray
from pygame.locals import DOUBLEBUF, HWSURFACE, K_BACKSPACE, KEYDOWN, QUIT

UpdateSimulationCallable = Callable[[], None]
RGBTransformCallable = Callable[[], ndarray]


class SimulationNdArrayWrapper(ABC):
    @abstractmethod
    def simulation_step(self):
        pass

    @abstractmethod
    def data_for_visualization(self) -> list[ndarray]:
        pass

    def data_to_rgba(self) -> ndarray:
        return stack(self.data_for_visualization(), axis=-1)

    def update_screen(
        self, screen: Surface | SurfaceType, screen_size: tuple[int, int]
    ):
        self.simulation_step()
        simulation_data = self.data_to_rgba()
        surface = pygame.Surface(simulation_data.shape[0:2])
        surfarray.blit_array(surface, simulation_data)
        surface = pygame.transform.scale(surface, screen_size)
        screen.blit(surface, (0, 0))


def pygame_loop(
    simulation_wrapper: SimulationNdArrayWrapper,
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
