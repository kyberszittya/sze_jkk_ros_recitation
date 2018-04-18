import numpy as np

import sys

import cv2
import roslib
import rospy

from cv_bridge import CvBridge, CvBridgeError

from sensor_msgs.msg import Image

class SobelImage(object):
    def __init__(self):
        self.image_pub = rospy.Publisher("image_topic_2",Image)
        self.bridge = CvBridge()
        self.subscriber = rospy.Subscriber("/camera/rgb/image_raw",
            Image, self.callback,  queue_size = 1)
        
    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data,"bgr8")
        except CvBridgeError as e:
            print(e)
        sobel_kernel_y = np.array([[1,0,-1],[10,0,-10],[1,0,-1]])
        sobel_kernel_x = np.array([[1,10,1],[0,0,0],[-1,-10,-1]])
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        faltung_x = cv2.filter2D(gray_image, -1, sobel_kernel_x)
        faltung_y = cv2.filter2D(faltung_x, -1, sobel_kernel_y)
        edges = cv2.Canny(faltung_y,100,200)
        cv2.imshow("Image window", edges)
        cv2.waitKey(3)
        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(edges, "mono8"))
        except CvBridgeError as e:
            print(e)

def main(args):
    '''Initializes and cleanup ros node'''
    ic = SobelImage()
    rospy.init_node('image_sobel', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutdown"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)