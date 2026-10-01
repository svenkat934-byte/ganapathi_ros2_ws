#!/usr/bin/env python3 

import rclpy
from rclpy.node import Node
# importing String from std_msgs/msg
from std_msgs.msg import String
# importing rant int from random 
from random import randint
# import RobotCommand 
from my_robot_interfaces.srv import RobotCommand

# creating a class for Node 
class Robot_State_commander(Node):
    # intializing the node functionality 
    def __init__(self):
        # with super() intialize the node name 
        super().__init__("robot_state")
        # defing the robot_State variable and value as none
        self.robot_state_ = None
        # now creating a publisher data type as string topic name as robot_command and queue size is 10
        self.robot_publisher_ = self.create_publisher(String, "/robot_command", 10)
        # now creating a subscriber with data type string, topic name as robot_command , and queue size is 10
        self.robot_subscriber_ = self.create_subscription(String, "/robot_command", self.callback_robot_state,  10)

        # making publihser method and publisher for every 5 seconds
        self.robot_timer_ = self.create_timer(5.0, self.publish_string)
        # # creating a serive 
        self.robot_command_service = self.create_service(RobotCommand, "robot_command", self.callback_robot_command)
        

    # defining the publish_string method
    def publish_string(self):
        # assiging msgs = String()
        msgs = String()
        # robot position 
        robot_position = randint(0,3)

        # writing condition for robot state 
        if robot_position == 0 :
            self.robot_state_ = "Stop"

        elif robot_position == 1:
            self.robot_state_ = "Forward"

        elif robot_position == 2:
            self.robot_state_ = "Left"

        elif robot_position == 3:
            self.robot_state_ = "Right"

        
        msgs.data = self.robot_state_
        # publishing string data
        self.robot_publisher_.publish(msgs)

        # making server client function 
        self.callback_client(self.robot_state_)

    # defining the robot callback function 
    def callback_robot_state(self, msg):
        

        # if robot state == forward print the forward messgae
        if msg.data == "Forward":
            self.get_logger().info("Robot moving forward")

        elif msg.data == "Left":
            self.get_logger().info("Robot turning left")

        elif msg.data == "Right":
            self.get_logger().info("Robot turning right")

        elif msg.data == "Stop":
            self.get_logger().info("Robot stopper")

    # defining the service callback function
    def callback_robot_command(self, request: RobotCommand.Request, response: RobotCommand.Response):

      
        if request.command :
            if request.command == "Forward":
                response.message = "Robot moving forward"
          
            elif request.command == "Left":
                response.message =  "Robot turning left"
          
            elif request.command == "Right":
                response.message = "Robot turning right"
          
            elif request.command == "Stop":
                response.message = "Robot stopper"
          
            else :
                response.message = "Unknown command"

        return response

    # defing the service client
    def callback_client(self, command):
        self.request.command = command


# defining main functiion 
def main(args=None):
    # initilizaing the rclpy 
    rclpy.init(args=args)
    # making the node as a instance to call class node
    node = Robot_State_commander()
    # spining the node to make alive of node 
    rclpy.spin(node)
    # destorying the node
    node.destroy_node()
    # shutdowning the rclpy
    rclpy.shutdown()

# making the conditio to run main program even program run directly 
if __name__ == "__main__":
    main()

