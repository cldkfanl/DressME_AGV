#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import CompressedImage
import cv2
from cv_bridge import CvBridge

def webcam_pub():
    rospy.init_node('webcam_pub', anonymous=True)
    pub = rospy.Publisher('camera/image/compressed', CompressedImage, queue_size=10)
    
    # 웹캠 열기
    cap = cv2.VideoCapture(0)  # 0은 보통 기본 카메라를 의미
    if not cap.isOpened():
        rospy.logerr("Failed to open webcam.")
        return

    rate = rospy.Rate(30)  # 웹캠의 프레임 속도에 맞춰 설정

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if not ret:
            rospy.logerr("Failed to capture frame from camera.")
            break

        # OpenCV 이미지를 압축된 이미지 메시지로 변환
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])  # JPEG 품질을 50으로 설정
        msg.data = buffer.tobytes()

        # 이미지 메시지 게시
        pub.publish(msg)
        rate.sleep()

    # 카메라 정리
    cap.release()

if __name__ == '__main__':
    try:
        webcam_pub()
    except rospy.ROSInterruptException:
        pass