import pygame
from collections import defaultdict
from typing import Literal, AnyStr, TypeVar
from general.setup import WIN, all_elements

_POSITION = Literal["manual", "auto"]
_DISPLAY = Literal["normal", "flex"]
_FLEX_DIRECTION = Literal["row", "column"]
_HORIZONTAL_ALIGN = Literal["center", "left", "right"]
_VERTICAL_ALIGN = Literal["center", "top", "bottom"]
_OVERFLOW = Literal["visible", "hidden", "scroll"]
_WIDTH = TypeVar("_WIDTH", str, int)
_HEIGHT = TypeVar("_HEIGHT", str, int)

class Theme(pygame.sprite.Sprite):
    def __init__(
        self, 
        *args, 
        name: str = "",
        pos_x: int = 0, 
        pos_y: int = 0,
        width: _WIDTH = 0,
        height: _HEIGHT = 0, 
        display_border: bool = False,
        position: _POSITION = "auto",
        clickable: bool = False,
        dragable: bool = False,
        controlable: bool = False,
        
        outline: int = 0,
        border_color: tuple = (0, 0, 0, 255),
        display: _DISPLAY = "normal",
        flex_direction: _FLEX_DIRECTION = "row",
        horizontal_align: _HORIZONTAL_ALIGN = "center",
        vertical_align: _VERTICAL_ALIGN = "center",
        
        overflow: _OVERFLOW = "visible",
        overflow_x: bool = False,
        overflow_y: bool = False,
        
        border_radius: int = -1,
        border_radius_top_left: int = -1,
        border_radius_top_right: int = -1,
        border_radius_bottom_left: int = -1,
        border_radius_bottom_right: int = -1,
        
        padding: int = 0,
        padding_left: int = 0,
        padding_right: int = 0,
        padding_top: int = 0,
        padding_down: int = 0,
        
        margin: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        margin_down: int = 0,
        
        **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.name = name
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.position = position
        self.display_border = display_border
        
        # relationships
        self.parent = None
        self.children = pygame.sprite.Group()
        
        # help finding a certain child more convenient
        self.children_map = defaultdict(object)
        
        self.rect = None
        self.set_rect = False
        
        # control settings
        self.clicked = False
        self.clickable = clickable
        
        self.dragged = False
        self.dragable = dragable
        
        self.controlable = controlable
        
        self.functions: list = []
        
        self._reorganized = False
        
        # attributes
        self.border_radius = border_radius
        self.border_radius_top_left = border_radius_top_left
        self.border_radius_top_right = border_radius_top_right
        self.border_radius_bottom_left = border_radius_bottom_left
        self.border_radius_bottom_right = border_radius_bottom_right
        
        self.display = display
        self.flex_direction = flex_direction
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align
        
        # component surface
        self.main_surface = WIN 
        self.surface = WIN
        self.surface_rect = self.surface.get_rect()
        
        self.width = self.surface.get_width() * (99/100) if self.width == "auto" or self.width == "fit" else self.width
        
        self.container_surface = pygame.surface.Surface((self.width, self.height)).convert_alpha()
        self.container_surface_rect = self.container_surface.get_rect()
        
        self.or_pos_x = 0
        self.or_pos_y = 0
        
        self.inner_pos_x = 0
        self.inner_pos_y = 0
        
        self.container_surface_rect.x = self.pos_x
        self.container_surface_rect.y = self.pos_y
        
        self.set_overlaped_rect = False
        self.overlaped_rect = None
        
        self.outline = outline
        self.border_color = border_color
        
        self.overflow = overflow
        self.overflow_x = overflow_x
        self.overflow_y = overflow_y
        
        self.padding = padding
        self.padding_left = padding_left
        self.padding_right = padding_right
        self.padding_top = padding_top
        self.padding_down = padding_down
        
        self.margin = margin
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_top = margin_top
        self.margin_down = margin_down
        
        if self.overflow == "scroll":
            self.overflow_x = True
            self.overflow_y = True
            
        self.focus = False
        self.added = False
        
        
        
        all_elements.appendleft(self)
        
    @property
    def reorganized(self):
        return self._reorganized
    
    @reorganized.setter
    def reorganized(self, value):
        self._reorganized = value
    
    def set_hitbox(self):
        # if not self.set_rect:
        self.rect = pygame.Rect(
            self.container_surface_rect.x, 
            self.container_surface_rect.y, 
            self.width, 
            self.height
        )
            # self.set_rect = True
        
        if self.display_border: 
            pygame.draw.rect(
                self.surface,
                pygame.Color(200, 143, 58, 255),
                self.rect,
                2
            )
            
    def create_overlaped_rect(self):
        if not self.set_overlaped_rect:
            print(self.name)
            
            surface_points = [
                (self.surface_rect.x, self.surface_rect.y),
                (self.surface_rect.x, self.surface_rect.y + self.surface_rect.height),
                (self.surface_rect.x + self.surface_rect.width, self.surface_rect.y),
                (self.surface_rect.x + self.surface_rect.width, self.surface_rect.y + self.surface_rect.height)
            ]
            
            container_surface_points = [
                (self.container_surface_rect.x, self.container_surface_rect.y),
                (self.container_surface_rect.x, self.container_surface_rect.y + self.height),
                (self.container_surface_rect.x + self.width, self.container_surface_rect.y),
                (self.container_surface_rect.x + self.width, self.container_surface_rect.y + self.height)
            ]
            
            print(surface_points)
            print(container_surface_points)
            
            surface_point = None
            container_surface_point = None
                
            if self.surface.get_rect().contains(self.container_surface_rect):
                self.overlaped_rect = self.container_surface_rect
                
            elif self.surface.get_rect().colliderect(self.container_surface_rect):
                for point in container_surface_points:
                    if self.surface.get_rect().collidepoint(point):
                        surface_point = point
                        break
                        
                for point in surface_points:
                    if self.container_surface_rect.collidepoint(point):
                        container_surface_point = point
                        break
                
                print("collided points")
                print(surface_point, container_surface_point)
                             
                center = (
                    abs(surface_point[0] - container_surface_point[0]) / 2, 
                    abs(surface_point[-1] - container_surface_point[-1]) / 2
                )
                
                self.overlaped_rect = pygame.Rect(
                    center[0] - abs(surface_point[0] - container_surface_point[0]) / 2,
                    center[-1] - abs(surface_point[0] - container_surface_point[0]) / 2,
                    abs(surface_point[0] - container_surface_point[0]),
                    abs(surface_point[-1] - container_surface_point[-1])
                )
                
            else:
                self.overlaped_rect = pygame.Rect(0, 0, 0, 0)
                
            # print(self.name)
            # print(self.overlaped_rect)
            print("-----------------------------------------------")
                    
            self.set_overlaped_rect = True
                                 
    def on_click(self):
        left_click = pygame.mouse.get_pressed(3)[0]
        mouse_pos = pygame.mouse.get_pos()
         
        if (left_click and 
            self.container_surface_rect.collidepoint(mouse_pos) and 
            self.clickable,
            not self.clicked):
            
            self.clicked = True
        
            for function in self.functions:
                func = function[0]
                args = function[1]
                
                func(**args)
            
        elif not left_click:
            self.clicked = False
                        
    def drag_drop(self):
        # get mouse pos
        # get mouse click, if mouse pos in the object => trigger drag_drop()
        # calculate distance between object.x, object.y and mouse.x, mouse.y
        # move the targeted object while mouse pressed
        
        if self.dragable:
            mouse_pos = pygame.mouse.get_pos()
            mouse_rel = pygame.mouse.get_rel()
            left_click = pygame.mouse.get_pressed(3)[0]
            
            if left_click and self.rect.collidepoint(mouse_pos):
                self.pos_x += mouse_rel[0]
                self.pos_y += mouse_rel[1]
            
    def move_object(self):
        if self.controlable:
            key_pressed = pygame.key.get_pressed()
            
            if key_pressed[pygame.K_w]:
                self.container_surface_rect.y -= 1
                
            elif key_pressed[pygame.K_s]:
                self.container_surface_rect.y += 1
                
            elif key_pressed[pygame.K_a]:
                self.container_surface_rect.x -= 1
                
            elif key_pressed[pygame.K_d]:
                self.container_surface_rect.x += 1
                
    def move_inner_container(self):
        if self.controlable and self.focus:
            key_pressed = pygame.key.get_pressed()
                
            if key_pressed[pygame.K_w]:
                self.inner_pos_y += 0
                
                if self.children.sprites()[0].container_surface_rect.y < 2 + self.padding_top:
                    for child in self.children:
                        child.container_surface_rect.y += 5
                
            elif key_pressed[pygame.K_s]:
                self.inner_pos_y -= 0
                
                # get the heighest child
                last_child = self.children.sprites()[-1]
                
                if last_child.container_surface_rect.y + last_child.container_surface_rect.height > self.container_surface_rect.height - 1:
                    for child in self.children:
                        child.container_surface_rect.y -= 5
                
            elif key_pressed[pygame.K_a]:
                self.inner_pos_x += 0
                
                if self.children.sprites()[0].container_surface_rect.x < 2:
                    for child in self.children:
                        child.container_surface_rect.x += 10
           
            elif key_pressed[pygame.K_d]:
                self.inner_pos_x -= 0
                
                last_child = self.children.sprites()[-1]
                
                if last_child.container_surface_rect.x + last_child.container_surface_rect.width > self.container_surface_rect.width - 1:
                    for child in self.children:
                        child.container_surface_rect.x -= 10
            
     # objects: containers, buttons, text, text box, image
    def add_child(self, object):
        self.children.add(object)
        self.reorganized = False
        
        object.added = True
        object.parent = self
        
        # modify display surface 
        object.surface = self.container_surface
        object.surface_rect = object.surface.get_rect()
        
        # create a children's mapping => easy to find object
        self.children_map[object.name] = object
        
       
    def render(self):
        return
        
    def get_child(self, child_name):
        return self.children_map[child_name]
               
    def update_position(self):
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
    
    def update(self):
        # self.create_overlaped_rect()
        
        self.render()
        # if self.clickable:
        #     self.on_click()
            
        # if self.dragable:
        #     self.drag_drop()
            
        # self.move_object()
        self.move_inner_container()
        self.children.update()
        self.set_hitbox()