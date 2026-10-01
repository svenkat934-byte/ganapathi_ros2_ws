#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import GoalResponse, CancelResponse, ActionServer
from rclpy.action.server import ServerGoalHandle

from my_robot_interfaces.action import PickObject

import time
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

from random import randint

# defing class 
class RobotArmOperation_server(Node):

    def __init__(self):
        # with super() initalizing the node
        super().__init__("robot_pickarm_operation_server")

        # storing the action server
        self.robot_pickarm_server_ = ActionServer(
            self, 
            PickObject,
            "robot_pickarm_operation",
            goal_callback=self.goal_callback,
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup() 
              )

    def goal_callback(self, goal_request: PickObject.Goal):
        # priting log messgae that goal recevied
        self.get_logger().info("Received a goal")
        # making a condition to check the goal 
        if (goal_request.object_id <=1 or goal_request.object_id >=10):
            # printing the goal as reject 
            self.get_logger().info("Rejecting the goal, target need to more than 0 and lessthan 11")
            # reject the goal
            return GoalResponse.REJECT

        # else accpeting the goal 
        self.get_logger().info("Accepting the Goal")
        # return goal response
        return GoalResponse.ACCEPT

    # creating execute callback method
    def execute_callback(self, goal_handle: ServerGoalHandle):
        # assigning the variables to store
        object_id = goal_handle.request.object_id
        result = PickObject.Result()
        feedback = PickObject.Feedback()
        move_robot_arm_x = 0
        move_robot_arm_y = 0


        # printing message executing goal
        self.get_logger().info("Executing the goal")
        feedback.current_state = f"Searching for object with object id: {object_id}"
        goal_handle.publish_feedback(feedback)

        # with for loop finding object id 
        for i in range(1,11):
            if i == object_id:
                # sending the object id found
                self.get_logger().info("Found object ")
                feedback.current_state = f"Moving Robot Arm towards object id: {object_id}"
                goal_handle.publish_feedback(feedback)
                time.sleep(0.5)
                # moving robot arm in x direction
                for i in range(1, object_id):
                    # incrementing robot arm x value
                    move_robot_arm_x += 1
                    time.sleep(0.5)
                    # printing message that robot moved in x axis 
                    self.get_logger().info(f"Moving Robot Arm towards  object id:{object_id}, reached object id :{move_robot_arm_x}")
                # printing that succesfully reached objrct id
                self.get_logger().info(f"Successfully  Robot Arm reached  object id {object_id}")
                # sending feedback
                feedback.current_state = f"Approaching object id: {object_id}"
                goal_handle.publish_feedback(feedback)
                time.sleep(0.5)
                # moving robot arm in y axis
                for i in range(5):
                    # making iteration for move y robot arm
                    move_robot_arm_y += 1
                    time.sleep(0.5)
                    # printing robot moving y axis 
                    self.get_logger().info(f"Robot Arm moving Approchaing object id:{object_id} moving down in y-axis direction: {move_robot_arm_y} ")
                # printing success message 
                self.get_logger().info(f"Successfully Approched object id:{object_id}")
                feedback.current_state = "Now Gripping Object"
                goal_handle.publish_feedback(feedback)
                time.sleep(0.5)

                # now moving towards griping object
                contact_point = randint(1,5)
                grip_conatct = False
                while not grip_conatct:
                    # condition for contact points
                    if contact_point == 5:
                        self.get_logger().info(f"Successfully contacted all 5 fingers of RobotArm with object ")
                        # send feedback to griping 
                        feedback.current_state = "Successfully griped the object, LIFTING Object"
                        goal_handle.publish_feedback(feedback)
                        time.sleep(0.5)
                        grip_conatct = True
                    else:
                        # printing fail message 
                        self.get_logger().info(f"Failed to Grip-Contact --> {contact_point} fingers are successful   ")
                        # changing direction 
                        self.get_logger().info("Changing the direction")
                        contact_point = randint(1,5)
                        time.sleep(0.5)

                # now moving to state lifted object
                for i in range(5,0, -1):
                                # making iteration for move y robot arm
                        move_robot_arm_y = i
                                   # printing robot moving y axis 
                        self.get_logger().info(f"Robot Arm Lifting, in y-axis direction: {move_robot_arm_y} ")
                               # printing success message 

                self.get_logger().info(f"Successfully Lifted  object id:{object_id}")
                goal_handle.succeed()
                result.success = True
                result.message = "Object picked successfully"
                return result


        


# main method
def main(args=None):
    # rclpy initalization 
    rclpy.init(args=args)
    # node intaization
    node = RobotArmOperation_server()
    # making node spin
    rclpy.spin(node)
    # makind node destroy
    node.destroy_node()
    # shutdown rclpy
    rclpy.shutdown()

if __name__ == "__main__":
    main()

