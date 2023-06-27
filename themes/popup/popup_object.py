import pygame
from objects import Object
from button.button_object import Button
from chess_piece.chess_piece_data import _chess_pieces_dict

class PromoButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.board = None
        self.player = None
        self.piece = None
        self.piece_data = None
    
        self.clicked = False
    
    def button_on_click(self):
        from chess_piece.chess_piece import Queen, Rock, Knight, Bishop
        
        # print("running")
        
        left_click = pygame.mouse.get_pressed(3)[0]
        mouse_pos = pygame.mouse.get_pos()
        
        pos_in_mask = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
        
        if (left_click and
            not self.clicked and
            self.rect.collidepoint(mouse_pos) and
            self.mask.get_at(pos_in_mask)):
            
            self.clicked = True
                
            promo_piece = None
            
            print(self.piece_data)
            print(len(self.board.chess_pieces_group))
            
            if self.button_name == "queen":
                promo_piece = Queen({**self.piece_data})
                
            elif self.button_name == "rock":
                promo_piece = Rock({**self.piece_data})
                
            elif self.button_name == "knight":
                promo_piece = Knight({**self.piece_data})
                
            elif self.button_name == "bishop":
                promo_piece = Bishop({**self.piece_data})
                
            promo_piece.pos_x = self.piece.pos_x
            promo_piece.pos_y = self.piece.pos_y
            promo_piece.source = "chess_piece/images"
            promo_piece.image = self.piece_data.get("image")
            promo_piece.image_changed = True
            promo_piece.player = self.player
            promo_piece.board = self.board
            promo_piece.side = self.player.side
            promo_piece.piece_coor = self.piece.piece_coor
            
            self.player.in_promotion = False
            self.player.game_state.second_layer.empty()
            self.piece.kill()
            self.board.chess_pieces_group.add(promo_piece)
            
        
            
    def update(self):
        super().update()
        
        self.button_on_click()
        

class PopUp(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # shared data
        self.pos_x = 0
        self.pos_y = 0
        self.board = None
        self.player = None
        
        # class variable
        self.opened = False
        
        self.popup_buttons = pygame.sprite.Group()
        
    def render_popup(self):
        return
        
    def update(self):
        if self.opened:
            self.render_popup()
        
        
class PromotionPopup(PopUp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.surface = None
        self.create_button = False
        
    def render_popup(self):
        # background
        
        pygame.draw.rect(
            self.window,
            (252, 252, 252),
            pygame.Rect(20, 20, 280, 280)
        )
        
        piece_alias = None
        
        # print(self.player.piece_color)

        if not self.create_button:
            self.create_button = True
        
            if self.player.piece_color == "black":
                piece_alias = ["b_q", "b_r", "b_kn", "b_b"]
                
            elif self.player.piece_color == "white":
                piece_alias = ["w_q", "w_r", "w_kn", "w_b"]
                
            for _ in range(len(piece_alias)):
                piece_data = _chess_pieces_dict.get(piece_alias[_], None)
                piece_name = piece_data.get("name").split(" ")[-1]
                piece_image = piece_data.get("image")
                
                button = PromoButton(
                    width=40,
                    height=40,
                    pos_x=30 + _ * 40 + 10,
                    pos_y=280 // 2 + 40 // 2,
                    surface=self.surface
                )
                
                button.button_name = piece_name
                button.piece = self.player.selected_piece
                button.piece_data = piece_data
                button.board = self.board
                button.player = self.player
                button.source = "chess_piece/images"
                button.image = piece_image
                button.image_changed = True
                
                self.popup_buttons.add(button)
                
        self.popup_buttons.update()
        
        