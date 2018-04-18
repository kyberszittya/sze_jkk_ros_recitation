import rospy

from nav_msgs.msg import Odometry

from geometry_msgs.msg import Twist

from recitation_msgs.msg import MoveForwardAction, MoveForwardFeedback, MoveForwardResult

import actionlib

class MoveForwardActionServer(object):
    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, 
            MoveForwardAction, 
            execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
        self.cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist)
      
    def execute_cb(self, goal):
        # helper variables
        print("Received: "+str(goal.secs_sum))
        r = rospy.Rate(goal.secs_sum)
        cmd_msg = Twist()
        cmd_msg.linear.x = goal.lin_vel
        self.cmd_vel_pub.publish(cmd_msg)
        fb = MoveForwardFeedback()
        r.sleep()
        fb.secs_elapsed = goal.secs_sum
        self._as.publish_feedback(fb)
        
        cmd_msg = Twist()
        self.cmd_vel_pub.publish(cmd_msg)
        res = MoveForwardResult()
        res.success = True
        self._as.set_succeeded(res)

        
        
        
if __name__ == '__main__':
    rospy.init_node('moveforwardserver')
    server = MoveForwardActionServer(rospy.get_name())
    rospy.spin()