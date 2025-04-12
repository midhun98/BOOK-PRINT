def is_valid(grid, row, col, num):
    """
    Check if placing a number at a position is valid.
    
    Args:
        grid (list): The 5x5 Sudoku grid
        row (int): Row index
        col (int): Column index
        num (int): Number to check (1-5)
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Check row
    for x in range(5):
        if grid[row][x] == num:
            return False
    
    # Check column
    for x in range(5):
        if grid[x][col] == num:
            return False
    
    return True

def find_empty(grid):
    """
    Find an empty cell in the grid.
    
    Args:
        grid (list): The 5x5 Sudoku grid
        
    Returns:
        tuple: (row, col) of empty cell, or None if no empty cells
    """
    for i in range(5):
        for j in range(5):
            if grid[i][j] == 0:
                return (i, j)
    return None

def solve_sudoku(grid):
    """
    Solve the Sudoku grid using backtracking.
    
    Args:
        grid (list): The 5x5 Sudoku grid
        
    Returns:
        bool: True if solved, False if no solution
    """
    # Find empty location
    empty_pos = find_empty(grid)
    
    # If no empty positions are left, puzzle is solved
    if not empty_pos:
        return True
    
    row, col = empty_pos
    
    # Try digits 1-5
    for num in range(1, 6):
        # Check if valid
        if is_valid(grid, row, col, num):
            # Make tentative assignment
            grid[row][col] = num
            
            # Recursively try to solve rest of grid
            if solve_sudoku(grid):
                return True
            
            # If assignment doesn't lead to solution, backtrack
            grid[row][col] = 0
    
    # No solution found
    return False

def count_solutions(grid, max_count=50):
    """
    Count solutions for the Sudoku grid up to max_count.
    
    Args:
        grid (list): The 5x5 Sudoku grid
        max_count (int): Maximum number of solutions to find
        
    Returns:
        int: Number of solutions found (up to max_count)
    """
    solutions = []
    
    def backtrack(row=0, col=0):
        if len(solutions) >= max_count:
            return
        
        if row == 5:
            # Found a solution, deep copy the grid and add to solutions
            solutions.append([row[:] for row in grid])
            return
        
        # Calculate next position
        next_row = row + (col + 1) // 5
        next_col = (col + 1) % 5
        
        if grid[row][col] != 0:
            # Cell is already filled, move to next cell
            backtrack(next_row, next_col)
        else:
            # Try each number 1-5
            for num in range(1, 6):
                if is_valid(grid, row, col, num):
                    grid[row][col] = num
                    backtrack(next_row, next_col)
                    grid[row][col] = 0  # Backtrack
    
    backtrack()
    return len(solutions)

def has_unique_solution(grid):
    """
    Check if the grid has a unique solution.
    
    Args:
        grid (list): The 5x5 Sudoku grid
        
    Returns:
        tuple: (bool, solution) - True if unique solution exists along with the solution,
               False otherwise (None for solution if no unique solution)
    """
    # Create a copy to avoid modifying the original
    grid_copy = [row[:] for row in grid]
    
    # Count solutions (stop after finding 2 to save time)
    num_solutions = count_solutions(grid_copy, max_count=2)
    
    if num_solutions == 1:
        # If unique solution exists, solve again to get the solution
        solution = [row[:] for row in grid]
        solve_sudoku(solution)
        return True, solution
    elif num_solutions == 0:
        return False, None  # No solution
    else:
        return False, None  # Multiple solutions

def print_grid(grid):
    """
    Print the grid in a readable format.
    
    Args:
        grid (list): The 5x5 Sudoku grid
    """
    for row in grid:
        print(row)

def main():
    # Example puzzle input
    puzzle = [[4, 2, 5, 0, 2],
            [0, 5, 3, 0, 0],
            [2, 3, 4, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 4, 0, 0, 0]]

    
    print("Input Puzzle:")
    print_grid(puzzle)
    
    unique, solution = has_unique_solution(puzzle)
    
    if unique:
        print("\nThe puzzle has a unique solution:")
        print_grid(solution)
    elif solution is None:
        print("\nThe puzzle has no solution.")
    else:
        print("\nThe puzzle has multiple solutions.")

if __name__ == "__main__":
    main()

# You can also use this to check any 5x5 Sudoku puzzle
# Just replace the "puzzle" variable with your input grid