import pygame
import os
import random
import copy
# from characters import normal_bullet_data

from general.setup import WIN

import random

def pick_random_image(images):
    return random.choice(images)

class Object(pygame.sprite.Sprite):
    def __init__(self, object_features: object = None):
        super().__init__()
           
        self.obj = copy.deepcopy(object_features)
        self.window = WIN
        self.freeze_action = False
        self.bound_x = 0
        self.bound_y = self.window.get_height()
        self.mask = None
        self.image_changed = False
        self.source = None
        self.image = None
        self.width = 0
        self.height = 0
        self.rotate = 0
        self.hitbox_color = (0, 0, 0)
        self.rect = None
        
        # if the image is provide directly
        if self.image:
            self.image = pygame.image.load(os.path.join(
                self.source, 
                (pick_random_image(self.image) if len(self.image) > 1 else self.image[0])
            )).convert_alpha() 
            
            self.image = pygame.transform.rotate(
                pygame.transform.scale(
                    self.image, 
                    (self.width, self.height)
                ), 
                self.rotate
            )
            
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
        
        
        # if the data is provided by dict
        if self.obj:
            self.name = self.obj.get("name", None)
            self.height = self.obj.get("height", 0)
            self.width = self.obj.get("width", 0)
            self.pos_x = self.obj.get("pos_x", 0)
            self.pos_y = self.obj.get("pos_y", 0)
            self.image = pygame.image.load(os.path.join(
                self.obj.get("source"), 
                (pick_random_image(self.obj.get("image")) if len(self.obj.get("image")) > 1 else self.obj.get("image")[0])
            )).convert_alpha() if self.obj.get("image") else ""
            self.rotate = self.obj.get("rotate", 0)
            self.hitbox = [(self.pos_x, self.pos_y), (self.width, self.height)]
            self.reset_image = False
            self.rect = None
            
            if self.image != "":
                self.image = pygame.transform.rotate(
                    pygame.transform.scale(
                        self.image, 
                        (self.width, self.height)
                    ), 
                    self.rotate
                )
                
                self.rect = self.image.get_rect()
                self.mask = pygame.mask.from_surface(self.image)
            
    def update_positions(self):
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
            
    def show_mask(self):
        return self.window.blit(
            self.mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)), 
            (self.rect.x, self.rect.y)
        )
        
    def object_mask(self):
        return pygame.mask.from_surface(self.image)
    
    def object_mask_outline(self):
        self.outline = [(_[0] + self.rect.x, _[1] + self.rect.y) for _ in self.mask.outline(every=1)]
        
        return pygame.draw.lines(self.window, (255, 0, 0), False, self.outline, 3)
    
    def hitbox(self):
        hitbox = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        return pygame.draw.rect(
            self.window, 
            self.hitbox_color,
            hitbox,
            2
        )
    
    def rect_object(self):
        return pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
    
    def handle_image(self):
        if self.image_changed:
            
            if self.image:
                self.image = pygame.image.load(os.path.join(
                self.source, 
                (pick_random_image(self.image) if len(self.image) > 1 else self.image[0])
            )).convert_alpha() 
            
            self.image = pygame.transform.rotate(
                pygame.transform.scale(
                    self.image, 
                    (self.width, self.height)
                ), 
                self.rotate
            )
            
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
                
            self.image_changed = False
    
    def rendering_object(self):
        # self.object_mask_outline()
        if str(type(self.image)) != "list":
            self.window.blit(self.image, (self.pos_x, self.pos_y))
        
    
class ImmobileObject(Object):
    # height, width , position, image, 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 

class MovingObject(Object):  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.vel = self.obj.get("velocity", None)
        self.keys = self.obj.get("control_keys", None)
        self.boundary = self.obj.get("boundary", None)
        
                  
            
                    
            
   