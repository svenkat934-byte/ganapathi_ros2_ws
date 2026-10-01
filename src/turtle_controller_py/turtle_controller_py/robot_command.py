#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import RobotCommand

# class 
class RobotCommandServer(Node):
    # intilization function 
    def __init__(self):
        # 
        super().__init__("robot_command")
        # creating a service
        self.robot_command_service_ = self.create_service(RobotCommand, "robot_command", self.callback_robot_command)

       
    

    # creatingservice function 
    def callback_robot_command(self, request: RobotCommand.Request, response: RobotCommand.Response):
        # now usings list making condtion 
        if request.command == "left":
            response.message = "Robot turning left"

        elif request.command == "right":
            response.message = "Robot turning right"

        elif request.command == "stop":
            response.message = "Robot stopped"

        elif request.command == "forward":
            response.message = "Robot moving forward"

        else:
            response.message = "Unknown Command"

        return response
  


# creating main function 
def main(args=None):
	# intializing rclpy
	rclpy.init(args=args)
	# creating a constructor for class 
	node = RobotCommandServer()
	# spin the node in terminal 
	rclpy.spin(node)
	#shutdown of the node
	rclpy.shutdown()

# making a condition to run this program
if __name__ == "__main__":
	main()
	