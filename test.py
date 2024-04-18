import math

def index_to_position(index, width):
    row = index // width
    col = index % width
    return row, col

def position_to_index(row, col, width):
    return row * width + col

def heuristic_cost_estimate(start, goal, width):
    start_row, start_col = index_to_position(start, width)
    goal_row, goal_col = index_to_position(goal, width)
    return math.sqrt((goal_row - start_row)**2 + (goal_col - start_col)**2)

def get_neighbors(index, width, height):
    row, col = index_to_position(index, width)
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < height and 0 <= new_col < width:
            neighbors.append(position_to_index(new_row, new_col, width))
    return neighbors

def a_star_pathfinding(start, goal, bricks, width, height):
    open_list = [start]
    closed_list = []
    came_from = {}

    g_score = {node: float('inf') for node in range(width * height)}  # Initialize all nodes
    g_score[start] = 0

    f_score = {node: float('inf') for node in range(width * height)}  # Initialize all nodes
    f_score[start] = heuristic_cost_estimate(start, goal, width)

    while open_list:
        current = min(open_list, key=lambda node: f_score[node])
        
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.insert(0, current)
            return path

        open_list.remove(current)
        closed_list.append(current)

        for neighbor in get_neighbors(current, width, height):
            if neighbor in closed_list or bricks[neighbor] == 1:
                continue

            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic_cost_estimate(neighbor, goal, width)

                if neighbor not in open_list:
                    open_list.append(neighbor)

    return None  # No path found

# Usage example
width = 6
height = 6
bricks = [0, 0, 0, 0, 1, 0,
          0, 1, 0, 0, 1, 0,
          0, 1, 1, 0, 1, 0,
          0, 0, 0, 0, 0, 0,
          0, 1, 1, 1, 1, 0,
          0, 0, 0, 0, 0, 0]

start = 5
goal = 35

path = a_star_pathfinding(start, goal, bricks, width, height)
print(path)