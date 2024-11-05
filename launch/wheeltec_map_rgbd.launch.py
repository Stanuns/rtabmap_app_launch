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
    qos = LaunchConfiguration('qos')
    localization = LaunchConfiguration('localization')

    
    parameters={
          'frame_id':'base_link',  
          'visual_odometry':True,
          'icp_odometry':False,
          'stereo':True,
          'subscribe_rgbd':True,
          'subscribe_stereo':False,
          'subscribe_odom_info':True, #True:选用内部视觉里程计或ICP里程计，False：选用外部里程计
          'subscribe_scan':True,
          'approx_sync':True,
          'Reg/Strategy':'0',     #选择 ICP 来改进使用激光扫描通过 ICP 发现的全局闭环。0=Visual, 1=ICP, 2=Visual+ICP
          'Rtabmap/TimeThr':'2000',
          'Rtabmap/MemoryThr': '2000',
          'qos_image':qos,
          'qos_imu':qos,
          'qos_scan':qos,
          'Grid/RangeMin':'0.2', 
          'Grid/Sensor': 'false',  #Gridmap is come from depth camera  or not ,default:false ,come from lidar
          'Reg/Force3DoF':'true',  #强制 3DoF 注册：roll、pitch和z不会被估计
          'Optimizer/Slam2D':True, #强制视觉里程计仅在3DOF（x，y，theta）中跟踪车辆,增加地图的鲁棒性,配合参数：Reg/Force3DoF=true
          'RGBD/AngularUpdate':'0.01',
          'RGBD/LinearUpdate': '0.01',
          'RGBD/NeighborLinkRefining':'true',
          'wait_for_transform':0.5,
          'latch':False,
          'wait_imu_to_init':False}

    remappings=[
          ('imu', '/imu'),
          ('scan', '/scan'),
          ('odom', '/stereo_odometry'),   #subscribe_odom_info=false时，重新映射该odom为外部里程计的topic名称
          ('rgbd_image', '/rgbd_image'),
          ('left/image_rect', '/camera/infra1/image_rect_raw'),
          ('left/camera_info', '/camera/infra1/camera_info'),
          ('right/image_rect', '/camera/infra2/image_rect_raw'),
          ('right/camera_info', '/camera/infra2/camera_info')]

    return LaunchDescription([
         DeclareLaunchArgument(
            'qos', default_value='2',
            description='QoS used for input sensor topics'),

         DeclareLaunchArgument(
            'localization', default_value='false',
            description='Launch in localization mode.'),


        Node(
            package='rtabmap_odom', executable='stereo_odometry', output='screen',
            parameters=[parameters],
            remappings=remappings),

        # # rtabmap不支持stereo与scan混合建图，需要现将stereo转为rgbd模式后，再与scan混合使用      
        # Node(
        #     package='rtabmap_sync', executable='stereo_sync', output='screen',
        #     parameters=[parameters],
        #     remappings=remappings),

        # SLAM Mode:
        Node(
            condition=UnlessCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters],
            remappings=remappings,
            arguments=['-d']),
            
        # Localization mode:
        Node(
            condition=IfCondition(localization),
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=[parameters,
              {'Mem/IncrementalMemory':'False',
               'Mem/InitWMWithAllNodes':'True'}],
            remappings=remappings),
                

    ])