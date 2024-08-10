"""
This is a Flappy Bird clone. 

__author__ = "Anand Maurya"
__author_github__ = "Syntax-Programmer"
__email__ = "anand6308anand@gmail.com"
"""

__author__ = "Anand Maurya"
__author_github__ = "Syntax-Programmer"
__email__ = "anand6308anand@gmail.com"


import pygame
import random

from sys import exit
from os import listdir
from os.path import join
from typing import List, Literal


pygame.init()


SCREEN_SIZE = 576, 768
window = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Flappy Bird")

assets_dir = join( "assets")
common_dir_objects = join(assets_dir, "game_objects")
common_dir_sounds = join(assets_dir, "sound_effects")
common_dir_ui = join(assets_dir, "ui")

bg_image_path = join(common_dir_objects, "bg_image.png")
bg_image = pygame.image.load(bg_image_path).convert()
bg_image = pygame.transform.scale(bg_image, SCREEN_SIZE)

bg_base_path = join(common_dir_objects, "bg_base.png")
bg_base = pygame.image.load(bg_base_path).convert()
bg_base = pygame.transform.scale(bg_base, (SCREEN_SIZE[0], 100))



def sprites_maker() -> List[pygame.Surface]:
    """
    This makes the sprite sheet for the bird.

    Returns:
    -------
        List[pygame.Surface]: The list of decoded sprite_sheets of the bird.
    """
    bird_image_name = [
        names for names in listdir(common_dir_objects) if names[:4] == "bird"
    ]
    return [
        pygame.image.load(join(common_dir_objects, names)).convert_alpha()
        for names in bird_image_name
    ]


class Bird(pygame.sprite.Sprite):
    """
    This handles the methods of the bird like jumping, falling and animation etc.

    Attributes:
    ----------
        GRAVITY (float): The acceleration due to gravity of the bird.
        ANIMATION_DELAY (int): The frame delay in switching the sprite.
        time_falling (int): The time spent by the bird falling.
        y_vel (int): The speed in the y-direction of the bird.
        animation_count (int): The number of frames passed in 1 cycle before reset.
        sprites (List[pygame.Surface]): The sprite_sheet of the bird.
    """

    GRAVITY = 0.2
    ANIMATION_DELAY = 8
    time_falling = 0
    y_vel = 0
    animation_count = 0

    def __init__(self, sprite_sheet: List[pygame.Surface]) -> None:
        """
        This initializes the Bird object.

        Args:
        ----
            sprite_sheet (List[pygame.Surface]): The sprite sheet of the bird.
        """
        pygame.sprite.Sprite.__init__(self)
        self.sprites = sprite_sheet
        self.image = self.sprites[0]
        self.mask = pygame.mask.from_surface(self.image)
        bird_pos, bird_size = (100, 100), self.image.get_size()
        self.rect = pygame.Rect(bird_pos, bird_size)

    def jump(self) -> None:
        """This sets conditions for the bird to jump."""
        self.y_vel = -self.GRAVITY * 25
        self.time_falling = 0

    def apply_gravity(self, fps: int) -> None:
        """
        This applies gravity to the bird.

        Args:
        ----
            fps (int): The max fps count of the game.
        """
        # The 1000 means the number of milliseconds in seconds.
        self.time_falling += fps / 1000
        # Using the formula:  v = u + at
        self.y_vel += self.GRAVITY * self.time_falling

    def animator(self) -> None:
        """This decides what sprite to be shown on the screen."""
        # Just to avoid dealing with numbers in billions or trillions.
        if self.animation_count // self.ANIMATION_DELAY > len(self.sprites):
            self.animation_count = 0
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(
            self.sprites
        )
        self.image = self.sprites[sprite_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count += 1

    def move(self) -> None:
        """This moves the bird according to its y_vel."""
        # The velocity is the same as the distance moved because v is ds/dt and as v is changing each frame
        # the equation becomes v = dx/1 = dx
        self.rect.move_ip(0, self.y_vel)

    def draw(self, window: pygame.Surface) -> None:
        """
        This draws the bird on the screen.

        Args:
        ----
            window (pygame.display): The display surface of the game.
        """
        window.blit(self.image, self.rect.topleft)


class Pipes(pygame.sprite.Sprite):
    """
    This handles a single pipe on the screen.

    Attributes:
    ----------
        PIPE_INITIAL_X (int): The initial x pos of every pipe.
        PIPE_MAX_Y (int): This is the max y-pos any pipe can go to
        X_VEL (int): The movement speed of the pipe.
    """

    PIPE_INITIAL_X = 800
    # bg_base_coords for the base of pipes.
    PIPE_MAX_Y = SCREEN_SIZE[1] - bg_base.get_height()
    X_VEL = -6

    def __init__(
        self, direction: Literal["up", "down"], pipe_opening_y_pos: int
    ) -> None:
        """
        This initializes a Pipe object.

        Args:
        ----
            direction (Literal["up", "down"]): The direction the pipe is facing.
            pipe_opening_y_pos (int): The pos of the opening of the pipe.
        """
        pygame.sprite.Sprite.__init__(self)
        y_pos = pipe_opening_y_pos if direction == "up" else 0
        self.image = pygame.image.load(
            join(common_dir_objects, "pipe.png")
        ).convert_alpha()
        self.image = (
            self.image
            if direction == "up"
            else pygame.transform.flip(self.image, False, True)
        )
        scaling_size = (
            (self.image.get_width(), self.PIPE_MAX_Y - y_pos)
            if direction == "up"
            else (self.image.get_width(), pipe_opening_y_pos - y_pos)
        )
        self.image = pygame.transform.scale(self.image, scaling_size)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect((self.PIPE_INITIAL_X, y_pos), self.image.get_size())

    def move(self) -> None:
        """This moves the pipe towards the bird."""
        self.rect.move_ip(self.X_VEL, 0)


def bird_handler(bird: Bird, fps: int, pipe_group: pygame.sprite.Group) -> bool:
    """
    This handles the bird of the game.]

    Args:
    ----
        bird (Bird): A bird object whom to handle.
        fps (int): The max fps cap of the game.
        pipe_group (pygame.sprite.Group): The group containing all the pipe objects.

    Returns:
    -------
        bool: True if game NOT over, False otherwise.
    """
    bird.animator()
    bird.apply_gravity(fps=fps)
    bird.move()
    return not (
        any(pygame.sprite.collide_mask(bird, pipe) for pipe in pipe_group)
        or bird.rect.y > SCREEN_SIZE[1] - bg_base.get_height()
        or bird.rect.y < 0
    )


def spawn_pipe(pipe_group: pygame.sprite.Group) -> None:
    """
    This spawns the pipes on the screen.

    Args:
    ----
        pipe_group (pygame.sprite.Group): The group containing all the pipe objects.
    """
    separating_factor = 150
    max_height = SCREEN_SIZE[1] - bg_base.get_height()
    up_y_pos = random.randrange(max_height - 300, max_height, 75)
    down_y_pos = up_y_pos - separating_factor
    pipe_group.add(Pipes("up", up_y_pos))
    pipe_group.add(Pipes("down", down_y_pos))


def pipes_handler(pipe_group: pygame.sprite.Sprite) -> None:
    """
    This handles everything related to pipes.

    Args:
    ----
        pipe_group (pygame.sprite.Group): The group containing all the pipe objects.
    """
    for pipe in pipe_group:
        pipe.move()
        if pipe.rect.x < -100:
            pipe_group.remove(pipe)


def draw(window: pygame.Surface, bird: Bird, pipe_group: pygame.sprite.Group) -> None:
    """
    This draws everything that needs to be on the screen.

    Args:
    ----
        window (pygame.display): The display surface of the game.
        bird (Bird): A bird object whom to handle.
        pipe_group (pygame.sprite.Group): The group containing all the pipe objects.
    """
    window.blit(bg_image, (0, 0))
    window.blit(bg_base, (0, SCREEN_SIZE[1] - bg_base.get_height()))
    bird.draw(window=window)
    pipe_group.draw(window)
    pygame.display.update()


def main(window: pygame.Surface) -> None:
    """
    This is the main function of the game.

    Args:
    ----
        window (pygame.display): The display surface of the game.
    """
    timer = pygame.time.Clock()
    fps = 60

    bird = Bird(sprite_sheet=sprites_maker())
    pipes = pygame.sprite.Group()

    running = True
    i = 0
    while running:
        timer.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()
        if not i % 240:
            spawn_pipe(pipe_group=pipes)
        running = bird_handler(bird=bird, fps=fps, pipe_group=pipes)
        pipes_handler(pipe_group=pipes)
        draw(window=window, bird=bird, pipe_group=pipes)
        i += 1

    pygame.quit()
    exit()


if __name__ == "__main__":
    main(window=window)
