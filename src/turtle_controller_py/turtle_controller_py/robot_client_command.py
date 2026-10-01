#!/usr/bin/env python3

import sys
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import RobotCommand

# class node
class RobotClientNode(Node):
    # creating a initizlination
    def __init__(self):
        # with super() intizlization node
        super().__init__("robot_command_client")

        # creating a client 
        self.robot_command_client_ = self.create_client(RobotCommand, "robot_command")

        # Wait until service is online
        while not self.robot_command_client_.wait_for_service(timeout_sec = 1.0):
            # printing the message that waiting for service
            self.get_logger().info("Service not available, waiting...")


    # creating a function 
    def callback_command_client(self, command_str):
        # 1. Create request object
        request = RobotCommand.Request()
        request.command = command_str

        # 2. Call service asynchronously
        future = self.robot_command_client_.call_async(request)

        # 3. Wait for response synchronously 
        rclpy.spin_until_future_complete(self, future)

        # 4. Process response 
        if future.result() is not None:
            self.get_logger().info(f"Response: {future.result().message}")
        else:
            self.get_logger().error("Service call failed")

# main functionalites
def main(args=None):
    # initizling the rclpy
    rclpy.init(args=args)
    # get command from CLI argument, default to "forward"
    command_input = sys.argv[1] if len(sys.argv) > 1 else "forward"

    node = RobotClientNode()
    node.callback_command_client(command_input)

    rclpy.shutdown()

if __name__ == "__main__":
    main()


