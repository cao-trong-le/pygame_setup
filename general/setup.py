import pygame
import time
import copy
from collections import deque
from helper.__function_tracker import run_once

# from main import player_group, bullet_group, enemy_group, bonus_group

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Silly Game")


upper_bar = pygame.Rect(0, 0, WIDTH, 50)
game_window = pygame.Rect(0, 50, WIDTH, 600)
lower_bar = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)


# divide the main window into 2 sections
# samples and main
sample_section = pygame.Surface((200, 500))
sample_section.fill((200, 123, 12))

design_section = pygame.Surface((500, 500))
design_section.fill((230, 123, 12))


# create a screen selection section

all_elements = deque([])

class GameScreen:
    # game setting
    def __init__(self):
        self.fps = 60
        self.volume = 0
        self.volume_on = True
        self.pause = False
        self.quit = False
        
        self.startover = False
        self.pressed_key = pygame.key.get_pressed
        
     
        # objects 
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.elapsed_time = 0
        
        # screen option
        
        self.screens = {
            "menu": False, 
            "gameover": False,
            "play": False,
            "maps": False,
            "settings": False,
            "exit": False,
            "design": False,
            "testing": True,
        }
        
        self.set_gameState = False
        self.gamestate = None
        
        self.set_testing_area = False
     
   
    # create a flag to prevent multiple runs
    def set_gamestate(self):
        from game_state.game_state import GameStateObject
        
        if not self.set_gameState:
            self.gamestate = GameStateObject()
            self.set_gameState = True
        
    def update_gamestate(self):
        if self.gamestate:
            self.gamestate.update()
        
    def game_background(self):
        WIN.fill((255, 255, 255))
    
    def gameover_screen(self):
        return
    
    def switcher(self, screen_name):
        for key in self.screens.keys():
            if self.screens[key]:
                self.screens[key] = False
            break
            
        self.screens[screen_name] = True
            
    def start_menu_screen(self):
        return
            
   
    def quit_game(self):
        if ((self.pressed_key()[pygame.K_LALT] or self.pressed_key()[pygame.K_RALT]) and 
            self.pressed_key()[pygame.K_F4]):
            self.quit = True
            
        # elif self.pressed_key[pygame.K_p]:
        #     self.quit = True
            
    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
                
         
    def set_current_time(self):
        self.elapsed_time = int(time.time() - self.start_time) 
        
    def create_testing_area(self):
        if self.gamestate and not self.set_testing_area:
            from themes.container.screen_object import Container
            from themes.button.button_object import Button
            from themes.text.text_object import Text
            from random import randint
            
            self.set_testing_area = True
            
            self.gamestate.create_testing_container()
            
            # get testing container
            test_container = self.gamestate.get_container("testing_container")
            # test_container.dislay
                
            def change_random_color(box):
                box.background_color = (randint(0, 252), randint(0, 252), randint(0, 252))
            
            # element => event listener
            blue_box = Container(
                surface=WIN, 
                name="blue_box",
                width=400,
                height=400,
                pos_x=100,
                pos_y=100,
                clickable=True,
                # position="manual",
                display="flex",
                flex_direction="column",
                display_border=True,
                controlable=True,
                background_color="lightblue",
                padding_left=10,
                padding_top=20
            )
            
            # blue_box.reorganized = False
            
            gray_box = Container(
                surface=WIN, 
                name="gray_box",
                width=100,
                height=100,
                pos_x=-50,
                pos_y=WIN.get_height() - 50,
                clickable=True,
                position="manual",
                display_border=True,
                background_color="gray",
            )
            
            pink_box = Container(
                surface=WIN, 
                name="pink_box",
                width=100,
                height=100,
                pos_x=WIN.get_width() - 50,
                pos_y=WIN.get_height() - 50,
                clickable=True,
                position="manual",
                display_border=True,
                background_color="pink",
            )
            
            orange_box = Container(
                surface=WIN, 
                name="orange_box",
                width=100,
                height=100,
                pos_x=WIN.get_width() - 50,
                pos_y=-50,
                clickable=True,
                position="manual",
                display_border=True,
                background_color="orange",
            )
            
            # add a listener
            blue_box.functions.append((change_random_color, {"box": blue_box}))

            
            # create a test button
            test_button = Button(
                name="test_button",
                text="Test",
                size=20,
                horizontal_align="center",
                vertical_align="center",
                button_type="text",
                color=(252, 252, 252),
                background=(123, 0, 0),
                clickable=True,
                controlable=True,
                width=100,
                height=200,
                pos_x=0,
                pos_y=0,
                display_border=True,
                outline=0,
                # position="manual",
                padding_top=5,
                padding_left=2,
            )
            
            test_button_2 = Button(
                name="test_button_2",
                button_type="image",
                color=(252, 252, 252),
                background=(123, 0, 0),
                clickable=True,
                width=100,
                height=50,
                pos_x=0,
                pos_y=0,
                source="themes/button/images/play_button.png",
                outline=0
            )
            
            # test_button_2 func
            def say_hello_world():
                print("hello world")
            
            test_button_2.functions.append((say_hello_world, {}))
            
            test_text = Text(
                name="test_text",
                text="In an actual interview situation, you want to deliver your prepared answer in a polished but natural way. Consider using one of the following lead-ins as the inspiration for crafting your tailored response:",
                size=15,
                width=300,
                height=300,
                pos_x=0,
                pos_y=0,
                padding_top=20,
                padding_left=5,
                padding_right=5,
                space=5
            )
            
            test_text_2 = Text(
                name="test_text",
                text="In an actual interview situation, you want to deliver your prepared answer in a polished but natural way. Consider using one of the following lead-ins as the inspiration for crafting your tailored response:",
                size=15,
                width=100,
                height=50,
                pos_x=0,
                pos_y=0,
                space=10
            )
            
            test_text_1 = Text(
                name="test_text",
                text="We are good!",
                size=15,
                width=100,
                height=50,
                pos_x=300,
                pos_y=0
            )
                      
            if test_container:
                test_container.add_child(blue_box)
                test_container.add_child(gray_box)
                test_container.add_child(pink_box)
                test_container.add_child(orange_box)
                
                # test_container.add_child(test_text)
                # test_container.add_child(test_text_1)
                # test_container.add_child(box_2)
                # test_container.add_child(test_button)
                # test_container.get_child("blue_box").add_child()
                
            blue_box.add_child(test_text_2)
            blue_box.add_child(test_button)
            blue_box.add_child(test_button_2)
            blue_box.add_child(test_text)
            # blue_box.add_child(test_button_2)
            
            # self.gamestate.container_maps["testing"].children.add(blue_box)
            
            
    def render_screen(self):
        while not self.quit:
            self.clock.tick(self.fps)
       
            self.event_handler()
            # self.set_current_time()
            
            # print(self.elapsed_time)
            
            if self.screens["menu"]:
                self.start_menu_screen()
            
            elif self.screens["gameover"]:
                self.gameover_screen()
                
            elif self.screens["testing"]:
                # self.game_background()
                self.create_testing_area()
            
            elif self.screens["play"]:
                self.game_background()
                
            self.set_gamestate()
            self.update_gamestate()

            pygame.display.update()
                
        pygame.quit()

        

        