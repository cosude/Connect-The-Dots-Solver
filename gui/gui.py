import pygame
import sys
import time
import random

from csp_approach import CSP_Solver, Board as CSPBoard
from search_approach import Board as SearchBoard, State, Astar, Heuristic, IDAstar, DFS, BFS, UCS

from .menu import Menu
from .setup import Setup
from .solving import Solving
from .done import Done


class App:
    def __init__(self, screen_res=700):
        pygame.init()

        self.grid_area = screen_res
        self.sidebar_w = 300
        self.screen = pygame.display.set_mode((self.grid_area + self.sidebar_w, screen_res))
        pygame.display.set_caption("CONNECT THE DOTS SOLVER")

        self.font = pygame.font.SysFont("Segoe UI", 24, bold=True)
        self.small_font = pygame.font.SysFont("Segoe UI", 18)
        self.title_font = pygame.font.SysFont("Segoe UI", 56, bold=True)

        self.palette = [
            (255, 140, 140),
            (140, 200, 255),
            (160, 255, 180),
            (255, 255, 180),
            (255, 180, 255),
            (180, 255, 255),
            (255, 210, 160),
            (200, 180, 255)
        ]

        self.grid_size = 5
        self.num_pairs = 3
        self.algo = "CSP"

        self.grid_data = []
        self.positions = []
        self.paths = {}
        self.current_placing = None

        self.solve_time = 0
        self.solved = False

        self.state = Menu(self)

    # ================= RUN LOOP =================
    def run(self):
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(60)
            events = pygame.event.get()

            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.state.handle_events(events)
            self.state.draw()

            pygame.display.flip()

    # ================= HELPERS =================
    def reset_grid(self):
        self.grid_data = [["" for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.positions = []
        self.paths = {}
        self.current_placing = None
        self.solved = False

    def generate_random(self):
        self.reset_grid()

        cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size)]
        random.shuffle(cells)

        for i in range(self.num_pairs):
            p1, p2 = cells.pop(), cells.pop()
            self.positions.append((p1, p2))

            char = chr(ord('a') + i)
            self.grid_data[p1[0]][p1[1]] = char
            self.grid_data[p2[0]][p2[1]] = char.upper()

        self.state = Setup(self)

    # ================= SOLVER =================
    def start_solver(self):
        start_t = time.time()
        self.paths = {}

        def callback(data, extra_paths=None):
            if hasattr(data, 'state'):
                self.grid_data = data.state.board.grid
                self.paths = data.get_paths(self.positions)
            elif isinstance(data, (list, tuple)) and extra_paths is not None:
                self.grid_data = data
                self.paths = extra_paths
            elif isinstance(data, list):
                self.grid_data = data

        success = False

        if self.algo == "CSP":
            board = CSPBoard(self.grid_size, self.grid_size, self.positions)
            result = CSP_Solver(board).solve(callback=callback)
            success = True if result else False

        else:
            search_board = SearchBoard(self.grid_size, self.grid_size, self.positions)
            initial_state = State(search_board)

            if self.algo == "A*":
                res = Astar(initial_state, Heuristic, callback=callback)
            elif self.algo == "IDA*":
                res = IDAstar(initial_state, Heuristic, callback=callback)
            elif self.algo == "DFS":
                res = DFS(initial_state, callback=callback)
            elif self.algo == "UCS":
                res = UCS(initial_state, callback=callback)
            else:
                res = BFS(initial_state, callback=callback)

            if res:
                self.grid_data = res.state.board.grid
                self.paths = res.get_paths(self.positions)
                success = True

        self.solve_time = time.time() - start_t
        self.solved = success

        self.state = Done(self)

    # ================= DRAW =================
    def draw_grid_only(self):
        cs = self.grid_area // self.grid_size
        thick = cs // 4

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                rect = pygame.Rect(c*cs, r*cs, cs, cs)
                pygame.draw.rect(self.screen, (100, 105, 120), rect, 1)

        for char, path_list in self.paths.items():
            if not path_list:
                continue

            color = self.palette[(ord(char.lower()) - ord('a')) % len(self.palette)]

            for i in range(len(path_list) - 1):
                p1, p2 = path_list[i], path_list[i+1]

                start = (p1[1]*cs + cs//2, p1[0]*cs + cs//2)
                end = (p2[1]*cs + cs//2, p2[0]*cs + cs//2)

                pygame.draw.line(self.screen, color, start, end, thick)

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                val = self.grid_data[r][c]
                if val:
                    color = self.palette[(ord(val.lower()) - ord('a')) % len(self.palette)]

                    is_endpoint = any((r,c) in pair for pair in self.positions) or (r, c) == self.current_placing

                    if is_endpoint:
                        pygame.draw.circle(self.screen, color, (c*cs+cs//2, r*cs+cs//2), cs//3)
                    else:
                        pygame.draw.circle(self.screen, color, (c*cs+cs//2, r*cs+cs//2), thick // 2)

    def draw_sidebar(self, text, color):
        pygame.draw.rect(self.screen, color, (self.grid_area + 30, 80, 240, 55), border_radius=10)
        img = self.small_font.render(text, True, (0, 0, 0))
        self.screen.blit(img, img.get_rect(center=(self.grid_area + 150, 108)))

    def draw_grid_at(self, grid, paths, offset_x, offset_y, width, height):
        cs = min(width, height) // self.grid_size
        thick = cs // 4

        grid_size_px = cs * self.grid_size
        
        start_x = offset_x + (width - grid_size_px) // 2
        start_y = offset_y + (height - grid_size_px) // 2

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                rect = pygame.Rect(start_x + c*cs, start_y + r*cs, cs, cs)
                pygame.draw.rect(self.screen, (100, 105, 120), rect, 1)

        for char, path_list in paths.items():
            if not path_list:
                continue

            color = self.palette[(ord(char.lower()) - ord('a')) % len(self.palette)]

            for i in range(len(path_list) - 1):
                p1, p2 = path_list[i], path_list[i+1]

                x1 = start_x + p1[1]*cs + cs//2
                y1 = start_y + p1[0]*cs + cs//2

                x2 = start_x + p2[1]*cs + cs//2
                y2 = start_y + p2[0]*cs + cs//2

                pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), thick)

                pygame.draw.circle(self.screen, color, (x1, y1), thick // 2)

        for char, path_list in paths.items():
            if path_list:
                r, c = path_list[-1]
                x = start_x + c*cs + cs//2
                y = start_y + r*cs + cs//2
                color = self.palette[(ord(char.lower()) - ord('a')) % len(self.palette)]
                pygame.draw.circle(self.screen, color, (x, y), thick // 2)

        endpoints = set()
        for (r1, c1), (r2, c2) in self.positions:
            endpoints.add((r1, c1))
            endpoints.add((r2, c2))

        for (r, c) in endpoints:
            val = grid[r][c]
            if val:
                color = self.palette[(ord(val.lower()) - ord('a')) % len(self.palette)]
                pygame.draw.circle(
                    self.screen,
                    color,
                    (start_x + c*cs + cs//2, start_y + r*cs + cs//2),
                    cs // 3
                )