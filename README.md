# rtabmap_app_launch

# 使用Astra pro plus进行rtabmap建图[reference](https://blog.csdn.net/weixin_45007300/article/details/133931877)

## CLI启动方式

- 1. 启动astra pro plus

```bashrc
ros2 launch astra_camera astra_mini.launch.py
```

- 2. 启动rtabmap

```bashrc
  ros2 launch rtabmap_launch rtabmap.launch.py \
    rtabmap_args:="--delete_db_on_start" \
    rgb_topic:=/camera/color/image_raw \
    depth_topic:=/camera/depth/image_raw \
    camera_info_topic:=/camera/color/camera_info \
    frame_id:=base_footprint \
    use_sim_time:=false \
    approx_sync:=true \
    qos:=2 \
    rviz:=true \
    queue_size:=30
```

## launch 文件启动方式
```bashrc
ros2 launch rtabmap_app_launch wheeltec_map_rgbd_whole.launch.py
```
