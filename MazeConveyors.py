def maze_solver_with_conveyors(maze: list[list[str]]) -> dict:
    import collections
    rows = len(maze)
    cols = len(maze[0])
    start_pos = None
    end_pos = None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start_pos = (r, c)
            elif maze[r][c] == 'E':
                end_pos = (r, c)

    if not start_pos or not end_pos:
        return {"distance": -1, "path": []}
    

    queue = collections.deque([(0, start_pos[0], start_pos[1], [list(start_pos)])])
    visited_distances = {}
    visited_distances[(start_pos[0], start_pos[1])] = 0
    

    directions = {'v': (1, 0), '^': (-1, 0), '>': (0, 1), '<': (0, -1),
                  'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

    while queue:
        distance, r, c, path = queue.popleft()
        
        if distance > visited_distances.get((r, c), float('inf')):
            continue

        if (r, c) == end_pos:
            return {"distance": distance, "path": path}
        
        for dr, dc in directions.values():
            next_r, next_c = r + dr, c + dc
            
            if not (0 <= next_r < rows and 0 <= next_c < cols):
                continue
            
            cell_type = maze[next_r][next_c]
            
            if cell_type == '#':
                continue
            
            if cell_type in ['.', 'S', 'E']:
                new_dist = distance + 1
                if new_dist < visited_distances.get((next_r, next_c), float('inf')):
                    visited_distances[(next_r, next_c)] = new_dist
                    new_path = path + [[next_r, next_c]]
                    queue.append((new_dist, next_r, next_c, new_path))
            elif cell_type in ['>', '<', '^', 'v']:
                conveyor_path = [list(path[-1])]  # Start with the cell before the conveyor
                current_r, current_c = r, c
                
                is_valid_conveyor_path = True
                while True:
                    current_r += dr
                    current_c += dc
                    
                    if not (0 <= current_r < rows and 0 <= current_c < cols):
                        is_valid_conveyor_path = False
                        break
                    
                    conveyor_path.append([current_r, current_c])
                    
                    if maze[current_r][current_c] == '#':
                        is_valid_conveyor_path = False
                        break
                    
                    if maze[current_r][current_c] in ['.', 'S', 'E']:
                        break
                    
                    if maze[current_r][current_c] in ['>', '<', '^', 'v']:
                        conveyor_char = maze[current_r][current_c]
                        dr, dc = directions[conveyor_char]
                
                if is_valid_conveyor_path:
                    final_r, final_c = conveyor_path[-1][0], conveyor_path[-1][1]
                    new_dist = distance + 1  # Cost of stepping onto the first conveyor cell
                    if new_dist < visited_distances.get((final_r, final_c), float('inf')):
                        visited_distances[(final_r, final_c)] = new_dist
                        new_path = path + conveyor_path[1:] # Add conveyor path, excluding the start point of conveyor
                        queue.appendleft((new_dist, final_r, final_c, new_path)) # Append to front for 0-cost moves
    
    return {"distance": -1, "path": []}


if __name__ == "__main__":
    maze = [
        ['S', '.', '>', '>', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 2, 'path': [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]}

    maze = [
        ['S', '.', '>', '#', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {"distance": -1, "path": []}


    maze = [
        ['S', '.', 'v', '.', 'E'],
        ['#', '#', 'v', '.', '#'],
        ['.', '.', 'v', '.', '.'],
        ['#', '#', '.', '.', '#'],
        ['.', '.', '.', '.', '.']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 7, 'path': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2], [3, 3], [2, 3], [1, 3], [0, 3], [0, 4]]}
