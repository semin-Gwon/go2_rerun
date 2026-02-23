# Unitree Go2 Rerun 시각화 배포 가이드 (Deployment Guide)

본 가이드는 **Ubuntu 22.04 LTS** 및 **ROS 2 Humble** 환경에서 Unitree Go2 로봇의 센서 데이터와 움직임을 Rerun 뷰어로 시각화하는 `map_success.py` 스크립트를 실행하기 위한 절차를 설명합니다.

## 1. 사전 준비 사항 (Prerequisites)

실행을 위해 다음 환경이 필수적으로 구성되어야 합니다.

*   **OS**: Ubuntu 22.04 LTS (Jammy Jellyfish)
*   **ROS**: ROS 2 Humble Hawksbill (Desktop Install 권장)
*   **Target Robot**: Unitree Go2 (Edu/Pro)

## 2. 필수 패키지 설치 (Installation)

### 2.1 Workspace 및 Unitree ROS2 패키지 설정
Unitree Go2의 커스텀 메시지 타입(`unitree_go.msg`)을 사용하기 위해 공식 패키지가 필요합니다.

```bash
# 1. 워크스페이스 생성 (이미 있다면 생략)
mkdir -p ~/go2_ws/src
cd ~/go2_ws/src

# 2. unitree_ros2 패키지 클론
git clone https://github.com/unitreerobotics/unitree_ros2.git

# 3. 빌드 (cyclonedds 관련 에러가 날 경우 unitree 가이드 참조)
cd ~/go2_ws
colcon build
source install/setup.bash
```

### 2.2 Python 의존성 설치
시각화 및 데이터 처리에 필요한 필수 Python 라이브러리를 설치합니다.
(터미널에 다음 명령어를 입력하세요. `pip3`가 없다면 `sudo apt install python3-pip` 선행)

```bash
pip3 install rerun-sdk==0.15.1  # 혹은 최신 버전 (0.28.1+ 호환 코드 작성을 권장)
pip3 install lz4                # VoxelMap 압축 해제용
pip3 install numpy              # 행렬 연산
pip3 install opencv-python      # 이미지 디코딩
```
> **참고**: 본 프로젝트의 `map_success.py`는 Rerun 최신 버전(0.28.1 이상)에서도 작동하도록 호환성 코드가 적용되어 있습니다.

## 3. 코드 설정 및 실행 (Execution)

### 3.1 파일 준비
`map_success.py` 파일을 `~/go2_ws` 폴더(워크스페이스 루트)로 복사합니다.

### 3.2 코드 수정 (필수)
새로운 PC 환경에 맞춰 `map_success.py` 내부의 경로를 수정해야 합니다. 텍스트 에디터로 파일을 열어 수정하세요.

1.  **3D 모델 애셋 경로 수정 (Line ~85)**:
    사용자의 홈 디렉터리 이름이 `jnu`가 아니라면 경로를 수정해야 합니다.
    ```python
    # 수정 전
    base_asset_path = "/home/jnu/go2_ws/go2_description/assets"
    
    # 수정 후 (예시: 사용자명이 'user'인 경우)
    base_asset_path = "/home/user/go2_ws/go2_description/assets"
    ```

2.  **강제 경로 설정 주석 처리 (Line ~5)**:
    환경 설정이 정상적인 PC라면, 코드 상단의 강제 경로 주입 부분은 오히려 에러를 유발할 수 있습니다. **주석 처리(`#`)** 하거나 삭제하세요.
    ```python
    # 정상 환경에서는 아래 내용을 주석 처리 권장
    # sys.path.append("...")
    # ctypes.CDLL("...")
    ```

### 3.3 실행
터미널에서 다음 순서로 실행합니다.

```bash
cd ~/go2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
python3 map_success.py
```

---

## 4. 통신 문제 해결 (Communication Troubleshooting)

로봇 데이터 수신, 특히 **관절(다리) 움직임이 멈추거나 끊기는 현상**이 발생할 경우 다음 가이드를 따르세요.

### Q1. 카메라는 나오는데 다리가 멈춰 있어요.
**진단**: **Thread Starvation (스레드 기아 현상)**
*   LiDAR, 카메라 등 고용량 데이터가 파이썬의 싱글 스레드를 꽉 채워서, 관절 데이터(`LowState`) 처리가 뒤로 밀리는 현상입니다.
*   **해결책**:
    1.  코드에서 반드시 **`MultiThreadedExecutor`**를 사용해야 합니다. (`map_success.py`에는 이미 적용됨)
    2.  `ReentrantCallbackGroup`이 모든 Subscription에 적용되었는지 확인하세요.

### Q2. `/lowstate` 토픽이 아예 안 들어와요.
**진단**: **네트워크 대역폭 차단**
*   일부 WiFi 환경이나 PC 성능 한계로 인해, 100Hz 이상의 고속 데이터인 `/lowstate`가 네트워크 레벨에서 드랍(Loss)될 수 있습니다.
*   **해결책**:
    1.  **`/lf/lowstate` 사용**: Unitree 로봇은 `/lf/lowstate` (Low Frequency, 20Hz)라는 저속 토픽을 별도로 송신합니다. 시각화 용도로는 이것으로도 충분합니다.
    2.  `map_success.py` 내의 구독 코드를 확인하세요:
        ```python
        # 안정적인 20Hz 토픽 사용
        self.create_subscription(LowState, "/lf/lowstate", ...)
        ```

### Q3. Rerun 경고 메시지 (`TypeError: ... not 'Vec3D'`)가 떠요.
**진단**: **Rerun 라이브러리 버전 불일치**
*   Rerun 0.28.1 버전 이상에서 `RotationAxisAngle` 헬퍼 함수가 에러를 일으킵니다.
*   **해결책**:
    *   `map_success.py`에 적용된 **Manual Quaternion 계산 로직**을 그대로 사용하세요. (수동으로 sin/cos 계산 후 Quaternion 주입)
