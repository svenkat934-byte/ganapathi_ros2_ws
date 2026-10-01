#!/usr/bin/env python3

import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle

from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

from my_robot_interfaces.action import BatteryCharge

# creating a class
class RobotBatteryChargingServer(Node):
    # initalizing the node 
    def __init__(self):
        # with super() creating node name
        super().__init__("robot_battery_charging_server")

        self.robot_battery_charging_server_ = ActionServer(
            self,
            BatteryCharge,
            "robot_battery_charging",
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup()    
        )

    # creating a goal_callback 
    def goal_callback(self, goal_request: BatteryCharge.Goal):
        # printing  goal is received 
        self.get_logger().info("Received a goal")
        # making a condition to check 
        if goal_request.target_percentage <= 0:
            #printing a reject goal
            self.get_logger().warn("Rejecting the goal, target need to more than 0 ")
            # now return the goal response 
            return GoalResponse.REJECT
        # printing a goal is acceoted
        self.get_logger().info("Accepting the goal")
        # return the goal response
        return GoalResponse.ACCEPT

    # creating a cancel_callback method
    def cancel_callback(self, goal_handle: ServerGoalHandle):
        # printing the cancel message
        self.get_logger().info("Received a cancel request")
        # returning goal cancelresponse
        return CancelResponse.ACCEPT

    # creating execute_callback method
    def execute_callback(self, goal_handle: ServerGoalHandle):
        # now assiging the variables to store 
        target_percentage = goal_handle.request.target_percentage
        delay = goal_handle.request.delay
        result = BatteryCharge.Result()
        feedback = BatteryCharge.Feedback()
        counter = 0

        # printing message executing goal
        self.get_logger().info("Executing the goal")

        # now with for loop incrementing the battery charging percentage
        for i in range(0,target_percentage,10):
            #self.get_logger().info(f"target_percentage is {target_percentage}")
            counter += 10
            # printing counter value
            self.get_logger().info(f"{counter}")
            # storting current percentage
            feedback.current_percentage = counter
            # publishing the current percentage
            goal_handle.publish_feedback(feedback)
            # making a delay 
            time.sleep(delay)
            # is goal was canceled then 
            if goal_handle.is_cancel_requested:
                # printing the messgae canceling goal
                self.get_logger().info("Canceling goal")
                # caling goal cancel() method
                goal_handle.canceled()
                result.final_percentage = counter
                return result
        # after complteing the target
        goal_handle.succeed()
        result.final_percentage = counter
        return result
    







# main method 
def main(args=None):
    # intializing rclpy
    rclpy.init(args=args)
    # node instance
    node = RobotBatteryChargingServer()
    # spining the node in background
    rclpy.spin(node)
    # destroying the node
    node.destroy_node()
    # rclpy shutdown
    rclpy.shutdown()

# condition for main function
if __name__ == "__main__":
    main()
