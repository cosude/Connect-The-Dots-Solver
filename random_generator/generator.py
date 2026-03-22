import random


def generate_random_problem(rows, cols, num_pairs):
    all_coords = [(r, c) for r in range(rows) for c in range(cols)]

    sampled = random.sample(all_coords, num_pairs * 2)
    
    target_positions = []
    initial_grid = [["" for _ in range(cols)] for _ in range(rows)]
    
    char_code = ord('a')
    for i in range(0, len(sampled), 2):
        start = sampled[i]
        end = sampled[i+1]
        
        target_positions.append((start, end))
        
        initial_grid[start[0]][start[1]] = chr(char_code)
        initial_grid[end[0]][end[1]] = chr(char_code).upper()
        
        char_code += 1
        
    return target_positions, initial_grid