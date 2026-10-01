from setuptools import find_packages, setup

package_name = 'my_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='saivenkat',
    maintainer_email='Saivenkatkadavergu@todo.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "namaha_Shivaya_node = my_py_pkg.my_first_node:main",
            "Jaganath_node = my_py_pkg.krishna_node:main",
            "robot_node = my_py_pkg.robot_node:main",
            "counter_node = my_py_pkg.counter_node:main",
            "battery_node = my_py_pkg.Battery_node:main",
            "namaskar_node = my_py_pkg.namaskar_node:main",
            "number_publisher_node = my_py_pkg.number_publisher:main",
            "number_counter_node = my_py_pkg.number_counter:main",
            "custom_message_publisher_node = my_py_pkg.custom_message:main", 
            "reset_counter_client_node = my_py_pkg.reset_counter_client:main",  
            "countuntilServerNode = my_py_pkg.count_until_server_minimal:main", 
            "countuntilclientNode = my_py_pkg.count_client_minimal:main",
            "countuntil_client = my_py_pkg.count_until_client:main",
            "countuntil_server = my_py_pkg.count_until_server:main",
            "RobotNavigation_Server = my_py_pkg.RobotNavigateServer:main",
            "RobotNavigation_Client = my_py_pkg.RobotNavigateClient:main",
            "RobotBattery_client = my_py_pkg.RobotBatterCharging_client:main",
            "RobotBattery_server = my_py_pkg.RobotBatterCharging_server:main",
            "RobotArmPick_client = my_py_pkg.RobotArmPickOpertaion_client:main",
            "RobotArmPick_server = my_py_pkg.RobotArmPickOpertaion_server:main",
            "RobotNavigation_Distance_server = my_py_pkg.RobotNavigationDistance_server:main",
            "RobotNavigation_Distance_client = my_py_pkg.RobotNavigationDistance_client:main",
            "RobotChargingSupply_sever = my_py_pkg.RobotChargingSupply_server:main",
            "RobotChargingSupply_client1 = my_py_pkg.RobotChargingSupply_client1:main",
            "RobotChargingSupply_client2 = my_py_pkg.RobotChargingSupply_clinet2:main",
            "robot_parameter = my_py_pkg.robot_parameter_example:main",

            

            
        ],
    },
)
