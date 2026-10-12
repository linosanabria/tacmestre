import pygame
from ..display import display
from ..constants import SCALE, TILE_MAP_LEVEL1
from ..utils import utils
from .grid import Grid
from .notify import Interested, Anchor

class Info(Interested):
    def __init__(self, grid:Grid): 
        super().__init__() 
        pygame.font.init()              
        self.delay:int = 1
        self.counter = self.delay           
        
        # Initialize a font (system default or custom font file)
        #self.font = pygame.font.SysFont("Arial", 14)
        fps_text = f"FPS:{str(int(display.clock.get_fps()))}"
        self.font = pygame.font.Font("assets/fonts/Call of Ops Duty II.otf", 200)        
        self.image = self.font.render(fps_text, True, pygame.Color("green")) 
        #self.image = pygame.transform.smoothscale_by(self.image, 1/(SCALE))
        self.rect = self.image.get_rect()
        # Converte e guarda o ID da GPU
        self.texture_id = utils.surface_to_texture(self.image)


        grid_text = f"({grid.x_tiles},{grid.y_tiles})"
        self.font2 = pygame.font.Font("assets/fonts/Call of Ops Duty II.otf", 150)
        self.image_grid_tiles = self.font2.render(grid_text, True, pygame.Color("green")) 
        self.image_grid_tiles = pygame.transform.smoothscale_by(self.image_grid_tiles, 1/(SCALE*4))
        self.rect_grid_tiles = self.image_grid_tiles.get_rect()
        # Converte e guarda o ID da GPU
        self.texture_id_grid_tiles = utils.surface_to_texture(self.image_grid_tiles)


        grid_text = f"{TILE_MAP_LEVEL1}"
        #self.font2 = pygame.font.Font("assets/fonts/Call of Ops Duty II.otf", 100)
        self.image_lv1_tiles = self.font2.render(grid_text, True, pygame.Color("green")) 
        self.image_lv1_tiles = pygame.transform.smoothscale_by(self.image_lv1_tiles, 1/(SCALE*4))
        self.rect_lv1_tiles = self.image_lv1_tiles.get_rect()
        # Converte e guarda o ID da GPU
        self.texture_id_lv1_tiles = utils.surface_to_texture(self.image_lv1_tiles)

        grid_text = f"{grid.anchor}"
        #self.font2 = pygame.font.Font("assets/fonts/Call of Ops Duty II.otf", 100)
        self.image_anchor_tiles = self.font2.render(grid_text, True, pygame.Color("green")) 
        self.image_anchor_tiles = pygame.transform.smoothscale_by(self.image_anchor_tiles, 1/(SCALE*4))
        self.rect_anchor_tiles = self.image_anchor_tiles.get_rect()
        # Converte e guarda o ID da GPU
        self.texture_id_anchor_tiles = utils.surface_to_texture(self.image_anchor_tiles)



    def update(self, dt:float, grid:Grid):        
        self.counter += dt 
        if self.counter >= self.delay:                      
            # clock.get_fps() returns a float, so we convert it to an int, then a string
            fps = display.clock.get_fps()
            valor = int(min(fps,10000))
            fps_text = f"FPS:{valor}"
            # Render the text (Text, Anti-aliasing, Color)
            self.image = self.font.render(fps_text, True, pygame.Color("green"))
            self.image = pygame.transform.smoothscale_by(self.image, 1/(SCALE*4)) 
            self.rect = self.image.get_rect()    
            self.texture_id = utils.update_texture(self.texture_id, self.image)    
            self.counter = 0

        for event in self.events_get():
            if event == Anchor:
                # atualizar anchor - condicao de evento
                #if self.counter >= self.delay: 
                #print("ddfdfd")
                grid_text = f"{grid.anchor}"
                #self.font2 = pygame.font.Font("assets/fonts/Call of Ops Duty II.otf", 100)
                self.image_anchor_tiles = self.font2.render(grid_text, True, pygame.Color("green")) 
                self.image_anchor_tiles = pygame.transform.smoothscale_by(self.image_anchor_tiles, 1/(SCALE*4))
                self.rect_anchor_tiles = self.image_anchor_tiles.get_rect()
                # Converte e guarda o ID da GPU
                self.texture_id_anchor_tiles = utils.update_texture(self.texture_id_anchor_tiles, self.image_anchor_tiles)
        
    

    def draw(self):
        x,y,w,h = 0, 0, self.rect.w, self.rect.h        
        utils.draw_textured_quad(self.texture_id, x,y,w,h) 

        x,y,w,h = 0, self.rect.h, self.rect_grid_tiles.w, self.rect_grid_tiles.h        
        utils.draw_textured_quad(self.texture_id_grid_tiles, x,y,w,h)

        x,y,w,h = 0, self.rect.h+self.rect_grid_tiles.h, self.rect_lv1_tiles.w, self.rect_lv1_tiles.h        
        utils.draw_textured_quad(self.texture_id_lv1_tiles, x,y,w,h)

        x,y = 0, self.rect.h + self.rect_grid_tiles.h + self.rect_lv1_tiles.h 
        w,h = self.rect_anchor_tiles.w, self.rect_anchor_tiles.h        
        utils.draw_textured_quad(self.texture_id_anchor_tiles, x,y,w,h)
        
       
