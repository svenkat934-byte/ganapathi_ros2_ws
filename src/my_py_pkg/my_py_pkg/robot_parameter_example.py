#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import time

class RobotNode(Node):

    def __init__(self):
        super().__init__("robot_motion")

        self.declare_parameter("speed", 0.5)
        #self.declare_parameter("distance", 10.0)
        self.position = 0 
        self.speed = self.get_parameter("speed").value
        self.timer_ = self.create_timer(1.0, self.robot_printing)
        #self.distance = self.get_parameter("distance").value
        # con = False
        # while con == False:
        #     if self.position == 10.0:
        #         self.get_logger().info("Successfully Target reached!")     
        #         con = True
        #     else:
        #         self.position += self.speed
        #         self.get_logger().info(f"Robot speed: {self.speed}")
        #         self.get_logger().info(f"Robot position: {self.position}")
        

    def robot_printing(self):
        self.speed = self.get_parameter("speed").value
        #self.distance = self.get_parameter("distance").value
        # con = False
        # while con == False:
        #     if self.position == 10.0:
        #         self.get_logger().info("Successfully Target reached!")

        #         con = True
        #     else:
        #         self.position += self.speed
        #         self.get_logger().info(f"Robot speed: {self.speed}")
        #         self.get_logger().info(f"Robot position: {self.position}")

        self.position += self.speed
        self.get_logger().info(f"Robot speed: {self.speed}")
        self.get_logger().info(f"Robot position: {self.position}")

            
            
       
        
       

    # def __init__(self):
    #     super().__init__("robot")

    #     self.declare_parameter("speed", 0.5)

        

    #     #repeat = self.get_logger().info(f"Robot speed: {speed}")

    #     self.timer_ = self.create_timer(1.0 , self.print_parameter )

    # def print_parameter(self):
    #     self.speed = self.get_parameter("speed").value
    #     self.get_logger().info(f"Robot speed: {self.speed}")

def main(args=None):
    rclpy.init(args=args)
    node = RobotNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()