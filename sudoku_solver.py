def is_valid_placement(grid, row, col, num):
    for x in range(5):
        if grid[row][x] == num:
            return False
    
    # Check column
    for x in range(5):
        if grid[x][col] == num:
            return False
    
    return True

def is_valid_grid(grid):
    for row in range(5):
        seen = set()
        for col in range(5):
            if grid[row][col] != 0:
                if grid[row][col] in seen or grid[row][col] < 1 or grid[row][col] > 5:
                    return False
                seen.add(grid[row][col])
    
    # Check each column
    for col in range(5):
        seen = set()
        for row in range(5):
            if grid[row][col] != 0:
                if grid[row][col] in seen or grid[row][col] < 1 or grid[row][col] > 5:
                    return False
                seen.add(grid[row][col])
    
    return True

def find_empty(grid):
    for i in range(5):
        for j in range(5):
            if grid[i][j] == 0:
                return (i, j)
    return None

def solve_sudoku(grid):
    empty_pos = find_empty(grid)
    if not empty_pos:
        return True
    
    row, col = empty_pos
    
    # Try digits 1-5
    for num in range(1, 6):
        # Check if valid
        if is_valid_placement(grid, row, col, num):
            # Make tentative assignment
            grid[row][col] = num
            
            # Recursively try to solve rest of grid
            if solve_sudoku(grid):
                return True
            
            # If assignment doesn't lead to solution, backtrack
            grid[row][col] = 0
    
    # No solution found
    return False

def count_solutions(grid, max_count=2):
    """
    Count solutions for the Sudoku grid up to max_count.
    
    Args:
        grid (list): The 5x5 Sudoku grid
        max_count (int): Maximum number of solutions to find
        
    Returns:
        int: Number of solutions found (up to max_count)
    """
    # First check if the grid is valid
    if not is_valid_grid(grid):
        return 0
    
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
                if is_valid_placement(grid, row, col, num):
                    grid[row][col] = num
                    backtrack(next_row, next_col)
                    grid[row][col] = 0  # Backtrack
    
    backtrack()
    return len(solutions)

def has_unique_solution(grid):
    if not is_valid_grid(grid):
        return False, None  # Invalid grid
    
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

def get_solution(puzzle):
    if not is_valid_grid(puzzle):
        return 'invalid', None
    
    unique, solution = has_unique_solution(puzzle)
    
    if unique:
        return 'valid', solution
    elif solution is None:
        return 'no_solution', None
    else:
        return 'multiple', None

# Example usage
def main(puzzle):
    status, solution = get_solution(puzzle)    
    if status == 'valid':
#         print("\nUnique Solution:")
#         for row in solution:
#             print(row)
#         print("\nSolution as List of Lists:")
        return(solution)
    elif status == 'invalid':
        print("\nThe puzzle is invalid! It contains duplicates in rows or columns.")
    elif status == 'no_solution':
        print("\nThe puzzle has no solution.")
    else:  # multiple
        print("\nThe puzzle has multiple solutions.")

        

puzzle = [[0, 0, 0, 0, 0],
          [4, 0, 3, 0, 2],
          [1, 4, 0, 0, 0],
          [0, 0, 2, 0, 5],
          [5, 0, 4, 0, 0]]	
puzzle = [[0, 0, 4, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 2, 0, 0, 0], [0, 3, 0, 0, 2]]

solved_puzzle = main(puzzle)
test_sol = [[2, 5, 4, 1, 3], [3, 4, 1, 2, 5], [5, 1, 2, 3, 4], [4, 2, 3, 5, 1], [1, 3, 5, 4, 2]]	
print(solved_puzzle)
print(solved_puzzle==test_sol)

#Empty cells
zero_count = sum(cell == 0 for row in puzzle for cell in row)
print("Number of zeros (empty cells):", zero_count)