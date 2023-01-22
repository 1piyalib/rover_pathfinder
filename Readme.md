Python Files
-------------

angle_calculations.py -  functions for distance, spherical and cartesian coordinate conversions, and azimuth and elevation angles from the formula provided in the handbook

create_sherical_matrix_and_maze.py - creates 300x300 matrix with lat,long,height, slope and the maze file

maze_bfs.py - takes the maze file and applies BFS algorithm to find the rover path

scatter_plots.py - all matplotlib scatter and line plots

terrain_plotly_meash.py - 3D mesh plots using plotly

csv files
----------

lunar_data.csv - original lunar data file with latitude, longitude, height and slope

matrix_300_300_cartesian.csv - 300x300 matrix in cartesian coordinates

matrix_300_300_spherical.csv - 300x300 matrix in spherical coordinates (lat, long,radius)

rover_maze.txt - maze text file with go/no-go cells for input to BFS algorithm (slop cutoff = 15)

rover_maze_slope20.txt - maze text file with go/no-go cells for input to BFS algorithm (slop cutoff = 20)

rover_path.csv - rover path array in latitude, longitude (slope =15)

