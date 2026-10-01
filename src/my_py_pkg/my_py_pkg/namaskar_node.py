# shebang line
#!/usr/bin/env python3

#import rclpy for intialization of ros python packages
import rclpy
# from rclpy.node importing node package for using node functionlaities
from rclpy.node import Node
from example_interfaces.msg import Int64

# creating a class for node named namaskar
class Namaskar_Node(Node):
    # creating a function for intialization of node
    def __init__(self):
        # with help of super function we initalizing the node 
        super().__init__("Namasakar_ji_node")
        # making a count
        self.count_ = 0
        # making a timer function for namsakr printing function
        #self.timer_ = self.create_timer(1.0, self.print_Namaskar)

        self.number_subscriber_ = self.create_subscription(Int64, "number_sh", self.callback_number, 10)

    def callback_number(self, msg):
        self.get_logger().info(f"Received number: {msg.data}")

    # creating a function for namaskar node
    def print_Namaskar(self):
        # print a statement using get_logger method
        self.get_logger().info("Namasakr guruji")
        # incrementing count 
        self.count_ +=1
        # writing a condition for count to stop the node after 5 times of printing
        if self.count_ == 5:
            # using destroy_node method to destroy the node
            self.destroy_node()
            # shutting the node after destroying the node
            rclpy.shutdown()

# creating the main method 
def main(args=None):
    # initializing the rclpy node
    rclpy.init(args=args)
    # making a constructor for class 
    node = Namaskar_Node()
    # now spin the node with rclpy.spin
    rclpy.spin(node)
    # now shutdowing the node
    rclpy.shutdown()

# making the main condition to start the program
if __name__ == "__main__":
    main()
