#Program: Quantum Robotics. Autonomous Navigation Test | University Rover Challenge
#Version: 1.0
#Developer: Emiliano Vivas Rodríguez
#Contact: a01424732@tec.mx
#Since: 2023/09/15

import pygame
import random
import math

class Rover:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.markers = []
        self.visited = []
        self.to_visit = []
        self.found = False
    
    def move(self):
        if not self.found:
            if not self.to_visit:
                new_x = random.randint(0, mars_surface_squared_size - 1)
                new_y = random.randint(0, mars_surface_squared_size - 1)
                while (new_x, new_y) in self.visited or (new_x, new_y) in self.markers:
                    new_x = random.randint(0, mars_surface_squared_size - 1)
                    new_y = random.randint(0, mars_surface_squared_size - 1)
                self.to_visit.append((new_x, new_y))
            destination_x, destination_y = self.to_visit.pop()
            distance = math.sqrt((destination_x - self.x) ** 2 + (destination_y - self.y) ** 2)
            if distance > 1:
                angle = math.atan2(destination_y - self.y, destination_x - self.x)
                velocity = 1
                dx = int(velocity * math.cos(angle))
                dy = int(velocity * math.sin(angle))
                self.x += dx
                self.y += dy
            else:
                self.x = destination_x
                self.y = destination_y
                if (self.x, self.y) in auxiliary_markers:
                    self.markers.append((self.x, self.y))
                    self.a_star()
            if (self.x, self.y) == goal_marker:
                    print(f"Information | Rover discovered the Goal ArUco Marker in coordenates ({self.x}, {self.y})")
                    self.found = True
            elif (self.x, self.y) not in self.visited:
                    self.visited.append((self.x, self.y))
            pygame.draw.rect(window, PATH_SURFACE_COLOR, [(MARGIN + GRID_SIDE) * self.x + MARGIN, (MARGIN + GRID_SIDE) * self.y + MARGIN, GRID_SIDE, GRID_SIDE])
    
    def a_star(self):
        opened_list = []
        closed_list = []
        fathers = {}
        costs = {}
        opened_list.append((self.x, self.y))
        costs[(self.x, self.y)] = 0
        while opened_list and not self.found:
            opened_list.sort(key=lambda grid: costs[grid] + self.heuristic(grid))
            current = opened_list.pop(0)
            closed_list.append(current)
            if current == goal_marker:
                path = []
                while current != (self.x, self.y):
                    path.append(current)
                    current = fathers[current]
                path.reverse()
                path = list(dict.fromkeys(path))
                path = [grid for grid in path if grid not in self.visited]
                path = [grid for grid in path if grid not in auxiliary_markers]
                path = [grid for grid in path if grid != goal_marker]
                for index in range(len(path) - 1):
                    current_distance = self.heuristic(path[index])
                    next_distance = self.heuristic(path[index + 1])
                    if next_distance > current_distance:
                        path = path[:index + 1]
                        break
                self.to_visit.extend(path)
            else:
                neighbors = self.create_neighbors(current)
                for neighbor in neighbors:
                    new_cost = costs[current] + math.sqrt((neighbor[0] - current[0]) ** 2 + (neighbor[1] - current[1]) ** 2)
                    if neighbor not in closed_list and (neighbor not in opened_list or new_cost < costs[neighbor]):
                        opened_list.append(neighbor)
                        costs[neighbor] = new_cost
                        fathers[neighbor] = current
    
    def heuristic(self, grid):
        return math.sqrt((grid[0] - self.x) ** 2 + (grid[1] - self.y) ** 2)

    def create_neighbors(self, grid):
        neighbors = []
        x, y = grid
        if x > 0 and (x - 1, y) not in self.visited and (x - 1, y) not in self.markers:
            neighbors.append((x - 1, y))
        if x < mars_surface_squared_size - 1 and (x + 1, y) not in self.visited and (x + 1, y) not in self.markers:
            neighbors.append((x + 1, y))
        if y > 0 and (x, y - 1) not in self.visited and (x, y - 1) not in self.markers:
            neighbors.append((x, y - 1))
        if y < mars_surface_squared_size - 1 and (x, y + 1) not in self.visited and (x, y + 1) not in self.markers:
            neighbors.append((x, y + 1))
        return neighbors
    
    def draw(self):
        pygame.draw.rect(window, ROVER_COLOR, [(MARGIN + GRID_SIDE) * self.x + MARGIN, (MARGIN + GRID_SIDE) * self.y + MARGIN, GRID_SIDE, GRID_SIDE])

if __name__ == "__main__":
    
    GRID_SIDE = 10
    MARGIN = 1
    MARS_SURFACE_COLOR = (255, 167, 38)
    OBJECTIVE_COLOR = (0, 0, 255)
    ROVER_COLOR = (0, 0, 0)
    PATH_SURFACE_COLOR = (205, 205, 205)
    AUXILIAR_COLOR = (0,255,0)
    FPS = 30
    PROGRAM_TITLE = "Quantum Robotics. Autonomous Navigation Test |  University Rover Challenge"

    print(PROGRAM_TITLE)
    rover = Rover()
    auxiliary_markers = []
    num_markers = int(input("Input | Number of Auxiliary ArUco Markers: "))
    mars_surface_squared_size = int(input("Input | Mars Surface Squared Size: "))
    goal_marker = None
    while not goal_marker:
        x = random.randint(0, mars_surface_squared_size - 1)
        y = random.randint(0, mars_surface_squared_size - 1)
        if (x, y) != (rover.x, rover.y) and (x, y) not in auxiliary_markers:
            goal_marker = (x, y)
    for i in range(num_markers):
        angle = random.uniform(0, 2 * math.pi)
        max_distance = min(goal_marker[0], mars_surface_squared_size - goal_marker[0], goal_marker[1], mars_surface_squared_size - goal_marker[1])
        medium_distance = max_distance / 2
        distance = random.uniform(medium_distance, max_distance)
        x = int(round(goal_marker[0] + distance * math.cos(angle)))
        y = int(round(goal_marker[1] + distance * math.sin(angle)))
        auxiliary_markers.append((x, y))
    pygame.init()
    window = pygame.display.set_mode((mars_surface_squared_size * (GRID_SIDE + MARGIN), mars_surface_squared_size * (GRID_SIDE + MARGIN)))
    icon_surface = pygame.Surface((32,32))
    icon_surface.fill((0,0,0))
    pygame.display.set_icon(icon_surface)
    pygame.display.set_caption(PROGRAM_TITLE)
    clock = pygame.time.Clock()
    print(f"Information | Goal ArUco Marker is located in coordenates ({goal_marker[0]}, {goal_marker[1]})")
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.KEYDOWN and rover.found:
                finished = True
        rover.move()
        window.fill(MARS_SURFACE_COLOR)
        print(f"Status |\tRover ({rover.x}, {rover.y})\t\tGoal ArUco ({goal_marker[0]}, {goal_marker[1]})")
        for grid in rover.visited:
            pygame.draw.rect(window, PATH_SURFACE_COLOR, [(MARGIN + GRID_SIDE) * grid[0] + MARGIN, (MARGIN + GRID_SIDE) * grid[1] + MARGIN, GRID_SIDE, GRID_SIDE])
        for marcador in auxiliary_markers:
            pygame.draw.rect(window, AUXILIAR_COLOR, [(MARGIN + GRID_SIDE) * marcador[0] + MARGIN, (MARGIN + GRID_SIDE) * marcador[1] + MARGIN, GRID_SIDE, GRID_SIDE])
        pygame.draw.rect(window, OBJECTIVE_COLOR, [(MARGIN + GRID_SIDE) * goal_marker[0] + MARGIN, (MARGIN + GRID_SIDE) * goal_marker[1] + MARGIN, GRID_SIDE, GRID_SIDE])
        rover.draw()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
