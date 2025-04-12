import random
import copy
import time

def create_solved_grid():
    """Create a solved 5x5 Sudoku grid."""
    # Start with a base pattern
    base = [
        [1, 2, 3, 4, 5],
        [3, 4, 5, 1, 2],
        [5, 1, 2, 3, 4],
        [2, 3, 4, 5, 1],
        [4, 5, 1, 2, 3]
    ]
    
    # Randomly permute the numbers
    numbers = list(range(1, 6))
    random.shuffle(numbers)
    mapping = {i+1: numbers[i] for i in range(5)}
    
    result = []
    for row in base:
        new_row = [mapping[num] for num in row]
        result.append(new_row)
    
    # Perform some random row and column swaps
    for _ in range(10):
        # Swap rows
        r1, r2 = random.sample(range(5), 2)
        result[r1], result[r2] = result[r2], result[r1]
        
        # Swap columns
        c1, c2 = random.sample(range(5), 2)
        for i in range(5):
            result[i][c1], result[i][c2] = result[i][c2], result[i][c1]
    
    return result

def is_valid(grid, row, col, num):
    """Check if placing a number at a position is valid."""
    # Check row
    for x in range(5):
        if grid[row][x] == num:
            return False
    
    # Check column
    for x in range(5):
        if grid[x][col] == num:
            return False
    
    return True

def count_solutions(grid, count=0, row=0, col=0):
    """Count the number of solutions for the grid up to 2."""
    if count > 1:
        return count  # Already found multiple solutions
    
    if row == 5:
        # Reached the end of the grid
        return count + 1
    
    # Calculate next position
    next_row = row + (col + 1) // 5
    next_col = (col + 1) % 5
    
    if grid[row][col] != 0:
        # Cell is already filled
        return count_solutions(grid, count, next_row, next_col)
    
    for num in range(1, 6):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            count = count_solutions(grid, count, next_row, next_col)
            grid[row][col] = 0  # Backtrack
            
            if count > 1:
                return count
    
    return count

def has_unique_solution(grid):
    """Check if the grid has a unique solution."""
    grid_copy = copy.deepcopy(grid)
    count = count_solutions(grid_copy)
    return count == 1

def generate_puzzle_with_exact_empty_cells(num_empty, timeout=30):
    """
    Generate a 5x5 Sudoku with exactly the specified number of empty cells.
    Ensures that the puzzle has a unique solution.
    
    Args:
        num_empty (int): Exact number of empty cells
        timeout (int): Maximum time in seconds to try generating a valid puzzle
    
    Returns:
        tuple: (puzzle, solution) as lists of lists, or (None, None) if timeout
    """
    # Ensure num_empty is within reasonable bounds
    num_empty = min(max(0, num_empty), 24)  # At least one clue must remain
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        # Create a solved grid
        solution = create_solved_grid()
        
        # Start with a full grid and randomly select cells to make empty
        puzzle = copy.deepcopy(solution)
        cells = [(i, j) for i in range(5) for j in range(5)]
        random.shuffle(cells)
        
        # Try to create a puzzle with exactly num_empty empty cells
        attempt_cells = cells[:num_empty]
        for i, j in attempt_cells:
            puzzle[i][j] = 0
        
        # Check if the puzzle has a unique solution
        if has_unique_solution(puzzle):
            return puzzle, solution
        
        # If we can't make a puzzle with exactly num_empty empty cells,
        # try a different arrangement of cells
    
    # If we couldn't generate a valid puzzle within the timeout
    return None, None

def test_maximum_empty_cells():
    """
    Test function to find the maximum number of empty cells that still allows
    a unique solution for a 5x5 Sudoku.
    """
    max_empty = 0
    for num_empty in range(15, 25):
        attempts = 5
        successes = 0
        
        for _ in range(attempts):
            puzzle, solution = generate_puzzle_with_exact_empty_cells(num_empty, timeout=10)
            if puzzle is not None:
                successes += 1
        
        success_rate = successes / attempts
        print(f"Empty cells: {num_empty}, Success rate: {success_rate * 100:.1f}%")
        
        if success_rate < 0.2:  # Less than 20% success rate
            break
        
        max_empty = num_empty
    
    print(f"Maximum practical number of empty cells: {max_empty}")

# Example usage
if __name__ == "__main__":
    # Generate a puzzle with exactly 15 empty cells
    num_empty = 5
    puzzle, solution = generate_puzzle_with_exact_empty_cells(num_empty)
    
    if puzzle is not None:
        print(f"Successfully generated puzzle with {num_empty} empty cells")
        print(puzzle) 
        print(solution)
        pass
        # To use elsewhere:
        # Do something with puzzle and solution...
    else:
        print(f"Failed to generate puzzle with {num_empty} empty cells")
    
    # Uncomment to find the maximum practical number of empty cells
    test_maximum_empty_cells()


# Start with a moderate difficulty (15 empty cells)
puzzle, solution = generate_puzzle_with_exact_empty_cells(15)
# Increase difficulty (more empty cells)
harder_puzzle, harder_solution = generate_puzzle_with_exact_empty_cells(18)
# Try an even harder puzzle (may take longer to generate)
very_hard_puzzle, very_hard_solution = generate_puzzle_with_exact_empty_cells(19)