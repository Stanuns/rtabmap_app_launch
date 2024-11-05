"""
  Copyright 2018 The Cartographer Authors
  Copyright 2022 Wyca Robotics (for the ros2 conversion)

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, SetRemap
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import Shutdown
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    wheeltec_bringup_dir = get_package_share_directory('turn_on_wheeltec_robot')
    wheeltec_launch_dir = os.path.join(wheeltec_bringup_dir, 'launch')
    wheeltec_robot = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(wheeltec_launch_dir, 'turn_on_wheeltec_robot.launch.py')),
            launch_arguments={'carto_slam': 'true'}.items(),
    )
    wheeltec_lidar = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(wheeltec_launch_dir, 'wheeltec_lidar.launch.py')),
    )

    camera_bringup_dir = get_package_share_directory('astra_camera')
    camera_launch_dir = os.path.join(camera_bringup_dir, 'launch')
    wheeltec_astra_camera = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(camera_launch_dir, 'astra_mini.launch.py')),
    )

    return LaunchDescription([
        wheeltec_robot,
        wheeltec_lidar,
        wheeltec_astra_camera,
    ])