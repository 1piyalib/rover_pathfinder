import plotly.graph_objects as go
import numpy as np
from angle_calculations import spherical_to_cartesion_list2, spherical_to_cartesion_list

#https://plotly.com/python/3d-mesh/

LUNAR_RADIUS = 1737.4 * 1000 #meter

"""
Plotly mesh plot of lat, long and hiegt with rover path and communication links
"""
def mesh_plot_height_cartesian(data_filename, rover_filename = 'rover_path.csv'):

    """
    Read File Convert x,y,z to cartesian
    """
    pts = np.loadtxt(np.DataSource().open(data_filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    x_list = lat_list
    y_list = long_list
    z_list = height_list
    # z_list = np.multiply(z_list, -1)

    print("terrain height_min: ", round(min(height_list), 1), " height_max: ", round(max(height_list), 1))
    plot_data = [go.Mesh3d(x=np.array(x_list), y=np.array(y_list), z=np.array(z_list), colorscale="rainbow", intensity=z_list,opacity=0.9)]
    """
    Read rover path file
    """
    #https://plotly.com/python/3d-line-plots/
    if (rover_filename != None):
        pts = np.loadtxt(np.DataSource().open(rover_filename), delimiter=",")
        r_lat_list, r_long_list, r_height_list, r_slope_list = pts.T
        #the rover files is in sprecial, so always convert to cartesian
        r_x_list, r_y_list, r_height_list_temp = spherical_to_cartesion_list2(r_lat_list, r_long_list, r_height_list)
        r_height_list = np.multiply(r_height_list, -1)
        plot_data.append(go.Scatter3d(x=np.array(r_x_list), y=np.array(r_y_list), z=np.array(r_height_list), marker=dict(size=4, line=dict(width=2,color='white')),line = dict(color='white',width=2)))
        print("rover path height_min: ", round(min(r_height_list), 1), " height_max: ", round(max(r_height_list), 1))
    """
    Plot
    """
    print("Printing Plotly 3D mesh plaot. It may take some time ....")
    fig = go.Figure(data = plot_data)
    #  Plotly colors:
    # ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
    # 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
    # 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
    # 'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
    # 'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
    # 'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
    # 'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
    # 'orrd', 'oryel', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg',
    # 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor',
    # 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy',
    # 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar', 'spectral',
    # 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'tealrose',
    # 'tempo', 'temps', 'thermal', 'tropic', 'turbid', 'twilight',
    # 'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd'].
    """
    Plot layout
    """
    fig.update_layout(
        title='lattitude (x) longitude (y) and height (z) in cartesian coordinate with rover path',
        width=1400,
        height=1200,
        autosize=False,
        scene=dict(
            camera=dict(
                up=dict(
                    x=0,
                    y=0,
                    z=1
                ),
                eye=dict(
                    x=-.7,
                    y= 0,
                    z=-1.5,
                )
            ),
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode='manual',
        ),
        xaxis=dict(range=[min(x_list), max(x_list)], ),
        yaxis=dict(range=[min(y_list), max(y_list)])
    )

    # offline html file
    # go_offline.plot(fig,filename='lunar_3d_terrain_height.html',validate=True, auto_open=False)

    fig.show()

def mesh_plot_height_spherical(data_filename,rover_filename = 'rover_path.csv'):

    """
    Read File Convert x,y,z to cartesian
    """
    pts = np.loadtxt(np.DataSource().open(data_filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    # convert to cartesian
    x_list, y_list, z_list = spherical_to_cartesion_list2(lat_list, long_list, height_list)

    print("terrain height_min: ", round(min(height_list), 1), " height_max: ", round(max(height_list), 1))
    plot_data = [go.Mesh3d(x=np.array(x_list), y=np.array(y_list), z=np.array(z_list), colorscale="rainbow", intensity=z_list,opacity=0.9)]
    """
    Read rover path file
    """
    # https://plotly.com/python/3d-line-plots/

    if (rover_filename != None):
        pts = np.loadtxt(np.DataSource().open(rover_filename), delimiter=",")
        r_lat_list, r_long_list, r_height_list, r_slope_list = pts.T
        #the rover files is in sprecial, so always convert to cartesian
        r_x_list, r_y_list, r_height_list = spherical_to_cartesion_list2(r_lat_list, r_long_list, r_height_list)
        plot_data.append(go.Scatter3d(x=np.array(r_x_list), y=np.array(r_y_list), z=np.array(r_height_list), marker=dict(size=4, line=dict(width=2,color='white')),line = dict(color='white',width=2)))
        print("rover path height_min: ", round(min(r_height_list), 1), " height_max: ", round(max(r_height_list), 1))
    """
    Plot
    """
    fig = go.Figure(data = plot_data)

    """
    Plot layout
    """
    fig.update_layout(
        title='lattitude (x) longitude (y) and height (z) in cartesian coordinate with rover path',
        width=1400,
        height=1200,
        autosize=False,
        scene=dict(
            camera=dict(
                up=dict(
                    x=0,
                    y=0,
                    z=1
                ),
                eye=dict(
                    x=0,
                    y=0,
                    z=1.6,
                )
            ),
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode='manual',
        ),
        xaxis=dict(range=[min(x_list), max(x_list)], ),
        yaxis=dict(range=[min(y_list), max(y_list)])
    )

    # offline html file
    # go_offline.plot(fig,filename='lunar_3d_terrain_height.html',validate=True, auto_open=False)

    fig.show()


"""
Plotly mesh plot of lat, long and hiegt with rover path and communication links, with first person perspective
"""
def mesh_plot_height_camera_control(data_filename, convert_to_cartesian, rover_filename = None, camera = "default"):

    """
    Read File Convert x,y,z to cartesian
    """
    pts = np.loadtxt(np.DataSource().open(data_filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    if (convert_to_cartesian == True):
        x_list, y_list, z_list = spherical_to_cartesion_list2(lat_list, long_list, height_list)
        #z_list = np.abs(z_list)
    else:
        x_list = lat_list
        y_list = long_list
        z_list = height_list
        #z_list = np.multiply(z_list, -1)

    print ("terrain height_min: ", round(min(height_list),1), " height_max: ", round(max(height_list),1))
    plot_data = [go.Mesh3d(x=np.array(x_list), y=np.array(y_list), z=np.array(z_list), colorscale="rainbow", intensity=z_list,opacity=0.9)]
    """
    Read rover path file
    """
    #https://plotly.com/python/3d-line-plots/
    if (rover_filename != None):
        pts = np.loadtxt(np.DataSource().open(rover_filename), delimiter=",")
        r_lat_list, r_long_list, r_height_list, r_slope_list = pts.T
        #the rover files is in sprecial, so always convert to cartesian
        r_x_list, r_y_list, r_height_list = spherical_to_cartesion_list2(r_lat_list, r_long_list, r_height_list)
        plot_data.append(go.Scatter3d(x=np.array(r_x_list), y=np.array(r_y_list), z=np.array(r_height_list), marker=dict(size=4, line=dict(width=2,color='DarkSlateGrey')),line = dict(color='white',width=2)))
        print("rover path height_min: ", round(min(r_height_list), 1), " height_max: ", round(max(r_height_list), 1))
    """
    Plot
    """
    fig = go.Figure(data = plot_data)
    """
    Camera control
    """
    if camera == "default":
        camera_dict = dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.25, y=1.25, z=1.25)
        )
    elif camera == "lower_view":
        camera_dict = dict(
            eye=dict(x=2, y=2, z=0.1)
        )
    elif camera == "xz_plane":
        camera_dict = dict(
        eye=dict(x=0., y=2.5, z=0.)
    )
    elif camera == "from_above":
        camera_dict = dict(
        eye=dict(x=0., y=0., z=2.5)
    )
    elif camera == "zooming_in":
        camera_dict = dict(
        eye=dict(x=0.1, y=0.1, z=1.5)
    )
    elif camera == "looking_up":
        camera_dict = dict(
        center=dict(x=0, y=0, z=0.7),
    )
    else:
        print("Invalid camera " + camera)
        return

    # fig.update_layout(
    #     title='lattitude (x) longitude (y) and height (z) in cartesian coordinate with rover path and communication links',
    #     width=1400,
    #     height=1200,
    #     autosize=False,
    #     scene=dict(camera= camera_dict,
    #         aspectratio=dict(x=1, y=1, z=0.7),
    #         aspectmode='manual',
    #     ),
    #     xaxis=dict(range=[min(x_list), max(x_list)], ),
    #     yaxis=dict(range=[min(y_list), max(y_list)])
    # )
    fig.update_layout(
        title='lattitude (x) longitude (y) and height (z) in cartesian coordinate with rover path and communication links',
        width=1400,
        height=1200,
        autosize=False,
        scene=dict(
            camera=dict(
                up=dict(
                    x=0,
                    y=0,
                    z=1
                ),
                eye=dict(
                    x=0.1,
                    y=0.1,
                    z=1.5,
                )
            ),
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode='manual',
        ),
        xaxis=dict(range=[min(x_list), max(x_list)], ),
        yaxis=dict(range=[min(y_list), max(y_list)])
    )

    #offline html file
    #go_offline.plot(fig,filename='lunar_3d_terrain_height.html',validate=True, auto_open=False)

    fig.show()

if __name__ == "__main__":

    spherical_matrix_file = "matrix_300_300_spherical_all.csv"
    cartesian_matrix_file = "matrix_300_300_cartesian.csv"
    rover_file = 'rover_path.csv'
    lunar_data_sprical_zoom = 'matrix_300_300_spherical_zoom.csv'

    # Plot Height mesh plot from spherical matrix file converted to cartesian with rover path (more resolution at the center, less resolution at side)
    #mesh_plot_height_spherical(spherical_matrix_file, rover_filename=rover_file)

    # Plot Height mesh plot from cartesian matrix file with rover path (uniform resolution)
    mesh_plot_height_cartesian(cartesian_matrix_file, rover_filename=rover_file)

    # camera "default" "lower_view" "xz_plane" "from_above" "zooming_in" "looking_up"
    #mesh_plot_height_camera_control(spherical_matrix_file, convert_to_cartesian=True,rover_filename=rover_file, camera="xz_plane")








