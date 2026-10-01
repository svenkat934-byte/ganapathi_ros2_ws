#!/usr/bin/env python3 # shebang line to specify the interpreter
# importing the rclpy library for  ROS 2 python client library
import rclpy
# importing the Node class from rclpy.node module
from rclpy.node import Node
# importing the int64 message type frim example_interfaces.msg
from example_interfaces.msg import Int64
from rclpy.parameter import Parameter

# creating a class NumberPublisherNode that inherits from Node class
class NumberPublisherNode(Node):
    # creating a function __init__  that initializes the Node
    def __init__(self):
        # calling the constructor of parent class Node with super() function and passing node name
        super().__init__("number_publisher")
        # #creating a number variable as data
        # self.number_ = 2
        # # creating a publisher object that will publish int64 message to the topic "number_publisher"
        # self.number_publisher_ = self.create_publisher(Int64, "number", 10)
        # # creating a timer that publish number for every 1 second
        # self.number_timer_ = self.create_timer(1.0, self.publish_number) 
        # # printing a log message as number publisher has been started
        # self.get_logger().info("Number publisher has been started")
        # #declaring the parameter
        self.declare_parameter("number", 2)
        self.declare_parameter("publish_period", 1.0)

        # declaring parameter
        self.number_ = self.get_parameter("number").value
        self.timer_period_ = self.get_parameter(
            "publish_period"
        ).value

        self.number_publisher_ = self.create_publisher(Int64, "number" , 10)

        self.number_timer_ = self.create_timer(
            self.timer_period_, self.publish_number
        )

        self.get_logger().info("Number publisher has been started.")

        self.add_post_set_parameters_callback(self.parameters_callback)


    # creating a function publish_number that will publish data
    def publish_number(self):
        # creating a message object of int54 type
        msg = Int64()
        # now assigining the self.number to this msg data
        msg.data = self.number_
        # publishing the message to the topic
        self.number_publisher_.publish(msg)


    def parameters_callback(self, params: list[Parameter]):
        for param in params:
            if param.name == "number":
                self.number_  = param.value

# defining the main function that will be executed when the script is executed from here
def main(args=None):
    # initializing the ROS 2 client library
    rclpy.init(args=args)
    # creating an instance of NumberPublisherNode class
    node = NumberPublisherNode()
    # spining the node to keep it alive and process in background
    rclpy.spin(node)
    # shutdown the ROS 2 client library
    rclpy.shutdown()

# making a condition to strat the main function when script is executed directly
if __name__ == "__main__":
    main()