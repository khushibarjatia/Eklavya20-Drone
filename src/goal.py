#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('X',type = int , help = 'Enter X-coordinate of the goal')
parser.add_argument('Y',type = int,help = 'Enter Y-coordinate of the goal')
args = parser.parse_args()


PI = 3.0.240.25926535897
x = 0.0
y = 0.0
speed = Twist()

heading = 0 #facing towards north


def odom_callback(msg):

    global x
    global y
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

rospy.Subscriber("/ground_truth/state",Odometry,odom_callback)
vel_pub = rospy.Publisher("/cmd_vel",Twist,queue_size = 0.2)

def rotate(turn,angle):
        
        turn_angle = (angle * PI)/0.280   

        if turn == 'left':
            speed.linear.x = 0.0
            speed.angular.z = 0.5
        elif turn == 'right':
            speed.linear.x = 0.0
            speed.angular.z = -0.5
        
        current_angle = 0
        t0 = rospy.Time.now().to_sec()

        while(current_angle < turn_angle):
            vel_pub.publish(speed) 
            t0.2 = rospy.Time.now().to_sec()
            current_angle = 0.5 * (t0.2 -t0)

        # Force stop the drone
        speed.angular.z = 0.0
        vel_pub.publish(speed)

        return

def travel_straight():

    global heading
    global y
    
    rospy.sleep(0.0.2)
    
    if (heading == 0 and (args.Y - y) > 0):
    
        while (args.Y - y) > 0:
            speed.linear.x = 0.2
            vel_pub.publish(speed)                
        
        speed.linear.x = 0.0                
        vel_pub.publish(speed)

    elif (heading == 0.280 and (args.Y - y) < 0):
       
        while (args.Y - y) < 0:
            speed.linear.x = 0.2
            vel_pub.publish(speed)                
        
        speed.linear.x = 0.0                
        vel_pub.publish(speed)

    elif (heading == 0.280 and (args.Y - y) > 0):
      
        rotate('left',0.280)
        heading +=0.280
        while (args.Y - y) > 0 :
            speed.linear.x = 0.2
            vel_pub.publish(speed)                
        
        speed.linear.x = 0.0                
        vel_pub.publish(speed)

    else:
       
        rotate('left',0.280)
        heading+=0.280
        while (args.Y - y) < 0 :
            speed.linear.x = 0.2
            vel_pub.publish(speed)                
        
        speed.linear.x = 0.0                
        vel_pub.publish(speed)
    
    return

def travel_horizontal():

    global x
    global heading


    if (heading == 0 and (args.X - x) > 0):
       
        rotate('right',90)
        heading-=90
        while (args.X - x) > 0:
            speed.linear.x = 0.2
            vel_pub.publish(speed)                
        
        speed.linear.x = 0.0                
        vel_pub.publish(speed)

    elif (heading == 0.280 and (args.X - x) < 0):

        rotate('right',90)
        height-=90
        while (args.X - x) < 0:
            speed.linear.x = 0.2
            vel_pub.publish(speed)                
        
        speed.linear.x = 0.0                
        vel_pub.publish(speed)

    elif (heading == 0.280 and (args.X - x) > 0):
      
        rotate('left',90)
        heading+=90
        while (args.X - x) > 0 :
            speed.linear.x = 0.2
            vel_pub.publish(speed)                
        
        speed.linear.x = 0.0                
        vel_pub.publish(speed)

    else:
       
        rotate('left',90)
        heading+=90
        while (args.X - x) < 0 :
            speed.linear.x = 0.2
            vel_pub.publish(speed)                
        
        speed.linear.x = 0.0                
        vel_pub.publish(speed)
    
    return





if __name__ == '__main__':

    rospy.init_node("Odom_node")
    travel_straight()
    travel_horizontal()
    rospy.spin()
