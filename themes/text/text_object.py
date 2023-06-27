from themes.theme_object import Theme
from typing import Any, AnyStr, TypeVar
import pygame 

_COLOR = TypeVar("_COLOR", tuple, str, int)

class Text(Theme):
    def __init__(
        self,
        *args,
        text: str = "",
        size: int = 10,
        font: str = "freesansbold.ttf",
        color: _COLOR = (0, 0, 0),
        bg_color: _COLOR = pygame.SRCALPHA,
        space: int = 0,
        **kwargs
    ):
        
        super().__init__(*args, **kwargs)
        
        self.type = "text"
        self.text = text
        self.size = size
        self.font = pygame.font.Font(font, self.size)
        self.color = color
        self.bg_color = bg_color
        self.space = space
        
        self.text_img = self.font.render("", True, "white")
        self.text_img_width, self.text_img_height = self.text_img.get_size()

        self.set_text = False
        self.lines = []
        self.max_length = 0
        
        print(self.parent)
    
        self.container_surface = pygame.surface.Surface((self.width, self.height)).convert_alpha()
        self.container_surface_rect = self.container_surface.get_rect()
        self.container_surface_rect.x = self.pos_x
        self.container_surface_rect.y = self.pos_y
           
    def render(self):
        self.break_text_into_lines()
        self.display_text()
        self.render_border()
        
    def render_border(self):
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
        
    # def set_padding(self, value):
    
            
    #     if self.padding_top != value or self.padding_down != value:
    #         self.height += (self.padding_top + self.padding_down)
          
    def convert_line_into_image(self, line):
        return self.font.render(line, True, "white")
        
    def break_text_into_lines(self):
        if not self.set_text:
            self.text = self.text.split(" ")
                  
            line = ""
            self.lines = []
            
            # print(self.container_surface.get_width())
            # print(self.surface.get_width())
            # print(self.surface.get_width() - (self.padding_left + self.padding_right))
            if self.width == "auto" or self.width == "fit":
                line_length = self.surface.get_width() - (self.padding_left + self.padding_right)
            else:
                line_length = self.width - (self.padding_left + self.padding_right)
            
            for word in self.text:
                text_img = self.font.render(line + f" {word}", True, "white")
                          
                # print(text_img.get_width(), self.surface.get_width())
                
                if text_img.get_width() <= line_length:
                    line += f" {word}"
                else:
                    self.lines.append(self.convert_line_into_image(line))
                    line = ""
                    
                self.max_length = max(
                    self.max_length, 
                    self.font.render(line, True, "white").get_width()
                )
                                   
            if line != "":
                self.lines.append(self.convert_line_into_image(line))
                
        
            print(f"max length: {self.width}")
            
            if self.width == 0:
                self.width = self.max_length + self.padding_left + self.padding_right
            
            self.height = max((self.text_img_height + self.padding_top + self.padding_down + self.space) * len(self.lines), self.height)
            
            self.container_surface = pygame.surface.Surface((self.width, self.height)).convert_alpha()
            self.container_surface_rect = self.container_surface.get_rect()
            self.container_surface_rect.x = self.pos_x
            self.container_surface_rect.y = self.pos_y
            
            print(self.container_surface_rect)
            
            
            # self.overlaped_rect = self.container_surface_rect
            self.set_overlaped_rect = False
            self.parent.reorganized = False
            
            self.set_text = True    
                
        
    def display_text(self):
        # create text image
        # adjust container surface height to chucks
      
        self.surface.blit(
            self.container_surface, 
            self.container_surface_rect
        )
        
        self.container_surface.fill("white")
          
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
         
        for i, line in enumerate(self.lines):
            self.container_surface.blit(
                line,
                (self.padding_left, (self.text_img_height + self.space) * i + self.padding_top)
            )
        
    def update(self):
        super().update()
        self.render()