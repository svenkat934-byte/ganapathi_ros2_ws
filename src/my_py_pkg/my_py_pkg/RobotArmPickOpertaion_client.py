#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus

from my_robot_interfaces.action import  PickObject

from random import randint

class RobotArmPickOperationClient(Node):
    def __init__(self):
        super().__init__("robot_pick_operation_client")

        self.robot_pickarm_client_ = ActionClient(
            self, 
            PickObject,
            "robot_pickarm_operation",
        )


    # defing send goal
    def send_goal(self, object_id):
        #  waiting for server
        self.robot_pickarm_client_.wait_for_server()
        # making instance variable creation
        goal = PickObject.Goal()
        goal.object_id = object_id
        self.robot_pickarm_client_.send_goal_async(
            goal, feedback_callback=self.goal_feedback_callback).add_done_callback(
                self.goal_response_callback)


    def goal_response_callback(self, future):
        self.goal_handle_ : ClientGoalHandle = future.result()

        if self.goal_handle_.accepted:
            self.get_logger().info("Goal got Accepted")
            self.goal_handle_.get_result_async().add_done_callback(
                self.goal_result_callback
            )
        else:
            self.get_logger().info("Goal got Rejected")


    def goal_result_callback(self, future):
        status = future.result().status
        result = future.result().result
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Success")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info("Aborted")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn("Canceled")
        self.get_logger().info(f"Result: {result.message}")

    def goal_feedback_callback(self, feedback_msg):
        state = feedback_msg.feedback.current_state
        self.get_logger().info(f"Got feedback: {state}")




def main(args=None):
    rclpy.init(args=args)
    node = RobotArmPickOperationClient()
    node.send_goal(randint(1,10))
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()