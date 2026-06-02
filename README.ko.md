# Unitree Go2 ROS2 Rerun 시각화 워크스페이스

언어: [English](README.md) | 한국어

[![ROS2 Humble](https://img.shields.io/badge/ROS2-Humble-blue)](https://docs.ros.org/en/humble/)
[![Ubuntu 22.04](https://img.shields.io/badge/Ubuntu-22.04-E95420?logo=ubuntu&logoColor=white)](https://releases.ubuntu.com/22.04/)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Rerun](https://img.shields.io/badge/Rerun-3D%20Visualization-ff6f00)](https://rerun.io/)

이 저장소는 실제 Unitree Go2 로봇 데이터를 Rerun에서 시각화하기 위한 ROS2 워크스페이스입니다. Unitree Go2 ROS 패키지, 로봇 모델 에셋, 커스텀 Python 시각화 스크립트를 조합해 RGB-D 카메라 스트림, LiDAR 포인트 클라우드, 오도메트리, 저주파 관절 상태, 압축 voxel map을 하나의 3D 장면에서 표시합니다.

이 저장소의 포트폴리오 핵심 결과물은 `map_success.py`입니다. 이 파일은 실제 Go2 센서 토픽을 구독하는 멀티스레드 ROS2 노드이며, Rerun을 통해 로봇 바디, 다리 관절, 카메라 이미지, LiDAR 포인트, voxel map을 렌더링합니다.

## 주요 기능

- 압축 ROS2 이미지 토픽 기반 실시간 RGB 카메라 시각화.
- `cv_bridge` 없이 depth image 시각화.
- LiDAR `PointCloud2` 파싱 및 높이 기반 색상 3D 렌더링.
- 오도메트리 기반 Go2 바디 포즈 시각화.
- `/lf/lowstate` 관절 데이터를 사용한 Go2 다리 관절 시각화.
- LZ4를 지원하는 Unitree 압축 voxel map 디코딩.
- `MultiThreadedExecutor` 기반 멀티스레드 ROS2 콜백 처리.
- Unitree Go2 의존 패키지를 submodule로 관리하는 ROS2 패키지 구조.
- README에 통합된 설치 및 실행 순서.

## 저장소 구조

```text
.
├── README.md                   # 영어 프로젝트 개요 및 실행 가이드
├── README.ko.md                # 한국어 프로젝트 개요 및 실행 가이드
├── map_success.py              # 최종 Rerun 시각화 노드
├── go2_description/            # Rerun에서 사용하는 로컬 Go2 모델 에셋
│   ├── assets/                 # map_success.py가 로드하는 OBJ mesh
│   ├── dae/                    # DAE mesh 에셋
│   └── urdf/
│       └── go2.urdf            # Go2 로봇 모델 description
├── src/                        # ROS2 패키지 submodule
│   ├── go2_bringup
│   ├── go2_description
│   ├── go2_driver
│   ├── go2_interfaces
│   ├── go2_robot
│   ├── go2_ros2_sdk
│   ├── go2_rviz
│   ├── unitree_api
│   └── unitree_go
├── .gitignore                  # 생성 파일 및 로컬 파일 제외 규칙
└── .gitmodules                 # 외부 패키지 출처
```

`build/`, `install/`, `log/`, Python cache처럼 ROS2 빌드 과정에서 생성되는 폴더와 파일은 의도적으로 Git에서 제외합니다.
개발 중간 산출물, 로컬 배포 노트, MuJoCo scene XML 파일, 제거된 PNG 에셋은 공개 프로젝트 트리에서 제외했습니다.

## 메인 시각화 노드

`map_success.py`는 다음 토픽을 구독합니다.

| Topic | Type | Purpose |
| --- | --- | --- |
| `/my_go2/color/image_raw/compressed` | `sensor_msgs/CompressedImage` | 전방 RGB 카메라 |
| `/my_go2/depth/image_rect_raw` | `sensor_msgs/Image` | Depth image |
| `/utlidar/cloud` | `sensor_msgs/PointCloud2` | LiDAR 포인트 클라우드 |
| `/utlidar/robot_odom` | `nav_msgs/Odometry` | 로봇 위치와 자세 |
| `/lf/lowstate` | `unitree_go/LowState` | 저주파 관절 상태 |
| `/utlidar/voxel_map_compressed` | `unitree_go/VoxelMapCompressed` | 압축 voxel map |

노드는 `world/robot`, `world/robot/body`, `world/robot/lidar/points`, `world/voxel_map` 같은 Rerun 경로를 사용해 장면을 구성합니다.

## 사전 준비

- Ubuntu 22.04 LTS
- ROS2 Humble
- Python 3.10
- 호환되는 ROS2 토픽을 publish하는 Unitree Go2 로봇
- Rerun Python SDK
- 이 워크스페이스에서 빌드된 Unitree Go2 ROS2 패키지

Python 의존성:

```bash
pip3 install rerun-sdk lz4 numpy opencv-python
```

아래 실행 순서는 개발 중 사용한 배포 노트를 README에 통합한 것입니다.

## 실행 순서

새 PC에서 워크스페이스를 설정할 때는 아래 순서를 따릅니다.

### 1. ROS2 준비

먼저 ROS2 Humble을 설치하고 source합니다.

```bash
source /opt/ros/humble/setup.bash
```

### 2. Submodule 포함 Clone

```bash
git clone --recursive git@github.com:semin-Gwon/go2_rerun.git go2_ws
cd go2_ws
```

submodule 없이 clone한 경우:

```bash
git submodule update --init --recursive
```

### 3. ROS 의존성 설치 및 빌드

```bash
cd ~/go2_ws
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Go2 SDK 설정에 따라 `src/go2_ros2_sdk/requirements.txt`의 Python 의존성이 추가로 필요할 수 있습니다.

### 4. Python 의존성 설치

```bash
pip3 install rerun-sdk lz4 numpy opencv-python
```

`VoxelMapCompressed` 데이터를 디코딩하려면 `lz4`가 필요합니다.

### 5. 로컬 경로 확인

다른 PC에서 실행하기 전에 `map_success.py`에 있는 하드코딩된 로컬 경로를 필요에 맞게 수정합니다.

```text
/home/jnu/go2_ws/install/unitree_go/...
/home/jnu/go2_ws/go2_description/assets
```

### 6. Go2 ROS2 데이터 Publisher 실행

아래 토픽들이 사용 가능하도록 로봇 쪽 또는 SDK 쪽 ROS2 노드를 먼저 실행합니다.

```text
/my_go2/color/image_raw/compressed
/my_go2/depth/image_rect_raw
/utlidar/cloud
/utlidar/robot_odom
/lf/lowstate
/utlidar/voxel_map_compressed
```

### 7. Rerun 시각화 실행

```bash
cd ~/go2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
python3 map_success.py
```

Rerun이 자동으로 열리고 live robot scene이 표시됩니다.

## 로컬 경로 관련 주의

현재 시각화 스크립트는 이 PC에서 개발되었기 때문에 다음과 같은 로컬 경로를 포함합니다.

```text
/home/jnu/go2_ws/install/unitree_go/...
/home/jnu/go2_ws/go2_description/assets
```

다른 사용자 계정이나 다른 PC에 clone하는 경우, 실행 전에 `map_success.py`의 경로를 수정하거나 환경 변수 기반으로 리팩터링하는 것이 좋습니다.

## 문제 해결

### RGB는 동작하지만 관절 움직임이 멈춰 보이는 경우

고속 `/lowstate` 대신 `/lf/lowstate`를 사용합니다. 저주파 토픽은 Wi-Fi 대역폭 제약에서 더 안정적이며 시각화 용도로 충분합니다.

### 센서 콜백이 서로 막히는 경우

`map_success.py`는 `MultiThreadedExecutor`와 `ReentrantCallbackGroup`을 사용해 카메라, LiDAR, 오도메트리, lowstate, voxel 콜백을 병렬로 처리합니다.

### Voxel map이 렌더링되지 않는 경우

LZ4를 설치합니다.

```bash
pip3 install lz4
```

### Rerun rotation API 오류가 나는 경우

이 스크립트는 최신 Rerun 버전과의 호환성을 위해 문제가 되었던 `RotationAxisAngle` helper 경로를 피하고, 수동 quaternion 값을 사용합니다.

## Git 관리 기준

이 저장소는 생성 파일과 머신 로컬 파일을 의도적으로 제외합니다.

- `build/`
- `install/`
- `log/`
- `__pycache__/`
- `*.bag`, `*.db3`, `*.mcap`
- `*.ply`, `*.pcd`

`src/` 아래 ROS2 패키지는 각 패키지의 중첩 `.git` 기록을 복사하지 않고 submodule로 추적합니다.

## 관련 프로젝트

이 워크스페이스는 다음 공개 Unitree Go2 ROS2 패키지와 SDK를 기반으로 합니다.

- `Unitree-Go2-Robot/go2_robot`
- `Unitree-Go2-Robot/go2_driver`
- `Unitree-Go2-Robot/go2_description`
- `Unitree-Go2-Robot/unitree_go`
- `abizovnuralem/go2_ros2_sdk`

## 라이선스

이 저장소는 커스텀 스크립트와 외부 ROS2 패키지, 로봇 에셋을 함께 사용합니다. 각 upstream submodule의 라이선스를 별도로 확인해야 합니다. 이 저장소를 독립적인 공개 프로젝트로 재배포하기 전에는 루트 `LICENSE` 파일을 추가하는 것이 좋습니다.
