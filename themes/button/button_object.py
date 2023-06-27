import pygame
import os
from objects import Object
from themes.theme_object import Theme
from typing import Literal

_BUTTON_TYPES = Literal["text", "image"]
_HORIZONTAL_ALIGN = Literal["center", "left", "right"]
_VERTICAL_ALIGN = Literal["center", "top", "bottom"]
_POSITION = Literal["manual", "auto"]

class Button(Theme):
    def __init__(
        self, 
        *args,
        text: str = "", 
        size: int = 10, 
        font: str = "freesansbold.ttf",
        color = (0, 0, 0),
        background = (255, 255, 255),
        source = None,
        bold: bool = False,
        italic: bool = False,
        outline: int = 0,
        horizontal_align: _HORIZONTAL_ALIGN = "center",
        vertical_align: _VERTICAL_ALIGN = "center",
        border_radius: int = -1,
        border_radius_top_left: int = -1,
        border_radius_top_right: int = -1,
        border_radius_bottom_left: int = -1,
        border_radius_bottom_right: int = -1,
        button_type: _BUTTON_TYPES = "text",
        **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.type = "button"
        self.text = text
        self.size = size
        self.font = pygame.font.Font(font, self.size)
        self.color = color
        self.bg_color = background
        self.source = source
        self.bold = bold
        self.italic = italic
        self.outline = outline
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align
        self.button_type = button_type
        
        # self.surface = surface
        
        self.border_radius = border_radius
        self.border_radius_top_left = border_radius_top_left
        self.border_radius_top_right = border_radius_top_right
        self.border_radius_bottom_left = border_radius_bottom_left
        self.border_radius_bottom_right = border_radius_bottom_right
        
        if self.button_type == "image":
            self.image = pygame.image.load(os.path.join(
                os.path.abspath("."),
                self.source
            )).convert_alpha() 
            
            print(os.path.join(os.path.abspath("."), self.source))
            
            self.image = pygame.transform.scale(
                self.image,
                (self.container_surface_rect.width, self.container_surface_rect.height)
            )
            
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
    
    def render(self):
        if self.button_type == "text":
            self.display_button()
            
        elif self.button_type == "image":
            self.display_image_button()
        
    def display_button(self):
        # self.container_surface_rect.x = self.parent.inner_pos_x, 
        # self.container_surface_rect.y = self.parent.inner_pos_y, 
        
        self.surface.blit(
            self.container_surface, 
            self.container_surface_rect
        )
        
        self.container_surface.fill("white")
       
        # draw a button bg
        pygame.draw.rect(
            self.container_surface,
            self.bg_color,
            pygame.Rect(
                0,
                0,
                self.width, 
                self.height
            ),
            self.outline,
            self.border_radius,
            self.border_radius_top_left,
            self.border_radius_top_right,
            self.border_radius_bottom_left,
            self.border_radius_bottom_right
        )
        
        # draw text on the bg
        # create a sysfont
        
        text_img = self.font.render(self.text, True, self.color)
        text_width, text_height = text_img.get_size()
        
        if self.vertical_align == "center":
            text_pos_y = self.padding_top + (self.height // 2 - text_height // 2)
            
        elif self.vertical_align == "top":
            text_pos_y = self.padding_top
            
        elif self.vertical_align == "bottom":
            text_pos_y = self.padding_top + (self.height - text_height)
            
        if self.horizontal_align == "center":
            text_pos_x = self.padding_left + (self.width // 2 - text_width // 2)
            
        elif self.horizontal_align == "left":
            text_pos_x = self.padding_left
        
        elif self.horizontal_align == "right":
            text_pos_x = self.padding_left + (self.width - text_width)
               
        if 0 <= text_width <= self.width and 0 <= text_height <= self.height:
            self.container_surface.blit(
                text_img, 
                (text_pos_x, text_pos_y)
            )
            
        else:
            self.container_surface.blit(
                text_img, 
                (self.container_surface_rect.x, self.container_surface_rect.y)
            )
            
        pygame.draw.rect(
            self.surface,
            pygame.Color(0, 0, 0),
            pygame.Rect(
                self.container_surface_rect.x, 
                self.container_surface_rect.y, 
                self.container_surface_rect.width, 
                self.container_surface_rect.height
            ),
            2
        )
            
    def display_image_button(self):
        self.surface.blit(
            self.container_surface, 
            self.container_surface_rect
        )
        
        self.container_surface.fill(pygame.SRCALPHA)
        
        self.container_surface.blit(
            self.image, 
            (0, 0)
        )
        

    def on_click(self):
        left_click = pygame.mouse.get_pressed(3)[0]
        mouse_pos = pygame.mouse.get_pos()
        
        def calculate_mouse_in_surface():   
            WIN_mouse_dx = mouse_pos[0] - self.main_surface.get_rect().x
            WIN_mouse_dy = mouse_pos[1] - self.main_surface.get_rect().y
            
            WIN_hovered_dx = self.parent.container_surface_rect.x - self.main_surface.get_rect().x
            WIN_hovered_dy = self.parent.container_surface_rect.y - self.main_surface.get_rect().y 
            
            dx, dy = WIN_mouse_dx - WIN_hovered_dx, WIN_mouse_dy - WIN_hovered_dy
            
            return (dx, dy)
        
        if self.button_type == "text":
            if (left_click and 
                self.container_surface_rect.collidepoint(mouse_pos) and 
                self.clickable):
                
                self.clicked = True
            
                for function in self.functions:
                    func = function[0]
                    args = function[1]
                    
                    func(**args)
                
                
        elif self.button_type == "image":
            mouse_pos = calculate_mouse_in_surface()
            mouse_pos_in_mask = mouse_pos[0] - self.rect.x, mouse_pos[-1] - self.rect.y
            
            # self.mask.get_rect
            # print(mouse_pos_in_mask)
            # print(self.mask.get_at(mouse_pos_in_mask))
            
            if (left_click and 
                self.rect.collidepoint(mouse_pos) and 
                self.mask.get_at(mouse_pos_in_mask) and
                self.clickable):
            
                # self.clicked = True
            
                for function in self.functions:
                    func = function[0]
                    args = function[1]
                    
                    func(**args)
                
            # elif not left_click:
            #     self.clicked = False
                
        
                
    def update(self):
        super().update()
        
        
        
        


