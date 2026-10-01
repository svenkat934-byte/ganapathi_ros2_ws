#!/usr/bin/env python3

# importing the rclpy package for node  working in ROS2
import rclpy
# from rclpy importing node to use 
from rclpy.node import Node

# creating class for node functionality 
class MyRobot(Node):
	# creating a function for intialization of node 
	def __init__(self):
		# initializing node by super method
		super().__init__("robot_controller")
		# making timer variable to call fucntion  for every 2 second
		self.timer_ = self.create_timer(2.0, self.print_my_robot)
	
	# creating a function to print
	def print_my_robot(self):
		# calling get_logger to print 
		self.get_logger().info("Robot is Running" )
	
# creating main function 
def main(args=None):
	# intializing rclpy
	rclpy.init(args=args)
	# creating a constructor for class 
	node = MyRobot()
	# spin the node in terminal 
	rclpy.spin(node)
	#shutdown of the node
	rclpy.shutdown()

# making a condition to run this program
if __name__ == "__main__":
	main()
	

