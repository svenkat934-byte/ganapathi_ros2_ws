#!/usr/bin/env python3

import rclpy
import time
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse

from rclpy.action.server import ServerGoalHandle

from my_robot_interfaces.action import RobotNavigate

from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup


class RobotNavigateServer(Node):
    # initalization of  node classs
    def __init__(self):
        # with super() intailzing the node
        super().__init__("robot_navigate_server")

        # creating action 
        self.robot_navigate_server_ = ActionServer(
            self,
            RobotNavigate, # calling the Action file 
            "robot_navigation", #creating a topic name
            goal_callback=self.goal_callback,
            cancel_callback= self.cancel_callback,
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup()

        )

    # creating a goal_callback method 
    def goal_callback(self, goal_request: RobotNavigate.Goal # calling the Goal fucntion from RobtoNavigation.action file
                      ):
        # printing that goal is received
        self.get_logger().info("Received a goal")
        # making a condition to check the target_distance is greater than zero not
        if goal_request.target_distance <= 0:
            # printing message as reject goal target must be greater than 0
            self.get_logger().warn("Rejecting the goal, target number must be greater than Zero")
            # now returning goal and exiting the goal
            return GoalResponse.REJECT
        # now if value is greater than zero priting Accpet goal
        self.get_logger().info("Accepting the goal")
        # return the goal reposene as accpet
        return GoalResponse.ACCEPT

    # now creating the cancel_callback method
    def cancel_callback(self, goal_handle: ServerGoalHandle ):
        # printing the cancel messgae
        self.get_logger().info("Received a cancel request")
        # returning the cancel response as accept
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle: ServerGoalHandle):
        # now assigning the variables to store the targte_distance from action file with help of serverGoalHandle
        target_distance = goal_handle.request.target_distance
        speed = goal_handle.request.speed
        result = RobotNavigate.Result()
        feedback = RobotNavigate.Feedback()
        counter = 0

        # now priting message executing the goal
        self.get_logger().info("Executing the goal")

        # now making a for to run till counter reaches the target_distance
        for i in range(target_distance):
            # incrementing the counter
            counter += 1 
            # printing the counter value
            self.get_logger().info(f"{counter}")
            # now making the feedback mesage dispaly 
            feedback.current_distance = counter
            # pushing the goal
            goal_handle.publish_feedback(feedback)
            # making a delay of speed rate
            time.sleep(speed)
            # now if user wante to cancel the request then canceling the request
            if goal_handle.is_cancel_requested:
                # printing the message as canceling goal
                self.get_logger().info("Canceling goal")
                # now calling the cancel() method
                goal_handle.canceled()
                # printing log result value
                result.distance_travelled = counter
                return result
            # if server runs continously 
        goal_handle.succeed()
            # printing result value
        result.distance_travelled = counter

            # now returning the result
        return result








# main function 
def main(args=None):
    # intializing rclpy 
    rclpy.init(args=args)
    # calling node constrctor 
    node = RobotNavigateServer()
    # making the node spin
    rclpy.spin(node)
    # making node destroy 
    node.destroy_node()
    # making rclpy shutdown
    rclpy.shutdown()

# making the main function condition
if __name__ == "__main__":
    main()