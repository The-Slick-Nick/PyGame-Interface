import pygame
import random

pygame.init()

class UI_Element:
    def __init__(self,
                 pos_x: int,
                 pos_y: int,
                 leftclick=None,
                 middleclick=None,
                 rightclick=None,
                 **kwargs):
        self.pos = (pos_x, pos_y)
        self.mouse_pos = (-1, -1)
        self.mouse_pressed = {
            'NEW': (False, False, False),
            'OLD': (False, False, False)
        }

        self.leftclick = leftclick
        self.middleclick = middleclick
        self.rightclick = rightclick

    def store_input(self, mouse_pos: tuple, mouse_pressed: tuple):
        self.mouse_pos = mouse_pos
        self.mouse_pressed['OLD'] = self.mouse_pressed['NEW']
        self.mouse_pressed['NEW'] = mouse_pressed

    def process_input(self):
        pass

    def mouse_collision(self) -> bool:
        # Template for detecting if currently stored mouse position intersects with this element
        # For base UI_Element template, there is no actual structure, so default to False
        return False

    def mouse_clicked(self, mouse_index: int = 0) -> bool:
        # Returns boolean if left mouse button is newly clicked
        return self.mouse_pressed['NEW'][mouse_index] and not self.mouse_pressed['OLD'][mouse_index]

    def mouse_held(self, mouse_index: int = 0) -> bool:
        # Returns boolean indicating if mouse button is held down
        return self.mouse_pressed['NEW'][mouse_index] and self.mouse_pressed['OLD'][mouse_index]

    def mouse_released(self, mouse_index: int = 0) -> bool:
        # Returns boolean indicating if mouse button has just been released
        return not self.mouse_pressed['NEW'][mouse_index] and self.mouse_pressed['OLD'][mouse_index]


class Button(UI_Element):
    # A type of interactable display element using pygame rectangles & text surfaces
    def __init__(self,
                 width: float,
                 height: float,
                 color: tuple = (255, 255, 255),
                 mouseover_color_mod: float = 1,
                 text: str = "",
                 font: str = 'Arial',
                 font_size: int = 10,
                 textfunc=None,
                 colorfunc=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.size = (width, height)
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], width, height)

        self.font = font
        self.text = text
        self.font_size = font_size

        self.text_surface = pygame.font.SysFont(self.font, self.font_size).render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

        self.display_color = None       # Stores color currently drawn on button
        self.display_text = None        # Stores text currently drawn on button

        self.textfunc = textfunc
        self.colorfunc = colorfunc

        self.color = color
        self.color_mod = mouseover_color_mod

    def mouse_collision(self) -> bool:
        return self.rect.collidepoint(self.mouse_pos)

    def get_rect(self):
        # Template function for determining shape to return
        return self.rect

    def get_color(self) -> tuple:
        # Returns color with which to color button
        # Obtains from a passed colorfunction if it exists.
        # Otherwise uses default color
        try:
            return_color = self.colorfunc()
        except (TypeError, AttributeError) as e:
            return_color = self.color

        if self.mouse_collision():
            return_color = tuple([
                    max(min(self.color_mod * col,255),0)
                    for col in return_color
            ])
        return return_color

    def get_text(self):
        # Returns text to write inside button
        # Obtains button from a given textfunc() if passed
        # Otherwise uses default text
        try:
            return_text = self.textfunc()
        except (TypeError, AttributeError) as e:
            return_text = self.text
        return return_text

    def change_text(self, new_text: str = "", new_font: str = 'Arial', new_font_size: int = 10):
        # Changes the text to be written into a button.
        # Text is drawn differently from a color (as it needs rendered), so we wrap all of those steps
        # into this method
        self.text_surface = pygame.font.SysFont(new_font, new_font_size).render(new_text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.text = new_text

    def draw(self, to_screen: pygame.Surface, force: bool = False):
        # Draws rectangle onto screen.
        # Draws rectangle color, then text on top of it.
        # Default logic only draws if either the text or the color have changed, but this method includes
        # a paramter (force) to draw these on call regardless of what is currently on the screen
        text_to_draw = self.get_text()
        color_to_draw = self.get_color()

        if text_to_draw != self.display_text:
            self.change_text(text_to_draw)

        if force or text_to_draw != self.display_text or color_to_draw != self.display_color:
            pygame.draw.rect(to_screen, color_to_draw, self.get_rect())
            to_screen.blit(self.text_surface, self.text_rect)

            # Store currently displayed color and text to check next time
            self.display_color = color_to_draw
            self.display_text = text_to_draw

    def process_input(self):
        if self.rect.collidepoint(self.mouse_pos):
            if self.mouse_clicked(0):
                self.leftclick()
            elif self.mouse_clicked(1):
                self.middleclick()
            elif self.mouse_clicked(2):
                self.rightclick()


class ImageButton(UI_Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    # A type of interactable display element using images




