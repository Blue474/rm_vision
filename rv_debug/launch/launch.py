import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('rv_debug'))

    rv_debug_node = Node(
        package='rv_debug',
        executable='fakecam',
        namespace='',
        output='',
        emulate_tty=True,
        parameters=[],
    )

    return LaunchDescription([rv_debug_node])
