# Eklavya20-Drone
Drone simulation project
# DRONE SIMULATION PROJECT
##  ABOUT THE PROJECT
   1)GOALS TO BE ACHIEVED
   2)WHY PROJECT HAS BEEN CHOSEN
 ##  GETTING STARTED:-
 
 PREREQUISITES:
 
1. ROS Installed:
 
 To install ROS, visit the following link: http://wiki.ros.org/ROS/Installation 
 
 If you just installed ROS from apt on Ubuntu then you will have setup.*sh files in '/opt/ros/<distro>/', and you could source them like so:
   
 $ source /opt/ros/<distro>/setup.bash
 Use the short name of your ROS distribution instead of <distro>.
  
 Let's create and build a catkin workspace:
 
 $ mkdir -p ~/catkin_ws/src
 $ cd ~/catkin_ws/
 $ catkin_make 
 
 Before continuing source your new setup.*sh file:
 
 $ source devel/setup.bash
 
2. Gazebo Installed:
 
 To install Gazebo, visit the following link: http://gazebosim.org/tutorials?tut=install_ubuntu 
 
 Make sure the stand-alone Gazebo works by running in terminal:
 
 $ gazebo
 
## INSTALLATION:
 
1. Clone the repository.

git clone https://github.com/pkjagesia/Eklavya20-Drone.git 

## Usage
TODO: Write usage instructions
##   RESULTS AND DEMO
TODO: Write a project description.
## FUTURE ASPECTS AND GOALS WE WANT TO ACHIEVE THROUGH THE PROJECT:-
1. Our first step is to integrate obstacle avoidance and the code which we have written 
for the drone to move from one destination to another within an environment of four walls .

 2. Our second step would be to implement obstacle detection code with obstacle avoidance as 
this would be a great aid for the drone to perform then future tasks like geography mapping  ,
aerial photography without having to worry about obstacles in its way.

3. We aim to achieve our goal of obstacle detection through contour detection.
Contour detection is based on detecting the outline of the object within the environment. It is preferred because it is based upon edge detection, which has been optimized in run time and complexity, therefore, allowing for near real-time run implementations.

4. We aim to expand on our avoidance goal in the near future by implementing SLAM,so the quadrotor can create a map of the environment it is navigating. When this path is to be chosen, a stereo camera can be mounted to the quadrotor for distance estimation. Supporting this, LiDAR can also be used, and the data acquired by the system can be processed and fused for a detection algorithm.
These are our future aspects of the project.

## TROUBLESHOOTING AND ERRORS:-
TODO:WRITE DESCRIPTION
## CONTRIBUTORS
TODO: Write
## ACKNOWLEDGE AND RESOURCES
TODO: Write 
## License
TODO: Write license
