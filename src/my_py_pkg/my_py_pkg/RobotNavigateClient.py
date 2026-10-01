#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
# importing actions client
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus

from my_robot_interfaces.action import RobotNavigate



# defing class 
class RobotNavigateClient(Node):
    # intializing the node
    def __init__(self):
        # with super() now intialzing the node name
        super().__init__("robot_navigation_client")

        # creating action client variabe
        self.robot_navigation_client_ = ActionClient(
            self, RobotNavigate, "robot_navigation"
        )

    # defing the send goal
    def send_goal(self, target_distance, speed):
        # waiting for to active 
        self.robot_navigation_client_.wait_for_server()
        # with instance calling goal varibale  and assoging tehm values
        goal = RobotNavigate.Goal()
        goal.target_distance = target_distance
        goal.speed = speed
        self.robot_navigation_client_.send_goal_async(
            goal, feedback_callback=self.goal_feedback_callback).add_done_callback(self.goal_response_callback)

    # defing the goal response callback
    def goal_response_callback(self, future):
        # now with clientgoalhandle handling future result
        self.goal_handle_ : ClientGoalHandle = future.result()
        # making a condition for check goal accpeted 
        if self.goal_handle_.accepted:
            # printing the goal is accpeted
            self.get_logger().info("Goal got accepted")
            # adding asynchorize calll
            self.goal_handle_.get_result_async().add_done_callback(
                self.goal_result_callback)
        #  if goal is not accpeted
        else:
            # printing the goal is rejected
            self.get_logger().info("Goal got rejected")

    # defing the goal_result_callback
    def goal_result_callback(self, future):
        # storing the future result status
        status = future.result().status
        # stroing the future result result
        result = future.result().result
        # checking the status as succeeded 
        if status == GoalStatus.STATUS_SUCCEEDED:
            # printing the success
            self.get_logger().info("Success")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().error("Aborted")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn("Canceled")
        self.get_logger().info(f"Result: {result.distance_travelled}")

    # defing the goal feedback callback
    def goal_feedback_callback(self, feedback_msg):
        # distance feedback
        distance = feedback_msg.feedback.current_distance
        self.get_logger().info(f"Got feedback: {distance}")
        if distance >= 2:
            self.cancel_goal()

    # deifng the cancel_goal
    def cancel_goal(self):
        self.get_logger().info("Send a cancel goal request")
        self.goal_handle_.cancel_goal_async()


# now main function
def main(args=None):
    # now initializing rclpy
    rclpy.init()
    # now making node insatnce
    node = RobotNavigateClient()
    # sending the goal 
    node.send_goal(10, 0.5)
    # now spining the node
    rclpy.spin(node)
    # now making node destroy 
    node.destroy_node()
    # now shutdowning the rclpy
    rclpy.shutdown()


# a condtion to execute file from main method 
if __name__ == "__main__":
    main()