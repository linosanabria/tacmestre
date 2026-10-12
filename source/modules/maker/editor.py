import pygame
import sys, os
from ..display import display
from .info import Info
from .grid import Grid
from ..entities.tiles import TileMap
from OpenGL.GL import *
from ..ui.background import Background
from ..ui.levels import Level1
from ..constants import TILE_MAP_LEVEL1, TILE_SIZE
from .notify import Notify, Anchor, Select, Fill
from .pallet import Pallet

class Editor:
    def run(self):
            self.running = True 
            display.create_display()
            self.bg = Background("Black")

            # load tiles
            self.tile_map = TileMap()        
            self.tile_map.load_sprite_maps()
            self.level1 = Level1()
            if not self.level1.load(self.tile_map):
                self.level1.load(self.tile_map)
            
            self.grid = Grid(self.level1)
            self.info = Info(self.grid)
            self.pallet = Pallet(self.tile_map)

            #self.notify = Notify([self.grid, self.info])
            self.notify_anchor = Notify([self.grid, self.info], Anchor)
            self.notify_select = Notify([self.pallet], Select)
            self.notify_fill = Notify([self.grid], Fill)
            
            
            
            """O Game Loop Principal"""
            #try:           
            while self.running:
                dt = display.game_tick()   
                self.handle_events()
                self.update(dt)
                self.draw()
            '''except Exception as e:
                print(e)            # log here
                self.running = False
                pygame.quit()
                sys.exit()'''


    def handle_events(self):
        """Loop de Eventos: Inputs globais do sistema e interrupções"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            # mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if self.pallet.rect.collidepoint(x,y):
                    for tile in self.pallet.tiles:
                        l = self.pallet.rect.left + tile.rect.left
                        t = self.pallet.rect.top + tile.rect.top                        
                        r = pygame.rect.Rect(l,t, tile.rect.w, tile.rect.h)
                        if r.collidepoint(x,y):
                            self.pallet.select = tile
                            self.notify_select.event()  
                            #print(tile.id)  
                            break  
                if self.grid.rect.collidepoint(x,y):
                    if self.pallet.select:
                        for tile in self.grid.tiles:
                            if tile.rect.collidepoint(x,y):
                                col, lin = tile.desc.split(",")
                                col = int(col)
                                lin = int(lin)
                                print(col, lin)
                                self.grid.level.tiles[lin][col] = self.pallet.select
                                left = (col + self.grid.anchor[0]) * TILE_SIZE
                                top = (lin + self.grid.anchor[1]) * TILE_SIZE
                                self.grid.level.tiles[lin][col].rect.topleft = (left, top)
                                self.notify_fill.event()
                                break

                        

        #game_events()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.grid.anchor[0] > 0:
                self.grid.anchor[0] -= 1
                self.notify_anchor.event()
        if keys[pygame.K_RIGHT]:
            max = TILE_MAP_LEVEL1[0] - self.grid.x_tiles
            if self.grid.anchor[0] < max:
                self.grid.anchor[0] += 1
                self.notify_anchor.event()
        if keys[pygame.K_UP]:
            if self.grid.anchor[1] > 0:
                self.grid.anchor[1] -= 1
                self.notify_anchor.event()
        if keys[pygame.K_DOWN]:
            max = TILE_MAP_LEVEL1[1] - self.grid.y_tiles
            if self.grid.anchor[1] < max:
                self.grid.anchor[1] += 1
                self.notify_anchor.event()
        

    def update(self, dt):
        """Loop de Atualização: Onde a lógica matemática acontece"""
        # new thread!                
        # check_collisions()
        #game.player.update(dt)
        self.info.update(dt, self.grid)
        self.grid.update(dt)
        self.pallet.update(dt)

            
    def draw(self):
        """Loop de Renderização: Onde desenhamos na tela"""                 
        # Render Phase
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # ordem importa - cada layer por vez - pode organizar
        self.bg.draw()
        self.info.draw()
        self.grid.draw()
        self.pallet.draw()
        
        pygame.display.flip()
        # forçar sincronização de hardware CPU e GPU - chamadas assincronas
        #glFinish()


editor = Editor()