import pygame
import threading
import queue
import time
import copy  
from .window import Window
from .button import Button

from search_approach import Board as SearchBoard, State, Astar, Heuristic, BFS, DFS, IDAstar, UCS
from csp_approach import Board as CSPBoard, CSP_Solver

class Race(Window):
    def __init__(self, app):
        super().__init__(app)
        self.algos = ["A*", "IDA*", "BFS", "DFS", "UCS", "CSP"]
        self.queues = {name: queue.Queue() for name in self.algos}

        self.boards = {}
        for name in self.algos:
            if name == "CSP":
                initial_grid = CSPBoard(app.grid_size, app.grid_size, app.positions).grid
            else:
                initial_grid = SearchBoard(app.grid_size, app.grid_size, app.positions).grid

            self.boards[name] = {
                "grid": initial_grid, 
                "paths": {},
                "sps": 0,
                "steps": 0
            }

        self.finished = {name: False for name in self.algos}
        self.started = False
        self.start_time = time.time()
        self.rankings = []
        btn_x = app.grid_area + 40
        self.stop_btn = Button(btn_x, 500, 220, 45, "STOP RACE", (200, 100, 100), (220, 120, 120))
        self.exit_btn = Button(btn_x, 560, 220, 45, "EXIT TO MENU", (100, 100, 100), (120, 120, 120))

        self.stop_flag = False

    # ================= HELPER =================
    def generate_paths_from_grid(self, grid):
        paths = {}
        colors = set(cell.lower() for row in grid for cell in row if cell)
        
        for char in colors:
            points = [(r, c) for r in range(self.app.grid_size) 
                    for c in range(self.app.grid_size) 
                    if grid[r][c].lower() == char]
            
            if not points: continue

            start = None
            for r, c in points:
                if grid[r][c] == char:
                    start = (r, c)
                    break
            
            if not start: start = points[0]

            sorted_path = [start]
            remaining = set(points)
            remaining.remove(start)

            while remaining:
                curr = sorted_path[-1]
                next_pt = None
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = curr[0] + dr, curr[1] + dc
                    if (nr, nc) in remaining:
                        next_pt = (nr, nc)
                        break
                
                if next_pt:
                    sorted_path.append(next_pt)
                    remaining.remove(next_pt)
                else:
                    break
            
            paths[char] = sorted_path
            
        return paths

    # ================= THREAD WORKER =================
    def run_algo(self, name):
        app = self.app
        q = self.queues[name]
        last_update_time = 0
        update_interval = 0.03 
        steps = 0
        start_time = time.time()

        def callback(data, extra_paths=None):
            if self.stop_flag:
                raise InterruptedError("User stopped the race")

            nonlocal last_update_time, steps
            steps += 1
            now = time.time()
            
            if now - last_update_time > update_interval:
                if hasattr(data, 'state'):
                    grid = copy.deepcopy(data.state.board.grid)
                    paths = data.get_paths(app.positions)
                else:
                    grid = copy.deepcopy(data)
                    paths = extra_paths if extra_paths else self.generate_paths_from_grid(grid)

                elapsed = now - start_time
                sps = int(steps / elapsed) if elapsed > 0 else 0
                
                q.put(("update", grid, paths, sps, steps))
                last_update_time = now

                if name in ["CSP", "DFS", "BFS"]:
                    time.sleep(0.01)

        try:
            if name == "CSP":
                board = CSPBoard(app.grid_size, app.grid_size, app.positions)
                final_grid, final_paths = CSP_Solver(board).solve(callback=callback)
                
                if final_grid:
                    q.put(("update", final_grid, final_paths, 0, steps))
                    q.put(("done", (final_grid, final_paths)))
                else:
                    q.put(("done", None))
            else:
                board = SearchBoard(app.grid_size, app.grid_size, app.positions)
                initial = State(board)
                algos = {
                    "A*": lambda: Astar(initial, Heuristic, callback=callback),
                    "IDA*": lambda: IDAstar(initial, Heuristic, callback=callback),
                    "UCS": lambda: UCS(initial, callback=callback),
                    "DFS": lambda: DFS(initial, callback=callback),
                    "BFS": lambda: BFS(initial, callback=callback)
                }
                res = algos[name]()

            q.put(("done", res))
        except Exception as e:
            q.put(("error", str(e)))

    # ================= DRAW =================
    def draw(self):
        app = self.app
        if not self.started:
            self.started = True
            for name in self.algos:
                threading.Thread(target=self.run_algo, args=(name,), daemon=True).start()

        app.screen.fill((38, 40, 48))
        
        cols, rows = 3, 2
        MARGIN = 10
        slot_w = app.grid_area // cols
        slot_h = app.grid_area // rows

        for i, name in enumerate(self.algos):
            q = self.queues[name]
            last_msg = None
            while not q.empty():
                last_msg = q.get()
                if last_msg[0] == "done": break

            if last_msg:
                if last_msg[0] == "update":
                    self.boards[name]["grid"] = last_msg[1]
                    self.boards[name]["paths"] = last_msg[2]
                    self.boards[name]["sps"] = last_msg[3]
                    self.boards[name]["steps"] = last_msg[4]
                elif last_msg[0] == "done":
                    if not self.finished[name]:
                        self.finished[name] = True
                        res = last_msg[1]
                        
                        if hasattr(res, 'state'): 
                            self.boards[name]["grid"] = res.state.board.grid
                            self.boards[name]["paths"] = res.get_paths(app.positions)
                        elif isinstance(res, tuple): 
                            self.boards[name]["grid"] = res[0]
                            self.boards[name]["paths"] = res[1] 
                            
                        t = time.time() - self.start_time
                        self.rankings.append((name, t))

            slot_x = (i % cols) * slot_w
            slot_y = (i // cols) * slot_h
            
            self.draw_algo_board(
                name, 
                slot_x + MARGIN, 
                slot_y + MARGIN, 
                slot_w - (MARGIN * 2), 
                slot_h - (MARGIN * 2)
            )

        self.draw_results()
        self.stop_btn.draw(app.screen, app.font)
        self.exit_btn.draw(app.screen, app.font)
        self.draw_results()

    def draw_algo_board(self, name, x, y, w, h):
        grid = self.boards[name]["grid"]
        if not grid: return

        text_color = (0, 255, 150) if self.finished[name] else (255, 255, 255)
        
        header_txt = f"{name}"
        if self.finished[name]:
            header_txt += " (DONE)"
            
        label = self.app.small_font.render(header_txt, True, text_color)
        
        self.app.screen.blit(label, (x, y - 5))

        self.app.draw_grid_at(grid, self.boards[name]["paths"], x, y, w, h)

        steps = self.boards[name].get("steps", 0)
        sps = self.boards[name].get("sps", 0)
        stats_txt = f"Steps: {steps} | {sps} step/s"
        stats_label = self.app.small_font.render(stats_txt, True, (150, 150, 150))
        self.app.screen.blit(stats_label, (x, y + 25))

    def draw_results(self):
        app = self.app
        x, y = app.grid_area + 20, 20

        title = app.font.render("RACE RESULTS", True, (255, 255, 255))
        app.screen.blit(title, (x, y))
        y += 50

        colors = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]

        for i, (name, t) in enumerate(self.rankings):
            color = colors[i] if i < 3 else (220, 220, 220)
            prefix = f"#{i+1}"
            
            txt = f"{prefix} {name} - {t:.3f}s"
            label = app.small_font.render(txt, True, color)
            app.screen.blit(label, (x, y))
            y += 30

    def handle_events(self, events):
        for e in events:
            if self.stop_btn.is_clicked(e):
                self.stop_flag = True
                print("Stopping all algorithms...")

            if self.exit_btn.is_clicked(e):
                self.stop_flag = True
                from .menu import Menu
                self.app.state = Menu(self.app)