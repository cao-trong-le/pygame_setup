import pygame
from themes.theme_object import Theme
from collections import defaultdict
from typing import Literal
from general.setup import all_elements



class Container(Theme):
    def __init__(self, 
            *args,
            surface,
            background_color = (0, 0, 0), 
            src = None,
            image = None,
            background = None, 
            outline = 0, 
            **kwargs
        ):
        
        super().__init__(*args, **kwargs)
        
        self.type = "container"
        self.background = background
        self.background_color = background_color
        self.outline: bool = outline
        self.src = src
        self.image = image
        
        self.set_scrollbar = False
       
        self.surface = surface
        
        # self.children = pygame.sprite.Group()
        
        self.top_layer = pygame.sprite.Group()
        
    
    def render(self):
        self.surface.blit(
            self.container_surface, 
            self.container_surface_rect
        )
        
        self.container_surface.fill(self.background_color)
        
        pygame.draw.rect(
            self.container_surface,
            self.background_color,
            pygame.Rect(
                self.padding_left, 
                self.padding_top, 
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
            
    
    def show_scrollbar(self):
        # create 2 boxes: one for x-bar, y-bar
        if self.overflow == "scroll" and not self.set_scrollbar:
            if self.overflow_x:
                x_bar = Container(
                    name="x_bar",
                    background_color="gray",
                    width=50,
                    height=100,
                    pos_x=self.pos_x - (self.width - 50),
                    pos_y=self.pos_y,
                    surface=self.surface
                )
                
                self.top_layer.add(x_bar)
            
            if self.overflow_y:
                y_bar = Container(
                    name="x_bar",
                    background_color="gray",
                    width=100,
                    height=50,
                    pos_x=self.pos_x,
                    pos_y=self.pos_y - (self.height - 100),
                    surface=self.surface
                )
                
                
                self.top_layer.add(y_bar)
            
            self.set_scrollbar = True
        
    # unfinished
    def reorganize_children(self):
        if not self.reorganized and self.position == "auto":
            self.reorganized = True
              
            children = self.children.sprites()
            
            # print(self.rect.x, self.rect.y, self.flex_direction, self.children)
            
            if self.display == "flex" and self.flex_direction == "column":
                current_height = 0
                
                for i in range(len(children)):
                    children[i].container_surface_rect.x = self.padding_left
                    
                    if i == 0:
                        children[i].container_surface_rect.y = self.padding_top
                        
                    elif i > 0:
                        current_height += (children[i - 1].container_surface_rect.height + children[i - 1].padding_top)
                        children[i].container_surface_rect.y += (current_height + self.margin_top + self.padding_top)
                        
                # self.container_surface_rect.height = max(self.container_surface_rect.height, current_height)
                        
                   
            elif self.display == "flex" and self.flex_direction == "row":
                current_width = 0
                
                for i in range(len(children)):
                    children[i].container_surface_rect.y = self.padding_top
                    
                    if i == 0:
                        children[i].container_surface_rect.x = self.padding_left
                        
                    elif i > 0:
                        current_width += (children[i - 1].container_surface_rect.width + children[i - 1].padding_left)
                        children[i].container_surface_rect.x += (current_width + self.margin_left)
                     
                    print("----------------------")
                    print(f"Reorganize {children[i].name}")
                    print(children[i].container_surface_rect)
                    
                current_width += children[-1].container_surface_rect.width
                
                print(current_width)
                    
                # self.container_surface_rect.width = max(self.container_surface_rect.width, current_width)
    
                   
    def update(self):
        super().update()
        # self.render()
        self.reorganize_children()
        # # self.render()
        
    
        
        
        