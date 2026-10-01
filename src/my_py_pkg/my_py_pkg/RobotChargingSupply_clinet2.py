#!/usr/bin/env python3

# importing rclpy library
import rclpy
# importing node functionality from rclpy.node 
from rclpy.node import Node
# importing Action client from rclpy.action
from rclpy.action import ActionClient
# importing clinetGoalhandle and goal status from rclpy.action.client
from rclpy.action.client import ClientGoalHandle, GoalStatus

# import Robotcharging from my_robot_interfaces/action 
from my_robot_interfaces.action import RobotCharging

# creating the node class 
class RobotChargingSupplyClient2(Node):
    # makng node init 
    # creating the function
    def __init__(self):
        # with super() function creating the node name
        super().__init__("robot_charging_supply_client2")

        # creating Action client
        self.robot_charging_supply_client2_ = ActionClient(
            self, 
            RobotCharging,
            "robot_charging_supply"
        )

    # creating send goal function 
    def send_goal(self, target_percentage, delay):
        # waiting for the server
        self.robot_charging_supply_client2_.wait_for_server()

        # creating vairable 
        goal = RobotCharging.Goal()
        goal.target_percentage = target_percentage
        goal.delay = delay
        self.robot_charging_supply_client2_.send_goal_async(
            goal, feedback_callback=self.goal_feedback_callback).add_done_callback(
                self.goal_response_callback
        )
        

    # creating goal response callback 
    def goal_response_callback(self, future):
        self.goal_handle_ : ClientGoalHandle = future.result()

        if self.goal_handle_.accepted:
            self.get_logger().info("Goal got accpted")
            self.goal_handle_.get_result_async().add_done_callback(
                self.goal_result_callback
            )
        else:
            self.get_logger().info("Goal got rejected")

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

    def goal_feedback_callback(self, feedback_msg):
        percentage = feedback_msg.feedback.current_percentage
        self.get_logger().info(f"Got feedback: {percentage}")

# writing main function 
def main(args=None):
    # initzlaing the rclpy
    rclpy.init(args=args)
    # creating node instance 
    node = RobotChargingSupplyClient2()
    # passing paramters to send goal function
    node.send_goal(60, 0.5)
    # making node alive in background
    rclpy.spin(node)
    # destroying the node
    node.destroy_node()
    # making rclpy shutdown
    rclpy.shutdown()


# condition to execution from main function
if __name__ == "__main__":
    main()
