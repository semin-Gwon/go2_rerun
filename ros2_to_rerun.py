import rclpy
from rclpy.node import Node
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, qos_profile_sensor_data
from sensor_msgs.msg import Image, CompressedImage  # 두 타입 모두 사용
import numpy as np
import rerun as rr
import cv2
from cv_bridge import CvBridge

class RerunMixedNode(Node):
    def __init__(self):
        super().__init__("rerun_mixed_node")
        self.get_logger().info("DEBUG: Node Starting...")
        
        # [디버깅] 노드가 살아있는지 확인하는 타이머 (1초마다 출력)
        self.create_timer(1.0, self.timer_callback)
        
        # 1. Rerun 초기화
        rr.init("go2_realtime_stream", spawn=True)
        # rr.set_memory_limit(4 * 1024 * 1024 * 1024) # 4GB넘어가면 old데이터 자동삭제
        self.bridge = CvBridge()

        # 2. Color: 압축 토픽 구독 (실시간성 확보)
        self.color_sub = self.create_subscription(
            CompressedImage,
            "/my_go2/color/image_raw/compressed",
            self.color_callback,
            10
        )

        # 3. Depth: 원본 토픽 구독 (Sensor Data QoS)
        # qos_profile_sensor_data는 Best Effort + Volatile로 설정되어 있어
        # 센서 데이터 수신에 가장 적합한 표준 프로필입니다.
        self.depth_sub = self.create_subscription(
            Image,
            "/my_go2/depth/image_rect_raw",
            self.depth_callback,
            qos_profile_sensor_data
        )

        self.get_logger().info("✅ 스트리밍 시작: Color(Compressed) + Depth(Raw)")

    def color_callback(self, msg):
        """압축된 RGB 데이터를 디코딩하여 Rerun에 전송"""
        # 바이너리 -> 넘파이 변환 및 디코딩
        np_arr = np.frombuffer(msg.data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        # BGR -> RGB 변환 (Rerun 규격)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        rr.log("camera/rgb", rr.Image(img_rgb))

    def timer_callback(self):
        # 노드가 멈추지 않았는지 확인용
        # self.get_logger().info("Node is alive... waiting for Depth data")
        pass

    def depth_callback(self, msg):
        """원본 Depth 데이터 처리 (mono8/16UC1 대응)"""
        # self.get_logger().info(f"Depth Received! Encoding: {msg.encoding}, Bytes: {len(msg.data)}")
        
        try:
            dtype = np.uint16 # 기본값
            
            if msg.encoding == 'mono8':
                dtype = np.uint8
            elif msg.encoding == '16UC1':
                dtype = np.uint16
            elif msg.encoding == '32FC1':
                dtype = np.float32

            # 버퍼 -> 넘파이 변환
            # 주의: dtype이 틀리면 크기가 안 맞아서 에러 남
            img_depth = np.frombuffer(msg.data, dtype=dtype).reshape(msg.height, msg.width)
            
            # Rerun 로그 (mono8인 경우 미터 단위가 아닐 수 있음, 일단 시각화가 우선)
            rr.log("camera/depth", rr.DepthImage(img_depth, meter=1000.0))
            
        except Exception as e:
            self.get_logger().error(f"Depth Conversion Error: {e}")

def main():
    rclpy.init()
    node = RerunMixedNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
