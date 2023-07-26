import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    #check if using sim time
    use_sim_time = LaunchConfiguration('use_sim_time')

    #process UDRF file
    package_path = os.path.join(get_package_share_directory('mobile_package'))
    xacro_file = os.path.join(package_path,'description','robot_URDF.xacro')
    #robot_description_config = Command(['xacro', xacro_file])
    robot_description_config = xacro.process_file(xacro_file)

    #robot_state_publisher node
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}
    robot_state_publisher_node = Node(
        package ='robot_state_publisher',
        executable = 'robot_state_publisher',
        output = 'screen',
        parameters = [params]
    )

    #launch
    return LaunchDescription([
        DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use sim time if true'
        ),
        robot_state_publisher_node
    ])