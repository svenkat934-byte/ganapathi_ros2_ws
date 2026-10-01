#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import ResetCounter

# creating a node class
class ResetCounterClientNode(Node):
    # intiazling the node function
    def __init__(self):
        super().__init__("reset_counter_client")
        # creating a client 
        self.client_ = self.create_client(ResetCounter, "reset_counter")

    # creating a service call function
    def call_reset_counter(self, value):
        # creating a while loop 
        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service...")

        request = ResetCounter.Request()
        request.reset_value = value
        future = self.client_.call_async(request)
        future.add_done_callback(
            self.callback_reset_counter_response )

    def callback_reset_counter_response(self, future):
        response = future.result()
        self.get_logger().info("Success flag: " +  str(response.success))
        self.get_logger().info(f"Message: {response.message}")

# defining the main function 
def main(args=None):
    rclpy.init(args=args)
    node = ResetCounterClientNode()
    node.call_reset_counter(20)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()