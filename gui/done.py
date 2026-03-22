import pygame
from .window import Window
from .button import Button


class Done(Window):
    def __init__(self, app):
        super().__init__(app)

        self.back_btn = Button(
            app.grid_area + 40, 150, 220, 50,
            "BACK TO MENU",
            (70, 70, 80), (100, 100, 120)
        )

    def handle_events(self, events):
        app = self.app

        for e in events:
            if self.back_btn.is_clicked(e):
                app.reset_grid()
                from .menu import Menu
                app.state = Menu(app)

    def draw(self):
        app = self.app

        app.screen.fill((38, 40, 48))

        app.draw_grid_only()

        if app.solved:
            msg = f"SOLVED: {app.solve_time:.2f}s"
            color = (0, 255, 120)
        else:
            msg = "NO SOLUTION FOUND"
            color = (255, 60, 60)

        app.draw_sidebar(msg, color)

        self.back_btn.draw(app.screen, app.font)