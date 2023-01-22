import collections
import numpy as np
from scatter_plots import scatter_slope_cartesian

"""
This runs a Breadth First Search on a maze
https://en.wikipedia.org/wiki/Breadth-first_search
https://stackoverflow.com/questions/47896461/get-shortest-path-to-a-cell-in-a-2d-array-in-python
"""

"""
Runs BSF algorithm on the maze file
"""
def run_bsf(grid):

    path = None;
    #definition, A is start point B is target
    wall, clear, goal, begin = "#", " ", "B", "A"

    # check grid size
    if(len(grid)< 1):
        print("Error: grid cannot be less than one element")
        return path;

    # find width and hieght of the grid
    width, height = len(grid[0]), len(grid)

    # find starting point
    i = 0
    j = -1
    for row in grid:
        if(begin in row):
            j = row.index(begin)
            break;
        i = i+ 1
    start = (j,i)
    if (j == -1):
        print("Error: Could not find starting point ", begin)
        return path;

    queue = collections.deque([[start]])
    seen = set([start])
    index = 1
    while queue:
        path = queue.popleft()
        index = index + 1
        #print(path)
        x, y = path[-1]
        if grid[y][x] == goal:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height:
                try:
                    if grid[y2][x2] != wall and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))
                except:
                    #print("Error: out of index ", x2,y2)
                    continue

    print("Calculated " + index + " paths to find destination")
    return(path)

"""
Create maze file from the matrix file, with default start as Artemis landing site and end as Shakelton Crater
"""
def create_maze_file(matrix_filename, matrix_n, maze_filename, slope_cutoff, start_coordinate = [-89.1, 55], end_coordinate = [-89.2, 120] ):

    from angle_calculations import closest_point
    landing_site_x_y = start_coordinate
    destination_site_x_y = end_coordinate

    pts = np.loadtxt(np.DataSource().open(matrix_filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    (landing_x, landing_y, landing_index) = closest_point(landing_site_x_y[0], landing_site_x_y[1], lat_list, long_list)
    (destination_x, destination_y, destination_index) = closest_point(destination_site_x_y[0], destination_site_x_y[1],lat_list, long_list)
    print("landing_x_y", landing_x, " ", landing_y)
    print("destination_x_y", destination_x, " ", destination_y)

    all_lines = ""
    for index in range(len(lat_list)):
            if (lat_list[index] == landing_x and long_list[index] == landing_y):
                all_lines = all_lines + "A"  # start point
            elif (lat_list[index] == destination_x and long_list[index] == destination_y):
                all_lines = all_lines + "B"  # end point
            elif (slope_list[index] < slope_cutoff):
                all_lines = all_lines + " "
            else:
                all_lines = all_lines + "#"

            if ((index + 1) % matrix_n == 0):
                all_lines = all_lines + "\n"

    #print(all_lines)
    maze_file = open(maze_filename, 'w')
    maze_file.write(all_lines + '\n')
    maze_file.close()
    print(maze_filename + " was created")


"""
takes the path from run_bsf() and reads the csv file, identifies 
corresponding indexes in the matrix_300_300_spherical_zoom.csv and writes the
coordinates into the rover_path.csv file
"""
def save_rover_path(path, matrix_file, matrix_n, rover_path_output_file):

    index_list = []
    for element in path:
        (a, b) = element
        index_list.append(matrix_n * b + a)  # 300 matrix_n

    pts = np.loadtxt(np.DataSource().open(matrix_file), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    all_lines = ""
    for index in index_list:
        all_lines = all_lines + str(lat_list[index]) + "," + str(long_list[index]) + "," + str(height_list[index]) + "," + str(slope_list[index]) +"\n"

    maze_file = open(rover_path_output_file, 'w')
    maze_file.write(all_lines + '\n')
    maze_file.close()
"""
This function is used by the Jypyter notebook to run BSF and create plots
"""
def create_slope_plot(slope):
    matrix_n = 300
    matrix_file = "matrix_300_300_spherical_zoom.csv"
    maze_file = "rover_maze_temp.txt"
    rover_path_output_file = "rover_path_temp.csv"
    slope_cutoff = slope  # 15 or 20

    # step 1: create maze from matrix
    print ("Creating maze fie from the 300x300 matrix...")
    create_maze_file(matrix_file, matrix_n, maze_file, slope_cutoff)
    # step 2: Find the best path in maze
    f = open(maze_file)
    print("Calculating path using BFS algorithm...")
    grid = f.readlines()
    path = run_bsf(grid)
    # step 3: save the best path to a lat, long file
    print("Saving Rover path to a csv file...")
    save_rover_path(path, matrix_file, matrix_n, rover_path_output_file)
    print("Plotting path...")
    # step 4: plot the path in matplotlib
    scatter_slope_cartesian(matrix_file, slope_cutoff, rover_path_output_file)
"""
A simple grid for debugging BSF
"""
def debug_grid():
    test_grid = ["          ",
                 "  ##   ## ",
                 "  ## A ## ",
                 "     ###  ",
                 "B         "]

    path = run_bsf(test_grid)
    print("----  Final Path --------")
    print("expected: [(5, 2), (4, 2), (4, 3), (3, 3), (2, 3), (1, 3), (0, 3), (0, 4)]")
    print("received:", path)
    # path is [(5, 2), (4, 2), (4, 3), (3, 3), (2, 3), (1, 3), (0, 3), (0, 4)]


"""
Creates matplotlib plots for all possible rover slopes (10 to 20) and stores them as png file for comparison
"""
def create_all_slope_plots():
    matrix_n = 300
    matrix_file = "matrix_300_300_spherical_zoom.csv"
    maze_file = "rover_maze_temp.txt"
    rover_path_output_file = "rover_path_temp.csv"

    # all slopes slope_cutoff = 20  # 15 or 20
    slope_list = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    for slope in slope_list:
        # step 1: create maze from matrix
        create_maze_file(matrix_file, matrix_n, maze_file, slope)
        # step 2: Find best path in maze
        f = open(maze_file)
        grid = f.readlines()
        path = run_bsf(grid)
        # step 3: save best path to a lat, long file
        save_rover_path(path, matrix_file, matrix_n, rover_path_output_file)
        # step 4: plot the path in matplotlib
        plot_file = "final_plots\\" + "rover_path_" + str(slope) + ".png"
        scatter_slope_cartesian(matrix_file, slope, rover_path_output_file, save_plot_file=plot_file)
        f.close()


def main():
    #debug_grid()
    #create_all_slope_plots()
    create_slope_plot(15)

    matrix_n = 300
    matrix_file = "matrix_300_300_spherical_zoom.csv" # sprecial zoom matrix file to create maze
    maze_file = "rover_maze.txt"  # temporary maze file
    rover_path_output_file = "rover_path.csv"
    slope_cutoff = 15  # 11 to 20, rover slope

    # step 1: create maze from matrix
    create_maze_file(matrix_file, matrix_n, maze_file, slope_cutoff)
    # step 2: Find best path in maze
    f = open(maze_file)
    grid = f.readlines()
    path = run_bsf(grid)
    # step 3: save best path to a lat, long file
    save_rover_path(path, matrix_file, matrix_n, rover_path_output_file)
    # step 4: plot the path in matplotlib in cartesian coordinate
    scatter_slope_cartesian(matrix_file, slope_cutoff, rover_path_output_file,convert_to_cartesian = True)
    pass

if __name__ == "__main__":
    main()


