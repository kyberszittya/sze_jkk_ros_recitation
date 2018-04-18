import actionlib
from recitation_msgs.msg import MoveForwardActionGoal, MoveForwardAction
import rospy



if __name__=="__main__":
    try:
        rospy.init_node("moveforward_client")
        client = actionlib.SimpleActionClient(
            'moveforwardserver', 
            MoveForwardAction)
        client.wait_for_server()
        g = MoveForwardActionGoal() 
        g.goal.lin_vel = 1
        g.goal.secs_sum = 1 
        client.send_goal(g.goal)
        client.wait_for_result()
        print(client.get_result())
    except rospy.ROSInterruptException:
        print("Interrupted unexpected")