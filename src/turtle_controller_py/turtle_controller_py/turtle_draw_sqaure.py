#!/usr/bin/env python3

# importing rclpy
import rclpy
# importing node class froom rclpy.node
from rclpy.node import Node
# importing Twist messages type from geometry_msgs.msg module
from geometry_msgs.msg import Twist
# importing pose from turtlesim.msg module
from turtlesim.msg import Pose

# creating class 
class Turtle_square_Node(Node):
    # creating a function to intialize 
    def __init__(self):
        # intializing the node by using super() 
        super().__init__("turtle_draw_suare")
        #creating a publisher to publish Twsit message to the /turtle1/smd_vel topic with queue size of 10
        self.cmd_vel_publisher_ = self.create_publisher(
            Twist, "/turtle1/cmd_vel", 10)
        # creating a subscriber to subscribe to pose message from the /turtle1/pose topic with queue size of 10
        self.pose_subscriber_ = self.create_subscription(
            Pose, "/turtle1/pose", self.callback_pose, 10)
        # creating a state varibale to store state of turtle bot
        self.state = "MOVE"
        # creating start_x variablle to indicate the starting poseition of turtle in x corrdinate
        self.start_x = None
        # creating start_y variable to indicate the starying postion of turtkebot in y corrdinate
        self.start_y = None
        # creating start_theta variable to indicate the angular position of turtlebot in z axis corrdinate
        self.start_theta = None
        # creating side_count variable to understand how many side are complted in square
        self.side_count = 0


    # creating a function for angle normalization 
    def normalize_angle(self, angle):
            # checking angle is above  pie = 3.14159 = 90 
        while angle > 3.14159:
            angle -= 2 * 3.14159
    
        while angle < -3.14159:
            angle += 2 * 3.14159
    
            # returning angle value
        return angle

    # creating a callback function to handle and recevive the pose message
    def callback_pose(self, pose: Pose):
         # assigining the Twist message to cmd  variable
        cmd = Twist()

        # geting initial position 
        if self.start_x is None:
            # assigin pose.x to x and pose.y to y
            self.start_x = pose.x
            self.start_y = pose.y
        # ---------------------------------------------------------------
        #  MOVE STATE
        # ---------------------------------------------------------------
        
        # making  a condition to indentify turtle bot current state 
        if self.state == "MOVE":
            # making turtlebot move in x direction of 1 mtr
            cmd.linear.x = 1.0
            cmd.angular.z = 0.0

               
                    # calculating the distance travelled
            distance = (
                ((pose.x - self.start_x) ** 2  +
                (pose.y - self.start_y) ** 2)  ) ** 0.5

            # checking the turtle bot is moved 2.0 mtrs or not 
            if distance >= 2.0:
                # recording the posistion angular value of turtlebot
                self.start_theta = pose.theta
                # making turtle bot state as rotate
                self.state = "ROTATE"
        # -------------------------------------------------------------
        # ROTATE STATE
        # -------------------------------------------------------------

        # cheking the condition of turtlebot state is rotation or not
        elif self.state == "ROTATE":
            # making turtlebot turn in 90 deg with angualar z axis
            cmd.linear.x = 0.0
            cmd.angular.z = 1.0

            # checking the angular of z axis by calculating current theta minus start theta
            angle_difference = self.normalize_angle(
                pose.theta - self.start_theta)

            # making the theta value around 1.57 with 0.02 tolerance
            target_angle = 1.5708
            tolerance = 0.02

            angle_error = target_angle - angle_difference
            # now checking angle is 90 or not
            if abs(angle_error) <= tolerance:
                # making turtle bot stop 
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0

                # now increasing side_count value as 1 side of square is completed 
                self.side_count += 1

                # checking the side of square if side = 4 then stoping performace
                if self.side_count >= 4:
                    self.state = "DONE"
                else:
                    self.start_x = pose.x
                    self.start_y = pose.y

                    self.state = "MOVE"

            # if angle is not 90 deg = 1.57
            else :
                cmd.linear.x = 0.0

                # rotate according to the remaining error
                if angle_error > 0:
                    cmd.angular.z = 0.5
                else:
                    cmd.angular.z = -0.5
        # -------------------------------------------------------------
        # DONE STATE
        # -------------------------------------------------------------
        elif self.state == "DONE":
            # stoping turtlebot stop 
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0


        # pusblishing the Twist velcotity 
        self.cmd_vel_publisher_.publish(cmd)
            
    

       

# writing main method to run the program in seauence
def main(args=None):
    # initilaixing the rclpy
    rclpy.init(args=args)
    # taking node constructor
    node = Turtle_square_Node()
    # making node to spin 
    rclpy.spin(node)
    # making node to destroy 
    node.destroy_node()
    # making node to shutdown 
    rclpy.shutdown()

# making a condition to run the main program if it runs directly 
if __name__ == "__main__":
    main()

