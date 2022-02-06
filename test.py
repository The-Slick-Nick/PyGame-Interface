import pygame
from Interface import *


class TestUI:
    def __init__(self):
        self.runtime_control = {
            'MAIN': False
        }
        self.main_window = None

    def toggle_runtime(self, runtime_type: str = 'MAIN'):
        self.runtime_control[runtime_type] = not self.runtime_control[runtime_type]

    def main_screen(self):
        self.runtime_control['MAIN'] = True
        self.main_window = pygame.display.set_mode((500, 500))

        buttons = [
            Button(
                pos_x=250,
                pos_y=250,
                width=50,
                height=50,
                leftclick=lambda: self.toggle_runtime("MAIN"),
                color=(150, 0, 25),
                mouseover_color_mod=0.5
            )
        ]

        while self.runtime_control['MAIN']:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.runtime_control['MAIN'] = False

            for button in buttons:
                button.store_input(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3))

            for button in buttons:
                button.process_input()

            for button in buttons:
                button.draw(self.main_window)

            pygame.display.flip()

def main():
    tui = TestUI()
    tui.main_screen()

if __name__ == "__main__":
    main()