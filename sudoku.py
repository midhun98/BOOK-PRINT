import random
import copy

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
    
    # Perform some random row and column swaps (within the same block)
    # For 5x5 we just have single rows/columns as blocks
    for _ in range(10):
        # Swap rows
        r1, r2 = random.sample(range(5), 2)
        result[r1], result[r2] = result[r2], result[r1]
        
        # Swap columns
        c1, c2 = random.sample(range(5), 2)
        for i in range(5):
            result[i][c1], result[i][c2] = result[i][c2], result[i][c1]
    
    return result

def remove_numbers(grid, num_empty):
    """Remove numbers from the grid to create a puzzle."""
    puzzle = copy.deepcopy(grid)
    cells = [(i, j) for i in range(5) for j in range(5)]
    random.shuffle(cells)
    
    count = 0
    for i, j in cells:
        if count >= num_empty:
            break
        
        temp = puzzle[i][j]
        puzzle[i][j] = 0
        
        # Check if the puzzle still has a unique solution
        if has_unique_solution(puzzle, grid):
            count += 1
        else:
            puzzle[i][j] = temp
    
    return puzzle

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

def count_solutions(grid, solution, count=0, row=0, col=0):
    """Count the number of solutions for the grid."""
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
        return count_solutions(grid, solution, count, next_row, next_col)
    
    for num in range(1, 6):
        if is_valid(grid, row, col, num):
            grid[row][col] = num
            count = count_solutions(grid, solution, count, next_row, next_col)
            grid[row][col] = 0  # Backtrack
            
            if count > 1 or (count == 1 and grid != solution):
                return count
    
    return count

def has_unique_solution(grid, solution):
    """Check if the grid has a unique solution."""
    # We'll use a simple approach: check if there's more than one solution
    # or if the found solution differs from the expected one
    grid_copy = copy.deepcopy(grid)
    count = count_solutions(grid_copy, solution)
    return count == 1

def generate_sudoku(num_empty):
    """Generate a 5x5 Sudoku with the specified number of empty cells."""
    # Ensure num_empty is within reasonable bounds
    num_empty = min(max(0, num_empty), 24)  # At least one clue must remain
    
    # Create a solved grid
    solution = create_solved_grid()
    
    # Create a puzzle by removing numbers
    puzzle = remove_numbers(solution, num_empty)
    
    return puzzle, solution

def print_grid(grid):
    """Print the grid in a readable format."""
    for row in grid:
        print(row)

# Example usage
if __name__ == "__main__":
    # Generate a Sudoku with 15 empty cells
    puzzle, solution = generate_sudoku(20)
    
    print("Generated Puzzle:")
    print_grid(puzzle)
    
    print("\nSolution:")
    print_grid(solution)