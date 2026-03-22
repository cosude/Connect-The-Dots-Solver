import pygame
from .window import Window
from .button import Button

from csp_approach import CSP_Solver, Board as CSPBoard
from search_approach import Board as SearchBoard, State, Astar, Heuristic, IDAstar, DFS, BFS, UCS
import sys
import time
import random

class Solving(Window):
    def __init__(self, app):
        super().__init__(app)

        self.stop_btn = Button(app.grid_area + 40, 20, 220, 45,
                               "STOP", (170,100,100), (200,120,120))

        
        self.start_t = 0
        self.started = False
    
    def run_solver(self):
        app = self.app
        self.paths = {}

        def callback(data, extra_paths=None):
            if hasattr(data, 'state'):
                app.grid_data = data.state.board.grid
                app.paths = data.get_paths(app.positions)

            elif isinstance(data, (list, tuple)) and extra_paths is not None:
                app.grid_data = data
                app.paths = extra_paths

            elif isinstance(data, list):
                app.grid_data = data

            app.screen.fill((38, 40, 48))
            app.draw_grid_only()

            self.stop_btn.draw(app.screen, app.font)
            app.draw_sidebar("Searching...", (255, 140, 0))

            pygame.display.flip()

            pygame.time.delay(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if self.stop_btn.is_clicked(event):
                    raise InterruptedError()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    raise InterruptedError()
                
        try:
            success = False

            if app.algo == "CSP":
                board = CSPBoard(app.grid_size, app.grid_size, app.positions)
                result = CSP_Solver(board).solve(callback=callback)
                success = True if result else False

            else:
                search_board = SearchBoard(app.grid_size, app.grid_size, app.positions)
                initial_state = State(search_board)

                if app.algo == "A*":
                    res = Astar(initial_state, Heuristic, callback=callback)
                elif app.algo == "IDA*":
                    res = IDAstar(initial_state, Heuristic, callback=callback)
                elif app.algo == "DFS":
                    res = DFS(initial_state, callback=callback)
                elif app.algo == "UCS":
                    res = UCS(initial_state, callback=callback)
                else:
                    res = BFS(initial_state, callback=callback)

                if res:
                    app.grid_data = res.state.board.grid
                    app.paths = res.get_paths(app.positions)
                    success = True

            app.solve_time = time.time() - self.start_t
            app.solved = success

            from .done import Done
            app.state = Done(app)

        except InterruptedError:
            app.reset_grid()
            from .menu import Menu
            app.state = Menu(app)

    def handle_events(self, events):
        for e in events:
            if self.stop_btn.is_clicked(e):
                from .menu import Menu
                self.app.reset_grid()
                self.app.state = Menu(self.app)

    def draw(self):
        app = self.app

        if not self.started:
            self.started = True
            self.start_t = time.time()
            self.run_solver()
            return
        
        app.screen.fill((38, 40, 48))
        app.draw_grid_only()

        self.stop_btn.draw(app.screen, app.font)

        app.draw_sidebar("Searching...", (255, 140, 0))