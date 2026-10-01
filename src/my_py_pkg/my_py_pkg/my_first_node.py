#!/usr/bin/env python3
# importing rclpy for intialize the ros2 python packages 
import rclpy
# from rclpy.node libary we importing node class for creating the node to perform some task
from rclpy.node import Node

# Creating class for writing a node related information
class MyCustomNode(Node):
    # creating a init function where intiaizing self parameters 
    def __init__(self):
        # assiging node as my_node_name by calling the super class init function 
        super().__init__("my_node_name")
        # creating a counter variable
        self.counter_ = 0
        # creating a timer variable to call the function for every 1 second
        self.timer_ = self.create_timer(0.5, self.print_hello)

    # Creating a print_hello function
    def print_hello(self):
        # calling the get_logger function to print the information on the terminal
        self.get_logger().info(str(self.counter_) + " Sri mahaganapathi subramanya paravathi ramana maheshwara ")
        # incrementing the counter variable by 1
        self.counter_ += 1


# creating a main function to intialize the node
def main(args=None):
    # intializing the ros2 python packages
    rclpy.init(args=args)
    # creating a node object for performing the task
    node = MyCustomNode()
    # making the node to spin in the background for performing the task
    rclpy.spin(node)
    # shutting down the node and destroying the node object after performing the task
    rclpy.shutdown()

# calling the main function to run the node
if __name__ == "__main__":
    main()
