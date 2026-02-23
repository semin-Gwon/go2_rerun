import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, qos_profile_sensor_data
from sensor_msgs.msg import Image, CompressedImage, PointCloud2
from nav_msgs.msg import Odometry
from unitree_go.msg import LowState, VoxelMapCompressed # [추가] VoxelMap
import sensor_msgs_py.point_cloud2 as pc2
import numpy as np
import rerun as rr
import time
import cv2
import zlib
import traceback
try:


    import lz4.block
except ImportError:

    lz4 = None
 # [추가] 압축 해제용
from collections import deque
# from cv_bridge import CvBridge # 제거

import inspect
print(f"DEBUG: Rerun Version: {rr.__version__}")
print(f"DEBUG: Rerun Time APIs: {[x for x in dir(rr) if 'set_time' in x]}")
try:
    print(f"DEBUG: rr.set_time signature: {inspect.signature(rr.set_time)}")
except Exception as e:
    print(f"DEBUG: Could not get signature: {e}")

class RerunImageNode(Node):
    def __init__(self):
        super().__init__("rerun_image_node")
        self.get_logger().info("🚀 로봇 시각화 노드 시작 중...")

        # 1. Rerun 초기화
        rr.init("ros2_rerun", spawn=True)
        
        # [중요] 초기 메쉬 로드 시에도 타임라인을 설정해야 3D 뷰어에 즉시 나타납니다.
        current_time_ns = self.get_clock().now().nanoseconds
        rr.set_time(timeline="ros_time", sequence=current_time_ns)

        # 2. QoS 및 구독 설정
        lidar_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        # 토픽 구독 (이름과 QoS 확인)
        self.create_subscription(CompressedImage, "/my_go2/color/image_raw/compressed", self.rgb_callback, qos_profile_sensor_data)
        self.create_subscription(Image, "/my_go2/depth/image_rect_raw", self.depth_callback, qos_profile_sensor_data)
        self.create_subscription(PointCloud2, "/utlidar/cloud", self.lidar_callback, lidar_qos)
        self.create_subscription(Odometry, "/utlidar/robot_odom", self.odom_callback, 10)
        self.create_subscription(LowState, "/lowstate", self.lowstate_callback, 10)
        self.create_subscription(VoxelMapCompressed, "/utlidar/voxel_map_compressed", self.voxel_map_callback, 
                                 QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT, history=HistoryPolicy.KEEP_LAST))

        # 3. 로봇 메쉬(Mesh) 로드 - hdc 계정 및 .dae 경로 기준
        base_asset_path = "/home/hdc/go2_ws/go2_description/assets"
        
        for i in range(5):
            mesh_path = f"{base_asset_path}/base_{i}.obj"
        try:
        # world/robot/body 아래에 조각들을 차곡차곡 쌓습니다.
            rr.log(f"world/robot/body/mesh_{i}", rr.Asset3D(path=mesh_path))
        except Exception:
        # 파일이 없는 번호는 건너뜁니다.
            pass

        # 4. 다리 설정 함수 호출 (중복 제거하여 1번만 호출)
        self.setup_leg_meshes()

        # 5. 기타 시각화 보조 도구 (TF 축, LiDAR 위치 등)
        rr.log("world/robot/tf_axes", rr.Arrows3D(
            vectors=[[0.3, 0, 0], [0, 0.3, 0], [0, 0, 0.3]],
            colors=[[255, 0, 0], [0, 255, 0], [0, 0, 255]],
            radii=0.01
        ))
        
        # LiDAR 오프셋 설정
        rr.log("world/robot/lidar", rr.Transform3D(translation=[0.25, 0.0, -0.3]))
        rr.log("world/robot/body/camera", rr.Transform3D(translation=[0.25, 0.0, 0.1],# 위치: 머리 앞 0.25m, 위 0.1m
        # [수정] 회전 추가: X축 기준 90도 회전하여 정면 응시
        rotation=rr.Quaternion(xyzw=[0.5, -0.5, 0.5, -0.5])
    )
)
        rr.log("world/robot/body/camera",rr.Pinhole(focal_length=300, # YAML의 image_from_camera [0] 값 참고
        width=640,
        height=480
        )
        )
        # 로봇 뒤쪽 1.5m, 위쪽 0.5m 지점에 시점 고정
        rr.log("world/robot/body/follow_view", rr.Transform3D(translation=[-1.5, 0.0, 0.5]))
        
        # 6. 타이머 및 초기화 변수
        self.last_rgb_time = time.perf_counter()
        self.dt_history = deque(maxlen=30) 
        self.create_timer(1.0, self.timer_callback)

        self.get_logger().info("🎊 모든 설정 완료! Rerun 뷰어를 확인하세요.")

    def timer_callback(self):
        # Check current Rerun time
        # Note: rr.get_time_nanos is not available in 0.28.1, so we just print Alive
        self.get_logger().info(f"Node Alive.")

    def rgb_callback(self, msg):
        self.get_logger().info("DEBUG: RGB Received", throttle_duration_sec=2.0)
        
        # [수정] 모든 타임스탬프를 수신 시간(System Time)으로 통일
        current_time_ns = self.get_clock().now().nanoseconds
        rr.set_time(timeline="ros_time", sequence=current_time_ns)

        # CompressedImage -> Numpy -> Decode -> RGB
        np_arr = np.frombuffer(msg.data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        rr.log("camera/rgb", rr.Image(img_rgb))
        rr.log("world/robot/body/camera", rr.Image(img_rgb))
        
    def depth_callback(self, msg):
        self.get_logger().info("DEBUG: Depth Received", throttle_duration_sec=2.0)
        
        # [수정] 수신 시간 사용
        current_time_ns = self.get_clock().now().nanoseconds
        rr.set_time(timeline="ros_time", sequence=current_time_ns)
        
        # [수정] Manual Numpy Parsing (Mono8/16UC1 대응)
        # CvBridge 제거 및 강건한 파싱 적용
        try:
            dtype = np.uint16 # 기본값
            
            if msg.encoding == 'mono8':
                dtype = np.uint8
            elif msg.encoding == '16UC1':
                dtype = np.uint16
            elif msg.encoding == '32FC1':
                dtype = np.float32

            img_depth = np.frombuffer(msg.data, dtype=dtype).reshape(msg.height, msg.width)
            rr.log("camera/depth", rr.DepthImage(img_depth, meter=1000.0))
        except Exception as e:
            self.get_logger().error(f"Depth Conversion Error: {e}")

    # [추가] LiDAR 콜백 함수
    def lidar_callback(self, msg):
        self.get_logger().info("DEBUG: LiDAR Received", throttle_duration_sec=2.0)
        # 1. 타임라인 동기화 (수신 시간 사용)
        current_time_ns = self.get_clock().now().nanoseconds
        rr.set_time(timeline="ros_time", sequence=current_time_ns)

        # 2. PointCloud2 메시지를 (N, 3) Numpy 배열로 변환
        # 2. PointCloud2 메시지를 (N, 3) Numpy 배열로 변환
        points_list = list(pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True))
        if not points_list:
            return
            
        points = np.array(points_list)
        
        # [Fix] Handle structured array case (1D array of logic)
        if points.ndim == 1:
            if points.dtype.names and 'x' in points.dtype.names:
                # Structure: [(x, y, z), ...] but as numpy void types
                points = np.column_stack([points['x'], points['y'], points['z']])
            else:
                # Flat array fallback
                try:
                    points = points.reshape(-1, 3)
                except Exception:
                    pass

        # 3. 데이터가 존재할 때만 로깅
        if points.shape[0] > 0:
            # --- [수정] 높이(Z) 기반 컬러맵 적용 ---
            z_values = points[:, 2]  # Z좌표 추출
            
            # 색상 매핑을 위한 정규화 (예: 바닥 -1m ~ 천장 2m 사이를 무지개색으로)
            # 상황에 따라 min/max 값은 조정 가능합니다.
            z_min, z_max = -0.5, 1.5 
            norm_z = (z_values - z_min) / (z_max - z_min)
            norm_z = np.clip(norm_z, 0, 1)  # 0~1 사이로 제한

            # 간단한 Turbo colormap (Rerun은 Numpy 배열로 색상 전달 가능)
            # matplotlib가 없어도 되도록 간단한 수식으로 구현하거나 
            # 여기서는 보기 좋게 colormap을 직접 계산합니다.
            
            # Blue(0) -> Green(0.5) -> Red(1) 느낌의 간단한 맵
            colors = np.zeros((points.shape[0], 3), dtype=np.uint8)
            
            # R: 높을수록 붉어짐
            colors[:, 0] = (255 * norm_z).astype(np.uint8)
            # G: 중간 높이에서 가장 밝음 (사인파 활용)
            colors[:, 1] = (255 * np.sin(norm_z * np.pi)).astype(np.uint8)
            # B: 낮을수록 파라짐
            colors[:, 2] = (255 * (1 - norm_z)).astype(np.uint8)

            rr.log(
                "world/robot/lidar/points",  # [수정] 경로를 로봇 하위로 변경
                rr.Points3D(points, colors=colors, radii=0.02) #이거 뭔가 수정하면 박스형태로 나올 듯?
            )

    # [추가] 다리 메시 설정하고 로드하는 함수
    def setup_leg_meshes(self):
        self.d_thigh = [0, -0.0955, 0] 
        self.d_calf = [0, 0, -0.213]   
        self.d_foot = [0, 0, -0.213]
        
        base_path = "/home/hdc/go2_ws/go2_description/assets"
        
    
    # [수정] 슬라이드와 똑같은 .obj 파일명 매핑
        parts = {
            "hip": [f"{base_path}/hip_0.obj", f"{base_path}/hip_1.obj"],
            "thigh": [f"{base_path}/thigh_0.obj", f"{base_path}/thigh_1.obj"],
            "thigh_mirror": [f"{base_path}/thigh_mirror_0.obj", f"{base_path}/thigh_mirror_1.obj"],
            "calf": [f"{base_path}/calf_0.obj", f"{base_path}/calf_1.obj"],
            "calf_mirror": [f"{base_path}/calf_mirror_0.obj", f"{base_path}/calf_mirror_1.obj"],
            "foot": [f"{base_path}/foot.obj"],
        }
    
    # self.legs 정의 (기존 코드 유지)
        self.legs = {
            "FR": {"offset": [0.1934, -0.0465, 0], "mirror": True},
            "FL": {"offset": [0.1934, 0.0465, 0],  "mirror": False},
            "RR": {"offset": [-0.1934, -0.0465, 0], "mirror": True},
            "RL": {"offset": [-0.1934, 0.0465, 0],  "mirror": False},
        }

        for name, cfg in self.legs.items():
            is_right = cfg["mirror"]
        
        # 1. Hip 조립 (0, 1번 파일 로그)
            for i, p in enumerate(parts["hip"]):
                rr.log(f"world/robot/{name}_hip/mesh/part_{i}", rr.Asset3D(path=p))

        # 2. Thigh 조립
            thigh_list = parts["thigh_mirror"] if is_right else parts["thigh"]
            for i, p in enumerate(thigh_list):
                rr.log(f"world/robot/{name}_hip/{name}_thigh/mesh/part_{i}", rr.Asset3D(path=p))

        # 3. Calf 조립
            calf_list = parts["calf_mirror"] if is_right else parts["calf"]
            for i, p in enumerate(calf_list):
                rr.log(f"world/robot/{name}_hip/{name}_thigh/{name}_calf/mesh/part_{i}", rr.Asset3D(path=p))

        # 4. Foot 조립
            rr.log(f"world/robot/{name}_hip/{name}_thigh/{name}_calf/{name}_foot/mesh", rr.Asset3D(path=parts["foot"][0]))


    # [추가] LowState 콜백: 관절 업데이트
    def lowstate_callback(self, msg: LowState):
    # [추가] 변수가 아직 생성 안 되었으면 그냥 리턴해서 에러 방지
        if not hasattr(self, 'd_thigh') or not hasattr(self, 'legs'):
            return

        current_time_ns = self.get_clock().now().nanoseconds
        rr.set_time(timeline="ros_time", sequence=current_time_ns)

        leg_names = ["FR", "FL", "RR", "RL"]
        for i, name in enumerate(leg_names):
            idx = i * 3
            q_hip = msg.motor_state[idx].q
            q_thigh = msg.motor_state[idx+1].q
            q_calf = msg.motor_state[idx+2].q
        
            self.update_leg_chain(name, q_hip, q_thigh, q_calf)

    def update_leg_chain(self, leg_name, q1, q2, q3):
        # 1. Base -> Hip
        cfg = self.legs[leg_name]
        # Hip Joint는 X축 회전 (Roll)
        rr.log(
            f"world/robot/{leg_name}_hip",
            rr.Transform3D(
                translation=list(cfg["offset"]),
                rotation=rr.RotationAxisAngle(axis=[1.0, 0.0, 0.0], radians=float(q1))
            )
        )
        # rr.log(f"world/robot/{leg_name}_hip/debug_sphere", rr.Points3D([[0,0,0]], colors=[255,0,0], radii=0.03))
        # [Debugging] Uncommented for visibility check
        # rr.log(f"world/robot/{leg_name}_hip/debug_sphere", rr.Points3D([[0,0,0]], colors=[255,0,0], radii=0.03))

        # 2. Hip -> Thigh
        # Thigh Joint는 Y축 회전 (Pitch)
        # Right 다리는 Y 오프셋이 음수일 수 있음
        thigh_offset = list(self.d_thigh)
        if cfg["mirror"]: thigh_offset[1] *= -1 # 대칭 반영
        
        rr.log(
            f"world/robot/{leg_name}_hip/{leg_name}_thigh",
            rr.Transform3D(
                translation=list(thigh_offset),
                rotation=rr.RotationAxisAngle(axis=[0.0, 1.0, 0.0], radians=float(q2))
            )
        )
        # rr.log(f"world/robot/{leg_name}_hip/{leg_name}_thigh/debug_sphere", rr.Points3D([[0,0,0]], colors=[0,255,0], radii=0.03))

        # 3. Thigh -> Calf
        # Calf Joint는 Y축 회전 (Pitch)
        rr.log(
            f"world/robot/{leg_name}_hip/{leg_name}_thigh/{leg_name}_calf",
            rr.Transform3D(
                translation=list(self.d_calf),
                rotation=rr.RotationAxisAngle(axis=[0.0, 1.0, 0.0], radians=float(q3))
            )
        )
        # rr.log(f"world/robot/{leg_name}_hip/{leg_name}_thigh/{leg_name}_calf/debug_sphere", rr.Points3D([[0,0,0]], colors=[0,0,255], radii=0.03))

        # 4. Calf -> Foot (Fixed joint, but has offset)
        rr.log(
            f"world/robot/{leg_name}_hip/{leg_name}_thigh/{leg_name}_calf/{leg_name}_foot",
            rr.Transform3D(translation=list(self.d_foot))
        )
        # rr.log(f"world/robot/{leg_name}_hip/{leg_name}_thigh/{leg_name}_calf/{leg_name}_foot/debug_sphere", rr.Points3D([[0,0,0]], colors=[255,255,0], radii=0.03))


    # [추가] Odom 콜백: 로봇 위치 업데이트
    def odom_callback(self, msg):
        # Odom 데이터 처리
        # self.get_logger().info("DEBUG: Odom Received", throttle_duration_sec=2.0)
        
        # [수정] 수신 시간 사용
        current_time_ns = self.get_clock().now().nanoseconds
        rr.set_time(timeline="ros_time", sequence=current_time_ns)

        # Transform3D 로깅
        t = msg.pose.pose.position
        pos = [t.x, t.y, t.z]

        # 3. 회전(Rotation) 추출 (x,y,z,w)
        q = msg.pose.pose.orientation
        quat = [q.x, q.y, q.z, q.w]

        # 4. TF Publish (Rerun이 TF를 자동으로 구성해주진 않으므로, Position 업데이트로 충분)
        # 하지만 로봇의 Pose(위치+회전)가 World 좌표계에서 어디인지 알려줘야 함.
        rr.log(
            "world/robot",
            rr.Transform3D(
                translation=pos,
                rotation=rr.Quaternion(xyzw=[q.x, q.y, q.z, q.w])
            )
        )

    # [추가] Voxel Map 콜백
    def voxel_map_callback(self, msg: VoxelMapCompressed):
        current_time_ns = self.get_clock().now().nanoseconds
        rr.set_time(timeline="ros_time", sequence=current_time_ns)

        if len(msg.data) == 0:
            return

        try:
            # 1. 압축 해제 (LZ4)
            # Unitree VoxelMap은 주로 LZ4로 압축됨
            # SrcSize = 77824 bytes (128*128*38 bits)
            if lz4:
                # lz4.block.decompress(data, uncompressed_size)
                # uncompressed_size를 명시해야 정확히 동작
                uncompressed_size = msg.src_size
                buf = lz4.block.decompress(msg.data, uncompressed_size=uncompressed_size)
            else:
                self.get_logger().error("LZ4 library not found. Please install: pip install lz4")
                return
            
            # 2. 비트 언패킹 (Bytes -> Bits)
            # np.unpackbits는 uint8 배열을 0/1 비트 배열로 변환합니다.
            # Rerun이나 Numpy 연산을 위해 bool/indices로 변환이 필요합니다.
            raw_uint8 = np.frombuffer(buf, dtype=np.uint8)
            bits = np.unpackbits(raw_uint8) # Shape: (TotalBits,)
            
            # 3. 3D Grid 재구성
            # Unitree VoxelMap은 [Width[2], Width[1], Width[0]] 순(Z, Y, X)일 가능성 높음. 
            # 혹은 Linear Index에서 X가 가장 빨리 변함.
            # Numpy reshape: (z, y, x) 순서로 reshape하면 C-order (마지막 차원이 가장 빨리 변함)와 일치
            # [중요] msg.width는 int16이므로 곧바로 곱하면 오버플로우 발생 가능 -> int로 변환 필수
            nx = int(msg.width[0])
            ny = int(msg.width[1])
            nz = int(msg.width[2])

            
            # 데이터 크기 검증 (패딩이 있을 수 있으므로 잘라냄)
            # 데이터 크기 검증 및 패딩/자르기
            # 데이터 크기 검증 및 패딩/자르기
            total_elements = nx * ny * nz
            current_size = bits.size
            if current_size != total_elements:
                # self.get_logger().warn(f"Resizing bits: {current_size} -> {total_elements}")
                new_bits = np.zeros(total_elements, dtype=np.uint8)
                msg_len = min(current_size, total_elements)
                new_bits[:msg_len] = bits[:msg_len]
                bits = new_bits
            
            # 이제 안전하게 Reshape 가능
            grid = bits.reshape((nz, ny, nx)) # Z, Y, X 순

            # 4. 점유된(Occupied) 복셀 인덱스 추출 (값 1인 위치)
            # Tuple of arrays: (z_indices, y_indices, x_indices)
            z_idx, y_idx, x_idx = np.nonzero(grid)
            
            if len(x_idx) == 0:
                return

            # 5. World 좌표계로 변환
            # Pos = Origin + Index * Resolution + Resolution/2 (Center)
            res = msg.resolution
            ox, oy, oz = msg.origin
            
            xs = ox + x_idx * res + res * 0.5
            ys = oy + y_idx * res + res * 0.5
            zs = oz + z_idx * res + res * 0.5
            
            # (N, 3) 배열 생성
            points = np.stack([xs, ys, zs], axis=-1)
            
            # 높이(Z)에 따른 색상 매핑 (Rainbow: Blue->Green->Red)
            colors = np.zeros((points.shape[0], 3), dtype=np.uint8)
            z_min, z_max = np.min(zs), np.max(zs)
            
            # 0으로 나누기 방지
            if z_max == z_min:
                z_range = 1.0
            else:
                z_range = z_max - z_min
                
            norm_z = (zs - z_min) / z_range
            
            # Simple Jet-like colormap
            # R: 높을수록(1.0) 255
            colors[:, 0] = (255 * norm_z).astype(np.uint8)
            # G: 중간(0.5)일 때 255 (sin graph)
            colors[:, 1] = (255 * np.sin(norm_z * np.pi)).astype(np.uint8)
            # B: 낮을수록(0.0) 255
            colors[:, 2] = (255 * (1 - norm_z)).astype(np.uint8)

            # 6. Rerun 로깅 (Voxel을 더 잘 보이게 Boxes3D 고려 가능하나 일단 Points3D 유지)
            # radii=res*0.5 하면 꽉 찬 느낌
            rr.log(
                "world/voxel_map",
                rr.Points3D(points, colors=colors, radii=res * 0.25)
            )
            
            # 원점 표시 (Debug)
            # rr.log("world/voxel_map/origin", rr.Points3D([msg.origin], radii=0.1, labels=["Map Origin"]))
            
            # 성공 로그 (한 번만 출력하거나 주기적으로)
            # self.get_logger().info(f"Voxel Map Logged: {len(points)} points", throttle_duration_sec=5.0)

        except Exception as e:
            self.get_logger().error(f"FINAL Voxel Error: {e}")
            self.get_logger().error(traceback.format_exc())



def main():
    rclpy.init()
    node = RerunImageNode()


    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
