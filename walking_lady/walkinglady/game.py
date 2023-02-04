from importlib import resources

import pygame

from walkinglady.config import cfg_item
from walkinglady.entities.hero import Hero

class Game:


    def __init__(self):
        pygame.init()

        self.__screen = pygame.display.set_mode(cfg_item("game","screen_size"),0,32) ## creamos la ventana con caracteristicas defindas
        pygame.display.set_caption(cfg_item("game","title"))

        with resources.path(cfg_item("game","background_image")[0],cfg_item("game","background_image")[1]) as bgrnd_file:
            self.__background = pygame.image.load(bgrnd_file).convert_alpha()

        self.__hero = Hero(self.__screen)

 
        self.__fps_clock = pygame.time.Clock()
        
        self.__running = False
        
    def run(self):
        self.__running = True
        self.__play_music()

        while self.__running:
            delta_time = self.__fps_clock.tick(cfg_item("timing","fps"))
            
            
            self.__process_events()
            self.__update(delta_time)
            self.__render(delta_time)
        
        self.__quit()

    def __process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            if event.type == pygame.KEYDOWN:
                self.__hero.handle_input(event.key, True)
            if event.type == pygame.KEYUP:
                self.__hero.handle_input(event.key, False)    

    def __update(self,delta_time):
            self.__hero.update(delta_time)

    def __render(self,delta_time):
        self.__screen.fill(cfg_item("game","background_color"))
        self.__screen.blit(self.__background,(0,0))

        self.__hero.render(self.__screen,delta_time)
            
        
        pygame.display.update()

    def __play_music(self):
        pygame.mixer.set_reserved(1)
        with resources.path(cfg_item("audio_game","song1","path_song")[0],cfg_item("audio_game","song1","path_song")[1]) as music_file:
            pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(cfg_item("audio_game","song1","music_volume"))
        pygame.mixer.music.play(-1)
    def __quit(self):
        pygame.quit()


