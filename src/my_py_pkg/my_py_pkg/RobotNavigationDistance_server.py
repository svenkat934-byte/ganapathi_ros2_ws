#!/usr/bin/env python3

import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle

from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

from my_robot_interfaces.action import NavigationDistance

#creating class for node creation
class RobotNavigationDistanceServer(Node):
    # intializing the node 
    def __init__(self):
        # with super() intailzing the node name
        super().__init__("robot_navigation_distance_server")

        # creating the server
        self.robot_distance_navigation_server_ = ActionServer(
            self,
            NavigationDistance,
            "robot_navigation_position",
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup()


        )

    # function for goal_request
    def goal_callback(self, goal_request: NavigationDistance.Goal):
        # printing goal is received
        self.get_logger().info("Received a goal")

        # making a condition to check
        if goal_request.target_position  < 0 or goal_request.delay < 0:
            # printing a reject goal
            self.get_logger().warn("Rejecting the goal")
            # returning goal response as reject
            return GoalResponse.REJECT
        # printing the accpet message
        self.get_logger().info("Accepting the goal")
        return GoalResponse.ACCEPT

    def execute_callback(self, goal_handle: ServerGoalHandle):
        target_position = goal_handle.request.target_position
        delay = goal_handle.request.delay
        result = NavigationDistance.Result()
        feedback = NavigationDistance.Feedback()
        counter = 0

        self.get_logger().info("Executing the goal ")

        for i in range(0, target_position):
            counter +=1

            self.get_logger().info(f"{counter}")

            feedback.current_position = counter

            goal_handle.publish_feedback(feedback)

            time.sleep(delay)

            if goal_handle.is_cancel_requested:
                self.get_logger().info("Canceling goal")

                goal_handle.canceled()

                result.final_position = counter
                result.robot_state = f"Robot Naviagted from 0 to {counter} position, could not reach target position due to canceling of goal"
                return result

        goal_handle.succeed()
        self.get_logger().info("Successfully Robot reached target position")
        result.final_position = counter
        result.robot_state = f"Robot successfully reached target position: {target_position}, and  Navigated from 0 to {counter} position, "
        return result

    def cancel_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info("Received a cancel request, so canceling the ActionServer")
        return CancelResponse.ACCEPT
        


# creation of main functionality
def main(args=None):
    # intailizing the rclpy libary
    rclpy.init(args=args)
    # making node instance 
    node = RobotNavigationDistanceServer()
    # making node spin in background to make run this program alive until we cancel 
    #rclpy.spin(node)
    rclpy.spin(node, MultiThreadedExecutor())
    # now destroying the node
    node.destroy_node()
    # making rclpy shutdown 
    rclpy.shutdown()

# condition to execution for main method
if __name__ == "__main__":
    main()

