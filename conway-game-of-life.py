#!/usr/bin/env python3

import sys
import time
from typing import List, Set, Tuple

def parse_args() -> Tuple[int, int, int]:
    """Parses command-line arguments for grid size and generations."""
    if len(sys.argv) != 4:
        print("Usage: python game_of_life.py [rows] [cols] [generations]")
        sys.exit(1)
    try:
        rows = int(sys.argv[1])
        cols = int(sys.argv[2])
        generations = int(sys.argv[3])
        if rows <= 0 or cols <= 0 or generations <= 0:
            raise ValueError
        return rows, cols, generations
    except ValueError:
        print("Arguments must be positive integers.")
        sys.exit(1)

def initialize_grid(rows: int, cols: int) -> Set[Tuple[int, int]]:
    """Initializes the grid with user-defined live cells."""
    live_cells = set()
    print("Initialize the grid:")
    print("1. Random configuration")
    print("2. Manual input")
    choice = input("Select an option (1 or 2): ").strip()
    if choice == '1':
        from random import randint
        density = input("Enter the density of live cells (0.0 to 1.0): ").strip()
        try:
            density = float(density)
            if not 0.0 <= density <= 1.0:
                raise ValueError
        except ValueError:
            print("Invalid density value. Using default density of 0.2.")
            density = 0.2
        for i in range(rows):
            for j in range(cols):
                if randint(0, 100) / 100.0 < density:
                    live_cells.add((i, j))
    elif choice == '2':
        print("Enter live cell coordinates (row and column), one per line.")
        print("When finished, enter an empty line.")
        while True:
            coords = input("Cell (row col): ").strip()
            if coords == '':
                break
            try:
                x_str, y_str = coords.split()
                x, y = int(x_str), int(y_str)
                if 0 <= x < rows and 0 <= y < cols:
                    live_cells.add((x, y))
                else:
                    print("Coordinates out of bounds.")
            except ValueError:
                print("Invalid input. Please enter two integers separated by a space.")
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)
    return live_cells

def get_neighbors(cell: Tuple[int, int], rows: int, cols: int) -> List[Tuple[int, int]]:
    """Returns the neighboring cells of a given cell, considering grid boundaries."""
    x, y = cell
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                neighbors.append((nx, ny))
    return neighbors

def next_generation(live_cells: Set[Tuple[int, int]], rows: int, cols: int) -> Set[Tuple[int, int]]:
    """Calculates the next generation of live cells based on the current state."""
    new_live_cells = set()
    cells_to_check = live_cells.union(
        {neighbor for cell in live_cells for neighbor in get_neighbors(cell, rows, cols)}
    )
    for cell in cells_to_check:
        neighbors = get_neighbors(cell, rows, cols)
        live_neighbors = sum((neighbor in live_cells) for neighbor in neighbors)
        if cell in live_cells:
            if live_neighbors == 2 or live_neighbors == 3:
                new_live_cells.add(cell)
        else:
            if live_neighbors == 3:
                new_live_cells.add(cell)
    return new_live_cells

def display_grid(live_cells: Set[Tuple[int, int]], rows: int, cols: int) -> None:
    """Displays the current state of the grid."""
    grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    for x, y in live_cells:
        grid[x][y] = '█'
    print('\n' + '\n'.join(''.join(row) for row in grid) + '\n')

def run_simulation(rows: int, cols: int, generations: int) -> None:
    """Runs the Game of Life simulation."""
    live_cells = initialize_grid(rows, cols)
    prev_states = []
    for gen in range(generations):
        print(f"Generation {gen + 1}")
        display_grid(live_cells, rows, cols)
        time.sleep(0.5)
        new_live_cells = next_generation(live_cells, rows, cols)
        if new_live_cells == live_cells:
            print("Stable configuration reached. Simulation ends.")
            break
        if new_live_cells in prev_states:
            print("Oscillating configuration detected. Simulation ends.")
            break
        prev_states.append(live_cells)
        live_cells = new_live_cells
    else:
        print("Simulation completed after reaching the specified number of generations.")

def main() -> None:
    """Main function to start the simulation."""
    rows, cols, generations = parse_args()
    run_simulation(rows, cols, generations)

if __name__ == "__main__":
    main()