#!/bin/usr/env python3 
# the above line is used to tell the system that this file is a python3 file and it should be executed using python3 interpreter

# importing the rclpy library for python ros2 packages
import rclpy
# importing the node class from rclpy.node library to intialized the node functionality
from rclpy.node import Node

# creating class for node functionality 
class My_krishna_node(Node):
	# creating a function to make initalization of node 
	def __init__(self):
		# initializing the node by super method
		super().__init__("Jaganath")
		self.counter_ = 0
		self.timer_ = self.create_timer(1.0, self.print_node)
	
	def print_node(self):
		# printing the value by using get_logger method
		self.get_logger().info("namaha shivya " + str(self.counter_))
		self.counter_ += 1


# Creating a main function	
def main(args=None):
	# initializing the rclpy library
	rclpy.init(args=args)
	# initializing the node by creating object of class
	node = My_krishna_node()
	# spinning the node to keep it alive and running
	rclpy.spin(node)
	# shutting down the node after performing the task and destroying the node object
	rclpy.shutdown()
	
if __name__ == '__main__':
	main()
