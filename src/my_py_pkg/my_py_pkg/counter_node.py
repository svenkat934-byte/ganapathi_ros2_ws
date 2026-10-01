#!/usr/bin/env python3 

# import rclpy package
import rclpy
#from rclpy.node importing node functionalities
from rclpy.node import Node

# creating node class 
class Counter(Node):
	# creating a function to initialize the node 
	def __init__(self):
		# creating a node by using super method
		super().__init__("counter_node")
		# creating a counter variable 
		self.counter_ = 0 
		# creating a  timer variable to make node do something for second interval 
		self.timer_ = self.create_timer(1.0 , self.print_counter)
		
	# creating a print_counter to print
	def print_counter(self):
		# by using get_logger function printing the value 
		self.get_logger().info("Count = " + str(self.counter_))
		# increament for counter
		self.counter_ += 1
	
# creating a function for rclpy init, spin , shutdown
def main(args=None):
	# initializing the rclpy init
	rclpy.init(args=args)
	# creating class objectiv
	node = Counter()
	# making node to spin in terminal 
	rclpy.spin(node)
	# shutdown the node
	rclpy.shutdown()
	
# making a condtion 
if __name__ == "__main__":
	main()
