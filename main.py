import pygame
# from player.generate_player import player_spaceship
from general.setup import GameScreen


def main():
    pygame.init()
    game_screen = GameScreen()
    game_screen.render_screen()
    
if __name__ == "__main__":
    main()