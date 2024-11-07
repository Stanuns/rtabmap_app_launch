import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription

def generate_launch_description():
    rtabmap_bringup_dir = get_package_share_directory('rtabmap_launch')
    rtabmap_launch_dir = os.path.join(rtabmap_bringup_dir, 'launch')
    rtabmap_ros = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(rtabmap_launch_dir, 'rtabmap.launch.py')),
            launch_arguments={'rtabmap_args': '--delete_db_on_start',
                              'rgb_topic': '/camera/color/image_raw',
                              'depth_topic': '/camera/depth/image_raw',
                              'camera_info_topic': '/camera/color/camera_info',
                              'frame_id': 'base_footprint',
                              'use_sim_time': 'false',
                              'approx_sync':'true',
                              'qos': '2',
                              'rviz': 'true',
                              'queue_size': '30',
                              }.items(),
    )

    return LaunchDescription([
        rtabmap_ros,
    ])