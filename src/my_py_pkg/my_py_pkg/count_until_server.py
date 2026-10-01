#!/usr/bin/env python3

# importing rclpy
import rclpy
# importing time
import time
# importing the node
from rclpy.node import Node
# import ActionServer, GoalResponse
from rclpy.action import ActionServer, GoalResponse, CancelResponse

# importing ServerGoalHandle from rclpy.action.server
from rclpy.action.server import ServerGoalHandle
# importing CountUntil action file 
from my_robot_interfaces.action import CountUntil

from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

class CountUntilServerNode(Node):
    # creating a initalization of node
    def __init__(self):
        # making a node intiazliation with super()
        super().__init__("count_until_server")

        # creating action
        self.count_until_server_ = ActionServer(
            self, 
            CountUntil,
            "count_until",
            goal_callback = self.goal_callback,
            cancel_callback = self.cancel_callback,
            execute_callback = self.execute_callback,
            callback_group = ReentrantCallbackGroup()
        )

    # goal_callback method to check whether goal need to accpet or not 
    def goal_callback(self, goal_request: CountUntil.Goal):
        # printing in terminal 
        self.get_logger().info("Received a goal")
        # making a condition 
        if goal_request.target_number <= 0:
            # printing message that need postive target number
            self.get_logger().warn("Rejecting the goal, target number must be positive")
            # now returning the Reject response
            return GoalResponse.REJECT
        # now we get positive number greater than zero so we accpeting goal
        self.get_logger().info("Accepting the goal")
        # returning goal accpet resposne
        return GoalResponse.ACCEPT

    # as goal is accpeted now executue callback work creating execute_callback function
    def execute_callback(self, goal_handle: ServerGoalHandle):
        target_number = goal_handle.request.target_number
        delay = goal_handle.request.delay
        result = CountUntil.Result()
        feedback = CountUntil.Feedback()
        counter = 0

        self.get_logger().info("Executing the goal")
        for i in range(target_number):
            counter += 1
            self.get_logger().info(f"{counter}")
            feedback.current_number = counter
            goal_handle.publish_feedback(feedback)
            time.sleep(delay)
            if goal_handle.is_cancel_requested:
                        self.get_logger().info("Canceling goal")
                        goal_handle.canceled()
                        result.reached_number = counter
                        return result

        goal_handle.succeed()
        result.reached_number = counter

        

        return result

    # creating the callback for canceling the node
    def cancel_callback(self, goal_handle: ServerGoalHandle):
        # printing the logger with receive a cancel request
        self.get_logger().info("Received a cancel request")
        # return the cancelresponse as accept
        return CancelResponse.ACCEPT






# main function
def main(args=None):
    # rclpy initazliation
    rclpy.init(args=args)
    # making node instance
    node = CountUntilServerNode()
    # making spin of node
    rclpy.spin(node, MultiThreadedExecutor())
    # making node destroy
    node.destroy_node()
    # making rclpy shutdown
    rclpy.shutdown()

# condition to exectue directly 
if __name__ == "__main__":
    main()
