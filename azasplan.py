#!/usr/bin/env python
# coding: utf-8
import utm
# # A_star
from enum import Enum
from queue import PriorityQueue
import numpy as np
import math
from skimage.morphology import medial_axis
from skimage.util import invert
# In[15]:
def grid(file, altitude, safe_dist):
        min_north= np.floor(min(file[:,0]-file[:,3])) #subtract x- delta_x and take the minimum
        max_north= np.ceil(max(file[:,0]+file[:,3])) #add x+ delta_x
        min_east= np.floor(min(file[:,1]-file[:,4])) #subtract y- delta_y and take the minimum
        max_east= np.ceil(max(file[:,1]+file[:,4])) #add y+ delta_y
        
        #create grid 
        north_size= int(np.ceil(max_north- min_north))
        east_size= int(np.ceil(max_east- min_east))
        grid = np.zeros((north_size,north_size))
        
        for i in range(file.shape[0]):
            x , y, z, d_x , d_y, d_z= file[i,:]
            if z+d_z+safe_dist >altitude:
                collision=[int(np.clip(x-d_x-safe_dist-min_north, 0, north_size-1) ), #minimum north or  x axis of obstacle in graph
                          int(np.clip(x+d_x+safe_dist-min_north, 0, north_size-1)), #maximum north or  x axis of obstacle in graph
                          int(np.clip(y-d_y-safe_dist-min_east,0, east_size-1)), #minimum east or  y axis of obstacle in graph
                          int(np.clip(y+d_y+safe_dist-min_east,0, east_size-1))
                    
                ] # 4 position indicies points that forms a square of obstacle area in grid
                grid[collision[0]:collision[1]+1,collision[2]:collision[3]+1]=1
                
        return grid, int(min_north), int(min_east)
    
def grid_edit(file, altitude, safe_dist):
        min_north= np.floor(min(file[:,0]-file[:,3])) #subtract x- delta_x and take the minimum
        max_north= np.ceil(max(file[:,0]+file[:,3])) #add x+ delta_x
        min_east= np.floor(min(file[:,1]-file[:,4])) #subtract y- delta_y and take the minimum
        max_east= np.ceil(max(file[:,1]+file[:,4])) #add y+ delta_y
        
        
        #create grid 
        north_size= int(np.ceil(max_north- min_north))
        east_size= int(np.ceil(max_east- min_east))
        grid = np.zeros((north_size,north_size))
        
        for i in range(file.shape[0]):
            x , y, z, d_x , d_y, d_z, alt= file[i,:]
            if abs(alt)+safe_dist > altitude:
                collision=[int(np.clip(x-d_x-safe_dist-min_north, 0, north_size-1) ), #minimum north or  x axis of obstacle in graph
                          int(np.clip(x+d_x+safe_dist-min_north, 0, north_size-1)), #maximum north or  x axis of obstacle in graph
                          int(np.clip(y-d_y-safe_dist-min_east,0, east_size-1)), #minimum east or  y axis of obstacle in graph
                          int(np.clip(y+d_y+safe_dist-min_east,0, east_size-1))
                    
                ] # 4 position indicies points that forms a square of obstacle area in grid
                grid[collision[0]:collision[1]+1,collision[2]:collision[3]+1]=1
                
        return grid, int(min_north), int(min_east)

from enum import Enum #i will use this library for my class to inharet some properties from
from queue import PriorityQueue
import numpy as np
from skimage.morphology import medial_axis
from skimage.util import invert
import utm
import numpy as np


# 
# ## 1) Actions 

# In[2]:


class Actions(Enum): 
    
    """
    every action has delta value for either direction in x or y, and cost for performing the action, that is relative to current position
    """
    left=(0,-1,-1)#west
    right=(0,1,-1)#east
    up=(-1,0,-1)#north
    down=(1,0,-1)#down
    NORTH_WEST = (-1, -1, -np.sqrt(2))
    NORTH_EAST = (-1, 1, -np.sqrt(2))
    SOUTH_WEST = (1, -1, -np.sqrt(2))
    SOUTH_EAST = (1, 1, -np.sqrt(2))
   

    @property
    def delta(self):
        # since delta is the delta of both x and y, so it's a tuple of first 2 values of any action
        return (self.value[0], self.value[1]) #note that .value is an inherated attribute from enum
    @property
    def cost(self):
        return self.value[2]


# ### 1.1) validate action

# In[3]:


"""
now i will write a function that tesets the valid action, to pass it tothe A* algorithm
if the action is not valid the algorithm will exclude it from search

cases where action is not valid

1) if current x_position -1 <0
2) if current y_position -1 <0
3) current x_position +1 > row_size of grid -1
4) current y_position +1 > col_size of grid -1

so we need grid as input to this function beside our position

"""
def validate_action(grid, cur_pos):
    row_size, col_size= grid.shape[0]-1, grid.shape[1]-1 #note that .shpe() returns tuple with the 2 d dimensions
    x_position,y_position= cur_pos
    valid_actions=[Actions.up, Actions.down, Actions.left,Actions.right, Actions.NORTH_WEST,Actions.NORTH_EAST, Actions.SOUTH_WEST, Actions.SOUTH_EAST]
    if x_position -1 <0 or grid[x_position-1 , y_position]==1: #note i could have or-ed it with grid[x_position-1 , y]==1 if i will add obstacles in my array 
        valid_actions.remove(Actions.up)
    if y_position -1 <0 or grid[x_position , y_position-1]==1: 
        valid_actions.remove(Actions.left)
    if x_position +1 >  row_size or grid[x_position+1 , y_position]==1: 
        valid_actions.remove(Actions.down)
    if y_position +1 >col_size or grid[x_position, y_position+1]==1: 
        valid_actions.remove(Actions.right)
    if (x_position - 1 < 0 or y_position - 1 < 0) or grid[x_position - 1, y_position - 1] == 1:
        valid_actions.remove(Actions.NORTH_WEST)
    if (x_position - 1 < 0 or y_position + 1 > col_size) or grid[x_position - 1, y_position + 1] == 1:
        valid_actions.remove(Actions.NORTH_EAST)
    if (x_position + 1 > row_size or y_position - 1 < 0) or grid[x_position + 1, y_position - 1] == 1:
        valid_actions.remove(Actions.SOUTH_WEST)
    if (x_position + 1 > row_size or y_position + 1 > col_size) or grid[x_position + 1, y_position + 1] == 1:
        valid_actions.remove(Actions.SOUTH_EAST)
    return valid_actions


# # 2) Heuristic

# In[5]:


"""
in this section i will define heuristic function:
for the shortest path wich uses manhattan distance h = ||x_i-x_{goal}|| + ||y_i-y_{goal}||


"""

def H_s(cur_pos, goal_pos):
    Manhattan= np.linalg.norm(np.array(cur_pos) - np.array(goal_pos))
    return Manhattan



# ## 3) A* search

# In[4]:


def a_star(grid,H_s, start, goal):
    path=[]
    cost=0
    queue=PriorityQueue()
    queue.put((0, start)) #(cost, node)
    visited=set(start)
    parents_branch ={} #this is dictionary that will carry tuple of parent cost, action
    found_flag=0
    while not queue.empty():
        
        extract_node=queue.get()
        current_node =extract_node[1]
        if current_node==start:
            current_cost=0
        else:
            current_cost=parents_branch[current_node][0]
        if current_node==goal  :
            found_flag=1
            break
        else: 
            for action in validate_action(grid, current_node ):
                #extract the cost of x, y 
                movement_delta= action.delta
                next_node=(current_node[0]+movement_delta[0] , current_node[1]+movement_delta[1])
                G_s = current_cost+action.cost
                F_s= G_s - H_s(next_node, goal)
                
                # to avoid revisiting 
                if next_node not in visited:
                    visited.add(next_node)
                    parents_branch[next_node]=(G_s,current_node, action) #current node is parent node for next node
                    queue.put((F_s,next_node))
    if found_flag:
        cost=parents_branch[goal][0]
        path.append(goal)
        counter=goal
        while parents_branch[counter][1] !=start:
            path.append(parents_branch[counter][1])#action
            counter= parents_branch[counter][1] #parent
            
        path.append(parents_branch[counter][1]) #append start
    else:
        print("path not found")
    return path[::-1], cost


# # longest path

# # Geodetic to NED UTM

# In[6]:


#convert to cartesian from lat- long
(easting, northing, zone_number, zone_letter) = utm.from_latlon(30.050543, 31.360652)
#convert to NED to Geo
(latitude, longitude) = utm.to_latlon(easting, northing, zone_number, zone_letter)


# ## Global to local
# in this part i will convert (lat, long, alt) to (north, east, down) and measure the net distance between home position and displaced position

# In[12]:


def global_to_local(current_position, home_position):
    (east , north, _, _)=utm.from_latlon(current_position[0], current_position[1])
    (home_east , home_north, _, _)=utm.from_latlon(home_position[0], home_position[1])
    travelled = np.array([north - home_north, east - home_east, -(current_position[2] - home_position[2])])
    return travelled


# # Configure space
# 
# in this section I will create a map for my space including the feasible 0 and infeasible 1 areas, also adding an extra offster for safety.
# 
# this section is important because when planning a path, the drone is not just a point but it has a physical space that we should consider to avoid collision
# 
# this map derives it's data from collider.csv file which has 6 columns [x, y, z, delta_x , delta_y, delta_z] 
# 
# if we assumed drone is cube then, the x, y, z or north, east, altitude are the center of the drone and the height is z+(2*delta_z)
# 
# GOAL EXTRACT 2-D MAP
# 

# In[1]:





# # WayPoints extraction
# 
# 
# waypoints is not about passing every polly point in the grid to the autopilot, but it's about passing points where a change in direction is required, or by other means if we passed points x->y->z and all of them are in same line, then we could simply pass x and z only.
# 
# 
# to know if 3 points are in same straight line or not, then in 2-d their area should be zero, if their area is not zero then they are not in same straight line, but they can form trianglr.
# 
#     we can test if their area = 0 if determanint  [x_1 y_1 z_1
# 
#                                                    x_2 y_2 z_2
#                                               
#                                                    x_3 y_3 z_3]
#                                               
# equals zero.
# 
# this condition is sufficiant in 2-D but not enough in 3-D

# In the following part we will run the modified A* in the grid

# #### WAY POINT EXTRACTION  
# 
# colleniarety check
# 
# 
# Now that we have an array of path points, we are going to loop over every 3 consecutive  points in the path,if their determinant = 0 or roughly zero (epsilon) then we are going to drop the second point  

# In[7]:


def check_collinear(p1, p2, p3): #p3 for now equals 1 since altitude is constant 2-d
    epsilon=0.9
    mat=np.concatenate((p1, p2, p3),0)
    det = np.linalg.det(mat)
    return abs(det) < epsilon


# In[8]:


def point(p):
    return np.array([p[0], p[1], 1.]).reshape(1, -1) #1 since p[2] is the altitude that is constant, reshape(1,-1 ) to make sure the result is row vector


# In[11]:


def Waypointz(path):
    waypoints=[p for p in path]
    i=0
    if path is not None:
        while i< len(waypoints)-2:
            if check_collinear(point(waypoints[i]), point(waypoints[i+1]), point(waypoints[i+2])):
                waypoints.remove(waypoints[i+1])
            else:
                i+=1
    else:
        waypoints=path
        
    return waypoints


# # GRIDS TO GRAPH
# 
# 
# as we are planning for the drone movement, we have to put in consideration the degrees of freedom or constraints that we are controlling, such as the drone orientation, diagonal movement, 3-d movement... so adding all of these in the grid-based search will be computationaly expensive though grids assure that u find the optimal and complete path according to its accuracy,,, unlike grphs that doesn't represent the geometry with obstacles of plane but it represents the topology of the map and the edges(curved/straight/diagonal) that connects nodes (STATES) together

# ## medial axes
# image processing technique to identify skeleton of binary image, this will allow us to circle the space around the obstacle as edges that are feasible for the path,, it returns one pixel wide skeleton and imported from Scikit-Image library.

# In[14]:


def create_graph(grid):
    return medial_axis(invert(grid))


# ### according to this we can project out start and goal point to the nearest start and goal point that are in the feasible parts of the path in graph 

# In[6]:


def skel_start_goal(start, goal, skeleton):
    feasible_paths=skeleton.nonzero()
    coordinates=np.transpose(feasible_paths)
    skeleton_start_index= np.linalg.norm(np.array(start)- np.array(coordinates), axis=1).argmin()
    skeleton_start=coordinates[skeleton_start_index]
    skeleton_goal_index= np.linalg.norm(np.array(goal)- np.array(coordinates), axis=1).argmin()
    skeleton_goal=coordinates[skeleton_goal_index]
    return skeleton_start, skeleton_goal
    


# ### To create the borders of the obstacle polygon, we will read from our map data and append the corner points of the polygon to shapely 

# In[46]:


def make_polygon(file): #remeber that file is the csv data of the field
    polygons=[] # in this list we will append all the polygons, evey polygon is represented by a tuple of 4 points (south_east,north_east,north_west, south_west)
    #as a reminder each row in file contains north, east , alt, d_x, d_y, d_z
    for row in file:
        north, east, alt, d_x, d_y, d_z =row
        
        north_min= north-d_x
        north_max= north+d_x
        east_min= east-d_y
        east_max= east+d_y
        alt_min= alt-d_z
        alt_max= alt+d_z
        
        south_east=(north_min, east_min)
        north_east= (north_max, east_min)
        north_west=(north_max, east_max)
        south_west=(north_min, east_max)
        
        coordinates=[south_east, north_east, north_west, south_west]
        
        poly= Polygon(coordinates)
        height= alt_max-alt_min
        polygons.append((poly, height))
        
    return polygons
        


# ## Random sampling search
# 
# In random sampling search, we are going to generate a random points through our map and check if they collide with obstacles or not

# In[48]:





# ## Remove samples colliding with obstacles

# In[60]:


def collision_filter(polygons, sample_point):
    for polygon, height in polygons:
        if polygon.contains(Point(sample_point)):# and height>= sample_point[2]:
            return True
    return False
            


# In[61]:


#now apply the collision filter on each point of the sample points




# In[124]:




# In[153]:


def points_in_polygons():
    polygon_coords = [np.array(poly[0].exterior.coords) for poly in polygons] #derives the 5 points coordinates of the polygon
    all_polygon_coords = np.concatenate(polygon_coords)                #flatten the coordinates [(1,2), (3,4) ...]
    unique_polygon_coords = np.unique(all_polygon_coords, axis=0)
    potential_points_idxs = tree.query_radius(unique_polygon_coords, r=10)
    # Iterate through potential points
    points_inside_polygons = []
    for polygon, potential_idxs in zip(polygons, potential_points_idxs):
        for idx in potential_idxs:
            point = Point(samples[idx])
            if polygon[0].contains(Point(point)) and polygon[1]>=drone_height:
                points_inside_polygons.append(point)
            


# In[ ]:




