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

As a part of the upcoming Artemis mission, NASA released a large dataset of the lunar south pole, including latitude, longitude, height, and slope. This data focuses on the area surrounding the designated landing and rover exploration sites near Shackleton Crater.
 I processed the raw data into an equally spaced and sequential matrix of latitude, longitude, height, and slope from the LRO satellite. I then converted this matrix into a go/no-go maze of the terrain and applied the Breadth First Search (BSF) and A* algorithms to find the optimal path. The terrain and path were plotted in 2D using Matplotlib and interactively displayed in 3D using Plotly. The results identified the minimum rover slope and viable paths.
 


