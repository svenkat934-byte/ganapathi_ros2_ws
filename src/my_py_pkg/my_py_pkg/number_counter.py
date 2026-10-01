#shebang for python3
# !/usr/bin/env python3
# import rclpy library for ROS 2 python client library
import rclpy
# import Node class from rclpy.node module 
from rclpy.node import Node
# import int64 message type from example_interfaces.msg
from example_interfaces.msg import Int64
# importing ResetCounter from my_robot_interfaces
from my_robot_interfaces.srv import ResetCounter


# creating a class NumberCounterNode
class NumberCounterNode(Node):
    # creating a function __init__ that initializes the Node
    def __init__(self):
        # calling the constructor of parent class Node with super() function and passing node name 
        super().__init__("number_counter")
        # creating a variable to store the counter value 
        self.counter_ = 0
        #creating a subscriber object that will subscribe to the topic Int64 message type , "number" topic with 10 queue size
        self.number_subscriber_ = self.create_subscription(Int64, "number", self.callback_number, 10)
        # creating a service that call reset_counter function 
        self.reset_counter_service_ = self.create_service(ResetCounter, "reset_counter", self.callback_reset_counter)
        # prtinting a log message as number counter has been started
        self.get_logger().info("Number Counter has been started.")

    # creating a function callback_number 
    def callback_number(self, msg: Int64):
        # assiging the counter value with msg.data
        self.counter_ += msg.data
        # printing a log message with counter value
        self.get_logger().info(f"Counter: {self.counter_}")

    # creating a function for reset_counter
    def callback_reset_counter(self, request: ResetCounter.Request, response: ResetCounter.Response):
        if request.reset_value < 0:
            response.success = False
            response.message = "Cannot reset counter to a negative value"
        elif request.reset_value > self.counter_:
            response.success = False
            response.message = "Reset value must be lower than current counter value"
        else: 
            self.counter_ = request.reset_value
            self.get_logger().info("Reset counter to " + str(self.counter_))
            response.success = True
            response.message = "Success"
        return response
    

# creating a main function that will be executed when the script is executed 
def main(args=None):
    # initializing the ROS 2 client library 
    rclpy.init(args=args)
    # creating an instance of NumberCounterNode class 
    node = NumberCounterNode()
    # spining the node to keep it alive and process in background
    rclpy.spin(node)
    # shutdown the ROS 2 client library
    rclpy.shutdown()

# making a condition to start with main function when script is executed directly
if __name__ == "__main__":
    main()