# Unitree Go2 ROS2 Rerun Visualization Workspace

Language: English | [한국어](README.ko.md)

[![ROS2 Humble](https://img.shields.io/badge/ROS2-Humble-blue)](https://docs.ros.org/en/humble/)
[![Ubuntu 22.04](https://img.shields.io/badge/Ubuntu-22.04-E95420?logo=ubuntu&logoColor=white)](https://releases.ubuntu.com/22.04/)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Rerun](https://img.shields.io/badge/Rerun-3D%20Visualization-ff6f00)](https://rerun.io/)

This repository is a ROS2 workspace for visualizing real Unitree Go2 robot data in Rerun. It combines Unitree Go2 ROS packages, robot model assets, and custom Python visualization scripts to display RGB-D camera streams, LiDAR point clouds, odometry, low-frequency joint states, and compressed voxel maps in a single 3D scene.

The main portfolio work in this repository is `map_success.py`: a multi-threaded ROS2 node that subscribes to real Go2 sensor topics and renders the robot body, articulated legs, camera images, LiDAR points, and voxel map through Rerun.

## Features

- Real-time RGB camera visualization from compressed ROS2 image topics.
- Depth image visualization without relying on `cv_bridge`.
- LiDAR `PointCloud2` parsing and height-colored 3D rendering.
- Go2 body pose visualization from odometry.
- Go2 leg articulation using `/lf/lowstate` joint data.
- Unitree compressed voxel map decoding with LZ4 support.
- Multi-threaded ROS2 callback handling using `MultiThreadedExecutor`.
- Submodule-based ROS2 package layout for Unitree Go2 dependencies.
- README-integrated setup and execution order for deployment.

## Repository Structure

```text
.
├── README.md                   # Project overview and execution guide
├── README.ko.md                # Korean project overview and execution guide
├── map_success.py              # Final Rerun visualization node
├── go2_description/            # Local Go2 model assets used by Rerun
│   ├── assets/                 # OBJ meshes loaded by map_success.py
│   ├── dae/                    # DAE mesh assets
│   └── urdf/
│       └── go2.urdf            # Go2 robot model description
├── src/                        # ROS2 package submodules
│   ├── go2_bringup
│   ├── go2_description
│   ├── go2_driver
│   ├── go2_interfaces
│   ├── go2_robot
│   ├── go2_ros2_sdk
│   ├── go2_rviz
│   ├── unitree_api
│   └── unitree_go
├── .gitignore                  # Generated and machine-local file exclusions
└── .gitmodules                 # External package sources
```

Generated ROS2 workspace folders such as `build/`, `install/`, `log/`, and Python cache files are intentionally ignored.
Development prototypes, local deployment notes, MuJoCo scene XML files, and removed PNG assets are kept out of the public project tree.

## Main Visualization Node

`map_success.py` subscribes to these topics:

| Topic | Type | Purpose |
| --- | --- | --- |
| `/my_go2/color/image_raw/compressed` | `sensor_msgs/CompressedImage` | Front RGB camera |
| `/my_go2/depth/image_rect_raw` | `sensor_msgs/Image` | Depth image |
| `/utlidar/cloud` | `sensor_msgs/PointCloud2` | LiDAR point cloud |
| `/utlidar/robot_odom` | `nav_msgs/Odometry` | Robot pose |
| `/lf/lowstate` | `unitree_go/LowState` | Low-frequency joint state |
| `/utlidar/voxel_map_compressed` | `unitree_go/VoxelMapCompressed` | Compressed voxel map |

The node uses Rerun paths such as `world/robot`, `world/robot/body`, `world/robot/lidar/points`, and `world/voxel_map` to organize the scene.

## Prerequisites

- Ubuntu 22.04 LTS
- ROS2 Humble
- Python 3.10
- A Unitree Go2 robot publishing compatible ROS2 topics
- Rerun Python SDK
- Unitree Go2 ROS2 packages built in this workspace

Python dependencies:

```bash
pip3 install rerun-sdk lz4 numpy opencv-python
```

The execution order below incorporates the deployment notes used during development.

## Execution Order

Follow this order when setting up the workspace on a new machine.

### 1. Prepare ROS2

Install and source ROS2 Humble first:

```bash
source /opt/ros/humble/setup.bash
```

### 2. Clone With Submodules

```bash
git clone --recursive git@github.com:semin-Gwon/go2_rerun.git go2_ws
cd go2_ws
```

If the repository was cloned without submodules:

```bash
git submodule update --init --recursive
```

### 3. Install ROS Dependencies and Build

```bash
cd ~/go2_ws
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Depending on your Go2 SDK setup, you may also need the Python dependencies from `src/go2_ros2_sdk/requirements.txt`.

### 4. Install Python Dependencies

```bash
pip3 install rerun-sdk lz4 numpy opencv-python
```

`lz4` is required for decoding `VoxelMapCompressed` data.

### 5. Check Local Paths

Before running on another PC, update the hardcoded local paths in `map_success.py` if needed:

```text
/home/jnu/go2_ws/install/unitree_go/...
/home/jnu/go2_ws/go2_description/assets
```

### 6. Start Go2 ROS2 Data Publishers

Start the robot-side or SDK-side ROS2 nodes first so these topics are available:

```text
/my_go2/color/image_raw/compressed
/my_go2/depth/image_rect_raw
/utlidar/cloud
/utlidar/robot_odom
/lf/lowstate
/utlidar/voxel_map_compressed
```

### 7. Run the Rerun Visualization

```bash
cd ~/go2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
python3 map_success.py
```

Rerun should open automatically and display the live robot scene.

## Notes About Local Paths

The current visualization script was developed on this machine and contains local paths such as:

```text
/home/jnu/go2_ws/install/unitree_go/...
/home/jnu/go2_ws/go2_description/assets
```

If you clone this repository to another user account or another machine, update those paths in `map_success.py` or refactor them into environment variables before running.

## Troubleshooting

### RGB works but joint motion is frozen

Use `/lf/lowstate` instead of high-rate `/lowstate`. The low-frequency topic is more stable under Wi-Fi bandwidth constraints and is sufficient for visualization.

### Sensor callbacks block each other

`map_success.py` uses `MultiThreadedExecutor` and `ReentrantCallbackGroup` so camera, LiDAR, odometry, lowstate, and voxel callbacks can be processed concurrently.

### Voxel map does not render

Install LZ4:

```bash
pip3 install lz4
```

### Rerun rotation API errors

The script avoids the problematic `RotationAxisAngle` helper path and uses manual quaternion values for compatibility with newer Rerun versions.

## Git Hygiene

This repository intentionally excludes generated or machine-local files:

- `build/`
- `install/`
- `log/`
- `__pycache__/`
- `*.bag`, `*.db3`, `*.mcap`
- `*.ply`, `*.pcd`

The ROS2 packages under `src/` are tracked as submodules instead of copying their nested `.git` histories into this repository.

## Related Work

This workspace builds on these external GitHub sources:

- [Unitree-Go2-Robot](https://github.com/Unitree-Go2-Robot) organization packages: `go2_bringup`, `go2_description`, `go2_driver`, `go2_interfaces`, `go2_robot`, `go2_rviz`, `unitree_api`, and `unitree_go`
- [abizovnuralem/go2_ros2_sdk](https://github.com/abizovnuralem/go2_ros2_sdk)

## License

This repository contains custom visualization code together with external ROS2 packages and robot model assets.

- Custom code in this repository, including `map_success.py`, does not currently have a separate root license.
- External packages under `src/` are governed by their original upstream licenses.
- Robot model assets under `go2_description/` may require separate license review from Unitree or the original upstream source.

Before redistributing or using this repository beyond personal portfolio purposes, review the upstream licenses and add a root `LICENSE` file for the custom code if needed.
