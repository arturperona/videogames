from importlib import resources

import pygame

from walkinglady.config import cfg_item

class Hero:
    def __init__(self, screen):
        self.__is_moving_up = False
        self.__is_moving_down = False
        self.__is_moving_left = False
        self.__is_moving_right = False
        self.__right_moves = dict()
        self.__left_moves = dict()
        self.__acum_time = 0
        self.__frame = 0

        self.__screen_width = screen.get_width()
        self.__screen_height = screen.get_height()

        with resources.path(cfg_item("entities", "hero", "path")[0], cfg_item("entities", "hero", "path")[1]) as hero_file:
            self.__hero_image = pygame.image.load(hero_file).convert_alpha()

        self._position = pygame.math.Vector2(self.__screen_width/2, self.__screen_height/2)

        self._image_size = cfg_item("entities","hero","image_size")
        self._columns = cfg_item("entities","hero","images_right")

        for i in range(cfg_item("entities","hero","images_right")):
            left = self._image_size[0] * (i % self._columns)
            self.__right_moves[i] = pygame.Rect(left,0,self._image_size[0],self._image_size[1])

        for j in range(cfg_item("entities","hero","images_right")):
            left = self._image_size[0] * (j % self._columns)
            self.__left_moves[j] = pygame.Rect(left,self._image_size[1],self._image_size[0],self._image_size[1]*2)


    def handle_input(self, key, is_pressed):
        if key == pygame.K_LEFT:
            self.__is_moving_left = is_pressed
        elif key == pygame.K_RIGHT:
            self.__is_moving_right = is_pressed
            

    def update(self, delta_time):
        movement = pygame.math.Vector2(0.0, 0.0)
        speed = cfg_item("entities","hero","speed")
        self.__acum_time += delta_time +1

        if self.__is_moving_left:
            self.__is_moving_left = True
            movement.x -= speed
            self.__frame += speed
            if self.__frame > self._columns:
                self.__frame = 1  
        if self.__is_moving_right:
            self.__is_moving_right = True
            movement.x += speed
            self.__frame += speed         
            if self.__frame > self._columns:
                self.__frame = 1


        distance = movement * delta_time

        if self.__allow_move_inside_limits(distance):
            self._position += distance
            

    def render(self, dst_surface,delta_time):
        for i in range(self._columns):
            if self.__is_moving_right and self.__acum_time > delta_time:
                index = int(self.__frame + i) % self._columns
                dst_surface.blit(self.__hero_image, self._position.xy,self.__right_moves[index])

            if self.__is_moving_left and self.__acum_time > delta_time:
                index = int(self.__frame + i) % self._columns
                dst_surface.blit(self.__hero_image, self._position.xy,self.__left_moves[index]) 
          
            elif (self.__is_moving_right == False and self.__is_moving_left == False) or (self.__is_moving_right == True and self.__is_moving_left == True):
                dst_surface.blit(self.__hero_image, self._position.xy,self.__right_moves[0])
                self.__frame = 0
            self.__acum_time = 0
            


    def __allow_move_inside_limits(self, movement):

        self.__hero_image_half_width = self.__right_moves[0][2]/2
        self.__hero_image_half_height = self.__right_moves[0][3]/2 
        new_pos = self._position + movement

        if new_pos.x < -self.__hero_image_half_width or new_pos.x > self.__screen_width - self.__hero_image_half_width or new_pos.y < -self.__hero_image_half_height or new_pos.y > self.__screen_height - self.__hero_image_half_height:
            return False
        return True

    def release(self):
        pass

