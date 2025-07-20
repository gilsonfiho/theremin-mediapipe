import pygame
import math

class FractalVisualizer:
    def __init__(self, width=800, height=600):
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height

    def draw(self, param):
        self.screen.fill((0, 0, 0))
        for x in range(0, self.width, 5):
            for y in range(0, self.height, 5):
                zx = 1.5 * (x - self.width / 2) / 200
                zy = 1.0 * (y - self.height / 2) / 200
                z = c = complex(zx, zy)
                i = 0
                while abs(z) < 4 and i < 30:
                    z = z * z + complex(math.sin(param), math.cos(param))
                    i += 1
                color = (i * 8 % 255, i * 5 % 255, i * 3 % 255)
                self.screen.set_at((x, y), color)
        pygame.display.update()
