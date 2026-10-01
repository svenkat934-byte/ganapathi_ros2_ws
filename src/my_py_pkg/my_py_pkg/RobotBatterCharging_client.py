#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus

from my_robot_interfaces.action import BatteryCharge

class RobotBatteryChargingClient(Node):
    def __init__(self):
        super().__init__("robot_battery_client")

        # creating the action client
        self.robot_battery_client_ = ActionClient(
            self, 
            BatteryCharge, 
            "robot_battery_charging")

        self.cancel_sent = False


    # defing send goal
    def send_goal(self, target_percentage, delay):
        # waiting server
        self.robot_battery_client_.wait_for_server()
        # with instance assiging the battery charging action values
        goal = BatteryCharge.Goal()
        goal.target_percentage = target_percentage
        goal.delay = delay
        self.robot_battery_client_.send_goal_async(
            goal, feedback_callback=self.goal_feedback_callback ).add_done_callback(self.goal_response_callback)

    # defing the goal response callback
    def goal_response_callback(self, future):
        # with clientgoalhandle instance handling the adavance result
        self.goal_handle_ : ClientGoalHandle = future.result()
        # condition to check the goal is accpeted or not
        if self.goal_handle_.accepted:
            self.get_logger().info("Goal got accepted")
            self.goal_handle_.get_result_async().add_done_callback(
                self.goal_result_callback)
        else:
            self.get_logger().info("Goal got rejected")

    # deinging the goal_resukr 
    def goal_result_callback(self, future):
        status = future.result().status
        result = future.result().result
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Success")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().error("Aborted")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn("Canceled")
        self.get_logger().info(f"Result: {result.final_percentage}")

        
    # goal feedback method 
    def goal_feedback_callback(self, feedback_msg):
        percentage = feedback_msg.feedback.current_percentage
        self.get_logger().info(f"Got feedback: {percentage}")

    #     if percentage >= 20 and not self.cancel_sent:
    #         self.cancel_sent = True
    #         self.cancel_goal()


    # #deing the cancelgoal
    # def cancel_goal(self):
    #     self.get_logger().info("Send a cancel goal request")
    #     self.goal_handle_.cancel_goal_async()


def main(args=None):
    rclpy.init(args=args)
    node = RobotBatteryChargingClient()
    node.send_goal(80, 0.5)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()