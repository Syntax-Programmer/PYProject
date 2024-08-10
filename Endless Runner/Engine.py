import pygame
import pygame.locals
from sys import exit
from typing import List, Tuple, Any
from random import choice, choices

pygame.init()


class Logic:
    def __init__(self) -> None:
        self.PLAYER_MAX_Y = 300
        self.PLAYER_MIN_Y = 500
        self.FALL_SPEED = 10
        self.OBSTACLE1 = pygame.Rect(1500, 500, 125, 75)
        self.OBSTACLE2 = pygame.Rect(1500, 475, 75, 100)
        self.OBSTACLE3 = pygame.Rect(1500, 500, 50, 75)
        self.MAX_OBSTACLE_X = -100
        self.OBSTACLE_SPACER = 1100
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.obstacle_speed = 10

    def PlayerMovement(
        self, player_rect: Any, jump_initiated: bool, fall_initiated: bool
    ) -> Tuple[Any, bool, bool]:
        """Handles the player movement i.e: Jumping."""
        if jump_initiated:
            # player[1] is the y_pos of the player.
            if player[1] == self.PLAYER_MAX_Y:
                fall_initiated = True
            if not fall_initiated:
                player[1] -= self.FALL_SPEED
            else:
                if player[1] == self.PLAYER_MIN_Y:
                    jump_initiated, fall_initiated = False, False
                else:
                    player[1] += self.FALL_SPEED
        return player_rect, jump_initiated, fall_initiated

    def ObstacleSpawner(self, obstacles_on_screen: List[Any]) -> List[Any]:
        """Spawns obstacles on the screen."""
        if choices([0, 1], weights=(0.97, 0.03), k=1)[0]:
            if (
                len(obstacles_on_screen) == 0
                or obstacles_on_screen[-1][0] <= self.OBSTACLE_SPACER
            ):
                obstacles_on_screen.append(
                    choice([self.OBSTACLE1, self.OBSTACLE2, self.OBSTACLE3]).copy()
                )
        return obstacles_on_screen

    def ObstacleMovement(self, obstacles_on_screen: List[Any]) -> List[Any]:
        """Moves the obstacles in each frame."""
        for obstacle_rect in obstacles_on_screen[:]:
            if obstacle_rect[0] <= self.MAX_OBSTACLE_X:
                obstacles_on_screen.remove(obstacle_rect)
            else:
                rect_index = obstacles_on_screen.index(obstacle_rect)
                obstacles_on_screen[rect_index][0] -= self.obstacle_speed
        return obstacles_on_screen

    def ScreenUpdater(
        self, screen: Any, player_rect: Any, obstacles_on_screen: List[Any]
    ) -> bool:
        """Updates the screen and checks for game overs."""
        game_over = False
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, self.GREEN, player_rect)
        for obstacle_rect in obstacles_on_screen[:]:
            pygame.draw.rect(screen, self.RED, obstacle_rect)
            if pygame.Rect.colliderect(player_rect, obstacle_rect):
                game_over = True
        return game_over


class Main(Logic):
    def __init__(self) -> None:
        super().__init__()

    def PlayingGame(
        self,
        screen: Any,
        player_rect: Any,
        jump_initiated: bool,
        fall_initiated: bool,
        obstacles_on_screen: List[Any],
    ) -> Tuple[Any, bool, bool, List[Any], bool]:
        """Handles all the stuff needed when the game is being played."""
        player_rect, jump_initiated, fall_initiated = self.PlayerMovement(
            player_rect=player_rect,
            jump_initiated=jump_initiated,
            fall_initiated=fall_initiated,
        )
        obstacles_on_screen = self.ObstacleSpawner(
            obstacles_on_screen=obstacles_on_screen
        )
        obstacles_on_screen = self.ObstacleMovement(
            obstacles_on_screen=obstacles_on_screen
        )
        game_over = self.ScreenUpdater(
            screen=screen,
            player_rect=player_rect,
            obstacles_on_screen=obstacles_on_screen,
        )
        return (
            player_rect,
            jump_initiated,
            fall_initiated,
            obstacles_on_screen,
            game_over,
        )


def MouseClickToGridPos(mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
    """Used to if the user has clicked a play/ quit/ any other btn."""
    GRID_SCALE = 50
    return (
        mouse_pos[0] - mouse_pos[0] % GRID_SCALE,
        mouse_pos[1] - mouse_pos[1] % GRID_SCALE,
    )


def NotPlayingLogic(mouse_grid_pos: Tuple[int, int]) -> bool:
    """Checks if the user has clicked play btn or quit btn."""
    game_started = False
    if mouse_grid_pos in [
        (x_pos, y_pos) for x_pos in [800, 850, 900] for y_pos in [350, 400, 450]
    ]:
        pygame.quit()
        exit()
    if mouse_grid_pos in [
        (x_pos, y_pos) for x_pos in [500, 550, 600] for y_pos in [350, 400, 450]
    ]:
        game_started = True
    return game_started


WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner")


title_img = pygame.transform.scale(
    pygame.image.load("Assets\\TitleScreen.png"), (1500, 800)
)
title_img_location = (0, 0)
title_play = pygame.transform.scale(
    pygame.image.load("Assets\\PlayBtn.png"), (150, 150)
)
title_play_location = (500, 350)
title_quit = pygame.transform.scale(
    pygame.image.load("Assets\\QuitBtn.png"), (150, 150)
)
title_quit_location = (800, 350)
lost_img = pygame.transform.scale(
    pygame.image.load("Assets\\LostScreen.png"), (700, 800)
)
lost_img_location = (400, 0)
lost_txt = pygame.transform.scale(pygame.image.load("Assets\\LostTxt.png"), (700, 300))
lost_txt_location = (400, 0)

timer = pygame.time.Clock()
FPS = 60


player = pygame.Rect(50, 500, 75, 75)
jump_initiated = fall_initiated = game_started = game_over = False
obstacles_on_screen = []
main = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_started:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_grid_pos = MouseClickToGridPos(mouse_pos=pygame.mouse.get_pos())
                game_started = NotPlayingLogic(mouse_grid_pos=mouse_grid_pos)
        if event.type == pygame.KEYDOWN and game_started and not game_over:
            # The and not _initiated condition is added to prevent abuse.
            if event.key in [pygame.K_SPACE, pygame.K_UP] and not jump_initiated:
                jump_initiated = True
        if game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_grid_pos = MouseClickToGridPos(mouse_pos=pygame.mouse.get_pos())
                game_started = NotPlayingLogic(mouse_grid_pos=mouse_grid_pos)
                if game_started:
                    player = pygame.Rect(50, 500, 75, 75)
                    jump_initiated = fall_initiated = game_over = False
                    game_started = True
                    obstacles_on_screen = []
    if not game_started:
        screen.blits(
            [
                (title_img, title_img_location),
                (title_play, title_play_location),
                (title_quit, title_quit_location),
            ]
        )
    if game_started and not game_over:
        player, jump_initiated, fall_initiated, obstacles_on_screen, game_over = (
            main.PlayingGame(
                screen=screen,
                player_rect=player,
                jump_initiated=jump_initiated,
                fall_initiated=fall_initiated,
                obstacles_on_screen=obstacles_on_screen,
            )
        )
    if game_over:
        screen.blits(
            [
                (lost_img, lost_img_location),
                (lost_txt, lost_txt_location),
                (title_play, title_play_location),
                (title_quit, title_quit_location),
            ]
        )
    pygame.display.update()
    timer.tick(FPS)
