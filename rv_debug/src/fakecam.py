import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

from std_msgs.msg import String
import cv2
from cv_bridge import CvBridge


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Image, 'image_raw', 10)
        timer_period = 0.01  # seconds. Maybe get rid of this?
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.cap = cv2.VideoCapture("/ros_ws/TestData/spinning_and_moving_target.avi")
        self.bridge = CvBridge()
        if not self.cap.isOpened():
            print("Error: Could not open video file.")
            exit()

    def timer_callback(self):
        ret, frame = self.cap.read()

        if not ret:
            return   # No more frames -> exit loop

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_msg = self.bridge.cv2_to_imgmsg(rgb_frame, encoding='rgb8')

        h,w = frame[:2]
        
        msg = Image()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "camera_optical_frame"
        msg.height = h
        msg.width = w
        msg.encoding = "rgb8"
        msg.step = w*3
        msg.data = rgb_msg
        
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()