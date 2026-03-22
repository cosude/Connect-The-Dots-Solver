import time
import os
from colorama import Fore, Back, Style, init

# Keep colors in the visualizer file ONLY
init(autoreset=True)
COLOR_MAP = {
    'a': Fore.RED, 'b': Fore.GREEN, 'c': Fore.BLUE, 
    'd': Fore.YELLOW, 'e': Fore.MAGENTA, 'f': Fore.CYAN,
    '.': Fore.BLACK + Style.DIM
}

class SearchVisualizer:
    def __init__(self, frame_skip=5, speed=0.01):
        self.count = 0
        self.frame_skip = frame_skip
        self.speed = speed
        self.start_time = time.time()

    def clear(self):
        # Moves cursor to top-left instead of full clear (prevents flickering)
        print("\033[H", end="")

    def draw(self, node):
        self.count += 1
        # Only draw every Nth state to keep performance high
        if self.count % self.frame_skip != 0:
            return

        self.clear()
        print(f"SEARCHING... States Explored: {Fore.CYAN}{self.count}")
        print(f"Current Depth: {Fore.YELLOW}{node.depth}{Style.RESET_ALL} | Time: {time.time()-self.start_time:.1f}s")
        
        # Build the grid string in memory first (much faster than printing cell by cell)
        output = []
        for row in node.state.board.grid:
            line = []
            for cell in row:
                char = cell if cell else "."
                color = COLOR_MAP.get(char.lower(), Fore.WHITE)
                line.append(f"{color}{char:2}")
            output.append("".join(line))
        
        print("\n".join(output))
        if self.speed > 0:
            time.sleep(self.speed)

if __name__ == "__main__":
    from engine import Board, State, generate_random_problem
    from solver import Astar, Heuristic  # Assuming your Astar now accepts a callback

    size, pairs = 12, 5
    targets, grid_data = generate_random_problem(size, size, pairs)
    initial_state = State(Board(size, size, targets, grid_data))

    # 1. Initialize the animator
    anim = SearchVisualizer(frame_skip=10, speed=0.01)

    # 2. Clear the screen once at the start
    print("\033[2J", end="") 

    # 3. Pass anim.draw as the callback!
    result = Astar(initial_state, Heuristic, weight=3.0, callback=anim.draw)

    if result:
        print(f"\n{Fore.GREEN}✔ SUCCESS! Path length: {result.path_cost}")