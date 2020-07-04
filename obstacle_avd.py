#!/usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan , Range
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
import argparse

parser = argparse.ArgumentParser(description = 'Destination of the drone')
parser.add_argument('X',type = int,help = 'x-coordinate of destination')
parser.add_argument('Y',type = int,help = 'y-coordinate of destination')

args = parser.parse_args()

PI = 3.1415926535897
front = 0.0   #distance of obstacle from the front
corner = []   #array for observing the change in values at corners to the right
height = 0.0 
x = 0.0
y = 0.0

heading = 0 #facing towards north
flag = 0

class obstacle_avoidance():


    def scan_call_back(self,msg):

        global front
        global corner
        
        front = msg.ranges[540]
        corner =  msg.ranges[880:925]

    def range_call_back(self,msg):

        global height
        height = msg.range

    def odom_call_back(self,msg):
        global x
        global y
        
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y    
            
    def __init__(self):        
        
        #Subscriber for reading laser data
        rospy.Subscriber("/scan",LaserScan,self.scan_call_back)

        #Subscriber for reading sonar data
        rospy.Subscriber("/sonar_height",Range,self.range_call_back)
        
        #Subscriber for reading odom data
        rospy.Subscriber("/ground_truth/state",Odometry,self.odom_call_back)

        #Publisher for publishing velocity commands
        self.vel_pub = rospy.Publisher("/cmd_vel",Twist,queue_size=1)
        
        self.speed = Twist()

    def take_off(self):
        
        print('Taking off!')
        while height < 0.5:
            self.speed.linear.z = 1.0
            self.speed.linear.x = 0.0
            self.vel_pub.publish(self.speed)

        self.speed.linear.z = 0.0
        self.vel_pub.publish(self.speed)

        return
    
    def land_drone(self):
      
        print('Reached my destination')
        print('Landing')
        while height > 0:
            self.speed.linear.z = -1
            self.speed.linear.x = 0.0

            self.vel_pub.publish(self.speed)

        self.speed.linear.z = 0.0
        self.vel_pub.publish(self.speed)

        return
    
    def corner_right(self):

        global corner
        
        count1 = 0
        count2 = 0
        count3 = 0

        lst1 = corner[:22]  #Logic to find corners : Divide the corner array into 2.
        lst2 = corner[22:]  #If atleast 10 values of the first half are inf and    
        for i in lst1:      # atleast 10 values of the second half are something other than inf
            if str(i) == 'inf': #then a corner is detected.
                count1 += 1
        for i in lst2:
            if str(i) != 'inf':    
                count2 += 1
        if (count1 >=10 and count2 >= 10) :
            return True
            
        for i in corner:
            if str(i) == 'inf': 
                count3 += 1
        if count3 > 40 :
            return False
        
    def rotate(self,turn,angle):
        
        turn_angle = (angle * PI)/180   #convert angle to radians

        if turn == 'left':
            self.speed.linear.x = 0.0
            self.speed.angular.z = 0.5
        elif turn == 'right':
            self.speed.linear.x = 0.0
            self.speed.angular.z = -0.5
        
        current_angle = 0
        t0 = rospy.Time.now().to_sec()

        while(current_angle < turn_angle):
            self.vel_pub.publish(self.speed) 
            t1 = rospy.Time.now().to_sec()
            current_angle = 0.5 * (t1 -t0) #updating the value of current angle after taking the turn using 
                                           #angle = (angular velocity) * time

        # Force stop the drone
        self.speed.angular.z = 0.0
        self.vel_pub.publish(self.speed)

        return

        
    def travel_horizontal(self):

        global x
        global heading
        global args

        print('Heading towards x-coordinate')
        
        if (heading == 0 and (args.X - x) > 0):

            self.rotate('right',90)
            heading-=90
            while (args.X - x) > 0:
                self.speed.linear.x = 0.8
                self.vel_pub.publish(self.speed)                
            
            self.speed.linear.x = 0.0                
            self.vel_pub.publish(self.speed)

        elif (heading == 180 and (args.X - x) < 0):

            self.rotate('right',90)
            heading-=90
            while (args.X - x) < 0:
                self.speed.linear.x = 0.8
                self.vel_pub.publish(self.speed)                
            
            self.speed.linear.x = 0.0                
            self.vel_pub.publish(self.speed)

        elif (heading == 180 and (args.X - x) > 0):
           
            self.rotate('left',90)
            heading+=90
            while (args.X - x) > 0 :
                self.speed.linear.x = 0.8
                self.vel_pub.publish(self.speed)                
            
            self.speed.linear.x = 0.0                
            self.vel_pub.publish(self.speed)

        else:
           
            self.rotate('left',90)
            heading+=90
            while (args.X - x) < 0 :
                self.speed.linear.x = 0.8
                self.vel_pub.publish(self.speed)                
            
            self.speed.linear.x = 0.0                
            self.vel_pub.publish(self.speed)
        
        return

    def travel_straight(self):

        global heading
        global y
        global args

        print('Heading towards y-coordinate')
        if (heading == -90 and (args.Y - y) > 0):

            self.rotate('left',90)
            while (args.Y - y) > 0:
                self.speed.linear.x = 0.8
                self.vel_pub.publish(self.speed)                
            
            self.speed.linear.x = 0.0                
            self.vel_pub.publish(self.speed)

        elif (heading == -90 and (args.Y - y) < 0):
           
            self.rotate('right',90)
                
            while (args.Y - y) < 0:
                self.speed.linear.x = 0.8
                self.vel_pub.publish(self.speed)                
            
            self.speed.linear.x = 0.0                
            self.vel_pub.publish(self.speed)

        elif (heading == 90 and (args.Y - y) > 0):
           
            self.rotate('right',90)
            while (args.Y - y) > 0 :
                self.speed.linear.x = 0.8
                self.vel_pub.publish(self.speed)                
            
            self.speed.linear.x = 0.0                
            self.vel_pub.publish(self.speed)

        else:
           
            self.rotate('left',180)
            heading+=180
            while (args.Y - y) < 0 :
                self.speed.linear.x = 0.8
                self.vel_pub.publish(self.speed)                
            
            self.speed.linear.x = 0.0                
            self.vel_pub.publish(self.speed)
        
        return
    
    

    def obj_avd(self):

        
        global front 
        global corner
        global heading
        global flag
        global args

        print("Distance from obstacle : {F}".format(F = front))
        
        if front < 1 :
            print("Obstacle Detected \n Turning Left")
            self.rotate('left',90)
            heading+=90
       
        elif self.corner_right() and flag == 0:

            print("Corner Detected")
                
            old = rospy.Time.now()
            dt = rospy.Duration(1)
            new = rospy.Time.now()
            
            while ((new - old) < dt) :
                self.speed.linear.x = 0.5
                self.vel_pub.publish(self.speed)
                new = rospy.Time.now()
            
            self.speed.linear.x = 0.0
            self.vel_pub.publish(self.speed)
            
            print('Turning now')
            self.rotate('right',90)
            heading-=90
            flag = 1

        elif self.corner_right() == False and str(front) == 'inf':
       
            self.travel_horizontal()
            self.travel_straight()
            self.land_drone()
        else:
            self.speed.linear.x = 0.5
            while self.vel_pub.get_num_connections() < 1:
                pass

            self.vel_pub.publish(self.speed)

        return

if __name__ == '__main__':

    rospy.init_node('Obs_avd',anonymous=True)
    R = rospy.Rate(3)
    obj = obstacle_avoidance()
    obj.take_off()
    try:    
        while not rospy.is_shutdown():    
        
            R.sleep()
            obj.obj_avd()            
            
    except rospy.ROSInterruptException:
        pass
    rospy.spin()
