#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    ld = LaunchDescription()

    param_config = os.path.join(
        get_package_share_directory("my_robot_bringup"),
        "config", "number_params.yaml"
    )

    number_publisher = Node(
        package="my_py_pkg",
        executable="number_publisher_node",
        name="num_pub1",
        remappings=[("/number", "/my_number")],
        parameters=[param_config],
        namespace="/abc",
        
    )


    number_counter = Node(
        package="my_py_pkg",
        executable="number_counter_node",
        remappings=[("number", "my_number")],
        namespace="/abc",
    )

    ld.add_action(number_publisher)
    ld.add_action(number_counter)
    return ld