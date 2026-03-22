import pygame
from .window import Window
from .button import Button


class Setup(Window):
    def __init__(self, app):
        super().__init__(app)
        self.esc_btn = Button(app.grid_area + 40, 20, 220, 45,
                              "EXIT TO MENU", (170,100,100), (200,120,120))
        self.solve_btn = Button(app.grid_area + 40, 150, 220, 60,
                                "SOLVE", (100,160,130), (120,190,150))
        self.mode = "SINGLE"
        self.mode_btn = Button(
            app.grid_area + 40, 250, 220, 50,
            "MODE: SINGLE",
            (120,120,160), (150,150,190)
        )

    def handle_events(self, events):
        app = self.app

        for e in events:
            pair_idx = len(app.positions)

            if self.esc_btn.is_clicked(e):
                app.reset_grid()
                from .menu import Menu
                app.state = Menu(app)

            if self.mode_btn.is_clicked(e):
                if self.mode == "SINGLE":
                    self.mode = "RACE"
                else:
                    self.mode = "SINGLE"
                # update button text
                self.mode_btn.text = f"MODE: {self.mode}"

            # Place dots
            if e.type == pygame.MOUSEBUTTONDOWN and pair_idx < app.num_pairs:
                mx, my = e.pos

                if mx < app.grid_area and my < app.grid_area:
                    cs = app.grid_area // app.grid_size
                    c, r = mx // cs, my // cs

                    if 0 <= r < app.grid_size and 0 <= c < app.grid_size:
                        if app.grid_data[r][c] == "":
                            char = chr(ord('a') + pair_idx)

                            if app.current_placing is None:
                                app.current_placing = (r, c)
                                app.grid_data[r][c] = char
                            else:
                                app.positions.append((app.current_placing, (r, c)))
                                app.grid_data[r][c] = char.upper()
                                app.current_placing = None

            # Solve
            if len(app.positions) >= app.num_pairs and self.solve_btn.is_clicked(e):
                if self.mode == "RACE":
                    from .race import Race
                    app.state = Race(app)
                else:
                    from .solving import Solving
                    app.state = Solving(app)

    def draw(self):
        app = self.app
        pair_idx = len(app.positions)

        app.screen.fill((38, 40, 48))

        app.draw_grid_only()

        self.esc_btn.draw(app.screen, app.small_font)
        self.mode_btn.draw(app.screen, app.small_font)
        if pair_idx < app.num_pairs:
            color = app.palette[pair_idx]
            mode = "END dot" if app.current_placing else "START dot"
            app.draw_sidebar(f"Color {pair_idx+1}: {mode}", color)

        else:
            self.solve_btn.draw(app.screen, app.font)