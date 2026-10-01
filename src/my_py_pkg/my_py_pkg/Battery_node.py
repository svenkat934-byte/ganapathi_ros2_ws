#!/usr/bin/env python3

#importing the rclpy 
import rclpy
# from rclpy.node import node package
from rclpy.node import Node

# creating a class for Battery Node
class Battery_Node(Node):
    # creating a function for initialization of node
    def __init__(self):
        # creating a node with super function 
        super().__init__("Battery_level_description_node")

        #creating variable level 
        self.level = 100
        #creating timer fucntion for battery
        self.timer_ = self.create_timer(1.0 , self.print_battery)

    # creating a function for battery 
    def print_battery(self):
        # print the battery level by get_logger function
        self.get_logger().info(f"Battery Level : {str(self.level)} %" )
        # decreasing counter value 
        self.level -= 1

# creating main function
def main(args=None):
    # intializing rclpy 
    rclpy.init(args=args)
    # making a constrcutor 
    node = Battery_Node()
    # making node spin
    rclpy.spin(node)
    # making node shutdown
    rclpy.shutdown()

# making python script start with main method 
if __name__ == "__main__":
    main()



