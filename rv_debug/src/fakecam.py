#!/bin/python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo

from std_msgs.msg import String
import cv2
from cv_bridge import CvBridge
import math


class MinimalPublisher(Node):

    def __init__(self):
        
        
        super().__init__('minimal_publisher')
        self.publisherImg_ = self.create_publisher(Image, 'image_raw', 10)
        self.publisherCamData_ = self.create_publisher(CameraInfo, 'camera_info', 10)
        self.cap = cv2.VideoCapture("/ros_ws/TestData/spinning_and_moving_target.avi")

        fps = self.cap.get(cv2.CAP_PROP_FPS)
        fps = fps if fps > 0 else 30.0
        timer_period = 1.0 / fps

        self.timer = self.create_timer(timer_period, self.timer_callback)

        
        self.bridge = CvBridge()
        if not self.cap.isOpened():
            print("Error: Could not open video file.")
            exit()

    def timer_callback(self):
        ret, frame = self.cap.read()

        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Rewind to start
            ret, frame = self.cap.read()
            if not ret:
                return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        msg = self.bridge.cv2_to_imgmsg(rgb_frame, encoding='rgb8')
        info_msg = CameraInfo()
        

        h,w,_ = frame.shape
        
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "camera_optical_frame"
        msg.height = h
        msg.width = w
        msg.encoding = "rgb8"
        msg.step = w*3

        info_msg.header = msg.header
        info_msg.height = h
        info_msg.width = w

        # all the camera calibration stuff is ai generated. I have no idea how lenses works lol
        info_msg.distortion_model = "plumb_bob"
        info_msg.d = [0.0,0.0,0.0,0.0,0.0]# Empty distortion model
        info_msg.r = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0
        ]
        fx = (w/2)/(math.tan((math.radians(60))/2))
        fy = fx
        cx = w/2
        cy = h/2
        info_msg.k = [
            fx,  0.0, cx,
            0.0, fy,  cy,
            0.0, 0.0, 1.0
        ]
        info_msg.p = [
            fx,  0.0, cx,  0.0,
            0.0, fy,  cy,  0.0,
            0.0, 0.0, 1.0, 0.0
        ]
        
        self.publisherImg_.publish(msg)
        self.publisherCamData_.publish(info_msg)


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