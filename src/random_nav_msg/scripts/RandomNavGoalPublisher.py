import rospy
import actionlib
import numpy as np
import numpy.linalg as linalg
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult

def main():
    rospy.init_node("random_nav_publisher")
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
    client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
    client.wait_for_server()
    vec_pos = np.random.normal(0,2,3)
    msg = MoveBaseGoal()
    msg.target_pose.header.frame_id = "base_link"
    msg.target_pose.pose.position.x = vec_pos[0]
    msg.target_pose.pose.position.y = vec_pos[1]
    msg.target_pose.pose.position.z = vec_pos[2]
    msg.target_pose.pose.orientation.x = 0
    msg.target_pose.pose.orientation.y = 0
    msg.target_pose.pose.orientation.z = 0
    msg.target_pose.pose.orientation.w = 1
    msg.target_pose.header.seq = 1
    c_now = rospy.Time.now()
    msg.target_pose.header.stamp.secs = c_now.secs
    msg.target_pose.header.stamp.nsecs = c_now.nsecs
    client.send_goal(msg)

    res = client.wait_for_result()
    print res
    

if __name__=="__main__":
    main()
        