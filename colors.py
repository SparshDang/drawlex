from pygame import Rect, display

from settings import *


class ColorBox(Rect):
    def __init__(self):
        super().__init__(0,0,0,0)

        self.width = display.get_window_size()[0] * SIDE_PANEL_WIDTH - 10
        self.x = display.get_window_size()[0] * SIDE_PANEL_X + 5

        self.colors = {
            (255, 0, 0) : None,       
            (0, 255, 0) : None,       
            (0, 0, 255) : None,       
            (255, 255, 0) : None,     
            (255, 165, 0) : None,     
            (128, 0, 128) : None,     
            (0, 255, 255) : None,     
            (255, 192, 203) : None,   
            (165, 42, 42) : None,     
            (0, 0, 0) : None,         
            (255, 255, 255) : None,   
            (128, 128, 128) : None,   
            (255, 0, 255) : None,     
            (173, 216, 230) : None,   
            (0, 128, 0) : None,       
            (128, 0, 0) : None,       
            (255, 215, 0) : None,     
            (0, 191, 255) : None,     
            (75, 0, 130) : None,      
            (240, 230, 140) :None 
        }

        self.__create_color_boxes_rect()


    def __create_color_boxes_rect(self):
        size = self.width//5
        self.height = size*4


        for i, j in enumerate(self.colors.keys()):
            self.colors[j] = Rect( self.left + i%5*size, self.top + i//5*size ,size,size)
            self.colors[j].scale_by_ip(0.95)

    def get_colors_boxes(self):
        for i in self.colors.items():
            yield i
    
    def update_size_pos(self):
        self.width = display.get_window_size()[0] * SIDE_PANEL_WIDTH - 10
        self.x = display.get_window_size()[0] * SIDE_PANEL_X + 5
        self.__create_color_boxes_rect()

    def get_clicked_color(self, pos):
        for i,j in self.colors.items():
            if j.collidepoint(pos):
                return i