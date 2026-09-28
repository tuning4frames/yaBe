import pygame

LANES = 4
KEYS = (
    (pygame.K_d, pygame.K_1, pygame.K_KP1, pygame.K_LEFT),
    (pygame.K_f, pygame.K_2, pygame.K_KP2, pygame.K_DOWN),
    (pygame.K_j, pygame.K_3, pygame.K_KP3, pygame.K_UP),
    (pygame.K_k, pygame.K_4, pygame.K_KP4, pygame.K_RIGHT),
)
LABELS = ("D", "F", "J", "K")

def key_to_lane(key):
    for i, ks in enumerate(KEYS):
        if key in ks:
            return i
    return None
