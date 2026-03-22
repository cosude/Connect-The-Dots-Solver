import pygame
from .window import Window
from .button import Button

class Menu(Window):
    def __init__(self, app):
        super().__init__(app)
        self.s_up = self.s_dn = None
        self.p_up = self.p_dn = None
        self.algo_btn = None
        self.rand_btn = None
        self.start_btn = None
        center_x = (app.grid_area + app.sidebar_w) // 2
        y_row3 = 380

        self.algo_btn = Button(
            center_x - 115, y_row3, 110, 45,
            app.algo,
            (180, 140, 100), (210, 160, 120)
        )

        self.rand_btn = Button(
            center_x + 5, y_row3, 110, 45,
            "RAND",
            (130, 120, 170), (150, 140, 200)
        )

        self.start_btn = Button(
            center_x - 115, 500, 230, 65,
            "START SETUP",
            (100, 140, 180), (120, 160, 210)
        )
        
    def handle_events(self, events):
        app = self.app
        for e in events:
            if self.s_up and self.s_up.is_clicked(e):
                app.grid_size = min(15, app.grid_size + 1)

            if self.s_dn and self.s_dn.is_clicked(e):
                app.grid_size = max(3, app.grid_size - 1)

            if self.p_up and self.p_up.is_clicked(e):
                app.num_pairs = min(8, app.num_pairs + 1)

            if self.p_dn and self.p_dn.is_clicked(e):
                app.num_pairs = max(1, app.num_pairs - 1)

            if self.algo_btn and self.algo_btn.is_clicked(e):
                if app.algo == "CSP": app.algo = "A*"
                elif app.algo == "A*": app.algo = "IDA*"
                elif app.algo == "IDA*": app.algo = "DFS"
                elif app.algo == "DFS": app.algo = "BFS"
                elif app.algo == "BFS": app.algo = "UCS"
                else: app.algo = "CSP"

            if self.rand_btn and self.rand_btn.is_clicked(e):
                app.generate_random()

            if self.start_btn and self.start_btn.is_clicked(e):
                app.reset_grid()
                from .setup import Setup
                app.state = Setup(app)

    def draw(self):
        app = self.app
        total_w = app.grid_area + app.sidebar_w
        center_x = total_w // 2

        app.screen.fill((38, 40, 48))

        title_surf = app.title_font.render("CONNECT THE DOTS SOLVER", True, (245, 245, 220))
        title_rect = title_surf.get_rect(center=(center_x, 80))
        app.screen.blit(title_surf, title_rect)

        self.s_dn, self.s_up = self.draw_control_row(200, "Grid Size:", str(app.grid_size))
        self.p_dn, self.p_up = self.draw_control_row(270, "Total Pairs:", str(app.num_pairs))

        self.algo_btn.text = app.algo 
        self.algo_btn.draw(app.screen, app.font)
        self.rand_btn.draw(app.screen, app.font)
        self.start_btn.draw(app.screen, app.font)

    def draw_control_row(self, y, label_str, value_str):
        app = self.app
        center_x = (app.grid_area + app.sidebar_w) // 2

        label_surf = app.font.render(label_str, True, (200, 200, 210))
        app.screen.blit(label_surf, (center_x - 180, y + 8))

        btn_minus = Button(center_x, y, 45, 45, "-", (60, 60, 70), (90, 90, 110))
        btn_plus = Button(center_x + 110, y, 45, 45, "+", (60, 60, 70), (90, 90, 110))

        val_surf = app.font.render(value_str, True, (255, 255, 255))
        val_rect = val_surf.get_rect(center=(center_x + 77, y + 22))

        btn_minus.draw(app.screen, app.font)
        btn_plus.draw(app.screen, app.font)
        app.screen.blit(val_surf, val_rect)

        return btn_minus, btn_plus
