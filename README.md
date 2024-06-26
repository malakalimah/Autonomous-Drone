# Path Planning and obstacle avoidance algorithm

Since we are talking about autonomous drones, then we have to consider
the main part of its autonomous behavior which is path planning.

To plan a path for anything, we should first know three major things,
where you are. Where do you want to go? How to get there?

In addition, to know the answers to these three major milestones we
used different things, for example, to know where you are we used GPS
with fusion with imu, to know where you are.

To know where you want to go, we used Google Maps APIs to geocode the
place where you want to go.

Finally, know how to get there we used the modified A\* algorithm, to create
a track that helps scan the field.

In the coming section, we are going to go through all these milestones
and know how we implemented them.

Figure 1 Path planning cycle
![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/8c1abd95-be96-44db-8387-903d845d65ba)

##  Localization

> Localization is mainly about knowing the location of your system in
> the world, or the space that it is in.\[41\]
>
> In our application since the drone will travel relatively in global
> spaces or frames as well as in local ones, like traveling from
> neighborhood A to neighborhood B as well as defining its location
> locally when it enters the region of neighborhood B; all these
> requirements require us to study its location locally and globally
>
> We used IMU to monitor and control the location changes of the drone
> relative to its inertial frame; also locally, we can define and
> monitor location of drone relative to working frame and nearby objects
> with computer vision.
>
> Globally, we used GNSS module:

- As its receiver has high sensitivity and assists more than one
  satellite system.

- Readily available with fair prices.

- Above all, of these since the drone will work in field so we have to
  choose a module that can define location for outdoor tasks, just as
  Neo-8m, so for example SLAM will not be serving for our application in
  this case.

> However, GNSS is not the only module that can help in global
> positioning, other alternatives can be RTK, LIDAR, PPP (Precise Point
> Positioning) or even SLAM and others, but they still have other
> constraints, or expensive expenses that might be required before
> deploying them in our system correctly.
>
> These constraints briefly can be like

- RTK requires a base station with known coordinates to provide
  real-time corrections for the drone receiver.

- PPP requires longer observation periods to achieve higher accuracy.

> Finally, to get high precision location data, IMU or inertial
> navigation system (INS) alone is not enough since it drifts over time,
> that requires data to be corrected from GNSS module, so a sensor
> fusion between imu and Neo-8m will be required to get accurate
> results. <u>In addition, this point is to be considered in our future
> work.</u>

### module that can define location for outdoor tasks, just as Neo-8m, so for GNSS module

#### How does GPS work

> With distance measurements from at least three satellites, the
> The receiver determines its position by finding the intersection of
> Spheres centered at each satellite with a radius equal to the
> calculated distance. Because one satellite only leads to infinite
> cloud points that a man could be in, and two intersected spheres from
> Two satellites lead to two points of intersection that a man could be
> in, but at least three spheres intersecting together will end up to
> one point of intersection that a man could be in.
>
> This method is called trilateration and that is how GPS defines your
> location.
>
>![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/a4f3b0f3-9dcf-476d-aae6-999ea3bf27f5)


#### NEO-M8N GNSS module 

> We used the Neo-M8N module to retrieve the position data from GNSS, note
> that Neo-M8N is not just a GPS, but GPS is one of the satellites that
> This GNSS (global navigation satellite system) module supports.
>
> That is because the GNSS module has concurrent reception for multiple GNSS
> like GPS, GLONASS, BeiDou, and Galileo.
>
> In addition, it is important to know that this GNSS sends an NMEA message
> that we will know more about it in [<u>next
>


#### NMEA sentence 

> NMEA stands for National Marine Electronics Association, which is a
> standard protocol created by the Navy so they can integrate different
> devices on board and communicate.
>
> ![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/6c8cdef4-2365-4f6b-a25e-018d2df36133)Basically,
> Every single NMEA sentence starts with a unique identifier which is
> “$” sign, followed by a string identifier that gives a combined ID to
> Which GNSS is sending this message, and which data arguments to expect
> From this sentence, for example, GPGGA is a string ID that combines
> talker id “GP” (GPS) with message-id “GGA” (Global positioning fix
> data) as shown in Figure 58 NMEA SentenceFigure 5 GGA sentence
>
> Finally, after streaming the defined data arguments that always have
> fixed arrangement of positions one after another in every different
> NMEA message ID, the NMEA line will end by Carriage return and line
> feed \<CR\>\<LF\>.
>
> ![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/7019c44f-8603-44d7-8cb1-cd34228f8c7b)


Figure  GGA sentence

#### NMEA decoding

> According to the defined structure of the NMEA message in the
> [<u>previous section</u>](#nmea-sentence), to extract a specific data
> like the latitude for example we first need to know, which message IDs
> that sends latitude among its data arguments, then where is the
> position in the latitude according to the sentence look up sequence,
> for example, in Figure 4, latitude is after the second comma, so
> splitting this comma separated sentence will lead to extracting
> arguments that we might be interested in.
>
> In our application, we mainly need latitude, longitude and
> course/heading/inclination angle; consequently, we choose to scrape
> the sentences that have message IDs of “GGA” and “RMC” since both of
> them has these data among their other different data arguments.
>
> ![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/cde4b292-d1c6-4269-955d-461b9dd3db6a)
So,
> following this logic will lead us to algorithm like the one
> illustrated in the following flow chart in Figure 6

##  Specify location with Google maps

> For a better user experience, we planned to use our beloved google
> maps to help us develop a good interface, that allows the user to add
> location pin where he wants his drone to arrive, then google maps APIs
> will help us in geocoding this location into a latitude and longitude,
> that can be projected into the field imaginary grids.
>
> Google maps offers a wide range of APIs for different purposes, such
> as

  1.  Maps API:

> Maps API mainly gives us insights into the following methods:

- Static maps

- Street view imagery

- Elevation

- Arial view and Map Tiles

  2.  Routes API

> Routes API mainly gives us insights into the following methods:

- Routes

- Roads

- Direction

- Geocoding and distance matrix

  3.  Places API

> Places API mainly gives us insights to the following methods:

- Geocoding

- Geolocation

- Address validation

- Time zones

  4.  Environment API

> Environment API mainly gives us insights into the environmental data
> of the location, like air quality, solar energy, and so on. And these
> data are the farthest of those APIs to our requirements.

Note that there are other choices for maps APIs that we can use instead
of Google, which can be like Opensource Routing, Mapbox, and others, but
we mainly chose Google Maps since it first supports maps for our region
and it has better insights with a free subscription plan than the limited
insights that other APIs might offer for free subscription plans.

Based on this we chose Routes API to generate the geocoded location.

  1.  1.  1. Destination geocoding 

![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/df5d05e1-8068-46c7-b1bc-9c3b4522fe16)

First, we need to generate an API key from Google Cloud to access its
service, then generate a client, and start calling the methods we need
from those mentioned
[<u>previously</u>](#specify-location-with-google-maps).

So, our algorithm will be simple as shown in Figure 7

1\. import google maps

2\. from pprint import pprint

3\. api=\*\*\*

4\. GClient=googlemaps.Client(api)

5\. MKAN='Egyptain Academy For Engineering And Advanced Technology,
Cairo, EG'

6\. pprint(GClient.geocode(MKAN))

Using the geocode method without parsing returns a raw dictionary with
several IDs and linked lists, latitude and longitude will be found in
the id of the name ‘geometry’ and inside this dictionary another dictionary
named ‘location’ that carries latitude and longitude so lat. and long.
can be extracted with

7\. pprint(GClient.geocode(MKAN)\[0\]\['geometry'\]\['location'\])

##  Algorithm

> Now that we know where we are and where we want to go, we can plan our
> path from start to end.
>
> We require that we want the drone to cover the whole field
> or as much as it can so that it detects as many plants as it can,
> and for this to happen we can say that this drone needs to take the
> longest path between the start and end.
>
> This will lead us to choose among the dynamic programming algorithms
> that are mainly Breadth-First search and Depth-First search.
>
> ![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/d8db2b21-4159-4de6-8b77-ec33ae69419c)
These
> Algorithms mainly consider the field as a grid as shown in Figure 62,
> with cells that are named Nodes, where each node has a defined ID, and
> The transition path between a Node and its adjacent is named Edge,
> Where every edge has a weight, they may all have the same weight, these
> Weights indicate a weighted value that adds extra cost to the
> traveling above the distance cost, like for example a node is
> Surrounded by 3 nodes, they might be all the same geometric distance away
> from this node, but not all of them are easily accessible this might
> be due to an extra turn before heading to a node, you can imagine it as
> extra traffic way, so the more crowded has a higher weight value.
>
> We can see that we are projecting the start and the end into the
> field, we can do this if we know the maximum latitude and longitude as
> well as the minimum latitude and longitude of each node, you can imagine
> it as that every node is a vector with tuples of latitudes and
> longitudes that can be inside this node, so by locating the start and
> end into 2 different nodes, we can start our path-finding search
> dynamic programming algorithm.

It is important to understand and specify the nature of the relationship
between these nodes and their edges before executing a path-finding
algorithm.

> From Graph, theory illustrated in Figure 9 we can get a grasp of the
> nature of our field.
>
> First, let us go through every graph of them to understand which of
> them is more similar to ours:

![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/ae67f08a-a9cb-4ceb-b869-59ded66996e1)

*Table
1 Graph Theory*

<table>
<colgroup>
<col style="width: 23%" />
<col style="width: 20%" />
<col style="width: 16%" />
<col style="width: 15%" />
<col style="width: 23%" />
</colgroup>
<thead>
<tr class="header">
<th>Graph</th>
<th>Tree Graph</th>
<th>Cyclic</th>
<th>Weighted</th>
<th>Directional</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><blockquote>
<p>properties</p>
</blockquote></td>
<td><ul>
<li><p>It is acyclic and it doesn’t have closed cycle</p></li>
<li><p>Every node has one and only parent</p></li>
</ul></td>
<td><ul>
<li><blockquote>
<p>It’s closed-loop path</p>
</blockquote></li>
<li><blockquote>
<p>The start node is also the end node</p>
</blockquote></li>
</ul></td>
<td><ul>
<li><p>The edges have weights from one node to another</p></li>
</ul></td>
<td><ul>
<li><p>Directed graphs illustrated sequential flows</p></li>
<li><p>Undirected graphs illustrate symmetric relationships</p></li>
</ul></td>
</tr>
</tbody>
</table>

> According to our understanding for *Table 1 Graph Theory* and our
> Requirements for this application the start node is not the end node
> In our case, or other words, the starting point is not our goal to
> reach, so our algorithm will adopt solving an Acyclic graph, also
> Visiting a node will require us in this application to visit the one
> following it in the flow, so it is not a symmetric relationship but a
> directed one, which leads to having an algorithm that solves Directed
> graphs. Also, we assumed that all the weights of the edges are constant
> and equal to -1 and we will understand why ‎1.3.2 section.
>
> Based on these observations and conclusion we can say that our graph
> is Direct Acyclic Graph aka DAG.

1.  

### Algorithm selection

> To select the best algorithm that matches our application, hardware
> constraints and requirements, we have to assess the available algorithms
> based on those KPIs:

- Computational Time

- Storage Space

- Relevant To Our Purpose

#### Computational Time

> We will use a notation called Big O from software engineering to
> assess the time computation for our algorithms.

![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/e97dd6c4-e52a-4378-bd63-eab94bff83b2)


> Big O notation briefly is a symbolism that relates the times of
> Computation as a function of the worst number of iterations of a
> specific line of code, so it indicates how fast growing is the
> function or declining it is.
>
> For example, a line of code that declares a variable is a constant
> time operation since we only have one variable that will be declared
> in x seconds.
>
> But for example, if we use a loop to iterate over each element of a
> list, so if the list has length n, then every operation for each
> element will take time t, repeating the same operation for the nth
> Elements ends up having n times the time of one operation to be
> executed so execution time is a function of n O(n).
>
> That doesn’t mean that necessarily all loops have O(n) computational
> time, that is because not all of them do the linear search or loop
> over every element in the list of Utterable.
>
> In our application, there are 2 loops one over the nodes ‘N’, followed
> by one over the edges ‘E’, so that we examine the neighborhood nodes
> of the current position, to choose the best to visit, and that is
> according to the weight of edges that also require to be examined, so
> We will also generally loop over the edge weights.
>
> From this we can estimate that Big (O) for DAG is O(N+E) in the worst
> case.

#### Algorithm approaches for our purpose

When talking about dynamic programming then there are mainly two
the algorithm that inspired other modified algorithms, two are BFS and
DFS that we have previously discussed in ‎1.3, but we have not
specified yet which approach is more relevant and why.

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th>BFS</th>
<th>DFS</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><ul>
<li><p>Searches in nodes level-by-level, covering adjacent nodes before
jumping into the next level.</p></li>
<li><p>Uses queue</p></li>
</ul></td>
<td><ul>
<li><p>Digs deep in each branch until its end then gets back to the
adjacent branch after it finishes searching the first one.</p></li>
<li><p>Uses stack</p></li>
</ul></td>
</tr>
<tr class="even">
<td><ul>
<li><p>Doesn’t get stuck into infinite loops</p></li>
<li><p>Always finds shortest path</p></li>
</ul></td>
<td><ul>
<li><p>Might get stuck in infinite loop</p></li>
<li><p>Doesn’t always find way</p></li>
</ul></td>
</tr>
</tbody>
</table>

*Table 2 BFS VS DFS*

Although DFS has better memory requirements than BFS because it uses
stack not queue, but the fact that it should visit all nodes to find the
path, makes it always reach the worst O(N+E), that might be infinite
with a large number of nodes, unlike BFS, that is more probable to find the
path before it reaches O(N+E), as it neglects other nodes if it reached
the goal already.

That is why we will proceed with BFS and its modified algorithms like
A\* algorithm, that solves the queue problem by using a Priority queue
that relies on the heuristic cost that we will discuss in Localization

Other algorithm approaches can be using computer vision to track some
features in the field and navigate upon these features, however it will
require bigger space to handle images captured online.

###  Longest path algorithm

As we have seen in ‎6.3.1BFS specifically the modified one which is
A\* algorithm is the most standing relative to our requirements so far.

However, A\* is a shortest path finding algorithm, when we said at
first, our goal is to generate the longest path in the field to scan it,
to do that let’s first understand the idea of A\*

![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/f9475ad6-7d17-407b-a0ea-84e46678f7d0)


**LONGEST PATH**

![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/b18dfffe-09d6-4fe8-9810-6a502f55c2b1)


As you can notice from Figure 11 A\* Algorithm, this algorithm is mainly
about choosing the sum of the minimum weights amongst the adjacent nodes to
every node.

<table>
<colgroup>
<col style="width: 9%" />
<col style="width: 67%" />
<col style="width: 22%" />
</colgroup>
<thead>
<tr class="header">
<th></th>
<th><span
class="math display"><em>f</em>(<em>n</em>) = <em>g</em>(<em>n</em>) + <em>h</em>(<em>n</em>)</span></th>
<th>(1.)</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

> Also note that the idea of A\* that stands out than any other thing is
> The heuristic function that we discussed earlier in ‎1.3, this
> The heuristic function is calculated from a distance formula called
> Manhattan distance or Euclidean distance, which gives an estimate of
> the shortest displacement (hypotenuse) between current point and goal,
> that helps to discriminate between two points that might geometrically
> have the same value length as the current node, but one of them might be
> much far from the endpoint We used this to generate the longest path
> by switching the weights from 1 to -1 so the minimum will always be
> the biggest absolute sum but the least numeric sum as well.

<table>
<colgroup>
<col style="width: 9%" />
<col style="width: 67%" />
<col style="width: 22%" />
</colgroup>
<thead>
<tr class="header">
<th></th>
<th><blockquote>
<p><span class="math display">$$Manhattan\  = \sum_{i = 1}^{k}\left|
x_{i} - y_{i} \right|$$</span></p>
</blockquote></th>
<th>(<strong>1.</strong>.)</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 9%" />
<col style="width: 67%" />
<col style="width: 22%" />
</colgroup>
<thead>
<tr class="header">
<th></th>
<th><blockquote>
<p><span class="math display">$$Euclidean\  = \sqrt{\sum_{\mathbf{i =
1}}^{\mathbf{k}}{\mathbf{(}\mathbf{x}_{\mathbf{i}}\mathbf{-}\mathbf{y}_{\mathbf{i}}\mathbf{)}}^{\mathbf{2}}}$$</span></p>
</blockquote></th>
<th>(1.)</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/6d4a8420-20d1-4053-a8fa-e33ff250043e)

## Geodetic to NED

> It is important to consider that the Control system is expected from
> us odometry data, not geo-coordinate ones that is why we need to
> Convert the output trajectories from tuples of latitudes and
> longitudes to distances in meters, so we used a formula called
> haversine formula.

  

###  Haversine

> We know that in a 2-D circle the length of arc = R\*𝞱, that is
> similarly the inspiration behind haversine, but in 3-D, where the
> radius is the radius of EARTH and theta is calculated from haversine law,
> as a function of lat. and long.

Haversine is a trigonometric formula that has value as shown in Equation
1.4.

<table>
<colgroup>
<col style="width: 9%" />
<col style="width: 67%" />
<col style="width: 22%" />
</colgroup>
<thead>
<tr class="header">
<th></th>
<th><blockquote>
<p><span class="math display">$$hav(\theta) = si_{n}^{2}\left(
\frac{\theta}{2} \right) = \frac{1 - \cos(\theta)}{2}$$</span></p>
</blockquote></th>
<th>(<strong>1.</strong>.)</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 72%" />
<col style="width: 22%" />
</colgroup>
<thead>
<tr class="header">
<th></th>
<th><blockquote>
<p><span class="math display">$$d = 2r\ arcsin\left(
\sqrt{\sin^{2}\left( \frac{\phi_{2} - \phi_{1}}{2} \right)} +
\cos{\left( \phi_{1} \right)\cos{\left( \phi_{2} \right)\sin^{2}\left(
\frac{\lambda_{2} - \lambda_{1}}{2} \right)}} \right)$$</span></p>
</blockquote></th>
<th>(1.)</th>
</tr>
</thead>
<tbody>
</tbody>
</table>



### Universal Transverse Mercator

As we know Latitude, Longitude, and Altitude coordinates are angular
quantities in the Geodetic Frame, which specifies the location on the Earth,
and it’s not easy or practical to calculate distances from angular
quantities.

As we have seen in section ‎1.4.1 to calculate distance we have to keep
cumulating values through time, which might not be a practical
computation over a long time.

In Aeronautics the standard local frame is known as the NED Frame, which
goes for North-East-Down, where North is the cartesian X-coordinate,
East is the Y-coordinate, and Down is the negative Z-coordinate, note that Z
points down as it’s common in Aeronautics to use right-handed-Coordinate
system.

![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/b27f6c99-5118-4956-9dc2-e589a07deed7)


Figure UTM map

To convert Geodetic to NED frame we can use Universal Transverse
Mercator (UTM), UTM divides the world’s 3-D sphere into a 2-D map with
neglecting the altitude, this map has 60 east-west numbered zones, and
24 north-south zones marked as letters.

In this part, we are interested in calculating the distance the drone
should take in x and y coordinates, just as we did in Haversine.
![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/18f74df7-de9a-4773-bf93-29eafdb0c125)

## Configuring Environment

In this section, we aim to define the feasible and infeasible parts of
our space for the global path plan.

To do that we have to get the static obstacles’ data, this data can be
derived from comparing the drone altitude with the elevation of
obstacles. We can get elevation from Google Maps, and generate a grid by
defining the size of the grid that we want, for example, size=100 means we
will get 100x100 meters far from the center latitude and center
We have chosen the longitude if the step's precision is 1 meter.

![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/647e5e94-a627-4f5c-9fea-21523e4daa35)

But
as we have mentioned earlier latitude and longitude are degree units,
so we need to know the step from one point to another or the precision in
degrees, not meters. To do that we should have a refresher on latitudes
and longitudes to calculate the distance between 2 degrees of latitude,
or 1 degree of longitude.

As we can see in Figure 18 Latitudes are parallel to each other’s, as
they are equidistant and never intersect, but longitudes intersect, they
are maximum at the equator and zero at the poles, in other words, they
decrease with cosine(latitude).

1 degree of latitude is equivalent to the Earth’s circumference/360^0

<table>
<colgroup>
<col style="width: 4%" />
<col style="width: 72%" />
<col style="width: 22%" />
</colgroup>
<thead>
<tr class="header">
<th></th>
<th><span
class="math display"><strong>1</strong> <strong>d</strong><strong>e</strong><strong>g</strong><strong>r</strong><strong>e</strong><strong>e</strong> <strong>o</strong><strong>f</strong> <strong>l</strong><strong>a</strong><strong>t</strong><strong>i</strong><strong>t</strong><strong>u</strong><strong>d</strong><strong>e</strong> = (<strong>40</strong>,<strong>075</strong> <strong>k</strong><strong>m</strong>)/<strong>360</strong>  = <strong>111</strong>, <strong>320</strong> <strong>m</strong><strong>e</strong><strong>t</strong><strong>e</strong><strong>r</strong><strong>s</strong> </span></th>
<th>(1.)</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

1 degree of longitude at a known altitude is equivalent to (Earth’s
circumference/360<sup>0</sup> )x cos(latitude)

<table>
<colgroup>
<col style="width: 76%" />
<col style="width: 23%" />
</colgroup>
<thead>
<tr class="header">
<th><span class="math display">$$\mathbf{1}\ \mathbf{degree}\
\mathbf{of}\ \mathbf{longitude} = \frac{\mathbf{40},\mathbf{075}\
\mathbf{km}}{\mathbf{360}}\ \mathbf{x}\
\mathbf{\cos}(\mathbf{latitude})\ \ \mathbf{meters}\ $$</span></th>
<th>(1.)</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

\[45\]

The Pseudo algorithm to get our static map and define the feasible and
infeasible points are as in the following pseudo-code.

1.  get_map(center_lat, center_long, size, precision):

2.  lat_precision = precision/ EQ. (‎6.6)

3.  long_precision = precision/EQ. (‎6.7)

4.  half_map= size/2

5.  lats = array(min_lat, max_lat, precision)

6.  longs = array(min_long, max_long, precision)

7.  map = \[(lat, long) for lat in lats for long in longs\]

8.  return map

<!-- -->

1.  loop(map):

2.  find elevation from Google Maps API Figure 61 GEOCODING flowchart

3.  calculate cartesian x, y Figure 17 UTM block diagram

4.  return cartesian_map_array



![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/a1163b33-a787-4ff8-be96-d3d0e08abb4a)
![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/4ed5701d-6624-469d-b2fd-e3db70e371e2)

Many factors change the profile of the grid, starting
from the precision or the step of each coordinate sample to the drone
altitude and the safe distance allowed in case of inaccuracy errors to
inaccuracy of elevation data from Google Maps; as some physical objects
might not be scanned by Google Maps like gates and fences, and some
other objects might be over-scaled. That is why the local path plan system is
as important as a global path plan.

## Way Points Extraction

After applying the longest path algorithm Figure 66 Longest Path, we
will have an array of waypoints that connect the start to the end.
waypoints are not about passing every poly-point in the grid to the
autopilot, but it's about passing points where a change in direction is
required, or by other means if we passed points xyz and all of them
are in the same east-west line, then we could simply pass x and z only.

to know if 3 points are in the same straight line or not, then in 2-d their
area should be zero, if their area is not zero then they are not in the same
straight line, but they can form a triangle.

we can test if their area = 0 if $\Delta\begin{bmatrix}
x\_{1} & y\_{1} & z\_{1} \\
x\_{2} & y\_{2} & z\_{2} \\
x\_{3} & y\_{3} & z\_{3}
\end{bmatrix}$ =0 (1.8)

This condition is sufficient in 2-D but not enough in 3-D, and since we
are working in 2.5 D map, to avoid burning a lot of computation memory,
then we can use this check to extract the waypoints from the filtering
poly-points in the same line.

The collinearity check system checks if P1, P2, and P3 are in same
straight line, then we will drop P2.

![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/99d9efd5-55e2-48a1-88db-2252c980b2c8)
![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/6cfcf6a3-e955-4f84-8e01-e6b67d37ac3a)


Figure Longest path plan for grid

## Skeletonization

As we are planning for the drone movement, we have to put in
consideration of the degrees of freedom or constraints that we are
controlling, such as drone orientation, diagonal movement, 3-D
movement and grid size. So, adding all of these in the grid-based search
will be computationally expensive though grids ensure that u find the
optimal and complete path according to its accuracy, unlike graphs that
doesn't represent the geometry with obstacles of the plane but it represents
the topology of the map and the edges(curved/straight/diagonal) that
connects nodes (STATES).

Skeletonization in our path plan can be simply done by finding the
Medial Axis of the grid, which creates less feasible points to visit,
where these points lie in the middle between each corresponding obstacle,
this drops other points that we have considered before such as the
points that almost touch the obstacles.

This consequently downsizes the feasible points that our A\* will search
for.

![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/502530b6-e1ef-40d0-9da6-30d90ff8ac1d)


Figure Grid skeleton

![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/7d63f48d-1429-4834-a6fd-ff20ab0e007a)


As we can observe from Figure 25 The Medial axis path covers a safe area
for the drone to fly over, with fewer points i.e. fewer way points, less
time, and less memory. However, we have also downsized the accuracy here,
since the camera can capture the wide view, but this might
not be the optimum solution for high-accuracy applications.
![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/41fef98c-68ec-4ecb-bb25-00ab798b77cd)


## Probabilistic Road Map

> In this section we will cover how to optimize the longest path
> algorithm, for vast fields, Figure 79 showed a map for a 900x900
> meters space, this space is empty, the algorithm will probably get
> stuck in computation. After skeletonization, the algorithm will
> work well, however, the size of feasible points is passed to the
> algorithm is *n* variables with the start and end chosen points, then
> An extra *m* variable is added after applying collinearity ‎6.6 over
> The waypoints resulted from the algorithm. This will burn a lot of
> time, to loop over every 3 points to check if they are collinear and
> the overall BIG(O) ‎6.3.1.1 of this process is loop *n* + loop *m*.
>
> To have a better control of this algorithm, we can create a random
> point with fixed length, ex. 2000 points including start and goal,
> that ranges over the size of the map, filter those points using K-D
> tree module to avoid the collision space, create segments between the
> points and choose the maximum length from start to end to serve our
> longest path, by passing them to the modified A\* algorithm ‎1.3.2.
>
> This way we can get a logarithmic BIG(O), as K-D tree module filters
> The search by using binary logarithmic search, not linear search as the
> Collinearity check.
>
> ![image](https://github.com/malakalimah/Autonomous-Drone/assets/70919728/c5a0be81-a209-40f6-98e8-0f6119bca668)
To
> To achieve that, we will create a Tree of random points and points
> Here are geometric points i.e. have area, permitted, and all the
> geometric properties using the Shapely module, and then query the polygons
> that are *x* length units far away from these points, if found we will
> Drop them from our random samples, with a much more optimized time.
