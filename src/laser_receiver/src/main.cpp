#include <iostream>
#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include <limits>

const float THRESHOLD_MIN_LASER = 0.25;

enum MonitorState {NORMAL, DANGER};


class LaserListener {
private:
    MonitorState state;
public:
    LaserListener()
    {
        state = NORMAL;        
    }
    
    void lasercallback(const sensor_msgs::LaserScan::ConstPtr& msg)
    {
        float min_val(std::numeric_limits<float>::max());
        for (int i =0; i<msg->ranges.size(); i++)
        {
            if (msg->ranges[i] < min_val)
            {
                min_val = msg->ranges[i];
            }
        }
        if (min_val <= THRESHOLD_MIN_LASER && state == NORMAL){
            std::cout << "UNDER LASER THRESHOLD: DANGER " << min_val << std::endl;
            state = DANGER;
        }
        else if (min_val > THRESHOLD_MIN_LASER && state == DANGER){
            std::cout << "Above laser threshold, normal operation " << min_val << std::endl;
            state = NORMAL;
        }
        
    }
};

int main(int argc, char** argv){
    ros::init(argc, argv, "laser_listener");
    ros::NodeHandle nh;
    LaserListener listener;
    ros::Subscriber sub = nh.subscribe("/scan", 1000, 
        &LaserListener::lasercallback, &listener);
    ros::spin();
    return 0;
}