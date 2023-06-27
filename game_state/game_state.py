from objects import pygame, os, random, MovingObject, Object
from general.screen_object import WIN, WIDTH, HEIGHT, all_elements
import copy
from themes.mouse_cursor.mouse_object import MouseObject
from themes.mouse_cursor.mouse_data import mouse_data
from helper.__function_tracker import run_once

from themes.button.button_object import Button as _Button

from themes.container.screen_object import Container
from collections import defaultdict, deque


class GameStateObject(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # set-ups
        self.set_testing = False
        
        # game layers
        self.first_layer = pygame.sprite.Group()
        self.second_layer = pygame.sprite.Group()
        
        # container maps
        self.children = pygame.sprite.Group()
        
        self.clicked = False
        self.prev_hovered_element = None
        self.hovered_element = None
        self.on_hover_d = 1
        self.expect_on_click = deque([])
        
        self.element_mouse_pos: tuple = (0, 0)
        
    def main_game_state(self):
        pass    
    
    def create_testing_container(self):
        if not self.set_testing:
            container = Container(
                name = "testing_container",
                width = self.window.get_width(),
                height = self.window.get_height(),
                pos_x = 0,
                pos_y = 0,
                outline = 0,
                display="normal",
                flex_direction="column",
                display_border=True,
                background_color = "blue",
                surface = self.window
            )
            
            container.added = True
            
            self.children.add(container)
            self.hovered_element = container
            self.hovered_element.focus = True
            
            self.set_testing = True
            
            
    def get_hovered_element(self):
        return self.hovered_element
    
    def set_hovered_element(self, value):
        # first line to change prev element back to non-focused status
        # if self.prev_hovered_element:
        #     print(self.prev_hovered_element.name, value.name)
        
        if self.prev_hovered_element and self.prev_hovered_element.name != value.name:
            self.prev_hovered_element.focus = False
            value.focus = True
            
            # set all children's controlable variable of the focused element 
            # for child in self.hovered_element.children.sprites():
            #     child.controlable = True
            
        self.prev_hovered_element = self.hovered_element
        self.hovered_element = value
        
    def get_container(self, container_name):
        for child in self.children.sprites():
            if child.name == container_name:
                return child
            
    def on_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for element in all_elements:
            if (element.container_surface_rect.collidepoint(mouse_pos) and 
                element.added and
                element.type == "container"):
                
                self.set_hovered_element(element)
                break
            
        if self.hovered_element:
            if self.hovered_element.name != "testing_container":
                # calculate d_x, d_y of WIN and mouse pos
                # calculate d_x, d_y of hovered element
                # calculate relative mouse pos in the hovered element
                
                WIN_mouse_dx = mouse_pos[0] - self.window.get_rect().x
                WIN_mouse_dy = mouse_pos[1] - self.window.get_rect().y
                
                WIN_hovered_dx = self.hovered_element.container_surface_rect.x - self.window.get_rect().x
                WIN_hovered_dy = self.hovered_element.container_surface_rect.y - self.window.get_rect().y 
                
                dx, dy = WIN_mouse_dx - WIN_hovered_dx, WIN_mouse_dy - WIN_hovered_dy
                
                self.element_mouse_pos = list(self.element_mouse_pos)
                self.element_mouse_pos[0] = dx
                self.element_mouse_pos[1] = dy
                self.element_mouse_pos = tuple(self.element_mouse_pos)
                
                
            elif self.hovered_element.name == "testing_container":
                self.element_mouse_pos = mouse_pos
            
            # print(self.element_mouse_pos)
            
    def on_click(self):
        left_click = pygame.mouse.get_pressed(3)[0]
        # mouse_pos = pygame.mouse.get_pos()
        clicked_target = self.hovered_element
        
        if left_click and not self.clicked:
            self.clicked = True
            
            for child in self.hovered_element.children:
                # print(child.name, child.added)
                if (child.container_surface_rect and 
                    child.container_surface_rect.collidepoint(self.element_mouse_pos) and
                    child.added):
                    # print(mouse_pos, element.container_surface_rect, element.surface_rect)
                    clicked_target = child
                    break
                
            clicked_target.on_click()
            print(clicked_target.name)
            
        elif not left_click:
            self.clicked = False
            
            
    def update(self):      
        # self.first_layer.update()
        
        # if self.get_container("testing_container"):
        #     print(self.get_container("testing_container").children)
        
        # for element in all_elements:
        #     print(element.name, element.focus)
        # print("----------------------------------")
        
        self.on_hover()
        self.on_click()
        self.children.update()
        self.second_layer.update()        

        
        

        
                    
        