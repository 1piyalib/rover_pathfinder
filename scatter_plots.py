import numpy as np
import matplotlib.pyplot as plt
import csv
import math
import os
from angle_calculations import spherical_to_cartesion, spherical_to_cartesion_list, closest_point, spherical_to_cartesion_list2

######    Sets the size of plots ######
plt.rcParams['figure.figsize'] = [15, 10]
plt.rcParams['figure.dpi'] = 100 # 200 e.g. is really fine, but slower

landing_site = [-89.1,55] #[-89.15,56] #[-89.232,54.794]
dest_site = [-89.200,120]
LUNAR_RADIUS = 1737.4 * 1000 #meter

"""
Gets polar coordinates for the polar scatter graph
"""
def get_polar_coordinate(lattitude, longitude):
    # convert longitude to theta (0-360) in radian
    # also polar scatter plot starts 0 theta at right hand side, it should be at the bottom for moon. So subtract 90 from theta
    if (longitude < 0):
        # theta is from 0-360.  -180W long =>  theta = 180, -90W long =>  theta = 270 also convert to radian deg * math.pi / 180
        theta = (((360 + longitude) * math.pi / 180) - math.pi / 2)
    else:
        # convert to radian
        theta= (((longitude) * math.pi / 180) - math.pi / 2)

    # radius is from zero scale (0 - max lattitude) by adding 90.  Latitude is -88S to -90S,
    r =(lattitude + 90)
    return(theta,r)
"""
Scatter slope plot in polar coordinate
Advantage: you can see as if it's on moon
"""
def scatter_slope_polar(filename):

    lat_list = []
    long_list = []
    r_list = []
    theta_list = []
    color = []

    f = open(filename, 'r')
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:

        # Read lattitude longitude slope from file
        lattitude = float(row[0])
        longitude = float(row[1])
        slope = float(row[3])
        #append to list
        lat_list.append(lattitude)
        long_list.append(longitude)

        theta, r = get_polar_coordinate(lattitude, longitude)
        theta_list.append(theta)
        r_list.append(r)

        if (slope <= 15):
            color.append("yellow")
        else:
            color.append("blue")

    """
    Print min/max values
    """
    print("lat min max: ",  min(lat_list), max(lat_list))
    print("long min max: ",  min(long_list), max(long_list))
    print("r min max: ",  min(r_list), max(r_list))
    print("theta min max: ",  min(theta_list), max(theta_list))

    """
    draw with landing and destination
    """
    ld_theta = []
    ld_r = []
    landing_theta, landing_r = get_polar_coordinate(landing_site[0], landing_site[1])
    ld_theta.append(landing_theta)
    ld_r.append(landing_r)
    dest_theta, dest_r = get_polar_coordinate(dest_site[0], dest_site[1])
    dest_theta_list = []
    dest_r_list = []
    dest_theta_list.append(dest_theta)
    dest_r_list.append(dest_r)

    """
    plot 
    """
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='polar')
    # r goes from 0 to one decimal above max r_list
    ax.set_ylim(0,math.ceil(max(r_list)*10)/10)
    ax.scatter(theta_list,r_list, color = color)
    ax.scatter(ld_theta, ld_r, color="red",s = 150, marker = "o")
    ax.scatter(dest_theta_list, dest_r_list, color="red",s = 200, marker = "*")
    #maximize plot
    #mng = plt.get_current_fig_manager()
    #mng.window.state('zoomed')
    #show
    plt.show()
"""
Scatter slope with lattitude/long in cartesian coordinate
Disadvantage: the axis does not show lattitude/longitude actual values
"""
def scatter_slope_polar_val_cartesian_coordinate(filename):
    lat_list = []
    long_list = []
    landing_dest_Lat_list = []
    landing_dest_Long_list = []

    color = []
    f = open(filename, 'r')
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        lattitude = float(row[0])
        longitude = float(row[1])
        slope = float(row[3])

        lat_list.append(lattitude)
        long_list.append(longitude)

        if (slope <= 15):
            color.append("yellow")
        else:
            color.append("blue")

    landing_dest_Lat_list.append(landing_site[0])
    landing_dest_Long_list.append(landing_site[1])
    landing_dest_Lat_list.append(dest_site[0])
    landing_dest_Long_list.append( dest_site[1])

    """
    Plot most significant data portion index 
    """
    plt.xlabel("latitude")
    plt.ylabel("longitude");
    plt.scatter(np.array(lat_list), np.array(long_list), color=color)
    # Put  landing and destination site as red star in the plot
    plt.scatter(np.array(landing_dest_Lat_list), np.array(landing_dest_Long_list), color="red", s=200, marker="*")
    plt.show()


def strf(val):
    return(str(round(val,1)))

"""
Scatter slope plot in cartesian coordinate
Disadvantage: the axis does not show lattitude/longitude actual values
"""
def scatter_slope_cartesian(filename, max_slope, rover_file_path = None, convert_to_cartesian = True, save_plot_file = None):

    """
    Get polar coordinates from file
    """
    print("Loading large lunar file ......")
    landing_dest_x_list = []
    landing_dest_y_list = []
    pts = np.loadtxt(np.DataSource().open(filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T
    print("Ploting Matplotlib graph......")
    """
    Convert to cartesian coordinates
    """
    if convert_to_cartesian:
        (x_list, y_list) = spherical_to_cartesion_list(lat_list,long_list,LUNAR_RADIUS)
    else:
        x_list = lat_list
        y_list = long_list

    """
    Convert to two lists, more_x_list > MAX_ROVER_SLOPE
    """
    more_x_list =[]
    more_y_list = []
    less_x_list = []
    less_y_list = []

    index =0
    for slope in slope_list:
        if (slope <= max_slope):
            less_x_list.append(x_list[index])
            less_y_list.append(y_list[index])
        else:
            more_x_list.append(x_list[index])
            more_y_list.append(y_list[index])
        index = index + 1

    color_less = "yellow"
    color_more = "blue"
    label_less = "slope below " + str(max_slope)
    label_more = "slope above " + str(max_slope)

    """
    Print min/max values
    """
    print("lat min max: ", min(lat_list), max(lat_list))
    print("long min max: ", min(long_list), max(long_list))

    """
    Convert destination and landing to cartesian
    """
    (x,y,z) =spherical_to_cartesion(landing_site[0], landing_site[1],LUNAR_RADIUS)
    landing_dest_x_list.append(x)
    landing_dest_y_list.append(y)
    (x, y, z) = spherical_to_cartesion(dest_site[0], dest_site[1], LUNAR_RADIUS)
    landing_dest_x_list.append(x)
    landing_dest_y_list.append(y)

    """
    Use rover path file (in spherical)
    """
    if rover_file_path != None:
        pts_rov = np.loadtxt(np.DataSource().open(rover_file_path), delimiter=",")
        rlat_list, rlong_list,rheight_list,rslope_list = pts_rov.T
        (rx_list, ry_list) = spherical_to_cartesion_list(rlat_list, rlong_list, LUNAR_RADIUS)

    """
    Plot 
    """
    plt.title("Slope between latitude " + strf(min(lat_list)) + "-" + strf(max(lat_list)) + " longitude " + strf(min(long_list)) + "-" + strf(max(long_list)))
    plt.xlabel("latitude in cartesian coordinate")
    plt.ylabel("longitude in cartesian coordinate");
    #plt.grid(color='green', linestyle='--', linewidth=0.2)

    plt.scatter(np.array(more_x_list), np.array(more_y_list), color=color_more,s= 1, label=label_more)
    plt.scatter(np.array(less_x_list), np.array(less_y_list), color = color_less, s=1, label = label_less)

    if rover_file_path != None:
        plt.scatter(np.array(rx_list), np.array(ry_list), color= "green", s= 30,label="rover path")

    # Put  landing and destination site as red star in the plot
    #plt.scatter(np.array(landing_dest_x_list), np.array(landing_dest_y_list), color="red", s=200, marker="*", label="landing and dest")
    plt.scatter(np.array([landing_dest_x_list[0]]), np.array([landing_dest_y_list[0]]), color="red", s=200, marker=">",label="landing")
    plt.scatter(np.array([landing_dest_x_list[1]]), np.array([landing_dest_y_list[1]]), color="red", s=200, marker="*",label="destination")

    plt.legend(loc = "upper left")
    # maximize plot
    
    #mng = plt.get_current_fig_manager()
    #mng.window.state('zoomed')
    if save_plot_file == None:
        plt.show()
    else:
        filename = os.path.abspath(save_plot_file)
        plt.savefig(filename)

"""
Scatter color plot of height
"""
def scatter_hieght_cartesian(filename):

    # min_height = -2872.0
    # max_height = 1958.0

    pts = np.loadtxt(np.DataSource().open(filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    x_list=[]
    y_list=[]
    z_list =[]
    color =[]

    """
       Convert to cartesian coordinates
       """
    (x_list, y_list,z_list) = spherical_to_cartesion_list2(lat_list, long_list, height_list)

    for height in height_list:
        #matplotlib colors
        #https://matplotlib.org/stable/gallery/color/named_colors.html

        if (height < -2500):
            color.append("darkgrey")
        elif (height >= -2500 and height < -2000):
            color.append("gray")
        elif (height >= -2000 and height <-1500):
            color.append("navy")
        elif (height >= -1500 and height < -1000):
            color.append("green")
        elif (height >= -1000 and height < -800):
            color.append("orange")
        elif (height >= -800 and height < -650):
            color.append("salmon")
        elif (height >= -650 and height < -500):
            color.append("lightcoral")
        elif (height >= -500 and height <0):
            color.append("cyan")
        elif (height >= 0 and height < 500):
            color.append("gold")
        elif (height >= 500 and height < 1000):
            color.append("chocolate")
        elif (height >= 1000 and height < 1500):
            color.append("lightcoral")
        else:
            color.append("firebrick")

    #check points
    plt.title("Height in colors")
    plt.xlabel("latitude in cartesian")
    plt.ylabel("longitude in cartesian");
    plt.scatter(np.array(x_list), np.array(y_list), color=color)
    plt.legend(loc="upper left")
    # maximize plot
    #mng = plt.get_current_fig_manager()
    #mng.window.state('zoomed')
    plt.show()

"""
Creates table from csv file
"""
def table_from_csv(csv_file, title = None):
    pts = np.loadtxt(np.DataSource().open(csv_file), delimiter=",")
    rows,columns = pts.shape

    column_label_list = []
    if columns == 4:
        column_label_list = ["Latitude","Longitude","Height","Slope"]
    elif columns == 3:
        column_label_list = ["Latitude","Longitude","Height"]
    else:
        for i in range(columns):
            column_label_list.append("col_" + str(i))

    row_label_list = []
    for i in range(rows):
            row_label_list.append(str(i))

    #table_2dVal = [["ab" for c in range(columns)] for r in range(rows)]
    table_2dVal = pts
    fig, ax = plt.subplots()
    ax.set_axis_off()
    table = ax.table(
        cellText=table_2dVal,
        rowLabels=row_label_list,
        colLabels=column_label_list,
        rowColours=["palegreen"] * rows,
        colColours=["palegreen"] * columns,
        cellLoc='center',
        loc='upper left')
    if title == None:
        title =csv_file.split(".")[0]
    ax.set_title(title,fontweight="bold")

    plt.show()

"""
Creates table from 2D list
"""
def table_from_data(column_label_list, table_2dVal, title = None):

    rows = len(table_2dVal)
    columns = len(table_2dVal[0])
    row_label_list = []
    for i in range(rows):
            row_label_list.append(str(i))
    fig, ax = plt.subplots()
    ax.set_axis_off()
    table = ax.table(
        cellText=table_2dVal,
        rowLabels=row_label_list,
        colLabels=column_label_list,
        rowColours=["palegreen"] * rows,
        colColours=["palegreen"] * columns,
        cellLoc='center',
        loc='upper left')
    ax.set_title(title,fontweight="bold")

    plt.show()

"""
Saves all png files final plots
"""
def create_matrix_plots():
    MAX_ROVER_SLOPE = 15
    rover_path_file = "rover_path.csv"
    files = [ 'matrix_300_300_spherical_all.csv','matrix_300_300_spherical_zoom.csv', 'matrix_300_300_cartesian.csv','lunar_data.csv']
    for filename in files:
        plot_file_name = "final_plots\\" + filename.replace(".csv",".png")
        convert_cartesian = True
        if "cartesian" in filename:
            convert_cartesian = False
        scatter_slope_cartesian(filename= filename, max_slope = MAX_ROVER_SLOPE, rover_file_path = rover_path_file,
                            convert_to_cartesian = convert_cartesian, save_plot_file=plot_file_name)



if __name__ == "__main__":
    
    MAX_ROVER_SLOPE = 15
    lunar_data_spherical_file = 'lunar_data.csv'  # the complete file provided by NASA
    lunar_data_spherical_matrix_zoom_file = 'matrix_300_300_spherical_zoom.csv'
    lunar_data_cartesian_file = 'lunar_data_cartesian.csv'
    lunar_data_cartesian_matrix_file = 'matrix_300_300_cartesian.csv'
    rover_path_file = 'rover_path.csv'

    """
    Zoom spherical matrix plot with rover path, converted to cartesian 
    """
    scatter_slope_cartesian(lunar_data_cartesian_matrix_file, MAX_ROVER_SLOPE, rover_path_file,convert_to_cartesian = True)
    """
    The original NASA file (cartesian) 
    """
    scatter_slope_cartesian(lunar_data_cartesian_matrix_file, MAX_ROVER_SLOPE, rover_file_path = rover_path_file, convert_to_cartesian = False)
    """
    Slope scatter plot with rover path, uses the original large nasa file with coordinates converted to cartesian
    """
    scatter_slope_cartesian(lunar_data_spherical_file, MAX_ROVER_SLOPE, rover_path_file, convert_to_cartesian=True)

    """
    Tables
    """
    # table_from_data(["col1","col2"],[[11,12],[21,22]], "test_table")
    # table_from_csv()



