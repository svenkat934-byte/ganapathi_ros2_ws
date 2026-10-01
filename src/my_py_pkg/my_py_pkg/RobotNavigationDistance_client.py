#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus

from my_robot_interfaces.action import NavigationDistance

class RobotNavigationClient(Node):

    def __init__(self):

        super().__init__("robot_navigation_poistionclient")

        self.robot_position_navigation_client_ = ActionClient(
            self, 
            NavigationDistance,
            "robot_navigation_position"
        )

    def send_goal(self, target_position, delay):
        self.robot_position_navigation_client_.wait_for_server()

        goal = NavigationDistance.Goal()
        goal.target_position = target_position
        goal.delay = delay
        self.robot_position_navigation_client_.send_goal_async(
            goal, feedback_callback=self.goal_feedback_callback).add_done_callback(self.goal_response_callback) 


    def goal_response_callback(self, future):
        self.goal_handle_ : ClientGoalHandle = future.result()

        if self.goal_handle_.accepted:
            self.get_logger().info("Goal got accepte")
            self.goal_handle_.get_result_async().add_done_callback(self.goal_result_callback)

        else:
            self.get_logger().info("Goal got rejected")


    def goal_result_callback(self, future):
        status = future.result().status
        result = future.result().result

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Success")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info("Aborted")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn("Canceled")

        self.get_logger().info(f"Result: final_position={result.final_position}  and robot_state={result.robot_state}")


    def goal_feedback_callback(self, feedback_msg):
        position = feedback_msg.feedback.current_position 
        self.get_logger().info(f"Got posistion feedback: {position} ")


        if position >5 :
            self.cancel_goal()

    def cancel_goal(self):
        self.get_logger().info("Send a cancel goal request")
        self.goal_handle_.cancel_goal_async()

def main(args=None):
    rclpy.init(args=args)
    node = RobotNavigationClient()
    node.send_goal(10, 0.5)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

