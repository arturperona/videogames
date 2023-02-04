import os
import pygame

from config import cfg_item
from scroll import Scroll

class Game:


    def __init__(self):
        pygame.init()

        self.__screen = pygame.display.set_mode(cfg_item("game","screen_size"),0,32) ## creamos la ventana con caracteristicas defindas
        pygame.display.set_caption(cfg_item("game","title"))

        self.__running = False
        self.__fps_clock = pygame.time.Clock()
        self.__scroll = Scroll()
        
    def run(self):
        self.__running = True
        self.play_music()
        

        while self.__running:
            delta_time = self.__fps_clock.tick(cfg_item("timing","fps"))
            
            self.__process_events()
            self.__update(delta_time)
            self.__render()
            

        self.__quit()

    def __process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
    

    def __update(self,delta_time):
            self.__scroll.update(delta_time)

    def __render(self):
        self.__screen.fill(cfg_item("game","background_color"))
        self.__scroll.render(self.__screen)
        
        pygame.display.update()
    

    def play_music(self):
        print(os.path.join(*cfg_item("audio_game","song1","path_song")))
        pygame.mixer.music.load(os.path.join(*cfg_item("audio_game","song1","path_song")))
        pygame.mixer.music.set_volume(cfg_item("audio_game","song1","music_volume"))
        pygame.mixer.music.play(-1)

    def __quit(self):
        pygame.quit()


