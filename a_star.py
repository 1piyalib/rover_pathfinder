# https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

import numpy as np
from scatter_plots import scatter_slope_cartesian

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            print(node_position)
            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

def create_maze_2D_list(matrix_filename, matrix_n, slope_cutoff):

    from angle_calculations import closest_point
    landing_site_x_y = [-89.1, 55]
    destination_site_x_y = [-89.2, 120]

    pts = np.loadtxt(np.DataSource().open(matrix_filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    (landing_x, landing_y, landing_index) = closest_point(landing_site_x_y[0], landing_site_x_y[1], lat_list, long_list)
    (destination_x, destination_y, destination_index) = closest_point(destination_site_x_y[0], destination_site_x_y[1],lat_list, long_list)
    print("landing_x_y", landing_x, " ", landing_y)
    print("destination_x_y", destination_x, " ", destination_y)

    maze_2D_list = []
    maze_one_row = []
    row_index =0
    column_index = 0
    for index in range(len(lat_list)):
            if (lat_list[index] == landing_x and long_list[index] == landing_y):
                start_index = (row_index,column_index)  # start point index tuple
            elif (lat_list[index] == destination_x and long_list[index] == destination_y):
                end_index = (row_index,column_index)  # start point index tuple  # end point

            if (slope_list[index] < slope_cutoff):
                maze_one_row.append(0)
            else:
                maze_one_row.append(1) #1 is no go

            column_index = column_index + 1
            if ((index + 1) % matrix_n == 0):
                maze_2D_list.append(maze_one_row)
                maze_one_row = []
                column_index = 0
                row_index = row_index + 1


    return(maze_2D_list, start_index, end_index)


def debug_astar():
    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]

    start = (1, 1)
    end = (8, 6)

    path = astar(maze, start, end)

    #print path
    row_num = 0
    column_num = 0
    path_str = ""
    for row in maze:
        for column in maze[0]:
            if (row_num,column_num) in path:
                path_str = path_str + "x "
            else:
                path_str = path_str + "  "
            column_num = column_num + 1

        path_str = path_str + "\n"
        column_num = 0
        row_num = row_num+ 1

    print(maze)
    print(path)
    print(path_str)
    pass



def main():
    #debug_astar()

    matrix_n = 300
    matrix_file = "matrix_300_300_spherical_zoom.csv"
    rover_path_output_file = "rover_path_temp.csv"
    slope_cutoff = 20  # 15 or 20
    (maze,start,end) = create_maze_2D_list(matrix_file, matrix_n, slope_cutoff)
    start = (100,20)
    end = (100,100)
    path = astar(maze, start, end)
    print(path)

if __name__ == '__main__':
    main()