#!/bin/usr/env python3 # shebang line to specify the interpreter
# importing the rclpy library for ROS 2 python client library
import rclpy
# importing the Node class from rclpy.node module
from rclpy.node import Node
# importing the HArdwareStatus message from my_robot_interfaces.msg
from my_robot_interfaces.msg import HardwareStatus

# creating a class CustomMessagePublisher that inherits from Node class
class CustomMessagePublisher(Node):
    # intailize the publisher node
    def __init__(self):
        # making node intialize with super class
        super().__init__("custom_message_publisher")
        self.number_ = 2
        # creating a publisher object that will publish HardwareStatus message to the topic 
        self.hardware_status_publisher_ = self.create_publisher(HardwareStatus, "hardware_status", 10)
        # create a publisher node timer to publish the msg every 1 second
        self.number_timer_ = self.create_timer(1.0, self.publish_msg_data)
        # printing a log message to indicate that node has been started
        self.get_logger().info("Hardware status publisher has been started")

    # creating a function publish_msg_data that take data from my_robot_interfaces.msg and publish data
    def publish_msg_data(self):
        # creating a message object of hardware status type 
        msg = HardwareStatus()
        # assigning the data to the msg object
        msg.temperature = 30.0
        # publishing the message to the  topic
        self.hardware_status_publisher_.publish(msg)


# defing the main function that will be executed when the script is executed 
def main(args=None):
    # intiliazing the ROS 2 client library
    rclpy.init(args=args)
    # creating an instance of custom message publisher class
    node = CustomMessagePublisher()
    # spining the node to keep it alive and procees in background
    rclpy.spin(node)
    # shutdown the ROS 2 client Library
    rclpy.shutdown()


# making a condition to start the main function when script is executed directly
if __name__ == "__main__":
    main()

        

        
