#!/usr/bin/env python3

# importing rclpy library
import rclpy
# import node functionality from rclpy.node library
from rclpy.node import Node
# import Action server and Goal response from actions library
from rclpy.action import ActionServer, GoalResponse, CancelResponse
# importing ServerGoalHandle from rclpy.action.sever
from rclpy.action.server import ServerGoalHandle

# importing MultiThreadedExecutor from rclpy.executors to implement multi node functionality
from rclpy.executors import MultiThreadedExecutor
# importing ReentrantCallbackgroup from rclpy.callback_grops to make group execution 
from rclpy.callback_groups import ReentrantCallbackGroup

# importing time 
import time


# import RobotCharging.action flie from my_robot_interface to implement action functionality 
from my_robot_interfaces.action import RobotCharging

# creating the class for node functionality 
class RobotChargingSupply_Server(Node):
    # making the node intizling with node init function 
    def __init__ (self):
        # with super() intiazling the node name
        super().__init__("robot_charging_server")

        # now creating the Action server variable to implement action server functionlaity 
        self.robot_charging_supply_server_ = ActionServer(
            self, 
            RobotCharging,
            "robot_charging_supply",
            goal_callback = self.goal_callback,
            cancel_callback= self.cancel_callback,
            execute_callback = self.execute_callback,
            callback_group=ReentrantCallbackGroup()


        )

    # now creating a function to check goal need to accpet or not 
    def goal_callback(self, goal_request: RobotCharging.Goal):
        # now printing a log message that Received a goal 
        self.get_logger().info("Received a goal")

        # making a condition to check whether goal should be accpeted or no t
        if goal_request.target_percentage <= 0 or goal_request.target_percentage >= 100 or goal_request.delay <= 0 :
            # priniting a log meessage that rejecting goal 
            self.get_logger().info("Rejecting the Goal")
            # return the goal response as reject
            return GoalResponse.REJECT
        # now printing log message as accpeted goal
        self.get_logger().info("Accepting the Goal")
        return GoalResponse.ACCEPT

    # creating cancel  callback function 
    def cancel_callback(self, goal_handle: ServerGoalHandle):
        # printing log as cancel request recieved
        self.get_logger().info("Received a cancel request, so canceling the server, thanks for cooperation ")
        # return cancel response as accpeted
        return CancelResponse.ACCEPT



    # creating execute callback function which main function here we say server what to do 
    def execute_callback(self, goal_handle_ : ServerGoalHandle):
        # assging the value for server action required varibles
        target_percentage = goal_handle_.request.target_percentage
        delay = goal_handle_.request.delay
        result = RobotCharging.Result()
        feedback = RobotCharging.Feedback()
        counter = 0

        # priniting a log message that executing a goal
        self.get_logger().info("Executing the Goal")

        # now runing the for to increasing the percentage and send feedback until targter_percentage macthes
        for i in range(0, target_percentage, 10):
            # incrementing counter value as 10
            counter += 10
            # printing the log message with counter value 
            self.get_logger().info(f"The current increment value is  {counter}")
            # making feedback varaible 
            feedback.current_percentage = counter
            # publishing the feedback
            goal_handle_.publish_feedback(feedback)
            # now making rclpy.spin take pause for 5 seconds
            time.sleep(delay)
            # checking is there any cancel request
            if goal_handle_.is_cancel_requested:
                # printing the cancel message
                self.get_logger().info("Canceling goal")
                goal_handle_.canceled()
                result.final_percentage = counter
                result.message = "Charging Failed ! "
                return result
        # after complteing for looop
        goal_handle_.succeed()
        result.final_percentage = counter
        result.message = "Charging Completed "
        return result




    

# defing main function of node excution 
def main(args=None):
    # making rclpy initalzition 
    rclpy.init(args=args)
    # making node class as instance
    node = RobotChargingSupply_Server()
    # making node spin in multi threading 
    rclpy.spin(node, MultiThreadedExecutor())
    # destroying node
    node.destroy_node()
    # shutown ing the rclpy 
    rclpy.shutdown()

# condition for execution of main method
if __name__ == "__main__":
    main()