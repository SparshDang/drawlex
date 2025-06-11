import pygame
from pixel import Pixel
from colors import ColorBox
from saveClass import Save

from tkinter.colorchooser import askcolor

from settings import *

pygame.init()


class Main():
    def __init__(self):
        self.window = pygame.display.set_mode(
            (1200, 700), pygame.RESIZABLE)
        pygame.display.set_caption("Drawlex")

        self.grid = []
        self.rows = 32
        self.columns = 32
        self.__set_grid()

        self.color_box = ColorBox()
        self.current_color = (255, 0, 0)
        self.background_color = (255, 255, 255)

        self.button_font = pygame.font.SysFont(None, 40)

        self.grid_toggle_button_rect = pygame.Rect(0, 0, 0, 0)
        self.custom_color_button_rect = pygame.Rect(0, 0, 0, 0)
        self.background_color_button_rect = pygame.Rect(0, 0, 0, 0)
        self.clear_button_rect = pygame.Rect(0, 0, 0, 0)
        self.row_plus_button_rect = pygame.Rect(0, 0, 0, 0)
        self.row_minus_button_rect = pygame.Rect(0, 0, 0, 0)
        self.columns_plus_button_rect = pygame.Rect(0, 0, 0, 0)
        self.columns_minus_button_rect = pygame.Rect(0, 0, 0, 0)
        self.save_button_rect = pygame.Rect(0, 0, 0, 0)

        self.show_grid = True
        self.running = True

        self.__mainloop()

    def __mainloop(self):
        while self.running:
            self.__handle_events()
            self.__setup_display()

            pygame.display.update()

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    for i in self.grid:
                        i.draw(event.pos, self.current_color)
                elif event.buttons[2]:
                    for i in self.grid:
                        i.clear(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if self.custom_color_button_rect.collidepoint(event.pos):
                    color = askcolor()
                    if color[0]:
                        self.current_color = color[0]

                elif self.background_color_button_rect.collidepoint(event.pos):
                    color = askcolor()
                    if color[0]:
                        self.background_color = color[0]

                elif self.color_box.collidepoint(event.pos):
                    color = self.color_box.get_clicked_color(
                        event.pos)
                    if color:
                        self.current_color = color

                elif self.clear_button_rect.collidepoint(event.pos):
                    self.__set_grid()

                elif self.grid_toggle_button_rect.collidepoint(event.pos):
                    self.show_grid = not self.show_grid

                elif self.row_plus_button_rect.collidepoint(event.pos):
                    if self.rows != 50:
                        self.rows += 1
                        self.__set_grid()

                elif self.row_minus_button_rect.collidepoint(event.pos):
                    if self.rows != 1:
                        self.rows -= 1
                        self.__set_grid()

                elif self.columns_plus_button_rect.collidepoint(event.pos):
                    if self.columns != 50:
                        self.columns += 1
                        self.__set_grid()

                elif self.columns_minus_button_rect.collidepoint(event.pos):
                    if self.columns != 1:
                        self.columns -= 1
                        self.__set_grid()

                elif self.save_button_rect.collidepoint(event.pos):
                    Save.save_as_image(self.rows, self.columns, self.grid, self.background_color)

                elif event.button == 1:
                    for i in self.grid:
                        i.draw(event.pos, self.current_color)

                elif event.button == 3:
                    for i in self.grid:
                        i.clear(event.pos)

    def __setup_display(self):
        width, height = pygame.display.get_window_size()
        self.window.fill((255, 255, 255))
        self.__draw_drawing_canvas(width, height)
        self.__draw_side_panel(width, height)
        self.__draw_status_bar(width, height)

    def __set_grid(self):
        self.grid = []
        for i in range(self.rows):
            for j in range(self.columns):
                pixel = Pixel(i, j)
                self.grid.append(pixel)

    def __draw_drawing_canvas(self, width, height):

        if (width*CANVAS_WIDTH)//self.columns > (height*CANVAS_HEIGHT)//self.rows:
            pixel_size = (height*CANVAS_HEIGHT)//self.rows
        else:
            pixel_size = (width*CANVAS_WIDTH)//self.columns

        board_start_x = (
            (width*CANVAS_WIDTH) - self.columns*pixel_size)//2
        board_start_y = (
            (height*CANVAS_HEIGHT) - self.rows*pixel_size)//2

        for i in self.grid:
            i.left = width*CANVAS_X + board_start_x + i.column*pixel_size
            i.top = height*CANVAS_Y + board_start_y + i.row*pixel_size
            i.height = pixel_size
            i.width = pixel_size

            if i.color:
                pygame.draw.rect(self.window, i.color, i)
            else:
                pygame.draw.rect(self.window, self.background_color, i)
            if self.show_grid:
                pygame.draw.rect(self.window, (0, 0, 0) if i.color !=
                                 (0, 0, 0) else (255, 255, 255), i, 1)

    def __draw_side_panel(self, width, height):
        pygame.draw.line(self.window, (0, 0, 0), (SIDE_PANEL_WIDTH*width, SIDE_PANEL_Y *
                         height), (SIDE_PANEL_WIDTH*width, SIDE_PANEL_HEIGHT*height), 2)
        text_rect = self.__draw_title(width, height)
        bottom_of_title = text_rect.bottom

        self.color_box.top = bottom_of_title+10
        self.color_box.update_size_pos()
        self.__draw_color_buttons()
        self.__draw_change_background_color_button(width, height)
        self.__draw_custom_color_button(width, height)
        self.__draw_grid_toggle_button(width, height)
        self.__draw_clear_button(width, height)
        self.__grid_settings(width, height)
        self.__draw_save_button(width,height)

    def __draw_title(self, width, height):
        def __draw_main_title():
            font = pygame.font.SysFont(None, 70, True, True)
            render = font.render("Drawlex", True, (0, 0, 0))
            text_rect = render.get_rect()

            text_rect.centerx = SIDE_PANEL_X*width+(SIDE_PANEL_WIDTH*width)//2
            text_rect.y = SIDE_PANEL_Y*height + 10

            self.window.blit(render, text_rect)
            pygame.draw.rect(self.window, (0, 0, 0),
                             [
                SIDE_PANEL_X*width+(SIDE_PANEL_WIDTH*width)//2 - text_rect.width//2, SIDE_PANEL_Y*height +
                10 + text_rect.height, text_rect.width, 10
            ])
            return text_rect

        def __draw_subheading(margin_in_x):

            font = pygame.font.SysFont(None, 30)
            render = font.render("Create Your own Pixel Art", True, (0, 0, 0))
            text_rect = render.get_rect()

            text_rect.centerx = SIDE_PANEL_X*width+(SIDE_PANEL_WIDTH*width)//2
            text_rect.y = SIDE_PANEL_Y*height + 10 + margin_in_x

            self.window.blit(render, text_rect)
            pygame.draw.rect(self.window, (0, 0, 0),
                             [
                SIDE_PANEL_X*width+(SIDE_PANEL_WIDTH*width)//2 - text_rect.width//2, SIDE_PANEL_Y *
                height + 10 + margin_in_x + text_rect.height, text_rect.width, 2
            ])

            return text_rect

        text_rect = __draw_main_title()
        text_rect = __draw_subheading(text_rect.height + 20)

        return text_rect

    def __draw_color_buttons(self):
        for i, j in self.color_box.get_colors_boxes():
            pygame.draw.rect(self.window, i, j)
            pygame.draw.rect(self.window, (0, 0, 0) if i !=
                             (0, 0, 0) else (255, 255, 255), j, 1)

    def __draw_custom_color_button(self, width, height):
        self.custom_color_button_rect = pygame.Rect(
            0.1*SIDE_PANEL_WIDTH*width, self.background_color_button_rect.bottom+10, 0.8*SIDE_PANEL_WIDTH*width, 0.05 * SIDE_PANEL_HEIGHT*height)

        pygame.draw.rect(
            self.window, (0, 0, 0), self.custom_color_button_rect, 2
        )

        render = self.button_font.render(
            "Custom Color", True, (0, 0, 0))
        text_rect = render.get_rect()
        text_rect.center = self.custom_color_button_rect.center
        self.window.blit(render, text_rect)

    def __draw_change_background_color_button(self, width, height):
        self.background_color_button_rect = pygame.Rect(
            0.1*SIDE_PANEL_WIDTH*width, self.color_box.bottom+10, 0.8*SIDE_PANEL_WIDTH*width, 0.05 * SIDE_PANEL_HEIGHT*height)

        pygame.draw.rect(
            self.window, (0, 0, 0), self.background_color_button_rect, 2
        )

        render = self.button_font.render(
            "Background Color", True, (0, 0, 0))
        text_rect = render.get_rect()
        text_rect.center = self.background_color_button_rect.center
        self.window.blit(render, text_rect)

    def __draw_grid_toggle_button(self, width, height):

        self.grid_toggle_button_rect = pygame.Rect(
            0.1*SIDE_PANEL_WIDTH*width, self.custom_color_button_rect.bottom+10, 0.8*SIDE_PANEL_WIDTH*width, 0.05 * SIDE_PANEL_HEIGHT*height)

        pygame.draw.rect(
            self.window, (0, 0, 0), self.grid_toggle_button_rect, 2
        )

        render = self.button_font.render(
            "Grid On" if self.show_grid else "Grid Off", True, (0, 0, 0))
        text_rect = render.get_rect()
        text_rect.center = self.grid_toggle_button_rect.center
        self.window.blit(render, text_rect)

    def __draw_clear_button(self, width, height):

        self.clear_button_rect = pygame.Rect(
            0.1*SIDE_PANEL_WIDTH*width, self.grid_toggle_button_rect.bottom+10, 0.8*SIDE_PANEL_WIDTH*width, 0.05 * SIDE_PANEL_HEIGHT*height)

        pygame.draw.rect(
            self.window, (0, 0, 0), self.clear_button_rect, 2
        )

        render = self.button_font.render("Clear", True, (0, 0, 0))
        text_rect = render.get_rect()
        text_rect.center = self.clear_button_rect.center
        self.window.blit(render, text_rect)

    def __grid_settings(self, width, height):
        def __row_settings():
            render = self.button_font.render(
                f"Rows : {self.rows}", True, (0, 0, 0))
            text_rect = render.get_rect()
            text_rect.top = self.clear_button_rect.bottom+10
            text_rect.left = SIDE_PANEL_X*width + 10
            self.window.blit(render, text_rect)

            self.row_plus_button_rect = pygame.Rect(0, 0, 0, 0)
            self.row_plus_button_rect.width = 0.2*SIDE_PANEL_WIDTH*width
            self.row_plus_button_rect.left = SIDE_PANEL_X*width + \
                SIDE_PANEL_WIDTH*width - 10 - self.row_plus_button_rect.width
            self.row_plus_button_rect.height = text_rect.height
            self.row_plus_button_rect.top = text_rect.top

            self.row_minus_button_rect = pygame.Rect(0, 0, 0, 0)
            self.row_minus_button_rect.width = 0.2*SIDE_PANEL_WIDTH*width
            self.row_minus_button_rect.left = SIDE_PANEL_X*width + SIDE_PANEL_WIDTH * \
                width - 20 - self.row_minus_button_rect.width - self.row_plus_button_rect.width
            self.row_minus_button_rect.height = text_rect.height
            self.row_minus_button_rect.top = text_rect.top

            pygame.draw.rect(self.window, (0, 255, 0),
                             self.row_plus_button_rect, 2)
            render = self.button_font.render("+", True, (0, 255, 0))
            text_rect = render.get_rect()
            text_rect.center = self.row_plus_button_rect.center
            self.window.blit(render, text_rect)

            pygame.draw.rect(self.window, (255, 0, 0),
                             self.row_minus_button_rect, 2)
            render = self.button_font.render("-", True, (255, 0, 0))
            text_rect = render.get_rect()
            text_rect.center = self.row_minus_button_rect.center
            self.window.blit(render, text_rect)

        def __column_settings():
            render = self.button_font.render(
                f"Cols. : {self.columns}", True, (0, 0, 0))
            text_rect = render.get_rect()
            text_rect.top = self.row_plus_button_rect.bottom+10
            text_rect.left = SIDE_PANEL_X*width + 10
            self.window.blit(render, text_rect)

            self.columns_plus_button_rect = pygame.Rect(0, 0, 0, 0)
            self.columns_plus_button_rect.width = 0.2*SIDE_PANEL_WIDTH*width
            self.columns_plus_button_rect.left = SIDE_PANEL_X*width + \
                SIDE_PANEL_WIDTH*width - 10 - self.columns_plus_button_rect.width
            self.columns_plus_button_rect.height = text_rect.height
            self.columns_plus_button_rect.top = text_rect.top

            self.columns_minus_button_rect = pygame.Rect(0, 0, 0, 0)
            self.columns_minus_button_rect.width = 0.2*SIDE_PANEL_WIDTH*width
            self.columns_minus_button_rect.left = SIDE_PANEL_X*width + SIDE_PANEL_WIDTH*width - \
                20 - self.columns_minus_button_rect.width - self.columns_plus_button_rect.width
            self.columns_minus_button_rect.height = text_rect.height
            self.columns_minus_button_rect.top = text_rect.top

            pygame.draw.rect(self.window, (0, 255, 0),
                             self.columns_plus_button_rect, 2)
            render = self.button_font.render("+", True, (0, 255, 0))
            text_rect = render.get_rect()
            text_rect.center = self.columns_plus_button_rect.center
            self.window.blit(render, text_rect)

            pygame.draw.rect(self.window, (255, 0, 0),
                             self.columns_minus_button_rect, 2)
            render = self.button_font.render("-", True, (255, 0, 0))
            text_rect = render.get_rect()
            text_rect.center = self.columns_minus_button_rect.center
            self.window.blit(render, text_rect)

        __row_settings()
        __column_settings()

    def __draw_save_button(self,width,height):
        self.save_button_rect = pygame.Rect(
            0.1*SIDE_PANEL_WIDTH*width, SIDE_PANEL_HEIGHT*height-10- 0.05 * SIDE_PANEL_HEIGHT*height, 0.8*SIDE_PANEL_WIDTH*width, 0.05 * SIDE_PANEL_HEIGHT*height)

        pygame.draw.rect(
            self.window, (0, 0, 0), self.save_button_rect, 2
        )

        render = self.button_font.render(
            "Save", True, (0, 0, 0))
        text_rect = render.get_rect()
        text_rect.center = self.save_button_rect.center
        self.window.blit(render, text_rect)        

    def __draw_status_bar(self, width, height):
        bar_rect = pygame.Rect(width*STATUS_BAR_X,
                               height*STATUS_BAR_Y,
                               width*STATUS_BAR_WIDTH,
                               height*STATUS_BAR_HEIGHT)

        pygame.draw.line(self.window, (0, 0, 0),
                         bar_rect.topleft, bar_rect.topright, 2)
        current_color_right = self.__show_current_color__and_get_its_right(
            bar_rect)
        self.__show_background_color(bar_rect, current_color_right+10)
        self.__draw_instructions(bar_rect)

    def __show_current_color__and_get_its_right(self, bar_rect):
        current_color_text = self.button_font.render(
            "Current Color : ", True, (0, 0, 0))
        text_rect = current_color_text.get_rect()
        text_rect.centery = bar_rect.centery
        text_rect.left = bar_rect.left + 20

        self.window.blit(current_color_text, text_rect)

        pygame.draw.rect(self.window, self.current_color, [
            text_rect.right + 10,
            text_rect.top,
            40,
            text_rect.height
        ])
        pygame.draw.rect(self.window, (0, 0, 0), [
            text_rect.right + 10,
            text_rect.top,
            40,
            text_rect.height
        ], 2)

        return text_rect.right+10+40

    def __show_background_color(self, bar_rect, left):
        background_color_text = self.button_font.render(
            "Background Color : ", True, (0, 0, 0))
        text_rect = background_color_text.get_rect()
        text_rect.centery = bar_rect.centery
        text_rect.left = left

        self.window.blit(background_color_text, text_rect)

        pygame.draw.rect(self.window, self.background_color, [
            text_rect.right + 10,
            text_rect.top,
            40,
            text_rect.height
        ])
        pygame.draw.rect(self.window, (0, 0, 0), [
            text_rect.right + 10,
            text_rect.top,
            40,
            text_rect.height
        ], 2)

    def __draw_instructions(self, bar_rect):
        font = pygame.font.SysFont(None, 30, False)
        text = font.render(
            "(Left Click : Draw - Right Click : Erase)", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.centery = bar_rect.centery
        text_rect.right = bar_rect.right - 20

        self.window.blit(text, text_rect)

if __name__ == "__main__":
    Main()
